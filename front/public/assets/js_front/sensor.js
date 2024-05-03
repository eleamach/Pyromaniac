import { apiClient } from "./api.js";
import { SensorHistoService, SensorService } from "./sensorService.js";
import { SettingService } from "./SettingService.js";
const sensorService = new SensorService(apiClient)
const settingService = new SettingService(apiClient)

const sensorHistoService = new SensorHistoService(apiClient)

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

export async function getSensorById(id) {
    try {
        var data
        await sensorService.getSensorById(id)
            .then(dataPromise => {
                data = dataPromise
            })
            .catch(error => {
                console.error(error);
            });
        return data
    } catch (error) {
        console.log(error)
    }
}

const gap = await getGap()

export function getColorByLevel(level) {
    level = Math.max(1, Math.min(9, level));
    const green = Math.floor((9 - level) * (255 / 8));
    return `rgba(255, ${green},0, 0.5)`;
}

// Exemple d'utilisation :
const level = 5; // Niveau entre 1 et 9
const color = getColorByLevel(level);

function findCenterArea(area) {
    var minSw = [400, 400]
    var maxNe = [-400, -400]

    area.forEach(subArea => {
        var _sw = subArea.sw
        var _ne = subArea.ne
        if (_sw[0] < minSw[0]) minSw[0] = _sw[0];
        if (_sw[1] < minSw[1]) minSw[1] = _sw[1];
        if (_ne[0] > maxNe[0]) maxNe[0] = _ne[0];
        if (_ne[1] > maxNe[1]) maxNe[1] = _ne[1];
    })

    // Gestion bord/coin
    if (area.length == 1) {
        var id = area[0].id
        if (id % nbCol == 0) {
            minSw[0] += (maxNe[0] - minSw[0]) / 2
        }
        if (id % nbCol == 1) {
            maxNe[0] -= (maxNe[0] - minSw[0]) / 2
        }
        if (id <= nbCol) {
            minSw[1] += (maxNe[1] - minSw[1]) / 2
        }
        if (id > (nbCol * nbLine) - nbCol) {
            maxNe[1] -= (maxNe[1] - minSw[1]) / 2
        }
    }

    var moyenneCoord = [
        (minSw[0] + maxNe[0]) / 2,
        (minSw[1] + maxNe[1]) / 2
    ]
    return moyenneCoord
}


export function getSensorCoverage(sensor, gap) {
    var sw = { "long": 0, "lat": 0 }
    var ne = { "long": 0, "lat": 0 }
    sw.long = sensor.sensor_longitude - gap / 2
    sw.lat = sensor.sensor_latitude - gap / 2
    ne.long = sensor.sensor_longitude + gap / 2
    ne.lat = sensor.sensor_latitude + gap / 2
    return { "sw": sw, "ne": ne }
}

export async function getSensors() {
    try {
        var data
        await sensorService.getAllSensor()
            .then(dataPromise => {
                data = dataPromise
            })
            .catch(error => {
                console.error(error);
            });

        data.forEach(sensor => {
            const coverage = getSensorCoverage(sensor, gap)
            sensor.ne = coverage.ne
            sensor.sw = coverage.sw
        });
        return data

    } catch (error) {
        console.log(error)
    }
}

export function getGlobalBounds(sensors) {
    if (sensors.length === 0) {
        return null; // Si la liste est vide, retourne null
    }

    var lastSensor = sensors[sensors.length - 1]
    var firstSensor = sensors[0]

    let sw = { "long": firstSensor.sw.long, "lat": lastSensor.sw.lat }
    let ne = { "long": lastSensor.ne.long, "lat": firstSensor.ne.lat }
    let se = { "long": lastSensor.ne.long, "lat": lastSensor.sw.lat }
    let nw = { "long": firstSensor.sw.long, "lat": firstSensor.ne.lat }

    return { sw, ne, se, nw };
}

export function getBounds(sensor) {
    let sw = { "long": sensor.sw.long, "lat": sensor.sw.lat }
    let se = { "long": sensor.ne.long, "lat": sensor.sw.lat }
    let nw = { "long": sensor.sw.long, "lat": sensor.ne.lat }
    let ne = { "long": sensor.ne.long, "lat": sensor.ne.lat }

    return { sw, ne, se, nw };
}

export function displaySensor(sensor, level, map) {
    const coverage = getSensorCoverage(sensor, gap)
    const boundSensor = getBounds(coverage)
    const color = getColorByLevel(level)

    var sensorFire = map.getLayer("sensor-fire-" + sensor.sensor_id)
    if (sensorFire) {
        map.setPaintProperty(sensorFire.id, 'fill-color', color)
    } else {
        var sensorGeo = {
            type: 'Feature',
            geometry: {
                type: 'Polygon',
                coordinates: [
                    [
                        [boundSensor.nw.long, boundSensor.nw.lat],
                        [boundSensor.ne.long, boundSensor.ne.lat],
                        [boundSensor.se.long, boundSensor.se.lat],
                        [boundSensor.sw.long, boundSensor.sw.lat],
                        [boundSensor.nw.long, boundSensor.nw.lat],
                    ]
                ]
            }
        };
        map.addLayer({
            id: 'sensor-fire-' + sensor.sensor_id,
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

export async function getSensorHistoByIncident(id) {
    try {
        var data 
        await sensorHistoService.getSensorHistoByIncidentService(id)
            .then(dataPromise => {
                data = dataPromise
            })
            .catch(error => {
                console.error(error);
            });
        return data

    } catch (error) {
        console.log(error)
    }
}

export async function getSensorOff() {
    try {
        var data
        await sensorService.getSensorOff()
            .then(dataPromise => {
                data = dataPromise
            })
            .catch(error => {
                console.error(error);
            });
        return data
    } catch (error) {
        console.log(error)
    }
}
