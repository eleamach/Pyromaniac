package fr.cpe.emergencymanager.Repository;

import fr.cpe.emergencymanager.Entities.Employee;
import fr.cpe.emergencymanager.Entities.FireStation;
import fr.cpe.emergencymanager.Entities.Team;

import java.util.Set;

public class TeamRepository extends Repository<Team> {
    public TeamRepository() {
        setType(Team.class);
        setEndpoint(Team.ENDPOINT);
    }

    public Set<Team> findByEmployee(Employee employee) {
        try {
            return (Set<Team>) httpToObject(API.get(getEndpoint() + "/" + employee.getIdentify() + "/teams"), mapper.getTypeFactory().constructCollectionType(Set.class, Team.class));
        } catch (Exception e) {
            errorOnExecution(e);
            return null;
        }
    }

    public Set<Team> findByFireStation(FireStation fireStation) {
        try {
            return (Set<Team>) httpToObject(API.get(getEndpoint() + "/" + FireStation.ENDPOINT + "/" + fireStation.getIdentify()), mapper.getTypeFactory().constructCollectionType(Set.class, Team.class));
        } catch (Exception e) {
            errorOnExecution(e);
            return null;
        }
    }
}