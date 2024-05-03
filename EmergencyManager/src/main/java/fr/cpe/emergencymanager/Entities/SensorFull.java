package fr.cpe.emergencymanager.Entities;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.HashSet;
import java.util.Set;

public class SensorFull extends Sensor {
    public SensorFull() {}

    public SensorFull(Sensor sensor, Set<SensorHisto> sensorHistos) {
        this.id = sensor.getId();
        this.longitude = sensor.getLongitude();
        this.latitude = sensor.getLatitude();
        this.sensorHistos = sensorHistos;
    }

    public SensorFull(Long id, Double longitude, Double latitude, Set<SensorHisto> sensorHistos) {
        this.id = id;
        this.longitude = longitude;
        this.latitude = latitude;
        this.sensorHistos = sensorHistos;
    }

    @JsonProperty("sensor_histo")
    private Set<SensorHisto> sensorHistos = new HashSet<>();

    @JsonIgnore
    public Set<SensorHisto> getSensorHistos() {
        return sensorHistos;
    }

    @Override
    public String toString() {
        return "SensorFull{" +
                "id=" + id +
                ", longitude=" + longitude +
                ", latitude=" + latitude +
                ", status=" + status +
                ", sensorHistos=" + sensorHistos +
                '}';
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if(o == null) return false;
        if (!(o instanceof SensorFull)) {
            if(o instanceof Sensor) {
                return id.equals(((Sensor) o).id);
            }
            return false;
        }
        SensorFull otherSensorFull = (SensorFull) o;
        if (this.getId() == null || otherSensorFull.getId() == null) {
            return false;
        }
        return id.equals(otherSensorFull.id);
    }
}