package fr.cpe.emergencymanager.Repository;

import fr.cpe.emergencymanager.Entities.Employee;
import fr.cpe.emergencymanager.Entities.SensorHisto;
import fr.cpe.emergencymanager.Entities.TypeEquipment;
import org.apache.http.HttpResponse;

import java.io.IOException;
import java.util.HashSet;
import java.util.Set;

public class TypeEquipmentRepository extends Repository<TypeEquipment> {
    public TypeEquipmentRepository() {
        setType(TypeEquipment.class);
        setEndpoint(TypeEquipment.ENDPOINT);
    }

    public Set<TypeEquipment> findByEmployee(Employee employee) {
        try {
            HttpResponse response = API.get("type-equipment-employee/" + employee.getIdentify() + "/type-equipments");
            return httpResponseIsOkay(response) ? (Set<TypeEquipment>) httpToObject(response, mapper.getTypeFactory().constructCollectionType(Set.class, TypeEquipment.class)) : new HashSet<TypeEquipment>();
        } catch (IOException e) {
            return new HashSet<TypeEquipment>();
        }
    }
}
