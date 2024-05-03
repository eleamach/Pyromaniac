mapboxgl.accessToken = 'pk.eyJ1Ijoic2thZmVlIiwiYSI6ImNscHNkajkxYzAyb3MyanQ3OTR6ZWl5bnkifQ.a_IZDhqmRKB_KJ6w6A24iA';

const nbCol = 10;
const nbLine = 6;
const nbSensor = nbCol * nbLine
const resolution_case = 2000

const lyonCoordinates = [4.85, 45.75];
const villeurbanneCoordinates = [4.88, 45.77];

var case_data = {
    case: []
}

var all_case = []

function random_rgba(opa) {
    var o = Math.round, r = Math.random, s = 255;
    return 'rgba(' + o(r() * s) + ',' + o(r() * s) + ',' + o(r() * s) + ',' + opa + ')';
}

// Largeur en degre de chaque case de la grille
// var gridSize = Math.min((villeurbanneCoordinates[0] - lyonCoordinates[0]) / 10, (villeurbanneCoordinates[1] - lyonCoordinates[1]) / 6);
// précision en mettre  / circumférence terre * 360 degre
const gridSize = resolution_case / 40075000 * 360

// Calculer le centre entre Lyon et Villeurbanne
var centerCoordinates = [
    (lyonCoordinates[0] + villeurbanneCoordinates[0]) / 2,
    (lyonCoordinates[1] + villeurbanneCoordinates[1]) / 2
];

// generate random incendie
var sw = [centerCoordinates[0], centerCoordinates[1]];
var ne = [centerCoordinates[0], centerCoordinates[1]];

function setGlobalBounds(_sw, _ne) {
    if (sw.length === 0 && ne.length === 0) {
        sw = _sw;
        ne = _ne;
    }

    if (_sw[0] < sw[0]) sw[0] = _sw[0];
    if (_sw[1] < sw[1]) sw[1] = _sw[1];
    if (_ne[0] > ne[0]) ne[0] = _ne[0];
    if (_ne[1] > ne[1]) ne[1] = _ne[1];
}

function getRandomPoint() {
    //45...
    lat = Math.random() * (ne[1] - sw[1]) + sw[1]

    //4...
    long = Math.random() * (ne[0] - sw[0]) + sw[0]

    return [long, lat]
}

function findCenter(point1, point2) {
    var newCoords = []
    newCoords[0] = (point1[0] + point2[0]) / 2
    newCoords[1] = (point1[1] + point2[1]) / 2

    return newCoords
}

