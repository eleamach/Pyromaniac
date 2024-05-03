package fr.cpe.emergencymanager.Repository;

import fr.cpe.emergencymanager.Entities.Incident;
import fr.cpe.emergencymanager.Entities.SensorHisto;
import org.apache.http.HttpResponse;

import java.io.IOException;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class SensorHistoRepository extends Repository<SensorHisto> {
    public SensorHistoRepository() {
        setType(SensorHisto.class);
        setEndpoint(SensorHisto.ENDPOINT);
    }

    public Set<SensorHisto> findSensorHistoByIncident(Incident incident) {
        try {
            HttpResponse response = API.get("incident-sensor-histo/incident/" + incident.getIdentify());
            return httpResponseIsOkay(response) ? (Set<SensorHisto>) httpToObject(response, mapper.getTypeFactory().constructCollectionType(Set.class, SensorHisto.class)) : new HashSet<SensorHisto>();
        } catch (IOException e) {
            return new HashSet<SensorHisto>();
        }
    }

    public List<SensorHisto> findSensorHistoNonProcessed() {
        try {
            HttpResponse response = API.get(getEndpoint() + "/non-processed/");
            return super.httpResponseIsOkay(response) ? (List<SensorHisto>) httpToObject(response, mapper.getTypeFactory().constructCollectionType(List.class, SensorHisto.class)) : new ArrayList<SensorHisto>();
        } catch (IOException e) {
            errorOnExecution(e);
            return new ArrayList<SensorHisto>();
        }
    }
}