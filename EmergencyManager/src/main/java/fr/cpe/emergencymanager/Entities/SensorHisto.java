package fr.cpe.emergencymanager.Entities;

import com.fasterxml.jackson.annotation.*;
import fr.cpe.emergencymanager.Repository.SensorRepository;

import java.time.LocalDateTime;
import java.util.Objects;

public class SensorHisto extends ManageObjects {
    public static final String ENDPOINT = "sensor-histo";

    private SensorRepository sensorRepository = new SensorRepository();

    public SensorHisto() {}

    public SensorHisto(Long id, Long sensorId, float level, LocalDateTime dateTime, boolean isProcessed) {
        this.id = id;
        this.sensorId = sensorId;
        this.level = level;
        this.dateTime = dateTime;
        this.isProcessed = isProcessed;
    }

    public SensorHisto(Long id, Long sensorId, float level, LocalDateTime dateTime, boolean isProcessed, SensorRepository sensorRepository) {
        this.sensorRepository = sensorRepository;
        this.id = id;
        this.sensorId = sensorId;
        this.level = level;
        this.dateTime = dateTime;
        this.isProcessed = isProcessed;
    }

    @JsonProperty("id_sensor_histo")
    private Long id;

    @JsonProperty("id_sensor")
    private Long sensorId;

    @JsonProperty("sensor_histo_value")
    private float level;

    @JsonProperty("sensor_histo_date")
    @JsonFormat(pattern = "yyyy-MM-dd'T'HH:mm:ss")
    private LocalDateTime dateTime;

    @JsonProperty("sensor_histo_is_processed")
    private boolean isProcessed;

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public Long getSensorId() {
        return sensorId;
    }

    public void setSensorId(Long sensorId) {
        this.sensorId = sensorId;
    }

    public float getLevel() {
        return level;
    }

    public void setLevel(float level) {
        this.level = level;
    }

    public LocalDateTime getDateTime() {
        return dateTime;
    }

    public void setDateTime(LocalDateTime dateTime) {
        this.dateTime = dateTime;
    }

    public boolean isProcessed() {
        return isProcessed;
    }

    public void setProcessed() {
        isProcessed = true;
    }

    @JsonIgnore
    public Sensor getSensor() {
        return sensorRepository.findById(sensorId);
    }

    @Override
    public String toString() {
        return "SensorHisto{" +
                "sensor=" + sensorId +
                ", level=" + level +
                ", dateTime=" + dateTime +
                ", isProcessed=" + isProcessed +
                '}';
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        SensorHisto that = (SensorHisto) o;
        return sensorId.equals(that.sensorId) && dateTime.equals(that.dateTime);
    }

    @Override
    public int hashCode() {
        return Objects.hash(sensorId, dateTime);
    }

    @Override
    public Long getIdentify() {
        return id;
    }
}
