package fr.cpe.emergencymanager.Entities;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonProperty;
import fr.cpe.emergencymanager.Repository.TeamRepository;
import fr.cpe.emergencymanager.Repository.TypeEquipmentRepository;

import java.util.Objects;
import java.util.Set;

public class Employee extends ManageObjects {
    public static final String ENDPOINT = "employees";
    private TeamRepository teamRepository = new TeamRepository();
    private TypeEquipmentRepository typeEquipmentRepository = new TypeEquipmentRepository();

    public Employee() {}

    public Employee(String firstName, String lastName, String matricule, boolean disabled, String password) {
        this.firstName = firstName;
        this.lastName = lastName;
        this.matricule = matricule;
        this.disabled = disabled;
        this.password = password;
    }

    public Employee(String firstName, String lastName, String matricule, boolean disabled, String password, TeamRepository teamRepository, TypeEquipmentRepository typeEquipmentRepository) {
        this.teamRepository = teamRepository;
        this.typeEquipmentRepository = typeEquipmentRepository;
        this.firstName = firstName;
        this.lastName = lastName;
        this.matricule = matricule;
        this.disabled = disabled;
        this.password = password;
    }

    @JsonProperty("employee_first_name")
    private String firstName;

    @JsonProperty("employee_last_name")
    private String lastName;

    @JsonProperty("employee_number")
    private String matricule;

    @JsonProperty("employee_disable")
    private boolean disabled;

    @JsonProperty("employee_password")
    private String password;

    public String getFirstName() {
        return firstName;
    }

    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }

    public String getLastName() {
        return lastName;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }

    public String getMatricule() {
        return matricule;
    }

    public void setMatricule(String matricule) {
        this.matricule = matricule;
    }

    public boolean isDisabled() {
        return disabled;
    }

    public void setDisabled(boolean disabled) {
        this.disabled = disabled;
    }

    @JsonIgnore
    public Set<TypeEquipment> getHabilitations() {
        return typeEquipmentRepository.findByEmployee(this);
    }

    @JsonIgnore
    public Set<Team> getTeams() {
        return teamRepository.findByEmployee(this);
    }

    @Override
    public String toString() {
        return "Employee{" +
                "firstName='" + firstName + '\'' +
                ", lastName='" + lastName + '\'' +
                ", matricule='" + matricule + '\'' +
                ", disabled=" + disabled +
                '}';
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Employee employe = (Employee) o;
        return matricule.equals(employe.matricule);
    }

    @Override
    public int hashCode() {
        return Objects.hash(matricule);
    }

    @Override
    public String getIdentify() {
        return matricule;
    }
}