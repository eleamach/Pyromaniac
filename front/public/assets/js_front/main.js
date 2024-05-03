// Déclaration
mapboxgl.accessToken = 'pk.eyJ1Ijoic2thZmVlIiwiYSI6ImNscHNkajkxYzAyb3MyanQ3OTR6ZWl5bnkifQ.a_IZDhqmRKB_KJ6w6A24iA';

import { apiClient } from "./api.js";

import { SimuMain } from "./Simulation.js"
import { mapMain } from "./maps.js";
import { debugMain } from "./debug.js";
import { CaserneMain } from "./caserne.js";
import { EquipmentMain } from "./equipment.js";
import { AuthenticationService } from "./connection.js";

const authenticationService = new AuthenticationService(apiClient)


//=========== Template ===========
function init() {
    authenticationService.logIn()
    // Charger le contenu du header.html
    fetch("/views/Maps/header.html")
        .then(response => response.text())
        .then(data => {
            document.getElementById("header").innerHTML = data;
        });

    // Charger le contenu du footer.html
    fetch("/views/Maps/footer.html")
        .then(response => response.text())
        .then(data => {
            document.getElementById("footer").innerHTML = data;
        });


}
document.addEventListener("DOMContentLoaded", init());

// ========== Simu ==========
var currentSimu

var map = await mapMain(map)
function simu() {
    const stopInterval = document.getElementById("stop-interval-button");
    SimuMain(map)
    simuIntervalId = setInterval(SimuMain, 3000, map)

    stopInterval.addEventListener("click", function () {
        console.log("Stopping interval...");
        clearInterval(equipmentIntervalId);
        console.log("Interval stopped");
    });
}
var simuIntervalId

document.addEventListener("DOMContentLoaded", simu());
// ========== Maps ==========
debugMain(map)
CaserneMain(map)
EquipmentMain(map)
var equipmentIntervalId = setInterval(EquipmentMain, 15000, map)
// CaserneMain(map)