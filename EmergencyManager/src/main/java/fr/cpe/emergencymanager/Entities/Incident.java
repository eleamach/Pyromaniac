package fr.cpe.emergencymanager.Entities;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonProperty;
import fr.cpe.emergencymanager.Repository.IncidentSensorHistoRepository;

import java.util.HashSet;
import java.util.Objects;
import java.util.Set;
import java.util.stream.Collectors;

public class Incident extends ManageObjects {
    public static final String ENDPOINT = "incidents";
    private IncidentSensorHistoRepository incidentSensorHistoRepository = new IncidentSensorHistoRepository();

    public Incident() {}

    public Incident(boolean status, Long id) {
        this.status = status;
        this.id = id;
    }

    public Incident(boolean status, Long id, IncidentSensorHistoRepository incidentSensorHistoRepository) {
        this.incidentSensorHistoRepository = incidentSensorHistoRepository;
        this.status = status;
        this.id = id;
    }

    @JsonProperty("incident_status")
    protected boolean status;

    @JsonProperty("id_incident")
    protected Long id;

    public boolean isStatus() {
        return status;
    }

    public void setStatus(boolean status) {
        this.status = status;
    }

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    @JsonIgnore
    public Set<SensorHisto> getSensorHistos() {
        return incidentSensorHistoRepository.findIncidentSensorHistoByIncident(this)
                .stream()
                .map(el -> el.getSensorHisto())
                .collect(Collectors.toCollection(HashSet::new));
    }
    @JsonIgnore
    public void addSensorHisto(SensorHisto sensorHisto) {
        incidentSensorHistoRepository.create(new IncidentSensorHisto(this, sensorHisto));
    }


    @Override
    public String toString() {
        return "Incident{" +
                "status=" + status +
                ", id=" + id +
                '}';
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Incident incident = (Incident) o;
        return id.equals(incident.id);
    }

    @Override
    public int hashCode() {
        return Objects.hash(id);
    }

    @Override
    public Long getIdentify() {
        return id;
    }
}