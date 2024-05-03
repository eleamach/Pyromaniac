package fr.cpe.emergencymanager.Config;

import fr.cpe.emergencymanager.Main;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

public class ConfigLoader {
    private static Logger log = LoggerFactory.getLogger(ConfigLoader.class);
    private static Config config = null;

    public static Config getConfig() {
        if(config == null) {
            // Charger le fichier de configuration
            Properties prop = new Properties();
            try (InputStream input = Main.class.getClassLoader().getResourceAsStream("config.properties")) {
                prop.load(input);
            } catch (IOException ex) {
                log.error("Erreur lors de la lecture du fichier de configuration : {}", ex.getMessage());
                System.exit(1);
            }

            // Lire les paramètres du fichier de configuration
            ApiConfig apiConfig = new ApiConfig(
                    prop.getProperty("api.url"),
                    prop.getProperty("api.username"),
                    prop.getProperty("api.password"),
                    prop.getProperty("api.urltoken")
            );
            log.debug("Configuration API chargée : {}", apiConfig);
            MqttConfig mqttConfig = new MqttConfig(
                    prop.getProperty("mqtt.broker"),
                    prop.getProperty("mqtt.clientId"),
                    prop.getProperty("mqtt.username"),
                    prop.getProperty("mqtt.password")
            );
            log.debug("Configuration MQTT chargée : {}", mqttConfig);

            Config config0 = new Config();
            config0.setApiConfig(apiConfig);
            config0.setMqttConfig(mqttConfig);

            config = config0;

            return config0;
        }
        return config;
    }
}
