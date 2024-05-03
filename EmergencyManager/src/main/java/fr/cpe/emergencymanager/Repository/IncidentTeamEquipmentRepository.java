package fr.cpe.emergencymanager.Repository;

import fr.cpe.emergencymanager.Entities.*;
import org.apache.http.HttpResponse;

import java.io.IOException;
import java.util.HashSet;
import java.util.Set;

public class IncidentTeamEquipmentRepository extends Repository<IncidentTeamEquipment> {
    public IncidentTeamEquipmentRepository() {
        setType(IncidentTeamEquipment.class);
        setEndpoint(IncidentTeamEquipment.ENDPOINT);
    }

    public Set<IncidentTeamEquipment> findByIncident(Incident incident) {
        try {
            HttpResponse response = API.get(getEndpoint() + "incident/" + incident.getIdentify());
            return httpResponseIsOkay(response) ? (Set<IncidentTeamEquipment>) httpToObject(response, mapper.getTypeFactory().constructCollectionType(Set.class, super.getType())) : new HashSet<IncidentTeamEquipment>();
        } catch (IOException e) {
            errorOnExecution(e);
            return new HashSet<IncidentTeamEquipment>();
        }
    }

    public Set<IncidentTeamEquipment> fincByTeam(Team team) {
        try {
            HttpResponse response = API.get(getEndpoint() + "team/" + team.getIdentify());
            return httpResponseIsOkay(response) ? (Set<IncidentTeamEquipment>) httpToObject(response, mapper.getTypeFactory().constructCollectionType(Set.class, super.getType())) : new HashSet<IncidentTeamEquipment>();
        } catch (IOException e) {
            errorOnExecution(e);
            return new HashSet<IncidentTeamEquipment>();
        }
    }

    public Set<IncidentTeamEquipment> fincByEquipment(Equipment equipment) {
        try {
            HttpResponse response = API.get(getEndpoint() + "/equipment/" + equipment.getIdentify());
            return httpResponseIsOkay(response) ? (Set<IncidentTeamEquipment>) httpToObject(response, mapper.getTypeFactory().constructCollectionType(Set.class, super.getType())) : new HashSet<IncidentTeamEquipment>();
        } catch (IOException e) {
            errorOnExecution(e);
            return new HashSet<IncidentTeamEquipment>();
        }
    }

    public Set<IncidentTeamEquipment> findByAll(Incident incident, Team team, Equipment equipment) {
        try {
            HttpResponse response = API.get(getEndpoint() + "all/" + incident.getIdentify() + "/" + team.getIdentify() + "/" + equipment.getIdentify());
            return httpResponseIsOkay(response) ? (Set<IncidentTeamEquipment>) httpToObject(response, mapper.getTypeFactory().constructCollectionType(Set.class, super.getType())) : new HashSet<IncidentTeamEquipment>();
        } catch (IOException e) {
            errorOnExecution(e);
            return new HashSet<IncidentTeamEquipment>();
        }
    }

    public Set<IncidentTeamEquipment> findByStatus(boolean isActive) {
        try {
            HttpResponse response = API.get("incident-team-equipmentis_active" + isActive);
            return httpResponseIsOkay(response) ? (Set<IncidentTeamEquipment>) httpToObject(response, mapper.getTypeFactory().constructCollectionType(Set.class, super.getType())) : new HashSet<IncidentTeamEquipment>();
        } catch (IOException e) {
            errorOnExecution(e);
            return new HashSet<IncidentTeamEquipment>();
        }
    }
}
