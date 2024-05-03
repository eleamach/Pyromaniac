package fr.cpe.emergencymanager.Service;

import fr.cpe.emergencymanager.Client.MqttClient;
import fr.cpe.emergencymanager.Entities.*;
import fr.cpe.emergencymanager.Repository.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.*;
import java.util.stream.Collectors;

public class IncidentService {
    private final Logger log = LoggerFactory.getLogger(IncidentService.class);
    private final EquipmentService equipmentService;
    private final IncidentRepository incidentRepository;
    private final IncidentTeamEquipmentRepository incidentTeamEquipmentRepository;
    private final EventIncidentTeamEquipmentRepository eventIncidentTeamEquipmentRepository;
    private final EquipmentRepository equipmentRepository;
    private final SensorService sensorService;
    private final SensorRepository sensorRepository;
    private final TeamService teamService;
    private final ParameterRepository parameterRepository;
    private final MqttClient mqttClient;

    public IncidentService() {
        this.equipmentService                     = new EquipmentService();
        this.incidentRepository                   = new IncidentRepository();
        this.incidentTeamEquipmentRepository      = new IncidentTeamEquipmentRepository();
        this.eventIncidentTeamEquipmentRepository = new EventIncidentTeamEquipmentRepository();
        this.equipmentRepository                  = new EquipmentRepository();
        this.sensorService                        = new SensorService();
        this.sensorRepository                     = new SensorRepository();
        this.teamService                          = new TeamService();
        this.parameterRepository                  = new ParameterRepository();
        this.mqttClient                           = new MqttClient();
    }

    public IncidentService(
            EquipmentService equipmentService,
            IncidentRepository incidentRepository,
            IncidentTeamEquipmentRepository incidentTeamEquipmentRepository,
            EventIncidentTeamEquipmentRepository eventIncidentTeamEquipmentRepository,
            EquipmentRepository equipmentRepository,
            SensorService sensorService,
            SensorRepository sensorRepository,
            TeamService teamService,
            ParameterRepository parameterRepository,
            MqttClient mqttClient
    ) {
        this.equipmentService = equipmentService;
        this.incidentRepository = incidentRepository;
        this.incidentTeamEquipmentRepository = incidentTeamEquipmentRepository;
        this.eventIncidentTeamEquipmentRepository = eventIncidentTeamEquipmentRepository;
        this.equipmentRepository = equipmentRepository;
        this.sensorService = sensorService;
        this.sensorRepository = sensorRepository;
        this.teamService = teamService;
        this.parameterRepository = parameterRepository;
        this.mqttClient = mqttClient;
    }

    public boolean assignEquipmentTeam(Incident incident, Equipment equipment, Team team, Site site, boolean update) {
        IncidentTeamEquipment incidentTeamEquipment;
        if(!update) {
            incidentTeamEquipment = new IncidentTeamEquipment(null, incident.getIdentify(), team.getIdentify(), equipment.getIdentify(), true);
            incidentTeamEquipment = incidentTeamEquipmentRepository.create(incidentTeamEquipment);
            eventIncidentTeamEquipmentRepository.create(new EventIncidentTeamEquipment(null, incidentTeamEquipment.getIdentify(), site.getLongitude(), site.getLatitude(), LocalDateTime.now(), EventIncidentTeamEquipmentMessage.ASSIGNE));
        } else {
            Optional<IncidentTeamEquipment> incidentTeamEquipmentOptional = equipmentService.findIncidentTeamEquipmentByEquipmentInProgress(equipment);
            if(!incidentTeamEquipmentOptional.isPresent()) {
                return false;
            }
            incidentTeamEquipment = incidentTeamEquipmentOptional.get();
            eventIncidentTeamEquipmentRepository.create(new EventIncidentTeamEquipment(null, incidentTeamEquipment.getIdentify(), site.getLongitude(), site.getLatitude(), LocalDateTime.now(), EventIncidentTeamEquipmentMessage.ASSIGNE));
        }
        mqttClient.sendMessage("equipment/" + equipment.getIdentify(), MqttMessage.INCIDENT + " " + site.getLongitude() + " " + site.getLatitude());
        return true;
    }

    public boolean unAssign(IncidentTeamEquipment incidentTeamEquipment) {
        if(incidentTeamEquipment.isDeployed()) {
            incidentTeamEquipment.setDeployed(false);
            incidentTeamEquipmentRepository.update(incidentTeamEquipment);
            eventIncidentTeamEquipmentRepository.create(new EventIncidentTeamEquipment(null, incidentTeamEquipment.getIdentify(), null, null, LocalDateTime.now(), EventIncidentTeamEquipmentMessage.ANNULE));
            mqttClient.sendMessage("equipment/" + incidentTeamEquipment.getEquipmentId(), MqttMessage.ANNULE.toString());
            return true;
        }
        return false;
    }

    public void checkEquipment(Incident incident) {
        Incident incFull = incidentRepository.findById(incident.getId());
        // TODO : Envoyer des véhicules
    }

    public boolean unAssignEquipmentDueToUnavailable(Equipment equipment) {
        Optional<IncidentTeamEquipment> incidentTeamEquipmentOptional = equipmentService.findIncidentTeamEquipmentByEquipmentInProgress(equipment);
        equipment.setAvailable(false);
        equipmentRepository.update(equipment);
        if(incidentTeamEquipmentOptional.isPresent()) {
            IncidentTeamEquipment incidentTeamEquipment = incidentTeamEquipmentOptional.get();
            incidentTeamEquipment.setDeployed(false);
            incidentTeamEquipmentRepository.update(incidentTeamEquipment);
            eventIncidentTeamEquipmentRepository.create(new EventIncidentTeamEquipment(null, incidentTeamEquipment.getIdentify(), null, null, LocalDateTime.now(), EventIncidentTeamEquipmentMessage.ANNULE));
            return true;
        }
        return false;
    }

