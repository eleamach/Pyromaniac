package fr.cpe.emergencymanager.Service;

import fr.cpe.emergencymanager.Entities.Equipment;
import fr.cpe.emergencymanager.Entities.IncidentTeamEquipment;
import fr.cpe.emergencymanager.Entities.TypeEquipment;
import fr.cpe.emergencymanager.Repository.EquipmentRepository;
import fr.cpe.emergencymanager.Repository.IncidentTeamEquipmentRepository;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;

import java.util.*;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
@DisplayName("EquipmentService")
public class EquipmentServiceTest {
    @Mock
    private EquipmentRepository equipmentRepository;

    @Mock
    private IncidentTeamEquipmentRepository incidentTeamEquipmentRepository;

    @InjectMocks
    private EquipmentService equipmentService;

    @Test
    @DisplayName("Equipment le plus proche")
    public void testGetClosestEquipments() {
        // Créer des équipements fictifs
        Equipment equipment1 = new Equipment(1L, "Camion1", 1L, 1L, 4.863284, 45.770538, true);
        Equipment equipment3 = new Equipment(3L, "Camion3", 1L, 1L, 4.886794, 45.776729, false);
        Equipment equipment2 = new Equipment(2L, "Camion2", 1L, 1L, 4.876487, 45.774849, true);
        Equipment equipment4 = new Equipment(4L, "Camion4", 1L, 1L, 4.860815, 45.791009, true);
        Equipment equipment5 = new Equipment(5L, "Camion5", 1L, 1L, 4.87958, 45.75853, true);

        // Configurer le mock pour simuler le comportement du repository
        when(equipmentRepository.findAll()).thenReturn(new ArrayList<>(List.of(equipment2, equipment3, equipment1, equipment4, equipment5)));

        // Appeler la méthode à tester
        List<Equipment> result = equipmentService.getClosestEquipments(45.769273, 4.850426);

        // Assertions pour vérifier que le résultat correspond aux attentes
        assertEquals(4, result.size());
        assertEquals(equipment1, result.get(0));
        assertEquals(equipment2, result.get(1));
        assertEquals(equipment4, result.get(2));
        assertEquals(equipment5, result.get(3));
    }

    @Test
    @DisplayName("Equipments par type")
    public void testGetEquipmentsByType() {
        // Créer des équipements fictifs
        Equipment equipment1 = new Equipment(1L, "Camion1", 1L, 1L, 0.1, 0.2, true);
        Equipment equipment2 = new Equipment(2L, "Camion2", 2L, 1L, 0.1, 0.2, true);
        Equipment equipment3 = new Equipment(3L, "Camion3", 3L, 1L, 0.1, 0.2, true);

        TypeEquipment typeEquipment1 = new TypeEquipment(1L, "Type1", 0, 0, null);
        TypeEquipment typeEquipment2 = new TypeEquipment(2L, "Type2", 0, 0, null);
        TypeEquipment typeEquipment3 = new TypeEquipment(3L, "Type3", 0, 0, null);

        // Configurer le mock pour simuler le comportement du repository
        when(equipmentRepository.findByTypeEquipment(typeEquipment1)).thenReturn(new HashSet<>(Arrays.asList(equipment1)));
        when(equipmentRepository.findByTypeEquipment(typeEquipment2)).thenReturn(new HashSet<>(Arrays.asList(equipment2, equipment3)));
        when(equipmentRepository.findByTypeEquipment(typeEquipment3)).thenReturn(new HashSet<>(Arrays.asList(equipment2, equipment3)));

        // Appeler la méthode à tester
        Set<TypeEquipment> habilitations = new HashSet<>(Set.of(typeEquipment1, typeEquipment2, typeEquipment3));
        Set<Equipment> result = equipmentService.getEquipmentsByType(habilitations);

        // Assertions pour vérifier que le résultat correspond aux attentes
        assertEquals(3, result.size());
        assertEquals(new HashSet<>(Arrays.asList(equipment1, equipment2, equipment3)), result);
    }

    @Test
    @DisplayName("Est disponible")
    public void testIsAvailable() {
        Equipment equipment1 = new Equipment(1L, "Camion 1", 1L, 1L, 0.1, 0.2, false);
        Equipment equipment2 = new Equipment(2L, "Camion 2", 1L, 1L, 0.1, 0.1,true);
        Equipment equipment3 = new Equipment(3L, "Camion 3", 1L, 1L, 0.1, 0.1,true);
        Equipment equipment4 = new Equipment(4L, "Camion 4", 1L, 1L, 0.1, 0.1,true);

        IncidentTeamEquipment incidentTeamEquipment1 = new IncidentTeamEquipment(1L, 1L, 1L, 2L, true);
        IncidentTeamEquipment incidentTeamEquipment2 = new IncidentTeamEquipment(2L, 1L, 2L, 4L, false);

        when(incidentTeamEquipmentRepository.findByStatus(true)).thenReturn(new HashSet<IncidentTeamEquipment>(Arrays.asList(incidentTeamEquipment2, incidentTeamEquipment1)));

        assertFalse(equipmentService.isAvailable(equipment1));
        assertFalse(equipmentService.isAvailable(equipment2));
        assertTrue(equipmentService.isAvailable(equipment3));
        assertTrue(equipmentService.isAvailable(equipment4));
    }
}