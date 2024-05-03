package fr.cpe.emergencymanager.Repository;

import fr.cpe.emergencymanager.Entities.Incident;
import org.apache.http.HttpResponse;

import java.io.IOException;
import java.util.HashSet;
import java.util.Set;

public class IncidentRepository extends Repository<Incident> {
    public IncidentRepository() {
        setType(Incident.class);
        setEndpoint(Incident.ENDPOINT);
    }

    public Set<Incident> findByStatus(boolean inProgress) {
        Set<Incident> retour = new HashSet<Incident>();
        try {
            HttpResponse response = API.get(getEndpoint() + "/status/" + inProgress);
            return httpResponseIsOkay(response) ? (Set<Incident>) httpToObject(response, mapper.getTypeFactory().constructCollectionType(Set.class, super.getType())) : retour;
        } catch (IOException e) {
            errorOnExecution(e);
            return retour;
        }
    }
}