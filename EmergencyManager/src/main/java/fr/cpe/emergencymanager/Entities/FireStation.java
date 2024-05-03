package fr.cpe.emergencymanager.Entities;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonProperty;
import fr.cpe.emergencymanager.Repository.EquipmentRepository;
import fr.cpe.emergencymanager.Repository.TeamRepository;

import java.util.HashSet;
import java.util.Objects;
import java.util.Set;

public class FireStation extends ManageObjects {
    public static final String ENDPOINT = "firestation";
    private EquipmentRepository equipmentRepository = new EquipmentRepository();
    private TeamRepository teamRepository = new TeamRepository();

    public FireStation() {}

    public FireStation(Long id, String name, Double longitude, Double latitude) {
        this.id = id;
        this.name = name;
        this.longitude = longitude;
        this.latitude = latitude;
    }
    public FireStation(Long id, String name, Double longitude, Double latitude, EquipmentRepository equipmentRepository, TeamRepository teamRepository) {
        this.equipmentRepository = equipmentRepository;
        this.teamRepository = teamRepository;
        this.id = id;
        this.name = name;
        this.longitude = longitude;
        this.latitude = latitude;
    }

    @JsonProperty("id_fire_station")
    private Long id;

    @JsonProperty("fire_station_name")
    private String name;

    @JsonProperty("fire_station_longitude")
    private Double longitude;

    @JsonProperty("fire_station_latitude")
    private Double latitude;


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

    @JsonIgnore
    public Set<Equipment> getEquipments() {
        return equipmentRepository.findByFireStation(this);
    }
    @JsonIgnore
    public Set<Team> getTeams() {
        return teamRepository.findByFireStation(this);
    }

    @Override
    public String toString() {
        return "FireStation{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", longitude=" + longitude +
                ", latitude=" + latitude +
                '}';
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        FireStation that = (FireStation) o;
        return id.equals(that.id);
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