package fr.cpe.emergencymanager.Entities;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.Objects;

public class Sensor extends ManageObjects {
    public static final String ENDPOINT = "sensor";

    @JsonProperty("id_sensor")
    private Long id;

    @JsonProperty("sensor_latitude")
    private Float latitude;

    @JsonProperty("sensor_longitude")
    private Float longitude;

    // TODO : Faire ajouter le dernier historique du capteur
    private SensorHisto lastSensorHisto;

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public Float getLatitude() {
        return latitude;
    }

    public Float getLongitude() {
        return longitude;
    }

    public void setLatitude(Float latitude) {
        this.latitude = latitude;
    }

    public void setLongitude(Float longitude) {
        this.longitude = longitude;
    }

    public SensorHisto getLastSensorHisto() {
        return lastSensorHisto;
    }

    @Override
    public String toString() {
        return "Sensor{" +
                "id=" + id +
                ", latitude=" + latitude +
                ", longitude=" + longitude +
                ", lastHistoSensor=" + lastSensorHisto +
                '}';
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Sensor sensor = (Sensor) o;
        return id.equals(sensor.id);
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
