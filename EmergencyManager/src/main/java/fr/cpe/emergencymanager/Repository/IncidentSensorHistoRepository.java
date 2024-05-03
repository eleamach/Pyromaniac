package fr.cpe.emergencymanager.Repository;

import fr.cpe.emergencymanager.Client.ApiClient;
import fr.cpe.emergencymanager.Entities.Incident;
import fr.cpe.emergencymanager.Entities.IncidentSensorHisto;
import fr.cpe.emergencymanager.Entities.Sensor;
import org.apache.http.HttpResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.util.HashSet;
import java.util.Set;

public class IncidentSensorHistoRepository extends Repository<IncidentSensorHisto> {
    private final Logger log = LoggerFactory.getLogger(IncidentSensorHistoRepository.class);
    public IncidentSensorHistoRepository() {
        setType(IncidentSensorHisto.class);
        setEndpoint(IncidentSensorHisto.ENDPOINT);
    }

    public Set<IncidentSensorHisto> findIncidentSensorHistoByIncident(Incident incident) {
        try {
            HttpResponse response = API.get(getEndpoint() + "/incident/" + incident.getIdentify());
            return httpResponseIsOkay(response) ? (Set<IncidentSensorHisto>) httpToObject(response, mapper.getTypeFactory().constructCollectionType(Set.class, IncidentSensorHisto.class)) : new HashSet<IncidentSensorHisto>();
        } catch (IOException e) {
            errorOnExecution(e);
            return new HashSet<IncidentSensorHisto>();
        }
    }

    public Set<IncidentSensorHisto> findIncidentSensorHistoBySensor(Sensor sensor) {
        try {
            HttpResponse response = API.get(getEndpoint() + "/sensor/" + sensor.getIdentify());
            return httpResponseIsOkay(response) ? (Set<IncidentSensorHisto>) httpToObject(response, mapper.getTypeFactory().constructCollectionType(Set.class, IncidentSensorHisto.class)) : new HashSet<IncidentSensorHisto>();
        } catch (IOException e) {
            errorOnExecution(e);
            return new HashSet<IncidentSensorHisto>();
        }
    }
}
