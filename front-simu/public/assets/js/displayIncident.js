import { apiClient } from "./api.js";
import { getColorByLevel } from "./sensor.js";
import { SettingService } from "./SettingService.js";
const settingService = new SettingService(apiClient)

const nbCol = 10;

function generateUniquePairs(arr) {
    const pairs = [];
  
    for (let i = 0; i < arr.length - 1; i++) {
      for (let j = i + 1; j < arr.length; j++) {
        // Vérifie que les éléments des paires sont différents
        const isEvenRow1 = Math.ceil((arr[i].sensor_id-1) / nbCol);
        const isEvenRow2 = Math.ceil((arr[j].sensor_id-1) / nbCol);
        if (arr[i] !== arr[j] && isEvenRow1 !== isEvenRow2) {
          const pair = [arr[i], arr[j]];
          // Vérifie si la paire n'est pas déjà présente dans le tableau
          if (!pairs.some(existingPair => arePairsEqual(existingPair, pair))) {
            pairs.push(pair);
          }
        }
      }
    }
    return pairs;
  }
  
  // Fonction pour vérifier si deux paires sont égales (même contenu)
  function arePairsEqual(pair1, pair2) {
    return (
      (pair1[0] === pair2[0] && pair1[1] === pair2[1]) ||
      (pair1[0] === pair2[1] && pair1[1] === pair2[0])
    );
  }

export async function getGap() {
    try {
        var data
        await settingService.getGap()
            .then(dataPromise => {
                data = dataPromise
            })
            .catch(error => {
                console.error(error);
            });
        return data.value
    } catch (error) {
        console.log(error)
    }
}

const gap = await getGap()

function findCenter(point1, point2) {
    var newCoords = []
    newCoords[0] = (point1.sensor_longitude + point2.sensor_longitude) / 2
    newCoords[1] = (point1.sensor_latitude + point2.sensor_latitude) / 2
    return newCoords
}

function displayPoint(map, id, point){
    var fireSource = map.getSource("incident-" + id)
    if (fireSource) {
        const newGeoJSONData = {
            type: 'FeatureCollection',
            features: [
                {
                    type: 'Feature',
                    geometry: {
                        type: 'Point',
                        coordinates: point
                    },
                },
            ],
        };
        fireSource.setData(newGeoJSONData);
    } else {
        map.addLayer({
            id: 'incident-' + id,
            type: 'symbol',
            source: {
                type: 'geojson',
                data: {
                    type: 'FeatureCollection',
                    features: [{
                        type: 'Feature',
                        geometry: {
                            type: 'Point',
                            coordinates: point
                        }
                    }]
                }
            },
            layout: {
                'icon-image': 'fire', // Nom de l'image personnalisée
                'icon-size': 0.2, // Taille de l'icône (ajustez au besoin)
                'icon-allow-overlap': true // Permettre le chevauchement d'icônes
            }
        });
    }
}

function displayArea(map, level, centerPointFire, id) {
    const color = getColorByLevel(level)

    var sensorFire = map.getLayer("sensor-fire-" + id)
    if (sensorFire) {
        map.setPaintProperty(sensorFire.id, 'fill-color', color)
    } else {
        var sensorGeo = {
            type: 'Feature',
            geometry: {
                type: 'Polygon',
                coordinates: [
                    [
                        [centerPointFire[0]+gap/4, centerPointFire[1]-gap/4],
                        [centerPointFire[0]+gap/4, centerPointFire[1]+gap/4],
                        [centerPointFire[0]-gap/4, centerPointFire[1]+gap/4],
                        [centerPointFire[0]-gap/4, centerPointFire[1]-gap/4],
                        [centerPointFire[0]+gap/4, centerPointFire[1]-gap/4],
                    ]
                ]
            }
        };
        map.addLayer({
            id: 'sensor-fire-' + id,
            type: 'fill',
            source: {
                type: 'geojson',
                data: sensorGeo
            },
            paint: {
                'fill-color': color,
                'fill-outline-color': 'rgba(255,0,0,1)'
            }
        });
    }
}

export function displayIncident(map, incidents, idIncident, level) {
    if (incidents.length <= 2 ){
        var centerPointFire
        if (incidents.length == 1){
            centerPointFire = [incidents[0].sensor_longitude, incidents[0].sensor_latitude]
        } else {
            centerPointFire = findCenter(incidents[0], incidents[1])
        }
        displayPoint(map, idIncident, centerPointFire)
        displayArea(map, level, centerPointFire, idIncident)
    } else {
        const allPairs = generateUniquePairs(incidents)
        allPairs.forEach((pair, id) => {
            displayIncident(map, pair, idIncident+"-"+id, level)
        })
    }
}