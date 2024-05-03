package fr.cpe.emergencymanager.Entities;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.Objects;

public class Sensor extends ManageObjects {
    public static final String ENDPOINT = "sensor";

    public Sensor() {}

    public Sensor(Long id, Double longitude, Double latitude, boolean status) {
        this.id = id;
        this.latitude = latitude;
        this.longitude = longitude;
        this.status = status;
    }

    @JsonProperty("id_sensor")
    protected Long id;

    @JsonProperty("sensor_latitude")
    protected Double latitude;

    @JsonProperty("sensor_longitude")
    protected Double longitude;

    @JsonProperty("sensor_status")
    protected boolean status;

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public Double getLatitude() {
        return latitude;
    }

    public Double getLongitude() {
        return longitude;
    }

    public void setLatitude(Double latitude) {
        this.latitude = latitude;
    }

    public void setLongitude(Double longitude) {
        this.longitude = longitude;
    }

    public boolean isStatus() {
        return status;
    }

    public void setStatus(boolean status) {
        this.status = status;
    }

    @Override
    public String toString() {
        return "Sensor{" +
                "id=" + id +
                ", latitude=" + latitude +
                ", longitude=" + longitude +
                ", status=" + status +
                '}';
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if(o == null) return false;
        if(o instanceof SensorFull) {
            return id.equals(((SensorFull) o).getId());
        }
        if (getClass() != o.getClass()) return false;
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