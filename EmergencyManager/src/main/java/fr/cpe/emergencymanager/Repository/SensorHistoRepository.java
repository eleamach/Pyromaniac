package fr.cpe.emergencymanager.Repository;

import fr.cpe.emergencymanager.Client.ApiClient;
import fr.cpe.emergencymanager.Entities.SensorHisto;
import org.apache.http.HttpResponse;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class SensorHistoRepository extends Repository<SensorHisto> {
    public SensorHistoRepository() {
        setType(SensorHisto.class);
        setEndpoint(SensorHisto.ENDPOINT);
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