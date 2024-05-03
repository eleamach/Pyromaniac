package fr.cpe.emergencymanager.Entities;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonProperty;
import fr.cpe.emergencymanager.Repository.IncidentTeamEquipmentRepository;

import java.time.LocalDateTime;
import java.util.Objects;

public class EventIncidentTeamEquipment extends ManageObjects {
    public static final String ENDPOINT = "event-incident-team-equipment/";
    private IncidentTeamEquipmentRepository incidentTeamEquipmentRepository = new IncidentTeamEquipmentRepository();

    public EventIncidentTeamEquipment() {}

    public EventIncidentTeamEquipment(Long id, Long incidentTeamEquipmentId, Double longitude, Double latitude, LocalDateTime date, EventIncidentTeamEquipmentMessage message) {
        this.id = id;
        this.incidentTeamEquipmentId = incidentTeamEquipmentId;
        this.longitude = longitude;
        this.latitude = latitude;
        this.date = date;
        this.message = message;
    }

    public EventIncidentTeamEquipment(Long id, Long incidentTeamEquipmentId, Double longitude, Double latitude, LocalDateTime date, EventIncidentTeamEquipmentMessage message, IncidentTeamEquipmentRepository incidentTeamEquipmentRepository) {
        this.incidentTeamEquipmentRepository = incidentTeamEquipmentRepository;
        this.id = id;
        this.incidentTeamEquipmentId = incidentTeamEquipmentId;
        this.longitude = longitude;
        this.latitude = latitude;
        this.date = date;
        this.message = message;
    }

    @JsonProperty("id_event_incident_team_equipment")
    private Long id;

    @JsonProperty("id_incident_team_equipment")
    private Long incidentTeamEquipmentId;

    @JsonProperty("event_incident_team_equipment_longitude")
    private Double longitude;

    @JsonProperty("event_incident_team_equipment_latitude")
    private Double latitude;

    @JsonProperty("event_incident_team_equipment_date")
    @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss")
    private LocalDateTime date;

    @JsonProperty("event_incident_team_equipment_info")
    private EventIncidentTeamEquipmentMessage message;


    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public Long getIncidentTeamEquipmentId() {
        return incidentTeamEquipmentId;
    }

    public void setIncidentTeamEquipmentId(Long incidentTeamEquipmentId) {
        this.incidentTeamEquipmentId = incidentTeamEquipmentId;
    }

    public Double getLongitude() {
        return longitude;
    }

    public void setLongitude(Double longitude) {
        this.longitude = longitude;
    }

    public Double getLatitude() {
        return latitude;
    }

    public void setLatitude(Double latitude) {
        this.latitude = latitude;
    }

    public LocalDateTime getDate() {
        return date;
    }

    public void setDate(LocalDateTime date) {
        this.date = date;
    }

    public EventIncidentTeamEquipmentMessage getMessage() {
        return message;
    }

    public void setMessage(EventIncidentTeamEquipmentMessage message) {
        this.message = message;
    }

    @JsonIgnore
    public IncidentTeamEquipment getIncidentTeamEquipment() {
        return incidentTeamEquipmentRepository.findById(incidentTeamEquipmentId);
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        EventIncidentTeamEquipment that = (EventIncidentTeamEquipment) o;
        return id.equals(that.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }

    @Override
    public String toString() {
        return "EventIncidentTeamEquipment{" +
                "id=" + id +
                ", incidentTeamEquipmentId=" + incidentTeamEquipmentId +
                ", longitude=" + longitude +
                ", latitude=" + latitude +
                ", date=" + date +
                ", message='" + message + '\'' +
                '}';
    }

    @Override
    public Long getIdentify() {
        return id;
    }
}