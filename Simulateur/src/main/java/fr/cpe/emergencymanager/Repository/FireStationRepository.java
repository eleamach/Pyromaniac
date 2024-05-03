package fr.cpe.emergencymanager.Repository;

import fr.cpe.emergencymanager.Entities.FireStation;

public class FireStationRepository extends Repository<FireStation> {
    public FireStationRepository() {
        setType(FireStation.class);
        setEndpoint(FireStation.ENDPOINT);
    }
}