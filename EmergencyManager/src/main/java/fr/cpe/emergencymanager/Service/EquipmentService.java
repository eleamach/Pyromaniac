package fr.cpe.emergencymanager.Service;

import fr.cpe.emergencymanager.Entities.*;
import fr.cpe.emergencymanager.Repository.EquipmentRepository;
import fr.cpe.emergencymanager.Repository.IncidentTeamEquipmentRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.*;
import java.util.stream.Collectors;

public class EquipmentService {
    private final Logger log = LoggerFactory.getLogger(EquipmentService.class);

    private final EquipmentRepository equipmentRepository;
    private final IncidentTeamEquipmentRepository incidentTeamEquipmentRepository;

    public EquipmentService() {
        this.equipmentRepository = new EquipmentRepository();
        this.incidentTeamEquipmentRepository = new IncidentTeamEquipmentRepository();
    }

    public EquipmentService(EquipmentRepository equipmentRepository, IncidentTeamEquipmentRepository incidentTeamEquipmentRepository) {
        this.equipmentRepository = equipmentRepository;
        this.incidentTeamEquipmentRepository = incidentTeamEquipmentRepository;
    }

    public boolean isAvailable(Equipment equipment) {
        if (!equipment.isAvailable()) return false;
        Set<IncidentTeamEquipment> incidentTeamEquipments = incidentTeamEquipmentRepository.findByStatus(true);
        return !incidentTeamEquipments
                .stream()
                .anyMatch(el -> el.isDeployed() && el.getEquipmentId().equals(equipment.getId()));
    }

    public Set<Equipment> getEquipmentsByType(Set<TypeEquipment> habilitations) {
        Set<Equipment> retour = new HashSet<Equipment>();
        for (TypeEquipment habilitation : habilitations) {
            retour.addAll(equipmentRepository.findByTypeEquipment(habilitation));
        }
        return retour;
    }

    public List<Equipment> getClosestEquipments(Site site, Set<Equipment> equipments) {
        return getClosestEquipments(site.getLatitude(), site.getLongitude(), equipments);
    }
    public List<Equipment> getClosestEquipments(Site site) {
        return getClosestEquipments(site.getLatitude(), site.getLongitude(), new HashSet<Equipment>());
    }
    public List<Equipment> getClosestEquipments(Double incidentLatitude, Double incidentLongitude) {
        return getClosestEquipments(incidentLatitude, incidentLongitude, new HashSet<Equipment>());
    }
    public List<Equipment> getClosestEquipments(Double incidentLatitude, Double incidentLongitude, Set<Equipment> equipments) {
        List<Equipment> sortedEquipments = equipmentRepository.findAll()
                .stream()
                .filter(equipment -> isAvailable(equipment) || equipments.contains(equipment))
                .collect(Collectors.toCollection(ArrayList::new));
        Collections.sort(sortedEquipments, Comparator.comparingDouble(equipment ->
                calculateHaversineDistance(equipment.getLatitude(), equipment.getLongitude(),
                        incidentLatitude, incidentLongitude)));
        return sortedEquipments;
    }

    private double calculateHaversineDistance(Double lat1, Double lon1, Double lat2, Double lon2) {
        final int R = 6371; // Rayon de la Terre en kilomètres

        double dLat = Math.toRadians(lat2 - lat1);
        double dLon = Math.toRadians(lon2 - lon1);

        double a = Math.sin(dLat / 2) * Math.sin(dLat / 2) +
                Math.cos(Math.toRadians(lat1)) * Math.cos(Math.toRadians(lat2)) *
                        Math.sin(dLon / 2) * Math.sin(dLon / 2);

        double c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

        return R * c;
    }

    public Optional<IncidentTeamEquipment> findIncidentTeamEquipmentByEquipmentInProgress(Equipment equipment) {
        return incidentTeamEquipmentRepository.findByStatus(true)
                .stream()
                .filter(el -> el.getEquipmentId().equals(equipment.getId()))
                .findFirst();
    }

    public float getActualCapacityBySite(Site site) {
        return (float) incidentTeamEquipmentRepository.findByStatus(true)
                .stream()
                .filter(el -> el.getEvents().stream().findFirst().isPresent())
                .filter(el -> {
                    EventIncidentTeamEquipment event = el.getEvents().stream().findFirst().get();
                    return event.getLongitude().equals(site.getLongitude())
                            && event.getLatitude().equals(site.getLatitude());
                })
                .filter(el -> el.getEquipment() != null && el.getEquipment().getTypeEquipment() != null)
                .mapToDouble(el -> el.getEquipment().getTypeEquipment().getLevel())
                .sum();
    }
}
