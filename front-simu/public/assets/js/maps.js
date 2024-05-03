mapboxgl.accessToken = 'pk.eyJ1Ijoic2thZmVlIiwiYSI6ImNscHNkajkxYzAyb3MyanQ3OTR6ZWl5bnkifQ.a_IZDhqmRKB_KJ6w6A24iA';

import { SensorService } from "./sensorService.js";
import { SimuService } from "./simuService.js";
import { apiClient } from "./api.js";


import { getGlobalBounds, getSensors } from "./sensor.js";


function findCenter(point1, point2) {
    var newCoords = []
    newCoords[0] = (point1.long + point2.long) / 2
    newCoords[1] = (point1.lat + point2.lat) / 2

    return newCoords
}


function getGlobalBoundsGEO(globalBounds) {
    const globalBoundsGEO = {
        type: 'Feature',
        geometry: {
            type: 'Polygon',
            coordinates: [
                [
                    [globalBounds.nw.long, globalBounds.nw.lat],
                    [globalBounds.ne.long, globalBounds.ne.lat],
                    [globalBounds.se.long, globalBounds.se.lat],
                    [globalBounds.sw.long, globalBounds.sw.lat],
                    [globalBounds.nw.long, globalBounds.nw.lat],
                ]
            ]
        }
    };
    return globalBoundsGEO
}

export async function mapMain() {
    const allSensors = await getSensors();
    const globalBounds = getGlobalBounds(allSensors);
    const globalBoundsGEO = getGlobalBoundsGEO(globalBounds);
    const center = findCenter(globalBounds.sw, globalBounds.ne);

    var map = new mapboxgl.Map({
        container: 'map',
        style: 'mapbox://styles/mapbox/streets-v11',
        center: center,
        zoom: 11.2
    });


    map.addControl(new mapboxgl.NavigationControl(), "top-left");
    class HomeButton {
        onAdd(map) {
            const div = document.createElement("div");
            div.className = "mapboxgl-ctrl mapboxgl-ctrl-group";
            div.innerHTML = `<button>
            <svg focusable="false" viewBox="0 0 24 24" aria-hidden="true" style="font-size: 20px;"><title>Reset map</title><path d="M10 20v-6h4v6h5v-8h3L12 3 2 12h3v8z"></path></svg>
            </button>`;
            div.addEventListener("contextmenu", (e) => e.preventDefault());
            div.addEventListener("click", () => {
                map.setCenter(center)
                map.setZoom(11.2)
            });
            return div;
        }
    }
    const homeButton = new HomeButton();
    map.addControl(homeButton, "bottom-right");
    map.loadImage('/public/assets/img/fire-station.png', (error, image) => { // Remplacez '/assets/img/votre-image.png' par le chemin de votre image PNG convertie
        if (error) throw error;
        map.addImage('firestation', image);
    });
    map.loadImage('/public/assets/img/fire-truck.png', (error, image) => { // Remplacez '/assets/img/votre-image.png' par le chemin de votre image PNG convertie
        if (error) throw error;
        map.addImage('firetruck', image);
    });
    map.loadImage('/public/assets/img/house-fire.png', (error, image) => { // Remplacez '/assets/img/votre-image.png' par le chemin de votre image PNG convertie
        if (error) throw error;
        map.addImage('fire', image);
    });

    map.on('load', function () {
        map.addLayer({
            id: 'grid',
            type: 'line',
            source: {
                type: 'geojson',
                data: globalBoundsGEO
            },
            paint: {
                'line-color': 'rgba(255,0,0,1)',
                'line-width': 3
            }
        });
    });

    return map

}