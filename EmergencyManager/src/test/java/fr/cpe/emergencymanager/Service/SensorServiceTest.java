/*
 * Copyright (c) 2024.
 * Autheur : Adrien JAUFRE
 */

package fr.cpe.emergencymanager.Service;

import fr.cpe.emergencymanager.Entities.Parameter;
import fr.cpe.emergencymanager.Entities.Sensor;
import fr.cpe.emergencymanager.Repository.IncidentRepository;
import fr.cpe.emergencymanager.Repository.ParameterRepository;
import fr.cpe.emergencymanager.Repository.SensorRepository;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.math.BigDecimal;
import java.util.*;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.lenient;

@DisplayName("SensorService")
public class SensorServiceTest {
    @Mock
    private SensorRepository sensorRepository;
    @Mock
    private IncidentRepository incidentRepository;
    @Mock
    private ParameterRepository parameterRepository;
    @InjectMocks
    private SensorService sensorService;

    private final double deltaLon = 0.2;
    private final double deltaLat = 0.1;
    List<Sensor> sensorList = new ArrayList<Sensor>();

    private Logger log = LoggerFactory.getLogger(SensorServiceTest.class);

    @BeforeEach
    public void setUpData() {
        MockitoAnnotations.openMocks(this);
        // Partie haute
        sensorList.add(new Sensor(1L, BigDecimal.valueOf(deltaLon).multiply(new BigDecimal(0)).doubleValue(), BigDecimal.valueOf(deltaLat).multiply(new BigDecimal(2)).doubleValue(), true)); // Bord haut gauche
        sensorList.add(new Sensor(2L, BigDecimal.valueOf(deltaLon).multiply(new BigDecimal(1)).doubleValue(), BigDecimal.valueOf(deltaLat).multiply(new BigDecimal(2)).doubleValue(), true)); // Bord haut
        sensorList.add(new Sensor(3L, BigDecimal.valueOf(deltaLon).multiply(new BigDecimal(2)).doubleValue(), BigDecimal.valueOf(deltaLat).multiply(new BigDecimal(2)).doubleValue(), true)); // Bord haut
        sensorList.add(new Sensor(4L, BigDecimal.valueOf(deltaLon).multiply(new BigDecimal(3)).doubleValue(), BigDecimal.valueOf(deltaLat).multiply(new BigDecimal(2)).doubleValue(), true)); // Bord haut droit

        // Milieu
        sensorList.add(new Sensor(5L, BigDecimal.valueOf(deltaLon).multiply(new BigDecimal(0)).add(BigDecimal.valueOf(deltaLon).divide(new BigDecimal(2))).doubleValue(), BigDecimal.valueOf(deltaLat).multiply(new BigDecimal(1)).doubleValue(), true)); // Bord milieu gauche
        sensorList.add(new Sensor(6L, BigDecimal.valueOf(deltaLon).multiply(new BigDecimal(1)).add(BigDecimal.valueOf(deltaLon).divide(new BigDecimal(2))).doubleValue(), BigDecimal.valueOf(deltaLat).multiply(new BigDecimal(1)).doubleValue(), true)); // Milieu
        sensorList.add(new Sensor(7L, BigDecimal.valueOf(deltaLon).multiply(new BigDecimal(2)).add(BigDecimal.valueOf(deltaLon).divide(new BigDecimal(2))).doubleValue(), BigDecimal.valueOf(deltaLat).multiply(new BigDecimal(1)).doubleValue(), true)); // Milieu
        sensorList.add(new Sensor(8L, BigDecimal.valueOf(deltaLon).multiply(new BigDecimal(3)).add(BigDecimal.valueOf(deltaLon).divide(new BigDecimal(2))).doubleValue(), BigDecimal.valueOf(deltaLat).multiply(new BigDecimal(1)).doubleValue(), true)); // Bord milieu droit

        // Bas
        sensorList.add(new Sensor(9L, BigDecimal.valueOf(deltaLon).multiply(new BigDecimal(0)).doubleValue(), BigDecimal.valueOf(deltaLat).multiply(new BigDecimal(0)).doubleValue(), true)); // Bord bas gauche
        sensorList.add(new Sensor(10L, BigDecimal.valueOf(deltaLon).multiply(new BigDecimal(1)).doubleValue(), BigDecimal.valueOf(deltaLat).multiply(new BigDecimal(0)).doubleValue(), true)); // Bord bas milieu
        sensorList.add(new Sensor(11L, BigDecimal.valueOf(deltaLon).multiply(new BigDecimal(2)).doubleValue(), BigDecimal.valueOf(deltaLat).multiply(new BigDecimal(0)).doubleValue(), true)); // Bord bas milieu
        sensorList.add(new Sensor(12L, BigDecimal.valueOf(deltaLon).multiply(new BigDecimal(3)).doubleValue(), BigDecimal.valueOf(deltaLat).multiply(new BigDecimal(0)).doubleValue(), true)); // Bord bas droit
    }

