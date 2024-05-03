import { apiClient } from "./api.js";
import { IncidentSensorHistoService, IncidentService } from "./IncidentService.js";
import { getSensorHistoByIncident } from "./sensor.js";
import { toaster } from "./toaster.js";

const incidentService = new IncidentService(apiClient)
const incidentHistoService = new IncidentSensorHistoService(apiClient)

export async function getAllIncident() {
    try {
        var data = []
        await incidentService.getAllIncident()
            .then(dataPromise => {
                dataPromise.forEach(incident => {
                    if (incident.incident_status) {
                        data.push(incident)
                    }
                });
            })
            .catch(error => {
                console.error(error);
            });
        return data

    } catch (error) {
        console.log(error)
    }
}


export async function getLastHistoIncident(id) {
    try {
        const data = await incidentHistoService.getIncidentHistoById(id);

        if (data.length !== 0) {
            const dernieresDonnees = {};
            
            const promises = data.map(async item => {
                const sensor_histo = await getSensorHistoByIncident(item.id_sensor_histo);
                const sensorId = sensor_histo.id_sensor;
                const sensorHistoDate = new Date(sensor_histo.sensor_histo_date);

                // Vérifier si le capteur existe déjà dans l'objet et si la date est plus récente
                if (
                    !dernieresDonnees[sensorId] ||
                    sensorHistoDate > dernieresDonnees[sensorId].sensor_histo_date
                ) {
                    // Mettre à jour les données les plus récentes pour ce capteur
                    dernieresDonnees[sensorId] = sensor_histo;
                }
            });

            await Promise.all(promises);
            const result = Object.values(dernieresDonnees);
            return result;
        } else {
            return null;
        }
    } catch (error) {
        console.error(error);
    }
}

