package fr.cpe.emergencymanager.Service;

import fr.cpe.emergencymanager.Entities.Employee;
import fr.cpe.emergencymanager.Entities.Team;
import fr.cpe.emergencymanager.Entities.TypeEquipment;
import fr.cpe.emergencymanager.Repository.EmployeeRepository;
import fr.cpe.emergencymanager.Repository.FireStationRepository;
import fr.cpe.emergencymanager.Repository.TeamRepository;
import fr.cpe.emergencymanager.Repository.TypeEquipmentRepository;
import fr.cpe.emergencymanager.Service.TeamService;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.lenient;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
@DisplayName("TeamService")
public class TeamServiceTest {
    @Mock
    private TeamRepository teamRepository;

    @Mock
    private EmployeeRepository employeeRepository;

    private FireStationRepository fireStationRepository;

    @Mock
    private TypeEquipmentRepository typeEquipmentRepository;

    @InjectMocks
    private TeamService teamService;


    @Test
    @DisplayName("Habilitations d'une team")
    public void testGetHabilitations() {
        // Créer une équipe fictive avec des employés et des habilitations
        TypeEquipment habilitation1 = new TypeEquipment(1L, "Habilitation1", 0, 0, null);
        TypeEquipment habilitation2 = new TypeEquipment(2L, "Habilitation2", 0, 0, null);
        TypeEquipment habilitation3 = new TypeEquipment(3L, "Habilitation3", 0, 0, null);

        Employee employee1 = new Employee("John", "Doe", "88", false, "", teamRepository, typeEquipmentRepository);
        Employee employee2 = new Employee("Jane", "Doe", "89", false, "", teamRepository, typeEquipmentRepository);
        Employee employee3 = new Employee("Compte", "Désactivé", "91", true, "", teamRepository, typeEquipmentRepository);

        Team team = new Team(1L, "Team", null, 1L, employeeRepository, fireStationRepository);

        // Configurer le mock pour simuler le comportement des repository
        when(employeeRepository.findByTeam(team)).thenReturn(new HashSet<>(Arrays.asList(employee1, employee2, employee3)));
        when(typeEquipmentRepository.findByEmployee(employee1)).thenReturn(new HashSet<>(Arrays.asList(habilitation1)));
        when(typeEquipmentRepository.findByEmployee(employee2)).thenReturn(new HashSet<>(Arrays.asList(habilitation2, habilitation1)));
        lenient().when(typeEquipmentRepository.findByEmployee(employee3)).thenReturn(new HashSet<>(Arrays.asList(habilitation3)));

        // Méthode à tester
        Set<TypeEquipment> result = teamService.getHabilitations(team);

        // Assert pour vérifier que le résultat correspond aux attentes
        assertEquals(2, result.size());
        assertEquals(new HashSet<>(Arrays.asList(habilitation1, habilitation2)), result);
    }

    @Test
    @DisplayName("Team par habilitation")
    public void testGetTeamsByHabilitations() {
        // Créer une habilitation fictive et une équipe fictive avec des employés
        TypeEquipment habilitation1 = new TypeEquipment(1L, "Type1", 0, 0, null);

        Employee employee1 = new Employee("John", "Doe", "78", false, "", teamRepository, typeEquipmentRepository);
        Employee employee2 = new Employee("Jane", "Doe", "79", false, "", teamRepository, typeEquipmentRepository);
        Employee employee3 = new Employee("Compte", "Désactivé", "80", true, "", teamRepository, typeEquipmentRepository);
        Employee employee4 = new Employee("Alice", "Smith", "81", false, "", teamRepository, typeEquipmentRepository);
        Employee employee5 = new Employee("Bob", "Johnson", "82", false, "", teamRepository, typeEquipmentRepository);

        Team team1 = new Team(1L, "Team1", null, 1L, employeeRepository, fireStationRepository); // Cas où tous les membres sont habilités
        Team team2 = new Team(2L, "Team2", null, 1L, employeeRepository, fireStationRepository); // Cas où un membre est habilité
        Team team3 = new Team(3L, "Team3", null, 1L, employeeRepository, fireStationRepository); // Cas où un membre habilité est désactivé
        Team team4 = new Team(4L, "Team4", null, 1L, employeeRepository, fireStationRepository); // Cas où un membre habilité est rattaché à deux équipes

        // Configurer le mock pour simuler le comportement du repository
        when(employeeRepository.findByTypeEquipment(habilitation1)).thenReturn(new HashSet<>(Arrays.asList(employee1, employee2, employee3, employee4, employee5)));
        when(teamRepository.findByEmployee(employee1)).thenReturn(new HashSet<Team>(Arrays.asList(team1)));
        when(teamRepository.findByEmployee(employee2)).thenReturn(new HashSet<Team>(Arrays.asList(team1)));
        lenient().when(teamRepository.findByEmployee(employee3)).thenReturn(new HashSet<Team>(Arrays.asList(team3)));
        when(teamRepository.findByEmployee(employee4)).thenReturn(new HashSet<Team>(Arrays.asList(team2)));
        when(teamRepository.findByEmployee(employee5)).thenReturn(new HashSet<Team>(Arrays.asList(team1, team4)));

        // Méthode à tester
        Set<Team> result = teamService.getTeamsByHabilitations(habilitation1);

        // Assert pour vérifier que le résultat correspond aux attentes
        assertEquals(3, result.size());
        assertEquals(new HashSet<>(Arrays.asList(team1, team2, team4)), result);
    }
}