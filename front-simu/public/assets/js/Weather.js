import { apiClient } from "./api.js";
import { WeatherService } from "./WeatherService.js";
const weatherService = new WeatherService(apiClient)


export function importWeather() {
    const meteoSelect = document.getElementById("meteo");
    meteoSelect.innerHTML = "";

    try {
        weatherService.getAllWeather()
            .then(data => {
                data.forEach(function (weather) {
                    const option = document.createElement("option");
                    option.value = weather.weather_id; // Utilisez l'ID comme valeur
                    option.text = weather.weather_name; // Utilisez le nom comme texte de l'option
                    if (option.text == "Soleil") {
                        option.selected = true;

                    }
                    meteoSelect.appendChild(option);
                });
                meteoSelect.disabled = false
            })
            .catch(error => {
                console.error(error);
            });
    } catch (error) {
        console.log(error)
    }
}