    public boolean unAssignEquipment(Equipment equipment) {
        Optional<IncidentTeamEquipment> incidentTeamEquipmentOptional = equipmentService.findIncidentTeamEquipmentByEquipmentInProgress(equipment);
        if(incidentTeamEquipmentOptional.isPresent()) {
            IncidentTeamEquipment incidentTeamEquipment = incidentTeamEquipmentOptional.get();
            if(incidentTeamEquipment.isDeployed()) {
                incidentTeamEquipment.setDeployed(false);
                incidentTeamEquipmentRepository.update(incidentTeamEquipment);
                eventIncidentTeamEquipmentRepository.create(new EventIncidentTeamEquipment(null, incidentTeamEquipment.getIdentify(), null, null, LocalDateTime.now(), EventIncidentTeamEquipmentMessage.DEPART));
                return true;
            }
        }
        return false;
    }

    public Set<Site> getSites(Incident incident) {
        Set<Site> sites = new HashSet<Site>();
        Set<SensorFull> sensors = incident.getSensorHistos()
                        .stream()
                        .map(el -> (SensorFull) el.getSensor())
                        .collect(Collectors.toCollection(HashSet::new));

        for(SensorFull sensor : sensors) {
            List<Sensor> neighbors = sensorService.sensorNeighbor(sensor);
            boolean traited = false;
            for(Sensor neighbor : neighbors) {
                if(sensors.contains(neighbor)) {
                    sites.add(twoSensors(sensor, neighbor));
                    traited = true;
                }
            }
            if(!traited) {
                sites.add(oneSensor(sensor));
            }
        }
        return sites;
    }

    private Site twoSensors(SensorFull sensor1, Sensor sensor2) {
        Double latitude = (BigDecimal.valueOf(sensor1.getLatitude()).add(BigDecimal.valueOf(sensor2.getLatitude()))).divide(new BigDecimal(2)).doubleValue();
        Double longitude = (BigDecimal.valueOf(sensor1.getLongitude()).add(BigDecimal.valueOf(sensor2.getLongitude()))).divide(new BigDecimal(2)).doubleValue();
        float sens1 = sensor1.getSensorHistos().stream().findFirst().get().getLevel();
        float sens2 = ((SensorFull)sensorRepository.findById(sensor2.getIdentify())).getSensorHistos().stream().findFirst().get().getLevel();
        return new Site(longitude, latitude, Math.max(sens1, sens2));
    }

    private Site oneSensor(SensorFull sensor) {
        if(sensorService.sensorNeighbor(sensor).size() == 4) {
            // Cas d'un seul capteur en incident au milieu de la map
            return new Site(sensor.getLongitude(), sensor.getLatitude(), ((SensorFull)sensorRepository.findById(sensor.getIdentify())).getSensorHistos().stream().findFirst().get().getLevel());
        } else {
            // Cas d'un seul capteur en incident sur un bord de la map
            Double deltaLatitude  = (BigDecimal.valueOf(Double.valueOf(parameterRepository.findById("neighbor-latitude").getValue())).divide(new BigDecimal(2)).doubleValue());
            Double deltaLongitude = (BigDecimal.valueOf(Double.valueOf(parameterRepository.findById("neighbor-longitude").getValue())).divide(new BigDecimal(2)).doubleValue());
            if(deltaLongitude == null || deltaLatitude == null) {
                log.error("Valeurs manquantes pour calculer les voisins dans les paramètres !");
                return null;
            }

            HashMap<SensorService.Direction, Boolean> hashMap = sensorService.sensorNeighborLocation(sensor);
            Double latitude = sensor.getLatitude();
            Double longitude = sensor.getLongitude();
            Set<SensorService.Direction> directions = hashMap.keySet()
                    .stream()
                    .filter(el -> hashMap.get(el) == false)
                    .collect(Collectors.toCollection(HashSet::new));
            if(directions.contains(SensorService.Direction.GAUCHE)) {
                longitude -= deltaLongitude;
            }
            if(directions.contains(SensorService.Direction.DROITE)) {
                longitude += deltaLongitude;
            }
            if(directions.containsAll(Arrays.asList(SensorService.Direction.HAUT_DROITE, SensorService.Direction.HAUT_GAUCHE))) {
                latitude += deltaLatitude;
            }
            if(directions.containsAll(Arrays.asList(SensorService.Direction.BAS_DROITE, SensorService.Direction.BAS_GAUCHE))) {
                latitude -= deltaLatitude;
            }
            return new Site(longitude, latitude, sensor.getSensorHistos().stream().findFirst().get().getLevel());
        }
    }

    public boolean isArrived(Equipment eq) {
        Optional<IncidentTeamEquipment> incidentTeamEquipmentOptional = equipmentService.findIncidentTeamEquipmentByEquipmentInProgress(eq);
        if(incidentTeamEquipmentOptional.isPresent()) {
            IncidentTeamEquipment incidentTeamEquipment = incidentTeamEquipmentOptional.get();
            EventIncidentTeamEquipment event = incidentTeamEquipment.getEvents().stream().findFirst().get();
            eventIncidentTeamEquipmentRepository.create(new EventIncidentTeamEquipment(null, incidentTeamEquipment.getIdentify(), event.getLongitude(), event.getLatitude(), LocalDateTime.now(), EventIncidentTeamEquipmentMessage.ARRIVE));
            return true;
        }
        return false;
    }
}
