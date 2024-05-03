package fr.cpe.emergencymanager;

import fr.cpe.emergencymanager.Config.Config;
import fr.cpe.emergencymanager.Config.ConfigLoader;
import fr.cpe.emergencymanager.Controller.MqttSubscribers;
import fr.cpe.emergencymanager.Controller.SensorsProcessing;

import fr.cpe.emergencymanager.Entities.Sensor;
import fr.cpe.emergencymanager.Repository.SensorRepository;
import fr.cpe.emergencymanager.Service.SensorService;
import org.quartz.*;
import org.quartz.impl.StdSchedulerFactory;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class Main {
    public static void main(String[] args) {
        Logger log = LoggerFactory.getLogger(Main.class);
        log.info("\n /$$$$$$$$                                                                                          /$$      /$$\n" +
                "| $$_____/                                                                                         | $$$    /$$$\n"  +
                "| $$       /$$$$$$/$$$$   /$$$$$$   /$$$$$$  /$$$$$$   /$$$$$$  /$$$$$$$   /$$$$$$$ /$$   /$$      | $$$$  /$$$$  /$$$$$$  /$$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$   /$$$$$$\n" +
                "| $$$$$   | $$_  $$_  $$ /$$__  $$ /$$__  $$/$$__  $$ /$$__  $$| $$__  $$ /$$_____/| $$  | $$      | $$ $$/$$ $$ |____  $$| $$__  $$ |____  $$ /$$__  $$ /$$__  $$ /$$__  $$ \n" +
                "| $$__/   | $$ \\ $$ \\ $$| $$$$$$$$| $$  \\__/ $$  \\ $$| $$$$$$$$| $$  \\ $$| $$      | $$  | $$      | $$  $$$| $$  /$$$$$$$| $$  \\ $$  /$$$$$$$| $$  \\ $$| $$$$$$$$| $$  \\__/ \n" +
                "| $$      | $$ | $$ | $$| $$_____/| $$     | $$  | $$| $$_____/| $$  | $$| $$      | $$  | $$      | $$\\  $ | $$ /$$__  $$| $$  | $$ /$$__  $$| $$  | $$| $$_____/| $$ \n" +
                "| $$$$$$$$| $$ | $$ | $$|  $$$$$$$| $$     |  $$$$$$$|  $$$$$$$| $$  | $$|  $$$$$$$|  $$$$$$$      | $$ \\/  | $$|  $$$$$$$| $$  | $$|  $$$$$$$|  $$$$$$$|  $$$$$$$| $$ \n" +
                "|________/|__/ |__/ |__/ \\_______/|__/      \\____  $$ \\_______/|__/  |__/ \\_______/ \\____  $$      |__/     |__/ \\_______/|__/  |__/ \\_______/ \\____  $$ \\_______/|__/ \n" +
                "                                            /$$  \\ $$                               /$$  | $$                                                  /$$  \\ $$  \n" +
                "                                           |  $$$$$$/                              |  $$$$$$/                                                 |  $$$$$$/ \n" +
                "                                            \\______/                                \\______/                                                   \\______/  \n");

        log.info("Chargement de la configuration...");
        Config config = ConfigLoader.getConfig();


        try {
            // Tâche planifiée
            SchedulerFactory schedulerFactory = new StdSchedulerFactory();
            Scheduler scheduler = null;
            scheduler = schedulerFactory.getScheduler();

            // Créer une tâche
            JobDetail job = JobBuilder.newJob(SensorsProcessing.class)
                    .withIdentity("SensorsProcessing", "Sensors")
                    .build();

            // Déclencheur toutes les 20 secondes
            Trigger trigger = TriggerBuilder.newTrigger()
                    .withIdentity("30 seconds", "Sensors")
                    .startNow()
                    .withSchedule(SimpleScheduleBuilder.simpleSchedule()
                            .withIntervalInSeconds(30)
                            .repeatForever())
                    .build();

            // Ajouter la tâche et le déclencheur au planificateur
            scheduler.scheduleJob(job, trigger);

            // Démarrer le planificateur
            scheduler.start();
        } catch (SchedulerException e) {
            e.printStackTrace();
        }

        new MqttSubscribers().main(); // Pour écouter les messages MQTT venant des equipments
    }
}