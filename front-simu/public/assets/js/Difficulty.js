import { apiClient } from "./api.js";
import { DifficultyService } from "./DifficultyService.js";
const difficultyService = new DifficultyService(apiClient)

export function importDifficulty() {
    const difficultySelect = document.getElementById("difficulte");
    difficultySelect.innerHTML = "";

    try {
        difficultyService.getAllDifficulty()
            .then(data => {
                data.forEach(function (difficulty) {
                    const option = document.createElement("option");
                    option.value = difficulty.difficulty_id; // Utilisez l'ID comme valeur
                    option.text = difficulty.difficulty_name; // Utilisez le nom comme texte de l'option
                    if (option.text == "Moyen") {
                        option.selected = true;
                    }
                    difficultySelect.appendChild(option);
                });
                difficultySelect.disabled = false
            })
            .catch(error => {
                console.error(error);
            });
    } catch (error) {
        console.log(error)
    }
}

export function selectInput(diff) {
    const selectElement = document.getElementById("difficulte"); // Obtenez l'élément select par son ID
    const options = selectElement.options; // Obtenez la liste des options

    // Parcourez les options pour trouver celle avec la valeur spécifique
    for (let i = 0; i < options.length; i++) {
        if (options[i].value == diff.difficulty_id) {
            options[i].selected = true
        }
    }
}