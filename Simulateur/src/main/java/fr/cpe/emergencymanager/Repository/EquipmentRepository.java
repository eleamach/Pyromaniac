package fr.cpe.emergencymanager.Repository;

import fr.cpe.emergencymanager.Entities.Equipment;
import fr.cpe.emergencymanager.Entities.FireStation;
import fr.cpe.emergencymanager.Entities.Incident;
import org.apache.http.HttpResponse;

import java.io.IOException;
import java.util.HashSet;
import java.util.Set;

public class EquipmentRepository extends Repository<Equipment> {
    public EquipmentRepository() {
        setType(Equipment.class);
        setEndpoint(Equipment.ENDPOINT);
    }

    public Set<Equipment> findByFireStation(FireStation fireStation) {
        Set<Equipment> retour = new HashSet<Equipment>();
        try {
            HttpResponse response = API.get(Equipment.ENDPOINT + "/fire-station/" + fireStation.getIdentify());
            return httpResponseIsOkay(response) ? (Set<Equipment>) httpToObject(response, mapper.getTypeFactory().constructCollectionType(Set.class, super.getType())) : retour;
        } catch (IOException e) {
            errorOnExecution(e);
            return retour;
        }
    }

    public Set<Equipment> findByIncident(Incident incident) {
        Set<Equipment> retour = new HashSet<Equipment>();
        try {
            HttpResponse response = API.get("incident-equipment/incident" + incident.getIdentify());
            return httpResponseIsOkay(response) ? (Set<Equipment>) httpToObject(response, mapper.getTypeFactory().constructCollectionType(Set.class, super.getType())) : retour;
        } catch (IOException e) {
            errorOnExecution(e);
            return retour;
        }
    }
}