package fr.cpe.emergencymanager.Entities;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonProperty;
import fr.cpe.emergencymanager.Repository.EquipmentRepository;
import fr.cpe.emergencymanager.Repository.IncidentRepository;

import java.util.Objects;

public class IncidentEquipment extends ManageObjects {
    public static final String ENDPOINT = "incident-equipment";
    private IncidentRepository incidentRepository = new IncidentRepository();
    private EquipmentRepository equipmentRepository = new EquipmentRepository();

    public IncidentEquipment() {}

    public IncidentEquipment(Incident incident, Equipment equipment) {
        this.incidentId = incident.getId();
        this.equipmentId = equipment.getId();
    }

    public IncidentEquipment(Long incidentId, Long equipmentId) {
        this.incidentId = incidentId;
        this.equipmentId = equipmentId;
    }

    public IncidentEquipment(Incident incident, Equipment equipment, IncidentRepository incidentRepository, EquipmentRepository equipmentRepository) {
        this.equipmentRepository = equipmentRepository;
        this.incidentRepository = incidentRepository;
        this.incidentId = incident.getId();
        this.equipmentId = equipment.getId();
    }

    public IncidentEquipment(Long incidentId, Long equipmentId, IncidentRepository incidentRepository, EquipmentRepository equipmentRepository) {
        this.incidentRepository = incidentRepository;
        this.equipmentRepository = equipmentRepository;
        this.incidentId = incidentId;
        this.equipmentId = equipmentId;
    }

    @JsonProperty("id_incident")
    private Long incidentId;

    @JsonProperty("id_equipment")
    private Long equipmentId;

    public Long getIncidentId() {
        return incidentId;
    }
    public Incident getIncident() {
        return incidentRepository.findById(incidentId);
    }

    public void setIncidentId(Long incidentId) {
        this.incidentId = incidentId;
    }
    public void setIncident(Incident incident) {
        this.incidentId = incident.getId();
    }

    public Long getEquipmentId() {
        return equipmentId;
    }
    @JsonIgnore
    public Equipment getEquipment() {
        return equipmentRepository.findById(equipmentId);
    }

    public void setEquipmentId(Long equipmentId) {
        this.equipmentId = equipmentId;
    }
    @JsonIgnore
    public void setEquipment(Equipment equipment) {
        this.equipmentId = equipment.getId();
    }

    @Override
    public String toString() {
        return "IncidentEquipment{" +
                "incidentId=" + incidentId +
                ", equipmentId=" + equipmentId +
                '}';
    }

    @Override
    public int hashCode() {
        return Objects.hash(incidentId, equipmentId);
    }

    @Override
    public boolean equals(Object obj) {
        if (obj instanceof IncidentEquipment) {
            IncidentEquipment incidentEquipment = (IncidentEquipment) obj;
            return incidentEquipment.getIncidentId().equals(incidentId) && incidentEquipment.getEquipmentId().equals(equipmentId);
        }
        return false;
    }

    @Override
    public String getIdentify() {
        return "incident/" + incidentId + "/equipment/" + equipmentId + "/";
    }
}