    @Test
    @DisplayName("sensorNeighbor")
    public void testSensorNeighbor() {
        lenient().when(parameterRepository.findById(eq("neighbor-latitude"))).thenReturn(new Parameter("neighbor-latitude", String.valueOf(deltaLat)));
        lenient().when(parameterRepository.findById(eq("neighbor-longitude"))).thenReturn(new Parameter("neighbor-longitude", String.valueOf(deltaLon)));

        lenient().when(sensorRepository.findByCoord(any(), any())).thenReturn(Optional.empty());
        for (Sensor sensor : sensorList) {
            lenient().when(sensorRepository.findById(eq(sensor.getIdentify()))).thenReturn(sensor);
            lenient().when(sensorRepository.findByCoord(eq(sensor.getLongitude()), eq(sensor.getLatitude()))).thenReturn(Optional.of(sensor));
        }

        HashMap<Integer, Set<Integer>> sensorHashMap = new HashMap<Integer, Set<Integer>>();
        sensorHashMap.put(1, new HashSet<>(Arrays.asList(5)));
        sensorHashMap.put(2, new HashSet<>(Arrays.asList(5,6)));
        sensorHashMap.put(3, new HashSet<>(Arrays.asList(6,7)));
        sensorHashMap.put(4, new HashSet<>(Arrays.asList(7,8)));
        sensorHashMap.put(5, new HashSet<>(Arrays.asList(1,2,9,10)));
        sensorHashMap.put(6, new HashSet<>(Arrays.asList(2,3,10,11)));
        sensorHashMap.put(7, new HashSet<>(Arrays.asList(3,4,11,12)));
        sensorHashMap.put(8, new HashSet<>(Arrays.asList(4,12)));
        sensorHashMap.put(9, new HashSet<>(Arrays.asList(5)));
        sensorHashMap.put(10, new HashSet<>(Arrays.asList(5,6)));
        sensorHashMap.put(11, new HashSet<>(Arrays.asList(6,7)));
        sensorHashMap.put(12, new HashSet<>(Arrays.asList(7,8)));
        int i = 0;
        for(Sensor sensor : sensorList) {
            List<Sensor> senss = sensorService.sensorNeighbor(sensor);
            assertEquals(senss.size(), sensorHashMap.get(i+1).size());
            for(Integer integer : sensorHashMap.get(i+1)) {
                assertTrue(senss.contains(sensorList.get(integer-1)));
            }
            i++;
        }
    }

