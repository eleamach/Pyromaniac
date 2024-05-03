/*
 * Copyright (c) 2024.
 * Autheur : Adrien JAUFRE
 */

package fr.cpe.emergencymanager.Entities;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.Objects;

public class Parameter extends ManageObjects {
    public static final String ENDPOINT = "parameters";
    @JsonProperty("id_parameter")
    private String parametre;

    @JsonProperty("value")
    private String value;

    public Parameter() {
    }

    public Parameter(String parametre, String value) {
        this.parametre = parametre;
        this.value = value;
    }

    public String getParametre() {
        return parametre;
    }

    public void setParametre(String parametre) {
        this.parametre = parametre;
    }

    public String getValue() {
        return value;
    }

    public void setValue(String value) {
        this.value = value;
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Parameter parameter = (Parameter) o;
        return parametre.equals(parameter.parametre);
    }

    @Override
    public int hashCode() {
        return Objects.hash(parametre);
    }

    @Override
    public String toString() {
        return "Parameter{" +
                "parametre='" + parametre + '\'' +
                ", value='" + value + '\'' +
                '}';
    }

    @Override
    public String getIdentify() {
        return parametre;
    }
}
