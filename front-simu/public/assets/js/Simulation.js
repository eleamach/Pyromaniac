import { apiClient } from "./api.js";
import { displayIncident } from "./displayIncident.js";
import { getAllIncident, getLastHistoIncident, getAllIncidentBySimu } from "./incident.js";
import { displaySensor } from "./sensor.js";
import { SimuService } from "./simuService.js";

const simulation = new SimuService(apiClient)

import { toaster } from "./toaster.js";

export async function startSimulation(weather = 0, difficulty = 0, speed = 0) {
    var lastSimu = await getLastSimu()
    if (lastSimu) {
        console.error("pas possible d'en créer")
        toaster.error("Une simulation est déjà en cours")
    } else {
        try {
            var data
            // todo créer la meteo aussi 
            await simulation.startSimu(weather, difficulty, speed)
                .then(dataPromise => {
                    data = dataPromise
                })
                .catch(error => {
                    console.error(error);
                });
            toaster.info("Simulation lancée")
            return data
        } catch (error) {
            console.log(error)
        }
    }
}

export async function getLastSimu() {
    try {
        var data
        await simulation.getCurrentSimu()
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

export async function deleteSimu(simu) {
    // console.log(simu)
    try {
        var data
        await simulation.deleteSimu(simu.simulation_id)
            .then(dataPromise => {
                data = dataPromise
            })
            .catch(error => {
                console.error(error);
            });
        toaster.info("Simulation stoppé")
        return data
    } catch (error) {
        console.log(error)
    }
}

export function clearAllMap(map) {
    const layers = map.getStyle().layers;
    layers.forEach(layer => {
        if (layer.id.includes("incident") || layer.id.includes("sensor-fire")) {
            map.removeLayer(layer.id)
            map.removeSource(layer.id)
        }
    })
}


export async function SimuMain(map) {
    // const allIncidents = await getAllIncidentBySimu(idSimu)
    const allIncidents = await getAllIncident()
    if (allIncidents) {
        var allIncidentsId = []
        const allSensorInvolved = new Array()
        /*
                const layers = map.getStyle().layers;
                for (let i = layers.length - 1; i >= 0; i--) {
                    const layer = layers[i];
                    if (layer.id.startsWith('sensor-fire-')) {
                        const incidentId = parseInt(layer.id.replace('sensor-fire-', ''), 10);
                        console.log(incidentId)
                        console.log(allIncidentsId)
                        console.log(allIncidentsId.includes(incidentId.toString()))
                        console.log("--------")
        
                        // Vérifie si l'incidentId n'est pas dans la liste des incidents autorisés
                        if (!allIncidentsId.includes(incidentId)) {
                        // Supprime le layer s'il ne fait pas partie des incidents autorisés
                        map.removeLayer(layer.id);
                        map.removeSource(layer.id); // Supprime également la source associée si nécessaire
                        // layers.splice(i, 1); // Retire le layer de la liste
                        }
                    }
                    // if (layer.id.startsWith('sensor-fire-')) {
                    //     map.removeLayer(layer.id);
                    //     map.removeSource(layer.id);
                    // }
                }
        */
        clearAllMap(map)
        await Promise.all(
            allIncidents.map(async (incident) => {
                const lastIncidents = await getLastHistoIncident(incident.incident_id);
                console.log(lastIncidents)
                console.log("******")
                if (lastIncidents) {
                    lastIncidents.forEach((lastIncident) => {
                        const sensor = lastIncident.sensor_histo.sensor;
                        allIncidentsId.push(sensor.sensor_id);
                        allSensorInvolved.push(sensor);
                        const id = lastIncident.incident.incident_id;
                        const sensorValue = lastIncident.sensor_histo.sensor_histo_value;
                        //   displaySensor(sensor, sensorValue, map);

                    });
                }
                if (lastIncidents) {
                    const sensorsInvolved = new Array()
                    lastIncidents.forEach(incident => {
                        sensorsInvolved.push(incident.sensor_histo.sensor)
                    });
                    const level = lastIncidents.reduce((max, item) => {
                        const sensorValue = item.sensor_histo.sensor_histo_value;
                        return sensorValue > max ? sensorValue : max;
                      }, -Infinity);
                    displayIncident(map, sensorsInvolved, incident.incident_id, level)
                }
            })
        );

    } else {
        toaster.error("Impossible de récupérer les incidents.")
    }
}