package fr.cpe.emergencymanager.Controller;

import fr.cpe.emergencymanager.Entities.Equipment;
import fr.cpe.emergencymanager.Entities.IncidentTeamEquipment;
import fr.cpe.emergencymanager.Entities.MqttMessage;
import fr.cpe.emergencymanager.Repository.EquipmentRepository;
import fr.cpe.emergencymanager.Client.MqttClient;
import fr.cpe.emergencymanager.Service.EquipmentService;
import fr.cpe.emergencymanager.Service.IncidentService;
import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.Optional;

public class MqttSubscribers {
    private final EquipmentRepository equipmentRepository;
    private final IncidentService incidentService;
    private final EquipmentService equipmentService;
    private final MqttClient mqttClient;
    private final Logger log = LoggerFactory.getLogger(MqttSubscribers.class);

    public MqttSubscribers() {
        this.equipmentRepository = new EquipmentRepository();
        this.incidentService = new IncidentService();
        this.equipmentService = new EquipmentService();
        this.mqttClient = new MqttClient();
    }

    public void main() {
        MqttCallback mqttCallback = new MqttCallback() {
            @Override
            public void connectionLost(Throwable throwable) {
                log.error("Connexion au serveur MQTT perdue");
                mqttClient.disconnect();
            }

            @Override
            public void messageArrived(String s, org.eclipse.paho.client.mqttv3.MqttMessage mqttMessage) throws Exception {
                if(s.startsWith("equipment/")) {
                    String[] parties = s.split("/");
                    Optional<Equipment> equipment = equipmentRepository.findOneById(Long.parseLong(parties[1]));
                    if (equipment.isPresent()) {
                        boolean ack = false;
                        Equipment eq = equipment.get();
                        Optional<IncidentTeamEquipment> incidentTeamEquipment =  equipmentService.findIncidentTeamEquipmentByEquipmentInProgress(eq);
                        String[] message = mqttMessage.toString().split(" ");
                        if (message[0].equals(MqttMessage.GEOLOC.toString())) {
                            // On met à jour la localisation actuelle des équipements
                            eq.setLongitude(Double.parseDouble(message[1]));
                            eq.setLatitude(Double.parseDouble(message[2]));
                            equipmentRepository.update(eq);
                        } else if (message[0].equals(MqttMessage.ANNULE.toString())) {
                            ack = incidentService.unAssignEquipmentDueToUnavailable(eq);
                        } else if (message[0].equals(MqttMessage.ARRIVE.toString())) {
                            ack = incidentService.isArrived(eq);
                            // TODO : Logguer l'arrivée sur site
                            // Récupérer l'incidentEquipment associé
                            // Mettre à jour le event associé
                        } else if (mqttMessage.toString().startsWith(MqttMessage.ACCEPTE.toString())) {
                            // TODO : Confirmer l'envoi
                            //  logguer l'envoi sur site
                        } else if (mqttMessage.toString().startsWith(MqttMessage.DEPART.toString())) {
                            ack = incidentService.unAssignEquipment(eq);
                        }
                        if(ack) mqttClient.sendMessage("equipment/" + eq.getId(), MqttMessage.ACK.toString());
                    } else {
                        log.error("Equipment inconnu sur MQTT");
                    }
                }
            }

            @Override
            public void deliveryComplete(IMqttDeliveryToken iMqttDeliveryToken) {
                log.debug("Message délivré");
            }
        };

        mqttClient.setCallback(mqttCallback);

        for(Equipment el : equipmentRepository.findAll()) {
            mqttClient.subscribe("equipment/" + el.getId());
        }
    }
}