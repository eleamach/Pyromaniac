package fr.cpe.emergencymanager.Service;

import fr.cpe.emergencymanager.Entities.Incident;
import fr.cpe.emergencymanager.Entities.Sensor;
import fr.cpe.emergencymanager.Repository.IncidentRepository;
import fr.cpe.emergencymanager.Repository.ParameterRepository;
import fr.cpe.emergencymanager.Repository.SensorRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.math.BigDecimal;
import java.util.*;

public class SensorService {
    private final Logger log = LoggerFactory.getLogger(SensorService.class);

    private final SensorRepository sensorRepository;
    private final IncidentRepository incidentRepository;
    private final ParameterRepository parameterRepository;

    public SensorService() {
        this.sensorRepository = new SensorRepository();
        this.incidentRepository = new IncidentRepository();
        this.parameterRepository = new ParameterRepository();
    }

    public SensorService(SensorRepository sensorRepository, IncidentRepository incidentRepository, ParameterRepository parameterRepository) {
        this.sensorRepository = sensorRepository;
        this.incidentRepository = incidentRepository;
        this.parameterRepository = parameterRepository;
    }

    public List<Sensor> sensorNeighbor(Sensor sensor) {
        Double deltaLatitude = Double.valueOf(parameterRepository.findById("neighbor-latitude").getValue());
        Double deltaLongitude = Double.valueOf(parameterRepository.findById("neighbor-longitude").getValue());
        if(deltaLongitude == null || deltaLatitude == null) {
            log.error("Valeurs manquantes pour calculer les voisins dans les paramètres !");
            return new ArrayList<Sensor>();
        }

        List<Sensor> sensorsNeighbor = new ArrayList<Sensor>(4);
        Double actualLatitude = sensor.getLatitude();
        Double actualLongitude = sensor.getLongitude();

        // Voisins carré
        for(int i = 0; i < 4; i++) {
            Double myLongitude, myLatitude;
            if(i < 2) {
                myLongitude = BigDecimal.valueOf(actualLongitude).add(BigDecimal.valueOf(deltaLongitude).divide(new BigDecimal(2))).doubleValue();
            } else {
                myLongitude = BigDecimal.valueOf(actualLongitude).subtract(BigDecimal.valueOf(deltaLongitude).divide(new BigDecimal(2))).doubleValue();
            }
            if(i%2 == 0) {
                myLatitude = BigDecimal.valueOf(actualLatitude).add(BigDecimal.valueOf(deltaLatitude)).doubleValue();
            } else {
                myLatitude = BigDecimal.valueOf(actualLatitude).subtract(BigDecimal.valueOf(deltaLatitude)).doubleValue();
            }
            Optional<Sensor> sensor1 = sensorRepository.findByCoord(myLongitude, myLatitude);
            if(sensor1.isPresent()) {
                sensorsNeighbor.add(sensor1.get());
            }
        }
        return sensorsNeighbor;
    }

    public boolean estConcerneParIncidentEnCours(Sensor sensor) {
        Set<Incident> incidents = incidentRepository.findByStatus(true);
        if(incidents.isEmpty()) {
            return false;
        }
        return incidents
                .stream()
                .anyMatch(incident -> incident.getSensorHistos()
                        .stream()
                        .anyMatch(sen -> sen.getSensorId().equals(sensor.getId())));
    }

    public Incident getIncidentEnCours(Sensor sensor) {
        Set<Incident> incidents = incidentRepository.findByStatus(true);
        if(incidents.isEmpty()) return null;
        return incidents
                .stream()
                .filter(incident -> incident.getSensorHistos()
                        .stream()
                        .anyMatch(sen -> sen.getSensorId().equals(sensor.getId()) && sen.getLevel() != 0))
                .findFirst()
                .orElse(null);
    }

    public boolean aUnVoisinEnIncident(Sensor sensor) {
        return sensorNeighbor(sensor)
                .stream()
                .anyMatch(this::estConcerneParIncidentEnCours);
    }

    public HashMap<Direction, Boolean> sensorNeighborLocation(Sensor sensor) {
        Double deltaLatitude = Double.valueOf(parameterRepository.findById("neighbor-latitude").getValue());
        Double deltaLongitude = Double.valueOf(parameterRepository.findById("neighbor-longitude").getValue());
        if(deltaLongitude == null || deltaLatitude == null) {
            log.error("Valeurs manquantes pour calculer les voisins dans les paramètres !");
            return new HashMap<Direction, Boolean>();
        }

        HashMap<Direction, Boolean> sensorsNeighbor = new HashMap<Direction, Boolean>(6);
        Double actualLatitude = sensor.getLatitude();
        Double actualLongitude = sensor.getLongitude();

        // Voisins latéraux
        ArrayList<Direction> string = new ArrayList<Direction>(Arrays.asList(Direction.DROITE, Direction.GAUCHE));
        for(int i = 0; i < 2; i++) {
            Optional<Sensor> sensor1;
            if(i % 2 == 0) {
                sensor1 = sensorRepository.findByCoord((BigDecimal.valueOf(actualLongitude).add(BigDecimal.valueOf(deltaLongitude)).doubleValue()), actualLatitude);
            } else {
                sensor1 = sensorRepository.findByCoord((BigDecimal.valueOf(actualLongitude).subtract(BigDecimal.valueOf(deltaLongitude)).doubleValue()), actualLatitude);
            }
            sensorsNeighbor.put(string.get(i), sensor1.isPresent());
        }

        // Voisins carré
        string = new ArrayList<Direction>(Arrays.asList(Direction.HAUT_DROITE, Direction.BAS_DROITE, Direction.HAUT_GAUCHE, Direction.BAS_GAUCHE));
        for(int i = 0; i < 4; i++) {
            Double myLongitude, myLatitude;
            if(i < 2) {
                myLongitude = BigDecimal.valueOf(actualLongitude).add((BigDecimal.valueOf(deltaLongitude).divide(new BigDecimal(2)))).doubleValue();
            } else {
                myLongitude = BigDecimal.valueOf(actualLongitude).subtract((BigDecimal.valueOf(deltaLongitude).divide(new BigDecimal(2)))).doubleValue();
            }
            if(i%2 == 0) {
                myLatitude = BigDecimal.valueOf(actualLatitude).add((BigDecimal.valueOf(deltaLatitude))).doubleValue();
            } else {
                myLatitude = BigDecimal.valueOf(actualLatitude).subtract(BigDecimal.valueOf(deltaLatitude)).doubleValue();
            }
            Optional<Sensor> sensor1 = sensorRepository.findByCoord(myLongitude, myLatitude);
            sensorsNeighbor.put(string.get(i), sensor1.isPresent());
        }
        return sensorsNeighbor;
    }

    public boolean areNeighbor(Sensor sensor1, Sensor sensor2) {
        return sensorNeighbor(sensor1).contains(sensor2) && sensorNeighbor(sensor2).contains(sensor1);
    }

    public enum Direction {
        DROITE,
        GAUCHE,
        HAUT_DROITE,
        BAS_DROITE,
        HAUT_GAUCHE,
        BAS_GAUCHE
    }
}
