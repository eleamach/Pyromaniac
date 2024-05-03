package fr.cpe.emergencymanager.Entities;

import java.util.Objects;

public class Site {
    private Double latitude;
    private Double longitude;
    private Float level;

    public Site() {}

    public Site(Double longitude, Double latitude, Float level) {
        this.latitude = latitude;
        this.longitude = longitude;
        this.level = level;
    }

    public Double getLatitude() {
        return latitude;
    }

    public void setLatitude(Double latitude) {
        this.latitude = latitude;
    }

    public Double getLongitude() {
        return longitude;
    }

    public void setLongitude(Double longitude) {
        this.longitude = longitude;
    }

    public Float getLevel() {
        return level;
    }

    public void setLevel(Float level) {
        this.level = level;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Site site = (Site) o;
        if(level != null && site.level != null) {
            if(!level.equals(site.level)) return false;
        }
        return latitude.equals(site.latitude) && longitude.equals(site.longitude);
    }

    @Override
    public int hashCode() {
        return Objects.hash(longitude, latitude);
    }

    @Override
    public String toString() {
        return "Site{" +
                "longitude=" + longitude +
                ", latitude=" + latitude +
                ", level=" + level +
                '}';
    }
}