involved_sensors = []
function getCapteurIncident(coords) {
    involved_sensor = [];

    for (i = 0; i < nbSensor; i++) {
        sensor = all_case[i];
        if (sensor.sw[0] <= coords[0] && coords[0] < sensor.ne[0] && sensor.sw[1] <= coords[1] && coords[1] < sensor.ne[1]) {
            involved_sensor.push(sensor);
        }

    }
    diff = involved_sensor.filter(x => involved_sensors.indexOf(x) === -1)
    involved_sensors.push(...diff)
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

function findIncidentFromSensor(sensors) {
    console.log(sensors)
    // Tableau pour stocker les résultats finaux
    console.log(sensors)
    const incidentSensor = [];

    // Tableau pour stocker les voisins de chaque capteur
    const allNeighboursSensor = sensors.map(sensor => {
        return findNeighbours(sensor.id);
    });
    // console.log(allNeighboursSensor)

    // Fonction pour filtrer les voisins non désirés
    function filterUnwantedNeighbours(neighboursList, desiredCases) {
        // Filtrer les voisins pour ne conserver que ceux présents dans desiredCases
        neighboursList = neighboursList.filter(neighbour => desiredCases.includes(neighbour));

        // console.log(neighboursList)
        sensorInit = neighboursList[0]

        return neighboursList
    }

    // Pour chaque capteur et ses voisins, filtrer les voisins non désirés
    console.log(allNeighboursSensor)
    for (let i = 0; i < allNeighboursSensor.length; i++) {
        const neighbor = allNeighboursSensor[i];
        const filteredNeighbours = filterUnwantedNeighbours(neighbor, sensors.map(s => s.id));
        console.log(neighbor)
        console.log(filteredNeighbours)
        console.log("------")

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
                    const isEvenRow = Math.ceil(sensorId / nbCol) % 2 === 0;

                    if (!isEvenRow) {
                        // Vérifier s'il est sur la première ligne ou le premier de la ligne
                        if (sensorId <= nbCol || sensorId % nbCol === 1) {
                            // console.log("oui:", filteredNeighbours);
                            incidentSensor.push(filteredNeighbours);
                        }
                    } else { // Si la ligne est impair
                        // Vérifier s'il est sur la dernière ligne ou à la fin de la ligne
                        const row = Math.ceil(sensorId / nbCol);
                        if (row === nbLine || sensorId % nbCol === 0) {
                            // console.log("oui:", filteredNeighbours);
                            incidentSensor.push(filteredNeighbours);
                        }
                    }
                } else {
                    // console.log("oui:", filteredNeighbours);
                    incidentSensor.push(filteredNeighbours);
                }
            }
        }
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

    // console.log(incidentSensor)
    // Supprimer les doublons de incidentSensor et stocker le résultat dans uniqueIncidentSensor
    const uniqueIncidentSensor = removeDuplicateArrays(incidentSensor);

    // Pour chaque groupe de capteurs uniques, trouver leur centre et stocker les coordonnées dans coordsIncident
    coordsIncident = [];

    for (let i = 0; i < uniqueIncidentSensor.length; i++) {
        subArea = uniqueIncidentSensor[i];
        for (let j = 0; j < subArea.length; j++) {
            subAreaItem = subArea[j];
            // Trouver le capteur correspondant à l'ID dans sensors
            sensor = sensors.find(objet => objet.id === subAreaItem);
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


function findCenterArea(area) {
    minSw = [400, 400]
    maxNe = [-400, -400]

    // console.log(area)

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

function sortAndStringify(arr) {
    return JSON.stringify(arr.slice().sort());
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

var map = new mapboxgl.Map({
    container: 'map',
    style: 'mapbox://styles/mapbox/streets-v11',
    center: centerCoordinates,
    zoom: 11.2
});

map.on('load', function () {
    map.addLayer({
        id: 'mapCenter',
        type: 'circle',
        source: {
            type: 'geojson',
            data: {
                type: 'FeatureCollection',
                features: [{
                    type: 'Feature',
                    geometry: {
                        type: 'Point',
                        coordinates: [centerCoordinates[0], centerCoordinates[1]]
                    }
                }]
            }
        },
        // centre de la carte 
        paint: {
            'circle-radius': 4,
            'circle-color': 'blue'
        }
    });
    for (var i = -nbLine / 2; i < nbLine / 2; i++) {
        for (var j = -nbCol / 2; j < nbCol / 2; j++) {
            // ajuster les coordonnées calculées pour gérer la superposition de moitier
            // var ajustJ = (gridSize/2)*(j+nbCol/2) - (gridSize*(nbCol/4+0.25))
            // var ajustJ = gridSize*(0.5*j-0.25)
            if (i % 2 == 0) {
                var ajustJ = gridSize / 2
            } else {
                var ajustJ = 0
            }
            // var ajustI = (gridSize/2)*(i+nbLine/2) - (gridSize*(nbLine/4+0.25))
            var ajustI = gridSize * (0.5 * i - 0.25)
            // var ajustI = 0

            var grid_coordinates = [
                [(centerCoordinates[0] - gridSize / 2) + j * gridSize - ajustJ, (centerCoordinates[1] - gridSize / 2) + i * gridSize - ajustI],
                [(centerCoordinates[0] - gridSize / 2) + (j + 1) * gridSize - ajustJ, (centerCoordinates[1] - gridSize / 2) + i * gridSize - ajustI],
                [(centerCoordinates[0] - gridSize / 2) + (j + 1) * gridSize - ajustJ, (centerCoordinates[1] - gridSize / 2) + (i + 1) * gridSize - ajustI],
                [(centerCoordinates[0] - gridSize / 2) + j * gridSize - ajustJ, (centerCoordinates[1] - gridSize / 2) + (i + 1) * gridSize - ajustI],
                [(centerCoordinates[0] - gridSize / 2) + j * gridSize - ajustJ, (centerCoordinates[1] - gridSize / 2) + i * gridSize - ajustI]
            ]

            var grid_area = {
                type: 'Feature',
                geometry: {
                    type: 'Polygon',
                    coordinates: [grid_coordinates]
                }
            };

            setGlobalBounds(grid_coordinates[0], grid_coordinates[2])

            // calcul centre case
            var centerLng = (centerCoordinates[0] - gridSize / 2) + j * gridSize - ajustJ + gridSize / 2;
            var centerLat = (centerCoordinates[1] - gridSize / 2) + i * gridSize - ajustI + gridSize / 2;

            // pour trouver l'id lié à la coordonné inversé de la génération
            id = ((-i + nbLine * 1.5 + 1) % (nbLine + 1) - 1) * nbCol + (j + nbCol * 1.5 + 1) % (nbCol + 1) + 1
            case_data.case[id - 1] = {
                "id": id,
                "coord": [centerLat, centerLng]
            }
            all_case.push({ 'id': id, 'sw': grid_coordinates[0], 'ne': grid_coordinates[2] })

            map.addLayer({
                id: 'grid-' + i + '-' + j,
                type: 'fill',
                source: {
                    type: 'geojson',
                    data: grid_area
                },
                paint: {
                    'fill-color': 'rgba(255,0,0,0.2)',
                    // 'fill-color': random_rgba(1) 
                    'fill-outline-color': 'rgba(255,0,0,1)'
                }
            });

            // affichage centre case
            map.addLayer({
                id: 'point-' + i + '-' + j,
                type: 'circle',
                source: {
                    type: 'geojson',
                    data: {
                        type: 'FeatureCollection',
                        features: [{
                            type: 'Feature',
                            geometry: {
                                type: 'Point',
                                coordinates: [centerLng, centerLat]
                            }
                        }]
                    }
                },
                paint: {
                    'circle-radius': 3,
                    'circle-color': 'black'
                }
            });

            // afficher coordonées centre case
            map.addLayer({
                id: 'grid-label-' + i + '-' + j,
                type: 'symbol',
                source: {
                    type: 'geojson',
                    data: {
                        type: 'FeatureCollection',
                        features: [{
                            type: 'Feature',
                            geometry: {
                                type: 'Point',
                                coordinates: [centerLng, centerLat]
                            },
                            properties: {
                                // label: '(' + centerLng.toFixed(6) + ', \n ' + centerLat.toFixed(6) + ')'

                                label: '(' + id + ')'
                            }
                        }]
                    }
                },
                layout: {
                    'text-field': ['get', 'label'],
                    'text-variable-anchor': ['top', 'bottom', 'left', 'right'],
                    'text-radial-offset': 0.5,
                    'text-justify': 'auto'
                },
                paint: {
                    'text-color': 'black',
                    'text-halo-color': 'white',
                    'text-halo-width': 0.5
                }
            });
        }
    }

    //debug
    // allIncident = [
    //     [
    //       4.885124125641507,
    //       45.72970089765904
    //     ],
    //     [
    //       4.850443854043286,
    //       45.77371457012844
    //     ],
    //     [
    //       4.841913704946563,
    //       45.731499467924806
    //     ],
    //     [
    //       4.881117501308516,
    //       45.759458602604376
    //     ],
    //     [
    //       4.857443761764803,
    //       45.76082656466434
    //     ],
    //     [
    //       4.865436048723783,
    //       45.75067210179121
    //     ],
    //     [
    //       4.913497344202285,
    //       45.7480647063997
    //     ],
    //     [
    //       4.845771217844128,
    //       45.76802487412693
    //     ],
    //     [
    //       4.823262638387391,
    //       45.732338624290634
    //     ],
    //     [
    //       4.863369893907695,
    //       45.767640409049335
    //     ],
    //     [
    //         4.912171053949781,
    //         45.7870753657824
    //     ]
    // ]

    // test2.forEach(incident => {
    //     marker = new mapboxgl.Marker({
    //         color:'#FFFFFF',
    //         draggable: false
    //     }).setLngLat(incident).addTo(map);

    //     getCapteurIncident(incident); 
    // });

    //random
    allIncident = []
    for (let i = 0; i < 10; i++) {
        randomPoint1 = getRandomPoint()
        allIncident.push(randomPoint1)
        marker = new mapboxgl.Marker({
            color: '#FFFFFF',
            draggable: false
        }).setLngLat(randomPoint1).addTo(map);

        getCapteurIncident(randomPoint1);
    }
    // console.log(allIncident)

    incidents = findIncidentFromSensor(involved_sensors)

    incidents.forEach(x => {
        marker = new mapboxgl.Marker({
            color: '#800080',
            draggable: false
        }).setLngLat(x)
            .setPopup(new mapboxgl.Popup().setHTML('<h3>' + x + '</h3>'))
            .addTo(map);
    })
});

var firestation_data = { firestation: [] }

fetch('casernes.json')
    .then(function (response) {
        return response.json();
    })
    .then(function (data) {
        data.firestation.forEach(function (firestation, index) {
            firestation_data.firestation[index] = firestation
            var coordinates = [firestation.coord.long, firestation.coord.lat];
            new mapboxgl.Marker()
                .setLngLat(coordinates)
                .setPopup(new mapboxgl.Popup().setHTML('<h3>' + firestation.name + '</h3>'))
                .addTo(map);
        });
    })
    .catch(function (error) {
        console.error('Erreur de chargement du fichier JSON :', error);
    });


function export_data() {
    const filename = "grid_data.json"
    data = { firestation: [], case: [] }
    data['case'] = case_data['case']
    data['firestation'] = firestation_data['firestation']
    data['center'] = centerCoordinates

    const jsonData = JSON.stringify(data)

    var blob = new Blob([jsonData], { type: "application/json" });
    var url = window.URL.createObjectURL(blob);
    var a = document.createElement("a");
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);

}
