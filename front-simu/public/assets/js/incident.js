import { apiClient } from "./api.js";
import { IncidentSensorHistoService, IncidentService, IncidentSimulationService } from "./IncidentService.js";
import { toaster } from "./toaster.js";

const incidentService = new IncidentService(apiClient)
const incidentHistoService = new IncidentSensorHistoService(apiClient)
const incidentSimulation = new IncidentSimulationService(apiClient)

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
        var data
        const dernieresDonnees = {};
        await incidentHistoService.getIncidentHistoById(id)
            .then(dataPromise => {
                data = dataPromise
            })
            .catch(error => {
                console.error(error);
            });
        if (data.length != 0) {
            data.forEach(item => {
                // const sensor_histo = 
                const sensorId = item.sensor_histo.sensor_id;
                if(sensorId == 9){
                    console.log(item)
                }
                const sensorHistoDate = new Date(item.sensor_histo.sensor_histo_date);

                // Vérifier si le capteur existe déjà dans l'objet et si la date est plus récente
                if (
                    !dernieresDonnees[sensorId] ||
                    sensorHistoDate > dernieresDonnees[sensorId].sensor_histo_date
                ) {
                    // Mettre à jour les données les plus récentes pour ce capteur
                    dernieresDonnees[sensorId] = item
                }
            });
            const result = Object.values(dernieresDonnees);
            return result
        } else {
            return null
        }
    } catch (error) {
        console.log(error)
    }
}

export async function getAllIncidentBySimu(id) {
    try {
        var data
        await incidentSimulation.getIncidentBySimu(id)
            .then(dataPromise => {
                data = dataPromise
            })
            .catch(error => {
                console.error(error);
            });
        return data[data.length - 1]

    } catch (error) {
        console.log(error)
    }
}