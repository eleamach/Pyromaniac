package fr.cpe.emergencymanager.Entities;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonProperty;
import fr.cpe.emergencymanager.Repository.FireStationRepository;
import fr.cpe.emergencymanager.Repository.TypeEquipmentRepository;


public class Equipment extends ManageObjects {
    public static final String ENDPOINT = "equipment";
    private FireStationRepository fireStationRepository = new FireStationRepository();
    private TypeEquipmentRepository typeEquipmentRepository = new TypeEquipmentRepository();

    public Equipment() {}

    public Equipment(Long id, String name, Long typeId, Long fireStationId, Double longitude, Double latitude, boolean available) {
        this.id = id;
        this.name = name;
        this.typeId = typeId;
        this.fireStationId = fireStationId;
        this.longitude = longitude;
        this.latitude = latitude;
        this.available = available;
    }

    public Equipment(Long id, String name, Long typeId, Long fireStationId, Double longitude, Double latitude, boolean available, FireStationRepository fireStationRepository, TypeEquipmentRepository typeEquipmentRepository) {
        this.fireStationRepository = fireStationRepository;
        this.typeEquipmentRepository = typeEquipmentRepository;
        this.id = id;
        this.name = name;
        this.typeId = typeId;
        this.fireStationId = fireStationId;
        this.longitude = longitude;
        this.latitude = latitude;
        this.available = available;
    }

    @JsonProperty("id_equipment")
    private Long id;

    @JsonProperty("equipment_name")
    private String name;

    @JsonProperty("id_type_equipment")
    private Long typeId;

    @JsonProperty("id_fire_station")
    private Long fireStationId;

    @JsonProperty("equipment_longitude")
    private Double longitude;

    @JsonProperty("equipment_latitude")
    private Double latitude;

    @JsonProperty("equipment_available")
    private boolean available;

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Long getTypeId() {
        return typeId;
    }

    public void setTypeId(Long typeId) {
        this.typeId = typeId;
    }

    public Long getFireStationId() {
        return fireStationId;
    }

    public void setFireStationId(Long fireStationId) {
        this.fireStationId = fireStationId;
    }

    @JsonIgnore
    public FireStation getFireStation() {
        return fireStationRepository.findById(this.fireStationId);
    }
    @JsonIgnore
    public void setFireStation(FireStation fireStation) {
        this.fireStationId = fireStation.getId();
    }

    @JsonIgnore
    public TypeEquipment getTypeEquipment() {
        return typeEquipmentRepository.findById(typeId);
    }
    @JsonIgnore
    public void setTypeEquipment(TypeEquipment typeEquipment) {
        this.typeId = typeEquipment.getIdentify();
    }

    public Double getLongitude() {
        return longitude;
    }

    public Double getLatitude() {
        return latitude;
    }

    public void setLongitude(Double longitude) {
        this.longitude = longitude;
    }

    public void setLatitude(Double latitude) {
        this.latitude = latitude;
    }

    public boolean isAvailable() {
        return available;
    }

    public void setAvailable(boolean available) {
        this.available = available;
    }

    @Override
    public String toString() {
        return "Equipment{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", typeId=" + typeId +
                ", fireStationId=" + fireStationId +
                ", longitude=" + longitude +
                ", latitude=" + latitude +
                '}';
    }

    @Override
    public Long getIdentify() {
        return id;
    }
}