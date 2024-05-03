package fr.cpe.emergencymanager.Repository;

import fr.cpe.emergencymanager.Entities.Employee;
import fr.cpe.emergencymanager.Entities.Team;
import org.apache.http.HttpResponse;

import java.io.IOException;
import java.util.HashSet;
import java.util.Set;

public class EmployeeRepository extends Repository<Employee> {
    public EmployeeRepository() {
        setType(Employee.class);
        setEndpoint(Employee.ENDPOINT);
    }

    public Set<Employee> findByTeam(Team team) {
        Set<Employee> retour = new HashSet<Employee>();
        try {
            HttpResponse response = API.get("team-employee/" + team.getIdentify() + "/" + Employee.ENDPOINT);
            return httpResponseIsOkay(response) ? (Set<Employee>) httpToObject(response, mapper.getTypeFactory().constructCollectionType(Set.class, super.getType())) : retour;
        } catch (IOException e) {
            errorOnExecution(e);
            return retour;
        }
    }
}
