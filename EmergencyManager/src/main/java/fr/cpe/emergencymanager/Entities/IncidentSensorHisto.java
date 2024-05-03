package fr.cpe.emergencymanager.Entities;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonProperty;
import fr.cpe.emergencymanager.Repository.IncidentRepository;
import fr.cpe.emergencymanager.Repository.SensorHistoRepository;

import java.util.Objects;

public class IncidentSensorHisto extends ManageObjects {
    public static String ENDPOINT = "incident-sensor-histo";

    private IncidentRepository incidentRepository = new IncidentRepository();
    private SensorHistoRepository sensorHistoRepository = new SensorHistoRepository();

    public IncidentSensorHisto() {}

    public IncidentSensorHisto(Incident incident, SensorHisto sensorHisto) {
        this.incidentId = incident.getId();
        this.sensorHistoId = sensorHisto.getId();
    }

    public IncidentSensorHisto(Incident incident, SensorHisto sensorHisto, IncidentRepository incidentRepository, SensorHistoRepository sensorHistoRepository) {
        this.incidentRepository = incidentRepository;
        this.sensorHistoRepository = sensorHistoRepository;
        this.incidentId = incident.getId();
        this.sensorHistoId = sensorHisto.getId();
    }

    @JsonProperty("id_incident")
    private Long incidentId;

    @JsonProperty("id_sensor_histo")
    private Long sensorHistoId;

    public Long getIncidentId() {
        return incidentId;
    }
    @JsonIgnore
    public Incident getIncident() {
        return incidentRepository.findById(incidentId);
    }

    public void setIncidentId(Long incidentId) {
        this.incidentId = incidentId;
    }
    public void setIncident(Incident incident) {
        this.incidentId = incident.getIdentify();
    }

    public Long getSensorHistoId() {
        return sensorHistoId;
    }
    @JsonIgnore
    public SensorHisto getSensorHisto() {
        return sensorHistoRepository.findById(sensorHistoId);
    }

    public void setSensorHistoId(Long sensorHistoId) {
        this.sensorHistoId = sensorHistoId;
    }
    public void setSensorHisto(SensorHisto sensorHisto) {
        this.sensorHistoId = sensorHisto.getIdentify();
    }

    @Override
    public String toString() {
        return "IncidentSensorHisto{" +
                "incidentId=" + incidentId +
                ", sensorHistoId=" + sensorHistoId +
                '}';
    }

    @Override
    public int hashCode() {
        return Objects.hash(incidentId, sensorHistoId);
    }

    @Override
    public boolean equals(Object obj) {
        return obj instanceof IncidentSensorHisto &&
                ((IncidentSensorHisto) obj).incidentId.equals(this.incidentId) &&
                ((IncidentSensorHisto) obj).sensorHistoId.equals(this.sensorHistoId);
    }

    @Override
    public Object getIdentify() {
        return null;
    }
}
