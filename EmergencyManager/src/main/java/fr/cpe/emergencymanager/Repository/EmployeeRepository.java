package fr.cpe.emergencymanager.Repository;

import fr.cpe.emergencymanager.Client.ApiClient;
import fr.cpe.emergencymanager.Entities.Employee;
import fr.cpe.emergencymanager.Entities.Team;
import fr.cpe.emergencymanager.Entities.TypeEquipment;
import org.apache.http.HttpResponse;

import java.io.IOException;
import java.util.Set;

public class EmployeeRepository extends Repository<Employee> {
    public EmployeeRepository() {
        setType(Employee.class);
        setEndpoint(Employee.ENDPOINT);
    }

    public Employee findByEmployeeNumber(String employeeNumber) {
        try {
            HttpResponse response = API.get(getEndpoint() + "/" + employeeNumber);
            return httpResponseIsOkay(response) ? (Employee) httpToObject(response, getType()) : null;
        } catch (IOException e) {
            errorOnExecution(e);
            return null;
        }
    }

    public Set<Employee> findByTeam(Team team) {
        try {
            return (Set<Employee>) httpToObject(API.get("team-employee/teams_id/" + team.getIdentify() + "/employees"), mapper.getTypeFactory().constructCollectionType(Set.class, Employee.class));
        } catch (Exception e) {
            errorOnExecution(e);
            return null;
        }
    }

    public Set<Employee> findByTypeEquipment(TypeEquipment typeEquipment) {
        try {
            return (Set<Employee>) httpToObject(API.get("type-equipment-employee/" + typeEquipment.getIdentify() + "/employees"), mapper.getTypeFactory().constructCollectionType(Set.class, Employee.class));
        } catch (Exception e) {
            errorOnExecution(e);
            return null;
        }
    }
}
