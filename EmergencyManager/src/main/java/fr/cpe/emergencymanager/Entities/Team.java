package fr.cpe.emergencymanager.Entities;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonProperty;
import fr.cpe.emergencymanager.Repository.EmployeeRepository;
import fr.cpe.emergencymanager.Repository.FireStationRepository;

import java.util.Objects;
import java.util.Set;

public class Team extends ManageObjects {
    public static final String ENDPOINT = "teams";

    private EmployeeRepository employeeRepository = new EmployeeRepository();
    private FireStationRepository fireStationRepository = new FireStationRepository();

    public Team() {}

    public Team(Long id, String nom, String schedule, Long fireStationId) {
        this.id = id;
        this.nom = nom;
        this.schedule = schedule;
        this.fireStationId = fireStationId;
    }

    public Team(Long id, String nom, String schedule, Long fireStationId, EmployeeRepository employeeRepository, FireStationRepository fireStationRepository) {
        this.employeeRepository = employeeRepository;
        this.fireStationRepository = fireStationRepository;
        this.id = id;
        this.nom = nom;
        this.schedule = schedule;
        this.fireStationId = fireStationId;
    }

    @JsonProperty("id_team")
    private Long id;

    @JsonProperty("team_name")
    private String nom;

    @JsonProperty("team_schedule")
    private String schedule;

    @JsonProperty("id_fire_station")
    private Long fireStationId;

    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getNom() {
        return nom;
    }

    public void setNom(String nom) {
        this.nom = nom;
    }

    public String getSchedule() {
        return schedule;
    }

    public void setSchedule(String schedule) {
        this.schedule = schedule;
    }

    public Long getFireStationId() {
        return fireStationId;
    }

    public void setFireStationId(Long fireStationId) {
        this.fireStationId = fireStationId;
    }

    @JsonIgnore
    public Set<Employee> getEmployees() {
        return employeeRepository.findByTeam(this);
    }
    @JsonIgnore
    public FireStation getFireStation() { return fireStationRepository.findById(fireStationId); }

    @Override
    public String toString() {
        return "Team{" +
                "id=" + id +
                ", nom='" + nom + '\'' +
                ", schedule='" + schedule + '\'' +
                ", fireStationId=" + fireStationId +
                '}';
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Team team = (Team) o;
        return id.equals(team.id);
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
