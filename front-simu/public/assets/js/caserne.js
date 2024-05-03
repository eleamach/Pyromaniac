import { CaserneService } from "./CaserneService.js";
import { apiEM } from "./api.js";

const caserneService = new CaserneService(apiEM)

export async function getCasernes() {
    try {
        var data
        await caserneService.getCasernes()
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

export async function CaserneMain(map) {
    var allCaserne = await getCasernes()

    allCaserne.forEach((caserne, id) => {
        map.on('load', function () {
            map.addLayer({
                id: 'caserne-' + id,
                type: 'symbol',
                source: {
                    type: 'geojson',
                    data: {
                        type: 'FeatureCollection',
                        features: [
                            {
                                type: 'Feature',
                                geometry: {
                                    type: 'Point',
                                    coordinates: [
                                        caserne.fire_station_longitude,
                                        caserne.fire_station_latitude
                                    ]
                                },
                            }
                        ]
                    }
                },
                layout: {
                    'icon-image': 'firestation', // Nom de l'image personnalisée
                    'icon-size': 0.06, // Taille de l'icône (ajustez au besoin)
                    'icon-allow-overlap': true // Permettre le chevauchement d'icônes
                }
            });
        });
    });
}