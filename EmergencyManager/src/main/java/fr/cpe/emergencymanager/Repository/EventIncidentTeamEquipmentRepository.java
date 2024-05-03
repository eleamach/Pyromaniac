/*
 * Copyright (c) 2023.
 * Autheur : Adrien JAUFRE
 */

package fr.cpe.emergencymanager.Repository;

import fr.cpe.emergencymanager.Entities.EventIncidentTeamEquipment;
import fr.cpe.emergencymanager.Entities.IncidentTeamEquipment;
import org.apache.http.HttpResponse;

import java.io.IOException;
import java.util.HashSet;
import java.util.Set;

public class EventIncidentTeamEquipmentRepository extends Repository<EventIncidentTeamEquipment> {
    public EventIncidentTeamEquipmentRepository() {
        setType(EventIncidentTeamEquipment.class);
        setEndpoint(EventIncidentTeamEquipment.ENDPOINT);
    }

    public Set<EventIncidentTeamEquipment> findByIncidentTeamEquipment(IncidentTeamEquipment incidentTeamEquipment) {
        try {
            HttpResponse response = API.get(getEndpoint() + "incident-team-equipment-id/" + incidentTeamEquipment.getIdentify());
            return httpResponseIsOkay(response) ? (Set<EventIncidentTeamEquipment>) httpToObject(response, mapper.getTypeFactory().constructCollectionType(Set.class, super.getType())) : new HashSet<EventIncidentTeamEquipment>();
        } catch (IOException e) {
            errorOnExecution(e);
            return new HashSet<EventIncidentTeamEquipment>();
        }
    }

    public Set<EventIncidentTeamEquipment> findByCoordinates(Double longitude, Double latitude) {
        try {
            HttpResponse response = API.get(getEndpoint() + "coordinates/" + longitude + "/" + latitude);
            return httpResponseIsOkay(response) ? (Set<EventIncidentTeamEquipment>) httpToObject(response, mapper.getTypeFactory().constructCollectionType(Set.class, super.getType())) : new HashSet<EventIncidentTeamEquipment>();
        } catch (IOException e) {
            errorOnExecution(e);
            return new HashSet<EventIncidentTeamEquipment>();
        }
    }
}