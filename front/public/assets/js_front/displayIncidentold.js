const nbCol = 10;
const nbLine = 6;

function sortAndStringify(arr) {
    return JSON.stringify(arr.slice().sort());
}

function findCenterArea(area) {
    const minSw = [400, 400]
    const maxNe = [-400, -400]

    console.log(area)

    area.forEach(subArea => {
        _sw = subArea.sw
        _ne = subArea.ne
        if (_sw[0] < minSw[0]) minSw[0] = _sw[0];
        if (_sw[1] < minSw[1]) minSw[1] = _sw[1];
        if (_ne[0] > maxNe[0]) maxNe[0] = _ne[0];
        if (_ne[1] > maxNe[1]) maxNe[1] = _ne[1];
    })

    // Gestion bord/coin
    if (area.length == 1) {
        id = area[0].id
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

    moyenneCoord = [
        (minSw[0] + maxNe[0]) / 2,
        (minSw[1] + maxNe[1]) / 2
    ]
    return moyenneCoord
}

function removeDuplicateArrays(arr) {
    const seenArrays = new Set();

    return arr.filter(subArray => {
        const subArrayString = sortAndStringify(subArray);
        if (!seenArrays.has(subArrayString)) {
            seenArrays.add(subArrayString);
            return true;
        }
        return false;
    });
}

function findNeighbours(sensorId) {
    const neighbours = [sensorId];

    // Liste des décalages pour les voisins en fonction de la ligne
    const offsets = [];

    // Calculer la ligne et la colonne de l'ID du capteur
    const row = Math.ceil(sensorId / nbCol);
    const col = (sensorId - 1) % nbCol + 1;

    // Si la ligne est paire
    if (row % 2 === 0) {
        if (col > 1) offsets.push(-nbCol); // Voisin en haut
        if (col < nbCol) offsets.push(-nbCol + 1); // Voisin en haut à droite
        if (neighbours % nbCol != 0) offsets.push(nbCol + 1);
        offsets.push(nbCol); // Voisins en bas et en bas à droite
    } else {
        if (col > 1) {
            offsets.push(-nbCol); // Voisins en haut et en haut à gauche
            if (neighbours % nbCol != 0) offsets.push(-nbCol - 1)
        }
        if (col < nbCol && neighbours % nbCol != 1) offsets.push(nbCol - 1); // Voisin en haut à droite
        offsets.push(nbCol); // Voisin en bas
    }

    offsets.forEach(offset => {
        const neighborId = sensorId + offset;
        if (neighborId >= 1 && neighborId <= nbLine * nbCol) {
            neighbours.push(neighborId);
        }
    });

    return neighbours;
}

// Fonction pour filtrer les voisins non désirés
function filterUnwantedNeighbours(neighboursList, desiredCases) {
    // Filtrer les voisins pour ne conserver que ceux présents dans desiredCases
    neighboursList = neighboursList.filter(neighbour => desiredCases.includes(neighbour));
    return neighboursList
}

// Fonction pour valider une paire
function validatePair(id1, id2) {
    // Ajoutez ici votre logique de validation
    // Par exemple, vérifiez si la paire est valide en fonction de vos critères
    const row1 = Math.ceil(id1 / nbCol);
    const col1 = (id1 - 1) % nbCol + 1;
    const row2 = Math.ceil(id2 / nbCol);
    const col2 = (id2 - 1) % nbCol + 1;

    const isEvenRow1 = Math.ceil(id1 / nbCol) % 2 === 0;
    const isEvenRow2 = Math.ceil(id2 / nbCol) % 2 === 0;
    const validPairs = isEvenRow1 ? [-nbCol, -nbCol + 1, nbCol, nbCol + 1] : [-nbCol, -nbCol - 1, nbCol - 1, nbCol];

    // Vérifier si les capteurs sont sur la même ligne ou la même colonne
    const sameRow = row1 === row2;
    // const sameCol = col1 === col2 && isEvenRow1 === isEvenRow2 ;
    const sameCol = col1 === col2;

    return (
        !sameRow && !sameCol && // Ne sont pas sur la même ligne ou colonne
        validPairs.includes(id2 - id1)
    );
}

function findIncidentFromSensor(sensors) {
    console.log(sensors)
    const incidentSensor = new Array()

    // Tableau pour stocker les voisins de chaque capteur
    const allNeighboursSensor = sensors.map(sensor => {
        return findNeighbours(sensor.sensor_id);
    });

    // Pour chaque capteur et ses voisins, filtrer les voisins non désirés
    // console.log(allNeighboursSensor)
    allNeighboursSensor.forEach(neighbor => {
        const filteredNeighbours = filterUnwantedNeighbours(neighbor, sensors.map(s => s.sensor_id));

        if (filteredNeighbours) {
            if (filteredNeighbours.length >= 3) {
                const pairs = [];
                for (let j = 0; j < filteredNeighbours.length; j++) {
                    pairs.push([filteredNeighbours[0], filteredNeighbours[j]]);
                }

                pairs.forEach(pair => {
                    const [id1, id2] = pair;
                    const isValidPair = validatePair(id1, id2);

                    if (isValidPair) {
                        // console.log("oui-3:", pair);
                        incidentSensor.push(pair);
                    }
                });
            } else if (filteredNeighbours.length < 3) {
                if (filteredNeighbours.length === 1) {
                    const sensorId = filteredNeighbours[0];
                    const isEvenRow = Math.ceil((sensorId-1) / nbCol) % 2 === 0;

                    if (!isEvenRow) {
                        // Vérifier s'il est sur la première ligne ou le premier de la ligne
                        if (sensorId <= nbCol || sensorId % nbCol === 1) {
                            incidentSensor.push(filteredNeighbours);
                        }
                    } else { // Si la ligne est impair
                        // Vérifier s'il est sur la dernière ligne ou à la fin de la ligne
                        const row = Math.ceil(sensorId / nbCol);
                        if (row === nbLine || sensorId % nbCol === 0) {
                            incidentSensor.push(filteredNeighbours);
                        }
                    }
                } else {
                    // console.log("oui:", filteredNeighbours);
                    incidentSensor.push(filteredNeighbours);
                }
            }
        }
    })

    console.log(incidentSensor)
    console.log("------")
    // Supprimer les doublons de incidentSensor et stocker le résultat dans uniqueIncidentSensor
    const uniqueIncidentSensor = removeDuplicateArrays(incidentSensor);

    // Pour chaque groupe de capteurs uniques, trouver leur centre et stocker les coordonnées dans coordsIncident
    var coordsIncident = [];

    for (let i = 0; i < uniqueIncidentSensor.length; i++) {
        const subArea = uniqueIncidentSensor[i];
        for (let j = 0; j < subArea.length; j++) {
            const subAreaItem = subArea[j];
            // Trouver le capteur correspondant à l'ID dans sensors
            const sensor = sensors.find(objet => objet.id === subAreaItem);
            // Remplacer l'ID par le capteur correspondant dans uniqueIncidentSensor
            uniqueIncidentSensor[i][j] = sensor;
        }
    }

    // Calculer le centre de chaque groupe de capteurs et stocker les coordonnées dans coordsIncident
    for (let i = 0; i < uniqueIncidentSensor.length; i++) {
        coordsIncident[i] = findCenterArea(uniqueIncidentSensor[i]);
    }
    // Retourner les coordonnées des incidents
    return coordsIncident;
}

export function displayIncident(map, allSensors) {
    // console.log(allSensors)
    const incidents = findIncidentFromSensor(allSensors)
    // console.log(incidents)

    /*
    const sensor = lastIncident.sensor_histo.sensor
    const id = lastIncident.incident.incident_id
    const sensorValue = lastIncident.sensor_histo.sensor_histo_value
    
    var fireSource = map.getSource("incident-" + id)
    if (fireSource) {
        const newGeoJSONData = {
            type: 'FeatureCollection',
            features: [
                {
                    type: 'Feature',
                    geometry: {
                        type: 'Point',
                        coordinates: [
                            sensor.sensor_longitude,
                            sensor.sensor_latitude
                        ]
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
                            coordinates: [
                                sensor.sensor_longitude,
                                sensor.sensor_latitude
                            ]
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
    */
}