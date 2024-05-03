package fr.cpe.emergencymanager.Controller;

import fr.cpe.emergencymanager.Entities.*;
import fr.cpe.emergencymanager.Repository.*;
import fr.cpe.emergencymanager.Service.EquipmentService;
import fr.cpe.emergencymanager.Service.IncidentService;
import fr.cpe.emergencymanager.Service.SensorService;
import fr.cpe.emergencymanager.Service.TeamService;
import org.quartz.Job;
import org.quartz.JobExecutionContext;
import org.quartz.JobExecutionException;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import java.util.Set;
import java.util.stream.Collectors;

public class SensorsProcessing implements Job {
    private final SensorHistoRepository sensorHistoRepository;
    private final SensorRepository sensorRepository;
    private final IncidentRepository incidentRepository;
    private final IncidentService incidentService;
    private final SensorService sensorService;
    private final EquipmentService equipmentService;
    private final TeamService teamService;
    private final IncidentTeamEquipmentRepository incidentTeamEquipmentRepository;

    private final Logger log = LoggerFactory.getLogger(SensorsProcessing.class);

    public SensorsProcessing() {
        this.sensorHistoRepository           = new SensorHistoRepository();
        this.sensorRepository                = new SensorRepository();
        this.incidentRepository              = new IncidentRepository();
        this.incidentService                 = new IncidentService();
        this.sensorService                   = new SensorService();
        this.equipmentService                = new EquipmentService();
        this.teamService                     = new TeamService();
        this.incidentTeamEquipmentRepository = new IncidentTeamEquipmentRepository();
    }

    private void mainThread() {
        // Main du thread exécuté toutes les X secondes
        List<SensorHisto> sensorHistoList =  sensorHistoRepository.findSensorHistoNonProcessed();
        for (SensorHisto sensorHisto: sensorHistoList) {
            log.debug("En traitement : " + sensorHisto);
            if (sensorHisto.getLevel() != 0) {
                traiterSensorHisto(sensorHisto);
            }
            sensorHisto.setProcessed();
            sensorHistoRepository.update(sensorHisto);
        }
        traiterIncidents();
    }

    private void traiterSensorHisto(SensorHisto sensorHisto) {
        // Ajouter sensorHisto à un incident en cours ou créer un nouvel incident
        Sensor sensor = sensorHisto.getSensor();
        Incident incident = null;
        if (sensorService.estConcerneParIncidentEnCours(sensor)) {
            log.debug("Le capteur {} est déjà concerné par un incident en cours", sensor);
            incident = sensorService.getIncidentEnCours(sensor);
            log.debug("L'incident {} a été récupéré", incident);
            incident.addSensorHisto(sensorHisto);
            incidentRepository.update(incident);
        } else {
            List<Sensor> sensorList = sensorService.sensorNeighbor(sensor);
            for (Sensor sensor1 : sensorList) {
                if (sensorService.estConcerneParIncidentEnCours(sensor1)) {
                    log.debug("Le capteur {} est déjà concerné par un incident en cours", sensor1);
                    if (incident == null) {
                        incident = sensorService.getIncidentEnCours(sensor1);
                        log.debug("L'incident {} a été récupéré", incident);
                    } else {
                        log.debug("Il existe un incident à proximité {} il est impossible de déterminer s'ils sont liés", sensorService.getIncidentEnCours(sensor1));
                    }
                }
            }
            if (incident != null) {
                log.debug("L'incident {} a été récupéré", incident);
            } else {
                log.debug("Le capteur {} n'a pas de voisin en incident, on créé un nouvel incident", sensor);
                Incident incident1 = new Incident();
                incident1.setStatus(true);
                incident = incidentRepository.create(incident1);
            }
            incident.addSensorHisto(sensorHisto);
        }
    }

