package fr.cpe.emergencymanager.Service;

import fr.cpe.emergencymanager.Entities.IncidentTeamEquipment;
import fr.cpe.emergencymanager.Entities.Team;
import fr.cpe.emergencymanager.Entities.TypeEquipment;
import fr.cpe.emergencymanager.Repository.EmployeeRepository;
import fr.cpe.emergencymanager.Repository.IncidentTeamEquipmentRepository;
import fr.cpe.emergencymanager.Repository.TeamRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.time.LocalTime;
import java.util.HashSet;
import java.util.Optional;
import java.util.Set;

public class TeamService {
    private final Logger log = LoggerFactory.getLogger(TeamService.class);

    private final TeamRepository teamRepository;
    private final EmployeeRepository employeeRepository;
    private final IncidentTeamEquipmentRepository incidentTeamEquipmentRepository;

    public TeamService() {
        this.teamRepository     = new TeamRepository();
        this.employeeRepository = new EmployeeRepository();
        this.incidentTeamEquipmentRepository = new IncidentTeamEquipmentRepository();
    }

    public TeamService(TeamRepository teamRepository, EmployeeRepository employeeRepository, IncidentTeamEquipmentRepository incidentTeamEquipmentRepository) {
        this.teamRepository = teamRepository;
        this.employeeRepository = employeeRepository;
        this.incidentTeamEquipmentRepository = incidentTeamEquipmentRepository;
    }

    public boolean isAvailable(Team team) {
        if (enPause(team)) return false;
        Optional<IncidentTeamEquipment> ret = incidentTeamEquipmentRepository.findByStatus(true)
                .stream()
                .filter(el -> el.isDeployed() && el.getTeamId().equals(team.getId()))
                .findFirst();
        return !ret.isPresent();
    }

    private boolean enPause(Team team) {
        // Par sécurité
        if(team.getSchedule() == null || team.getSchedule().isEmpty() || team.getSchedule().length() != 24) {
            return false;
        }

        LocalTime now = LocalTime.now();

        // Récupérer le Xème caractère de la chaîne en fonction de l'heure actuelle
        char carac = team.getSchedule().charAt(now.getHour());

        // Si le caractère est un 0, alors l'équipe est en pause
        // Sinon, elle est disponible
        return carac == '0';
    }

    public Set<TypeEquipment> getHabilitations(Team team) {
        Set<TypeEquipment> retour = new HashSet<TypeEquipment>();
        team.getEmployees()
                .stream()
                .filter(employee -> !employee.isDisabled())
                .forEach(employee -> {
                    retour.addAll(employee.getHabilitations());
                });
        return retour;
    }

    public Set<Team> getTeamsByHabilitations(TypeEquipment habilitation) {
        Set<Team> retour = new HashSet<Team>();
        employeeRepository.findByTypeEquipment(habilitation)
                .stream()
                .filter(employee -> !employee.isDisabled())
                .forEach(employee -> {
                    retour.addAll(employee.getTeams());
                });
        return retour;
    }
}