    @Test
    @DisplayName("sensorNeighborLocation")
    public void testSensorNeighborLocation() {
        lenient().when(parameterRepository.findById(eq("neighbor-latitude"))).thenReturn(new Parameter("neighbor-latitude", String.valueOf(deltaLat)));
        lenient().when(parameterRepository.findById(eq("neighbor-longitude"))).thenReturn(new Parameter("neighbor-longitude", String.valueOf(deltaLon)));

        lenient().when(sensorRepository.findByCoord(any(), any())).thenReturn(Optional.empty());
        for (Sensor sensor : sensorList) {
            lenient().when(sensorRepository.findById(eq(sensor.getIdentify()))).thenReturn(sensor);
            lenient().when(sensorRepository.findByCoord(eq(sensor.getLongitude()), eq(sensor.getLatitude()))).thenReturn(Optional.of(sensor));
        }

        HashMap<Integer, Set<SensorService.Direction>> sensorHashMap = new HashMap<Integer, Set<SensorService.Direction>>();
        sensorHashMap.put(1, new HashSet<>(Arrays.asList(SensorService.Direction.DROITE, SensorService.Direction.BAS_DROITE)));
        sensorHashMap.put(2, new HashSet<>(Arrays.asList(SensorService.Direction.DROITE, SensorService.Direction.GAUCHE, SensorService.Direction.BAS_DROITE, SensorService.Direction.BAS_GAUCHE)));
        sensorHashMap.put(3, new HashSet<>(Arrays.asList(SensorService.Direction.DROITE, SensorService.Direction.GAUCHE, SensorService.Direction.BAS_DROITE, SensorService.Direction.BAS_GAUCHE)));
        sensorHashMap.put(4, new HashSet<>(Arrays.asList(SensorService.Direction.GAUCHE, SensorService.Direction.BAS_DROITE, SensorService.Direction.BAS_GAUCHE)));
        sensorHashMap.put(5, new HashSet<>(Arrays.asList(SensorService.Direction.DROITE, SensorService.Direction.HAUT_DROITE, SensorService.Direction.HAUT_GAUCHE, SensorService.Direction.BAS_DROITE, SensorService.Direction.BAS_GAUCHE)));
        sensorHashMap.put(6, new HashSet<>(Arrays.asList(SensorService.Direction.DROITE, SensorService.Direction.GAUCHE, SensorService.Direction.HAUT_DROITE, SensorService.Direction.HAUT_GAUCHE, SensorService.Direction.BAS_DROITE, SensorService.Direction.BAS_GAUCHE)));
        sensorHashMap.put(7, new HashSet<>(Arrays.asList(SensorService.Direction.DROITE, SensorService.Direction.GAUCHE, SensorService.Direction.HAUT_DROITE, SensorService.Direction.HAUT_GAUCHE, SensorService.Direction.BAS_DROITE, SensorService.Direction.BAS_GAUCHE)));
        sensorHashMap.put(8, new HashSet<>(Arrays.asList(SensorService.Direction.GAUCHE, SensorService.Direction.HAUT_GAUCHE, SensorService.Direction.BAS_GAUCHE)));
        sensorHashMap.put(9, new HashSet<>(Arrays.asList(SensorService.Direction.DROITE, SensorService.Direction.HAUT_DROITE)));
        sensorHashMap.put(10, new HashSet<>(Arrays.asList(SensorService.Direction.DROITE, SensorService.Direction.GAUCHE, SensorService.Direction.HAUT_DROITE, SensorService.Direction.HAUT_GAUCHE)));
        sensorHashMap.put(11, new HashSet<>(Arrays.asList(SensorService.Direction.DROITE, SensorService.Direction.GAUCHE, SensorService.Direction.HAUT_DROITE, SensorService.Direction.HAUT_GAUCHE)));
        sensorHashMap.put(12, new HashSet<>(Arrays.asList(SensorService.Direction.GAUCHE, SensorService.Direction.HAUT_DROITE, SensorService.Direction.HAUT_GAUCHE)));
        int i = 1;
        for(Sensor sensor : sensorList) {
            HashMap<SensorService.Direction, Boolean> senss = sensorService.sensorNeighborLocation(sensor);
            assertEquals(senss.size(), SensorService.Direction.values().length);
            for(SensorService.Direction direction : SensorService.Direction.values()) {
                assertEquals(senss.get(direction), sensorHashMap.get(i).contains(direction));
            }
            i++;
        }
    }
}