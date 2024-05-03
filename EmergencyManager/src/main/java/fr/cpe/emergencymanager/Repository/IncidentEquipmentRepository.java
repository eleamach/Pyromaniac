package fr.cpe.emergencymanager.Repository;

import com.fasterxml.jackson.core.JsonEncoding;
import fr.cpe.emergencymanager.Client.ApiClient;
import fr.cpe.emergencymanager.Entities.Equipment;
import fr.cpe.emergencymanager.Entities.Incident;
import fr.cpe.emergencymanager.Entities.IncidentEquipment;
import org.apache.http.HttpResponse;

import java.io.IOException;
import java.util.HashSet;
import java.util.Set;

public class IncidentEquipmentRepository extends Repository<IncidentEquipment> {
    public IncidentEquipmentRepository() {
        setType(IncidentEquipment.class);
        setEndpoint(IncidentEquipment.ENDPOINT);
    }

    public Set<IncidentEquipment> findByIncident(Incident incident) {
        try {
            HttpResponse response = API.get(getEndpoint() + "/incident/" + incident.getIdentify());
            return httpResponseIsOkay(response) ? (Set<IncidentEquipment>) httpToObject(response, mapper.getTypeFactory().constructCollectionType(Set.class, super.getType())) : new HashSet<IncidentEquipment>();
        } catch (IOException e) {
            errorOnExecution(e);
            return new HashSet<IncidentEquipment>();
        }
    }

    public boolean assignEquipment(IncidentEquipment incidentEquipment) {
        try {
            return httpResponseIsOkay(API.post(getEndpoint(), incidentEquipment));
        } catch (IOException e) {
            errorOnExecution(e);
            return false;
        }
    }

    public boolean unAssignEquipment(IncidentEquipment incidentEquipment) {
        try {
            return httpResponseIsOkay(API.post(getEndpoint(), incidentEquipment));
        } catch (IOException e) {
            errorOnExecution(e);
            return false;
        }
    }
}
