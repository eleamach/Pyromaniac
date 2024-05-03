package fr.cpe.emergencymanager.Entities;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonProperty;
import fr.cpe.emergencymanager.Repository.EquipmentRepository;
import fr.cpe.emergencymanager.Repository.EventIncidentTeamEquipmentRepository;
import fr.cpe.emergencymanager.Repository.IncidentRepository;
import fr.cpe.emergencymanager.Repository.TeamRepository;

import java.util.ArrayList;
import java.util.Comparator;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;

public class IncidentTeamEquipment extends ManageObjects {
    public static final String ENDPOINT = "incident-team-equipment/";

    private IncidentRepository incidentRepository = new IncidentRepository();
    private TeamRepository teamRepository = new TeamRepository();
    private EquipmentRepository equipmentRepository = new EquipmentRepository();
    private EventIncidentTeamEquipmentRepository eventIncidentTeamEquipmentRepository = new EventIncidentTeamEquipmentRepository();

    public IncidentTeamEquipment() {
    }

    public IncidentTeamEquipment(Long id, Long incidentId, Long teamId, Long equipmentId, boolean isDeployed) {
        this.id = id;
        this.incidentId = incidentId;
        this.teamId = teamId;
        this.equipmentId = equipmentId;
        this.isDeployed = isDeployed;
    }

    public IncidentTeamEquipment(Long id, Long incidentId, Long teamId, Long equipmentId, boolean isDeployed, IncidentRepository incidentRepository, TeamRepository teamRepository, EquipmentRepository equipmentRepository, EventIncidentTeamEquipmentRepository eventIncidentTeamEquipmentRepository) {
        this.incidentRepository = incidentRepository;
        this.teamRepository = teamRepository;
        this.equipmentRepository = equipmentRepository;
        this.eventIncidentTeamEquipmentRepository = eventIncidentTeamEquipmentRepository;
        this.id = id;
        this.incidentId = incidentId;
        this.teamId = teamId;
        this.equipmentId = equipmentId;
        this.isDeployed = isDeployed;
    }

    @JsonProperty("id_incident_team_equipment")
    private Long id;

    @JsonProperty("id_incident")
    private Long incidentId;

    @JsonProperty("id_team")
    private Long teamId;

    @JsonProperty("id_equipment")
    private Long equipmentId;

    @JsonProperty("is_active")
    private boolean isDeployed;

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public Long getIncidentId() {
        return incidentId;
    }

    public void setIncidentId(Long incidentId) {
        this.incidentId = incidentId;
    }

    public Long getTeamId() {
        return teamId;
    }

    public void setTeamId(Long teamId) {
        this.teamId = teamId;
    }

    public Long getEquipmentId() {
        return equipmentId;
    }

    public void setEquipmentId(Long equipmentId) {
        this.equipmentId = equipmentId;
    }

    public boolean isDeployed() {
        return isDeployed;
    }

    public void setDeployed(boolean deployed) {
        isDeployed = deployed;
    }

    @JsonIgnore
    public Incident getIncident() {
        return incidentRepository.findById(incidentId);
    }

    @JsonIgnore
    public Team getTeam() {
        return teamRepository.findById(teamId);
    }

    @JsonIgnore
    public Equipment getEquipment() {
        return equipmentRepository.findById(equipmentId);
    }

    @JsonIgnore
    public List<EventIncidentTeamEquipment> getEvents() {
        return eventIncidentTeamEquipmentRepository.findByIncidentTeamEquipment(this)
                .stream()
                .sorted(Comparator.comparing(EventIncidentTeamEquipment::getDate).reversed())
                .collect(Collectors.toCollection(ArrayList::new));
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        IncidentTeamEquipment that = (IncidentTeamEquipment) o;
        return id.equals(that.id) && incidentId.equals(that.incidentId) && teamId.equals(that.teamId) && equipmentId.equals(that.equipmentId);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id, incidentId, teamId, equipmentId);
    }

    @Override
    public String toString() {
        return "IncidentTeamEquipment{" +
                "id=" + id +
                ", incidentId=" + incidentId +
                ", teamId=" + teamId +
                ", equipmentId=" + equipmentId +
                ", deployé=" + isDeployed +
                '}';
    }

    @Override
    public Long getIdentify() {
        return id;
    }
}