package fr.cpe.emergencymanager.Entities;

import com.fasterxml.jackson.annotation.JsonProperty;
import fr.cpe.emergencymanager.Repository.EmployeeRepository;
import fr.cpe.emergencymanager.Repository.TeamRepository;

import java.util.Objects;

public class TeamEmployee extends ManageObjects {
    public static final String ENDPOINT = "team-employee";

    private TeamRepository teamRepository = new TeamRepository();
    private EmployeeRepository employeeRepository = new EmployeeRepository();

    public TeamEmployee() {}

    public TeamEmployee(Long teamId, String employeeId) {
        this.teamId = teamId;
        this.employeeId = employeeId;
    }

    public TeamEmployee(Long teamId, String employeeId, TeamRepository teamRepository, EmployeeRepository employeeRepository) {
        this.teamRepository = teamRepository;
        this.employeeRepository = employeeRepository;
        this.teamId = teamId;
        this.employeeId = employeeId;
    }

    @JsonProperty("id_team")
    private Long teamId;

    @JsonProperty("employee_number")
    private String employeeId;

    public Long getTeamId() {
        return teamId;
    }
    public Team getTeam() {
        return teamRepository.findById(teamId);
    }

    public void setTeamId(Long teamId) {
        this.teamId = teamId;
    }
    public void setTeam(Team team) {
        this.teamId = team.getId();
    }

    public String getEmployeeId() {
        return employeeId;
    }
    public Employee getEmployee() {
        return employeeRepository.findById(employeeId);
    }

    public void setEmployeeNumber(String employeeNumber) {
        this.employeeId = employeeNumber;
    }

    @Override
    public String toString() {
        return "TeamEmployee{" +
                "teamId=" + teamId +
                ", employeeId='" + employeeId + '\'' +
                '}';
    }

    @Override
    public int hashCode() {
        return Objects.hash(teamId, employeeId);
    }

    @Override
    public boolean equals(Object obj) {
        if (obj instanceof TeamEmployee) {
            TeamEmployee teamEmployee = (TeamEmployee) obj;
            return teamEmployee.getTeamId().equals(teamId) && teamEmployee.getEmployeeId().equals(employeeId);
        }
        return false;
    }

    @Override
    public String getIdentify() {
        return "emp/" + employeeId + "/tea/" + teamId + "/";
    }
}
