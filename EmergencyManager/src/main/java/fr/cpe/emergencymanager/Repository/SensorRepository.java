package fr.cpe.emergencymanager.Repository;

import fr.cpe.emergencymanager.Client.ApiClient;
import fr.cpe.emergencymanager.Entities.Sensor;
import fr.cpe.emergencymanager.Entities.SensorFull;
import org.apache.http.HttpResponse;

import java.io.IOException;
import java.text.DecimalFormat;
import java.text.DecimalFormatSymbols;
import java.util.Optional;

public class SensorRepository extends Repository<Sensor> {
    public SensorRepository() {
        setType(Sensor.class);
        setEndpoint(Sensor.ENDPOINT);
    }

    @Override
    public Optional<Sensor> findOneById(Long id) {
        try {
            HttpResponse response = API.getOneById(getEndpoint(), id);
            return httpResponseIsOkay(response) ? Optional.of(httpToObject(response, SensorFull.class)) : Optional.empty();
        } catch (IOException e) {
            errorOnExecution(e);
            return Optional.empty();
        }
    }

    @Override
    public Sensor findById(Long id) {
        try {
            HttpResponse response = API.getOneById(getEndpoint(), id);
            return httpResponseIsOkay(response) ? httpToObject(response, SensorFull.class) : null;
        } catch (IOException e) {
            errorOnExecution(e);
            return null;
        }
    }

    public Optional<Sensor> findByCoord(Double longitude, Double latitude) {
        try {
            DecimalFormat df = new DecimalFormat();
            DecimalFormatSymbols dfs = new DecimalFormatSymbols();
            dfs.setDecimalSeparator('.');
            df.setDecimalFormatSymbols(dfs);
            df.setMaximumFractionDigits(14);
            HttpResponse response = API.get(getEndpoint() + "/coordinates/" + df.format(longitude) + "/" + df.format(latitude));
            return httpResponseIsOkay(response) ? Optional.of(httpToObject(response, SensorFull.class)) : Optional.empty();
        } catch (IOException e) {
            errorOnExecution(e);
            return Optional.empty();
        }
    }
}