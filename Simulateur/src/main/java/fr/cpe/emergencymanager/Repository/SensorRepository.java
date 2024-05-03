package fr.cpe.emergencymanager.Repository;

import fr.cpe.emergencymanager.Entities.Sensor;

public class SensorRepository extends Repository<Sensor> {
    public SensorRepository() {
        setType(Sensor.class);
        setEndpoint(Sensor.ENDPOINT);
    }
}