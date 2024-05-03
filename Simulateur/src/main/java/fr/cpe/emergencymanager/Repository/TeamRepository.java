package fr.cpe.emergencymanager.Repository;

import fr.cpe.emergencymanager.Entities.Team;

public class TeamRepository extends Repository<Team> {
    public TeamRepository() {
        setType(Team.class);
        setEndpoint(Team.ENDPOINT);
    }
}