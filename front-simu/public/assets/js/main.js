// Déclaration
mapboxgl.accessToken = 'pk.eyJ1Ijoic2thZmVlIiwiYSI6ImNscHNkajkxYzAyb3MyanQ3OTR6ZWl5bnkifQ.a_IZDhqmRKB_KJ6w6A24iA';

import { apiEM } from "./api.js";

import { clearAllMap, deleteSimu, getLastSimu, SimuMain, startSimulation } from "./Simulation.js"
import { importWeather } from "./Weather.js";
import { importDifficulty, selectInput } from "./Difficulty.js";
import { mapMain } from "./maps.js";
import { debugMain } from "./debug.js";
import { CaserneMain } from "./caserne.js";
import { EquipmentMain } from "./equipment.js";
import { AuthenticationService } from "./connection.js";
import { toaster } from "./toaster.js";

const authenticationService = new AuthenticationService(apiEM)


//=========== Template ===========
function init() {
    authenticationService.logIn()
    // Charger le contenu du header.html
    fetch("/views/header.html")
        .then(response => response.text())
        .then(data => {
            document.getElementById("header").innerHTML = data;
        });

    // Charger le contenu du footer.html
    fetch("/views/footer.html")
        .then(response => response.text())
        .then(data => {
            document.getElementById("footer").innerHTML = data;
        });

    // Charge form
    importWeather()
    importDifficulty()

}
document.addEventListener("DOMContentLoaded", init());

// ========== Simu ==========
var currentSimu

function simu() {
    const startButton = document.getElementById("start-simu-button");
    const stopButton = document.getElementById("stop-simu-button");
    const findButton = document.getElementById("find-simu-button");
    const stopInterval = document.getElementById("stop-interval-button");
    const meteoSelect = document.getElementById("meteo");
    const difficulteSelect = document.getElementById("difficulte");
    const vitesseSelect = document.getElementById("vitesse");

    // Gestion du clic sur le bouton "Start"
    startButton.addEventListener("click", async function () {
        currentSimu = await startSimulation(meteoSelect.value, difficulteSelect.value, vitesseSelect.value)

        if (currentSimu){
            // Masquer le bouton "Start" et afficher le bouton "Stop"
            startButton.style.display = "none";
            stopButton.style.display = "inline-block";
    
            // Désactiver les champs de formulaire
            meteoSelect.disabled = true;
            difficulteSelect.disabled = true;
            vitesseSelect.disabled = true;
            findButton.disabled = true;

            SimuMain(map)
            simuIntervalId = setInterval(SimuMain,2000, map)
        }
    });

    // Gestion du clic sur le bouton "Stop"
    stopButton.addEventListener("click", async function () {
        // Masquer le bouton "Stop" et réafficher le bouton "Start"
        startButton.style.display = "inline-block";
        stopButton.style.display = "none";

        // Activer à nouveau les champs de formulaire
        meteoSelect.disabled = false;
        difficulteSelect.disabled = false;
        vitesseSelect.disabled = false;
        findButton.disabled = false;
        await deleteSimu(currentSimu)
        clearInterval(simuIntervalId);
        clearAllMap(map)
    });

    findButton.addEventListener("click", async function () {
        currentSimu = await getLastSimu()
        if(currentSimu){
            selectInput(currentSimu.difficulty)
            // Masquer le bouton "Start" et afficher le bouton "Stop"
            startButton.style.display = "none";
            stopButton.style.display = "inline-block";
    
            // Désactiver les champs de formulaire
            meteoSelect.disabled = true;
            difficulteSelect.disabled = true;
            vitesseSelect.disabled = true;
            findButton.disabled = true;
    
            toaster.info("Simulation trouvé ! Lancement en cours")
            SimuMain(map)
            simuIntervalId = setInterval(SimuMain,30000, map)
        } else {
            toaster.error("Aucune simulation de trouvé en cours")
        }
    });
    
    stopInterval.addEventListener("click", function () {
        console.log("Stopping interval...");
        clearInterval(equipmentIntervalId);
        console.log("Interval stopped");
    });
}
var simuIntervalId

document.addEventListener("DOMContentLoaded", simu());
// ========== Maps ==========
var map = await mapMain(map)
debugMain(map)
CaserneMain(map)
EquipmentMain(map)
var equipmentIntervalId = setInterval(EquipmentMain,15000, map)
// CaserneMain(map)