    private void traiterIncidents() {
        Set<Incident> incidents = incidentRepository.findByStatus(true);
        for(Incident incident : incidents) {
            Set<Site> sites = incidentService.getSites(incident);
            Set<IncidentTeamEquipment> incidentTeamEquipments = incidentTeamEquipmentRepository.findByIncident(incident);
            List<IncidentTeamEquipment> aSupprimer = new ArrayList<IncidentTeamEquipment>();
            for(IncidentTeamEquipment incidentTeamEquipment : incidentTeamEquipments) {
                // Lister les incidentTeamEquipment qui ne sont pas déployés au bon endroit (mise à jour du lieu où les véhicules sont envoyés)
                if(incidentTeamEquipment.getEvents().stream().findFirst().isPresent()) {
                    EventIncidentTeamEquipment event = incidentTeamEquipment.getEvents().stream().findFirst().get();
                    if(!sites.contains(new Site(event.getLongitude(), event.getLatitude(), null))) {
                        log.debug("L'incident {} n'est pas sur le bon site, il faut le déplacer", incidentTeamEquipment);
                        aSupprimer.add(incidentTeamEquipment);
                    }
                }
            }
            for(Site site : sites) {
                float level = equipmentService.getActualCapacityBySite(site);
                if(site.getLevel() > level) {
                    log.debug("Le site {} est en sous-capacité, il faut d'autres unités", site);
                    // Récupérer les équipements les plus proches du site
                    List<Equipment> equipmentList = equipmentService.getClosestEquipments(site, aSupprimer.stream().map(IncidentTeamEquipment::getEquipment).collect(Collectors.toSet()));
                    for(Equipment equipment : equipmentList) {
                        log.debug("L'équipement {} est le plus proche du site {}", equipment, site);
                        if(aSupprimer.stream().map(IncidentTeamEquipment::getEquipment).collect(Collectors.toSet()).contains(equipment)) {
                            // Si c'était déjà un véhicule sur place, il faut le mettre à jour, mais il garde le même équipage
                            log.debug("L'équipement {} est déjà en cours de déplacement, il faut mettre à jour sa destination", equipment);
                            Optional<IncidentTeamEquipment> incidentTeamEquipmentOptional = equipmentService.findIncidentTeamEquipmentByEquipmentInProgress(equipment);
                            if(incidentTeamEquipmentOptional.isPresent()) {
                                IncidentTeamEquipment incidentTeamEquipment = incidentTeamEquipmentOptional.get();
                                aSupprimer.remove(incidentTeamEquipment);
                                incidentService.assignEquipmentTeam(incident, equipment, incidentTeamEquipment.getTeam(), site, true);
                                aSupprimer.remove(incidentTeamEquipment);
                                level += equipment.getTypeEquipment().getLevel();
                            }
                        } else {
                            log.debug("L'équipement {} n'est pas en cours de déplacement, il faut l'envoyer avec une équipe", equipment);
                            // Rechercher une équipe disponible
                            Optional<Team> team = equipment.getFireStation().getTeams()
                                    .stream()
                                    .filter(el -> teamService.isAvailable(el))
                                    .filter(el -> teamService.getHabilitations(el).contains(equipment.getTypeEquipment()))
                                    .findFirst();
                            if(team.isPresent()) {
                                log.debug("L'équipe {} est disponible, on l'envoie", team.get());
                                incidentService.assignEquipmentTeam(incident, equipment, team.get(), site, false);
                                level += equipment.getTypeEquipment().getLevel();
                            } else {
                                log.warn("Aucune équipe disponible pour envoie de véhicule");
                            }
                        }
                        if(site.getLevel() <= level) {
                            log.debug("Le site {} est à niveau", site);
                            break;
                        }
                    }
                } else {
                    log.debug("Le site {} est en cours de traitement par les équipes sur place", site);
                }
                supprimeSite(aSupprimer);
            }
        }
    }

    private void supprimeSite(List<IncidentTeamEquipment> aSupprimer) {
        for(IncidentTeamEquipment incidentTeamEquipment : aSupprimer) {
            incidentService.unAssignEquipment(incidentTeamEquipment.getEquipment());
        }
    }

    @Override
    public void execute(JobExecutionContext jobExecutionContext) throws JobExecutionException {
        new SensorsProcessing().mainThread();
    }
}
