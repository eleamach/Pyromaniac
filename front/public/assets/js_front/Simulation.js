import { apiClient } from "./api.js";
import { displayIncident, displaySensorOff } from "./displayIncident.js";
import { getAllIncident, getLastHistoIncident } from "./incident.js";
import { displaySensor, getSensorById, getSensorHistoByIncident, getSensorOff } from "./sensor.js";

import { toaster } from "./toaster.js";

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
    const sensorsOff = await getSensorOff()
    clearAllMap(map)
    displaySensorOff(map, sensorsOff)

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
        await Promise.all(
            allIncidents.map(async (incident) => {
                const lastIncidents = await getLastHistoIncident(incident.id_incident);
                if (lastIncidents) {
                    lastIncidents.forEach((lastIncident) => {
                        allIncidentsId.push(lastIncident.id_sensor);
                        // allSensorInvolved.push(sensor);
                        // const id = lastIncident.incident.incident_id;
                        // const sensorValue = lastIncident.sensor_histo.sensor_histo_value;
                        //   displaySensor(sensor, sensorValue, map);

                    });
                }

                // await Promise.all(
                //     allIncidentsId.map(async (sensorId) => {
                //         const sensor = await getSensorById(sensorId)
                //         allSensorInvolved.push(sensor);
                //     })
                // )

                if (lastIncidents) {
                    const sensorsInvolved = new Array();
                    
                    const promises = lastIncidents.map(async (incident) => {
                        const sensor = await getSensorById(incident.id_sensor);
                        sensorsInvolved.push(sensor);
                    });
                    
                    await Promise.all(promises);

                    function areElementsPresent(array1, array2) {
                        const set2 = new Set(array2.map(item => item["id_sensor"]));
                        return array1.some(item => set2.has(item["id_sensor"]));
                    }

                    if(!areElementsPresent(sensorsOff, sensorsInvolved)){
                        const level = lastIncidents.reduce((max, item) => {
                            const sensorValue = item.sensor_histo_value;
                            return sensorValue > max ? sensorValue : max;
                        }, -Infinity);
                        displayIncident(map, sensorsInvolved, incident.id_incident, level);
                    }
                }
            })
        );

    } else {
        toaster.error("Impossible de récupérer les incidents.")
    }
}