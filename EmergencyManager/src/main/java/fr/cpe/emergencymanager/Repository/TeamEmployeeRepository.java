package fr.cpe.emergencymanager.Repository;

import fr.cpe.emergencymanager.Client.ApiClient;
import fr.cpe.emergencymanager.Entities.TeamEmployee;

public class TeamEmployeeRepository extends Repository<TeamEmployee> {
    public TeamEmployeeRepository() {
        setType(TeamEmployee.class);
        setEndpoint(TeamEmployee.ENDPOINT);
    }
}
