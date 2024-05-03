package fr.cpe.emergencymanager.Entities;

import com.fasterxml.jackson.annotation.JsonProperty;

public class TypeEquipment extends ManageObjects {
    public static final String ENDPOINT = "type-equipment";

    @JsonProperty("id_type_equipment")
    private Long id;

    @JsonProperty("type_equipment_name")
    private String nom;

    @JsonProperty("type_equipment_pers")
    private int capacityPers;

    @JsonProperty("type_equipment_level_incident")
    private float level;

    @JsonProperty("type_equipment_image")
    private String image;

    public String getNom() {
        return nom;
    }

    public void setNom(String nom) {
        this.nom = nom;
    }

    public int getCapacityPers() {
        return capacityPers;
    }

    public void setCapacityPers(int capacityPers) {
        this.capacityPers = capacityPers;
    }

    public float getLevel() {
        return level;
    }

    public void setLevel(float level) {
        this.level = level;
    }

    public String getImage() {
        return image;
    }

    public void setImage(String image) {
        this.image = image;
    }

    @Override
    public String toString() {
        return "TypeEquipment{" +
                "nom='" + nom + '\'' +
                ", capacityPers=" + capacityPers +
                ", level=" + level +
                ", image='" + image + '\'' +
                '}';
    }

    @Override
    public Long getIdentify() {
        return id;
    }
}