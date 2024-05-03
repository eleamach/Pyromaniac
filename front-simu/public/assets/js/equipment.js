import { EquipmentService } from "./EquipmentService.js";
import { apiClient } from "./api.js";
import { getCasernes } from "./caserne.js";
// import { logger } from "./logger.js";
const equipmentService = new EquipmentService(apiClient)

// const logger = new logger()

async function getEquipment(){
    const casernes = await getCasernes()
    var data
    try{
        await equipmentService.getEquipment()
        .then(dataPromise => {
            data = dataPromise
        })
        .catch(error => {
            console.error(error);
        });
    } catch (error) {
        console.log(error)
    }

    data.forEach(truck => {
        truck.home = false;
        casernes.forEach(caserne => {
            if (truck.equipment_latitude == caserne.fire_station_latitude & truck.equipment_longitude == caserne.fire_station_longitude) {
                truck.home = true;
            }
        })     
    });

    return data
}

export async function EquipmentMain(map){
    const equipments = await getEquipment()
    equipments.forEach((equipment, id) => {
        if (!equipment.home){
            // console.log("INFO: equipment " + equipment.equipment_id + " at " + [equipment.equipment_longitude, equipment.equipment_latitude])

        }
        var equipmentSource = map.getSource("equipment-"+id)
        if (equipmentSource){
            const newGeoJSONData = {
                type: 'FeatureCollection',
                features: [
                    {
                        type: 'Feature',
                        geometry: {
                            type: 'Point',
                            coordinates: equipment.home ? [0,0] : [equipment.equipment_longitude, equipment.equipment_latitude]
                        },
                    },
                ],
            };
            equipmentSource.setData(newGeoJSONData);

        } else {
            map.addLayer({
                id: 'equipment-'+id,
                type: 'symbol',
                source: {
                    type: 'geojson',
                    data: {
                        type: 'FeatureCollection',
                        features: [{
                            type: 'Feature',
                            geometry: {
                                type: 'Point',
                                coordinates: equipment.home ? [0,0] : [equipment.equipment_longitude, equipment.equipment_latitude]
                            }
                        }]
                    }
                },
                layout: {
                    'icon-image': 'firetruck', // Nom de l'image personnalisée
                    'icon-size': 0.07, // Taille de l'icône (ajustez au besoin)
                    'icon-allow-overlap': true // Permettre le chevauchement d'icônes
                }
            });
        }
        
    });
}