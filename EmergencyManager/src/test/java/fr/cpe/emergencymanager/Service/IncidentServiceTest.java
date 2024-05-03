/*
 * Copyright (c) 2024.
 * Autheur : Adrien JAUFRE
 */

package fr.cpe.emergencymanager.Service;

import fr.cpe.emergencymanager.Client.MqttClient;
import fr.cpe.emergencymanager.Entities.*;
import fr.cpe.emergencymanager.Repository.*;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.DisplayName;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.math.BigDecimal;
import java.time.LocalDateTime;
import java.util.*;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.lenient;

@DisplayName("IncidentService")
public class IncidentServiceTest {
    private Logger log = LoggerFactory.getLogger(IncidentServiceTest.class);

    @Mock
    private EquipmentService equipmentService;

    @Mock
    private IncidentRepository incidentRepository;

    @Mock
    private IncidentTeamEquipmentRepository incidentTeamEquipmentRepository;

    @Mock
    private EventIncidentTeamEquipmentRepository eventIncidentTeamEquipmentRepository;

    @Mock
    private EquipmentRepository equipmentRepository;

    @Mock
    private SensorService sensorService;

    @Mock
    private ParameterRepository parameterRepository;

    @Mock
    private MqttClient mqttClient;

    @Mock
    private IncidentSensorHistoRepository incidentSensorHistoRepository;

    @Mock
    private SensorRepository sensorRepository;

    @Mock
    private SensorHistoRepository sensorHistoRepository;

    @InjectMocks
    private IncidentService incidentService;

    @BeforeEach
    public void setUp() {
        MockitoAnnotations.openMocks(this);
    }

