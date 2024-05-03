package fr.cpe.emergencymanager.Repository;

import fr.cpe.emergencymanager.Client.ApiClient;
import fr.cpe.emergencymanager.Entities.Equipment;
import fr.cpe.emergencymanager.Entities.FireStation;
import fr.cpe.emergencymanager.Entities.TypeEquipment;
import org.apache.http.HttpResponse;

import java.io.IOException;
import java.util.HashSet;
import java.util.Optional;
import java.util.Set;

public class EquipmentRepository extends Repository<Equipment> {
    public EquipmentRepository() {
        setType(Equipment.class);
        setEndpoint(Equipment.ENDPOINT);
    }

    public Set<Equipment> findByFireStation(FireStation fireStation) {
        try {
            HttpResponse response = API.get(getEndpoint() + "/fire-station/" + fireStation.getIdentify());
            return httpResponseIsOkay(response) ? (Set<Equipment>) httpToObject(response, mapper.getTypeFactory().constructCollectionType(Set.class, super.getType())) : new HashSet<Equipment>();
        } catch (IOException e) {
            errorOnExecution(e);
            return new HashSet<Equipment>();
        }
    }

    public Optional<Equipment> findByName(String name) {
        try {
            HttpResponse response = API.get(getEndpoint() + "/name/" + name);
            return httpResponseIsOkay(response) ? Optional.of((Equipment) httpToObject(response, super.getType())) : Optional.empty();
        } catch (IOException e) {
            errorOnExecution(e);
            return Optional.empty();
        }
    }

    public Set<Equipment> findByTypeEquipment(TypeEquipment typeEquipment) {
        try {
            HttpResponse response = API.get(getEndpoint() + "/" + TypeEquipment.ENDPOINT + "/" + typeEquipment.getIdentify());
            return httpResponseIsOkay(response) ? (Set<Equipment>) httpToObject(response, mapper.getTypeFactory().constructCollectionType(Set.class, super.getType())) : new HashSet<Equipment>();
        } catch (IOException e) {
            errorOnExecution(e);
            return new HashSet<Equipment>();
        }
    }

    public Set<Equipment> findByAvailable(boolean available) {
        try {
            HttpResponse response = API.get(getEndpoint() + "/available/" + available);
            return httpResponseIsOkay(response) ? (Set<Equipment>) httpToObject(response, mapper.getTypeFactory().constructCollectionType(Set.class, super.getType())) : new HashSet<Equipment>();
        } catch (IOException e) {
            errorOnExecution(e);
            return new HashSet<Equipment>();
        }
    }

    @Override
    public Optional<Equipment> findOneById(Long id) {
        try {
            HttpResponse response = API.get(getEndpoint() + "/id/" + id);
            return httpResponseIsOkay(response) ? Optional.of(httpToObject(response, getType())) : Optional.empty();
        } catch (IOException e) {
            errorOnExecution(e);
            return Optional.empty();
        }
    }

    @Override
    public Equipment findById(Long id) {
        try {
            HttpResponse response = API.get(getEndpoint() + "/id/" + id);
            return httpResponseIsOkay(response) ? httpToObject(response, getType()) : null;
        } catch (IOException e) {
            errorOnExecution(e);
            return null;
        }
    }
}