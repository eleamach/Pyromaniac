import { getBounds, getGlobalBounds, getSensors } from "./sensor.js";

export async function debugMain(map) {
    const debugButtonOn = document.getElementById("debug-on-simu-button");
    const debugButtonOff = document.getElementById("debug-off-simu-button");
    const allSensors = await getSensors();
    debugButtonOn.addEventListener("click", function () {
        debugButtonOn.style.display = "none";
        debugButtonOff.style.display = "inline-block";
        allSensors.forEach((sensor, i) => {
            var bound = getBounds(sensor)
            var grid_area = {
                type: 'Feature',
                geometry: {
                    type: 'Polygon',
                    coordinates: [
                        [
                            [bound.nw.long, bound.nw.lat],
                            [bound.ne.long, bound.ne.lat],
                            [bound.se.long, bound.se.lat],
                            [bound.sw.long, bound.sw.lat],
                            [bound.nw.long, bound.nw.lat],
                        ]
                    ]
                }
            };
            map.addLayer({
                id: 'grid-' + i,
                type: 'fill',
                source: {
                    type: 'geojson',
                    data: grid_area
                },
                paint: {
                    'fill-color': 'rgba(255,0,0,0.2)',
                    'fill-outline-color': 'rgba(255,0,0,1)'
                }
            });
        });
    });

    debugButtonOff.addEventListener("click", function () {
        debugButtonOff.style.display = "none";
        debugButtonOn.style.display = "inline-block";

        allSensors.forEach((sensor, i) => {
            map.removeLayer('grid-' + i);
            map.removeSource('grid-' + i);
        });
    });
}