    @Test
    @DisplayName("getSites()")
    public void testGetSites() {
        double deltaLon = 0.2; // Correspond à l'axe x
        double deltaLat = 0.1; // Correspond à l'axe y

        List<Sensor> sensorList = new ArrayList<Sensor>();
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


        //  ------------------------------------------------  Général  -------------------------------------------------

        lenient().when(parameterRepository.findById(eq("neighbor-latitude"))).thenReturn(new Parameter("neighbor-latitude", String.valueOf(deltaLat)));
        lenient().when(parameterRepository.findById(eq("neighbor-longitude"))).thenReturn(new Parameter("neighbor-longitude", String.valueOf(deltaLon)));

        lenient().when(sensorService.sensorNeighbor(any())).thenAnswer(invocation -> {
            Sensor argument = invocation.getArgument(0);
            return new SensorService(sensorRepository, incidentRepository, parameterRepository).sensorNeighbor(argument);
        });
        lenient().when(sensorService.sensorNeighborLocation(any())).thenAnswer(invocation -> {
            Sensor argument = invocation.getArgument(0);
            return new SensorService(sensorRepository, incidentRepository, parameterRepository).sensorNeighborLocation(argument);
        });
        lenient().when(sensorService.areNeighbor(any(), any())).thenAnswer(invocation -> {
            Sensor argument1 = invocation.getArgument(0);
            Sensor argument2 = invocation.getArgument(1);
            return new SensorService(sensorRepository, incidentRepository, parameterRepository).areNeighbor(argument1, argument2);
        });

        lenient().when(sensorRepository.findByCoord(any(), any())).thenReturn(Optional.empty());
        for (Sensor sensor : sensorList) {
            lenient().when(sensorRepository.findById(eq(sensor.getIdentify()))).thenReturn(sensor);
            lenient().when(sensorRepository.findByCoord(eq(sensor.getLongitude()), eq(sensor.getLatitude()))).thenReturn(Optional.of(sensor));
        }

        // -----------------------------------  Incident 1 : cas 1 bord haut milieu  -----------------------------------
        Incident incident1 = new Incident(true, 1L, incidentSensorHistoRepository);
        SensorHisto sensorHisto11 = new SensorHisto(1L, 2L, 1, LocalDateTime.MIN, true, sensorRepository);
        SensorHisto sensorHisto12 = new SensorHisto(2L, 2L, 2, LocalDateTime.now(), true, sensorRepository);
        List<SensorHisto> sensorHistoList = new ArrayList<SensorHisto>(Arrays.asList(sensorHisto11, sensorHisto12));
        IncidentSensorHisto incidentSensorHisto11 = new IncidentSensorHisto(incident1, sensorHisto11, incidentRepository, sensorHistoRepository);
        IncidentSensorHisto incidentSensorHisto12 = new IncidentSensorHisto(incident1, sensorHisto12, incidentRepository, sensorHistoRepository);
        Set<IncidentSensorHisto> incidentSensorHistos1 = new HashSet<IncidentSensorHisto>(Arrays.asList(incidentSensorHisto11, incidentSensorHisto12));

        for (SensorHisto sensorHisto : sensorHistoList) {
            lenient().when(sensorHistoRepository.findById(eq(sensorHisto.getIdentify()))).thenReturn(sensorHisto);
        }

        lenient().when(incidentSensorHistoRepository.findIncidentSensorHistoByIncident(eq(incident1))).thenReturn(incidentSensorHistos1);

        lenient().when(sensorRepository.findById(eq(sensorList.get(1).getIdentify()))).thenReturn(new SensorFull(sensorList.get(1), new HashSet<SensorHisto>(Arrays.asList(sensorHisto12))));

        Set<Site> sites1 = incidentService.getSites(incident1);

        assertFalse(sites1.isEmpty());
        assertEquals(1, sites1.size());
        Site site = sites1.iterator().next();
        assertEquals(new Site((1 * deltaLon), (2 * deltaLat + deltaLat / 2), null), site);


        // ------------------------------------  Incident 2 : cas 1 capteur centre  ------------------------------------
        Incident incident2 = new Incident(true, 2L, incidentSensorHistoRepository);
        SensorHisto sensorHisto21 = new SensorHisto(1L, 5L, 3, LocalDateTime.now(), true, sensorRepository);
        sensorHistoList = new ArrayList<SensorHisto>(Arrays.asList(sensorHisto21));
        IncidentSensorHisto incidentSensorHisto21 = new IncidentSensorHisto(incident2, sensorHisto21, incidentRepository, sensorHistoRepository);
        Set<IncidentSensorHisto> incidentSensorHistos2 = new HashSet<IncidentSensorHisto>(Arrays.asList(incidentSensorHisto21));

        for (SensorHisto sensorHisto : sensorHistoList) {
            lenient().when(sensorHistoRepository.findById(eq(sensorHisto.getIdentify()))).thenReturn(sensorHisto);
        }

        lenient().when(incidentSensorHistoRepository.findIncidentSensorHistoByIncident(eq(incident2))).thenReturn(incidentSensorHistos2);

        lenient().when(sensorRepository.findById(eq(sensorList.get(4).getIdentify()))).thenReturn(new SensorFull(sensorList.get(4), new HashSet<SensorHisto>(Arrays.asList(sensorHisto21))));

        Set<Site> sites2 = incidentService.getSites(incident2);

        assertFalse(sites2.isEmpty());
        assertEquals(1, sites2.size());
        site = sites2.iterator().next();
        assertEquals(new Site(sensorList.get(4).getLongitude(), sensorList.get(4).getLatitude(), null), site);


        // -----------------------------------  Incident 3 : cas 2 capteurs voisins  -----------------------------------
        Incident incident3 = new Incident(true, 3L, incidentSensorHistoRepository);
        SensorHisto sensorHisto31 = new SensorHisto(1L, 5L, 3, LocalDateTime.now(), true, sensorRepository);
        SensorHisto sensorHisto32 = new SensorHisto(2L, 9L, 3, LocalDateTime.now(), true, sensorRepository);
        sensorHistoList = new ArrayList<SensorHisto>(Arrays.asList(sensorHisto31, sensorHisto32));
        IncidentSensorHisto incidentSensorHisto31 = new IncidentSensorHisto(incident3, sensorHisto31, incidentRepository, sensorHistoRepository);
        IncidentSensorHisto incidentSensorHisto32 = new IncidentSensorHisto(incident3, sensorHisto32, incidentRepository, sensorHistoRepository);
        Set<IncidentSensorHisto> incidentSensorHistos3 = new HashSet<IncidentSensorHisto>(Arrays.asList(incidentSensorHisto31, incidentSensorHisto32));

        for (SensorHisto sensorHisto : sensorHistoList) {
            lenient().when(sensorHistoRepository.findById(eq(sensorHisto.getIdentify()))).thenReturn(sensorHisto);
        }

        lenient().when(incidentSensorHistoRepository.findIncidentSensorHistoByIncident(eq(incident3))).thenReturn(incidentSensorHistos3);

        lenient().when(sensorRepository.findById(eq(sensorList.get(4).getIdentify()))).thenReturn(new SensorFull(sensorList.get(4), new HashSet<SensorHisto>(Arrays.asList(sensorHisto31))));
        lenient().when(sensorRepository.findById(eq(sensorList.get(8).getIdentify()))).thenReturn(new SensorFull(sensorList.get(8), new HashSet<SensorHisto>(Arrays.asList(sensorHisto32))));

        Set<Site> sites3 = incidentService.getSites(incident3);

        assertFalse(sites3.isEmpty());
        assertEquals(1, sites3.size());
        site = sites3.iterator().next();
        assertEquals(new Site((sensorList.get(8).getLongitude() + sensorList.get(4).getLongitude()) / 2, (sensorList.get(8).getLatitude() + sensorList.get(4).getLatitude()) / 2, null), site);


        // -----------------------------------  Incident 4 : cas 2 capteurs non voisin  --------------------------------
        Incident incident4 = new Incident(true, 4L, incidentSensorHistoRepository);
        SensorHisto sensorHisto41 = new SensorHisto(1L, 4L, 1, LocalDateTime.now(), true, sensorRepository);
        SensorHisto sensorHisto42 = new SensorHisto(2L, 5L, 2, LocalDateTime.now(), true, sensorRepository);
        SensorHisto sensorHisto43 = new SensorHisto(3L, 5L, 3, LocalDateTime.now(), true, sensorRepository);
        sensorHistoList = new ArrayList<SensorHisto>(Arrays.asList(sensorHisto41, sensorHisto42, sensorHisto43));
        IncidentSensorHisto incidentSensorHisto41 = new IncidentSensorHisto(incident4, sensorHisto41, incidentRepository, sensorHistoRepository);
        IncidentSensorHisto incidentSensorHisto42 = new IncidentSensorHisto(incident4, sensorHisto42, incidentRepository, sensorHistoRepository);
        IncidentSensorHisto incidentSensorHisto43 = new IncidentSensorHisto(incident4, sensorHisto43, incidentRepository, sensorHistoRepository);
        Set<IncidentSensorHisto> incidentSensorHistos4 = new HashSet<IncidentSensorHisto>(Arrays.asList(incidentSensorHisto41, incidentSensorHisto42, incidentSensorHisto43));

        for (SensorHisto sensorHisto : sensorHistoList) {
            lenient().when(sensorHistoRepository.findById(eq(sensorHisto.getIdentify()))).thenReturn(sensorHisto);
        }

        lenient().when(incidentSensorHistoRepository.findIncidentSensorHistoByIncident(eq(incident4))).thenReturn(incidentSensorHistos4);

        lenient().when(sensorRepository.findById(eq(sensorList.get(3).getIdentify()))).thenReturn(new SensorFull(sensorList.get(3), new HashSet<SensorHisto>(Arrays.asList(sensorHisto41))));
        lenient().when(sensorRepository.findById(eq(sensorList.get(4).getIdentify()))).thenReturn(new SensorFull(sensorList.get(4), new HashSet<SensorHisto>(Arrays.asList(sensorHisto43))));

        Set<Site> sites4 = incidentService.getSites(incident4);

        assertFalse(sites4.isEmpty());
        assertEquals(2, sites4.size());
        assertTrue(sites4.contains(new Site(sensorList.get(4).getLongitude(), sensorList.get(4).getLatitude(), 3.0f)));
        assertTrue(sites4.contains(new Site(sensorHisto41.getSensor().getLongitude() + (deltaLon/2), sensorHisto41.getSensor().getLatitude() + (deltaLat/2), 1.0f)));


        // ------------------------------------  Incident 5 : cas 3 capteurs voisins  ----------------------------------
        Incident incident5 = new Incident(true, 5L, incidentSensorHistoRepository);
        SensorHisto sensorHisto51 = new SensorHisto(1L, 2L, 2, LocalDateTime.now(), true, sensorRepository);
        SensorHisto sensorHisto52 = new SensorHisto(2L, 5L, 3, LocalDateTime.now(), true, sensorRepository);
        SensorHisto sensorHisto53 = new SensorHisto(3L, 9L, 5, LocalDateTime.now(), true, sensorRepository);
        sensorHistoList = new ArrayList<SensorHisto>(Arrays.asList(sensorHisto51, sensorHisto52, sensorHisto53));
        IncidentSensorHisto incidentSensorHisto51 = new IncidentSensorHisto(incident4, sensorHisto51, incidentRepository, sensorHistoRepository);
        IncidentSensorHisto incidentSensorHisto52 = new IncidentSensorHisto(incident4, sensorHisto52, incidentRepository, sensorHistoRepository);
        IncidentSensorHisto incidentSensorHisto53 = new IncidentSensorHisto(incident4, sensorHisto53, incidentRepository, sensorHistoRepository);
        Set<IncidentSensorHisto> incidentSensorHistos5 = new HashSet<IncidentSensorHisto>(Arrays.asList(incidentSensorHisto51, incidentSensorHisto52, incidentSensorHisto53));

        for (SensorHisto sensorHisto : sensorHistoList) {
            lenient().when(sensorHistoRepository.findById(eq(sensorHisto.getIdentify()))).thenReturn(sensorHisto);
        }

        lenient().when(incidentSensorHistoRepository.findIncidentSensorHistoByIncident(eq(incident5))).thenReturn(incidentSensorHistos5);

        lenient().when(sensorRepository.findById(eq(sensorList.get(1).getIdentify()))).thenReturn(new SensorFull(sensorList.get(1), new HashSet<SensorHisto>(Arrays.asList(sensorHisto51))));
        lenient().when(sensorRepository.findById(eq(sensorList.get(4).getIdentify()))).thenReturn(new SensorFull(sensorList.get(4), new HashSet<SensorHisto>(Arrays.asList(sensorHisto52))));
        lenient().when(sensorRepository.findById(eq(sensorList.get(8).getIdentify()))).thenReturn(new SensorFull(sensorList.get(8), new HashSet<SensorHisto>(Arrays.asList(sensorHisto53))));

        Set<Site> sites5 = incidentService.getSites(incident5);

        assertFalse(sites5.isEmpty());
        assertEquals(2, sites5.size());
        assertTrue(sites5.contains(new Site(((BigDecimal.valueOf(sensorList.get(1).getLongitude()).add(BigDecimal.valueOf(sensorList.get(4).getLongitude()))).divide(new BigDecimal(2)).doubleValue()), ((BigDecimal.valueOf(sensorList.get(1).getLatitude()).add(BigDecimal.valueOf(sensorList.get(4).getLatitude()))).divide(new BigDecimal(2))).doubleValue(), 3.0f)));
        assertTrue(sites5.contains(new Site((BigDecimal.valueOf(sensorList.get(4).getLongitude()).add(BigDecimal.valueOf(sensorList.get(8).getLongitude()))).divide(new BigDecimal(2)).doubleValue(), ((BigDecimal.valueOf(sensorList.get(4).getLatitude()).add(BigDecimal.valueOf(sensorList.get(8).getLatitude()))).divide(new BigDecimal(2))).doubleValue(), 5.0f)));
    }
}