package fr.cpe.emergencymanager.Client;

import fr.cpe.emergencymanager.Config.ConfigLoader;
import fr.cpe.emergencymanager.Config.MqttConfig;
import org.eclipse.paho.client.mqttv3.MqttCallback;
import org.eclipse.paho.client.mqttv3.MqttConnectOptions;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import javax.net.ssl.SSLSocketFactory;
import java.nio.charset.StandardCharsets;

public class MqttClient {
    private final Logger log = LoggerFactory.getLogger(MqttClient.class);

    private org.eclipse.paho.client.mqttv3.MqttClient mqttClient;
    private MqttConfig mqttConfig;

    public MqttClient() {
        this.mqttConfig = ConfigLoader.getConfig().getMqttConfig();

        try {
            mqttClient = new org.eclipse.paho.client.mqttv3.MqttClient(mqttConfig.getBroker(), mqttConfig.getClientId());
            MqttConnectOptions connectOptions = new MqttConnectOptions();
            connectOptions.setUserName(mqttConfig.getUsername());
            connectOptions.setPassword(mqttConfig.getPassword().toCharArray());
            connectOptions.setCleanSession(true);
            connectOptions.setSocketFactory(SSLSocketFactory.getDefault()); // Remplacez SSLSocketFactoryWrapper par votre propre implémentation si nécessaire
            connectOptions.setMqttVersion(MqttConnectOptions.MQTT_VERSION_3_1_1);
            mqttClient.connect(connectOptions);
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    public boolean sendMessage(String topic, String message) {
        try {
            MqttMessage mqttMessage = new MqttMessage(message.getBytes(StandardCharsets.UTF_8));
            mqttClient.publish(topic, mqttMessage);
            return true;
        } catch(MqttException e) {
            e.printStackTrace();
            return false;
        }
    }

    public void setCallback(MqttCallback callback) {
        mqttClient.setCallback(callback);
    }

    public void subscribe(String topic) {
        try {
            mqttClient.subscribe(topic);
        } catch (MqttException e) {
            e.printStackTrace();
        }
    }

    public boolean disconnect() {
        try {
            mqttClient.disconnect();
            return true;
        } catch (MqttException e) {
            return false;
        }
    }
}