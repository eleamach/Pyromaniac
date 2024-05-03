import { ApiClient } from './apiClient.js';
import { AuthenticationService } from './authenticationService.js';
import { PersonnelService } from './personnelService.js';
import { CaserneService } from './caserneService.js';
import { TypeEquipmentService } from './typeEquipmentService.js';
import { equipeService } from './equipeService.js';


// Utilisation des classes


const apiClient = new ApiClient('https://projet.jaufre.fr'); // Apiclient nous permet de faire les requêtes API

const authenticationService = new AuthenticationService(apiClient);
authenticationService.isConnected();

const personnelService = new PersonnelService(apiClient); // PersonnelService nous permet de faire les requêtes liées au personnel
const caserneService = new CaserneService(apiClient); // CaserneService nous permet de faire les requêtes liées aux casernes
const typeEquipmentService = new TypeEquipmentService(apiClient); // TypeEquipmentService nous permet de faire les requêtes liées aux types d'équipements
const equipeServiceInstance  = new equipeService(apiClient);

// On charge le header et le footer
$(document).ready(function() 
{
    $("#header").load("/views/Gestion/header.html");
    $("#footer").load("/views/Gestion/footer.html");
});


function convertFormDataToArray(formData) 
{
    const result = {};

    formData.forEach((field) => 
    {
        result[field.name] = field.value;
    });

    return result;
}



$(document).ready(function () 
{
    // Afficher les données
    if (document.getElementById("affichagePersonnel")) 
    {
        loadPersonnel(personnelService, typeEquipmentService);
    }
    if (document.getElementById("equipementContainer")) 
    {
        loadequipement(typeEquipmentService);
    }
    if (document.getElementById("sitesContainer")) 
    {
        loadCasernes(caserneService);
    }    
    if (document.getElementById("teamContainer")) 
    {
        loadteam(equipeServiceInstance);
    }

    // Intercepter le formulaire d'ajout de personnel
    $('.add-personnel').submit(function (event) 
    {
        // Empêcher le comportement par défaut du formulaire qui provoquerait un rechargement de la page
        event.preventDefault();
        // Appeler la fonction pour traiter les données du formulaire
        addPersonnel(personnelService);
        $('.add-personnel').trigger("reset");
    });

    $('.sub-personnel').submit(async function (event) 
    {
        event.preventDefault();
        var matriculeToDelete = $('form.sub-personnel #matricule').val();
        await personnelService.deletePersonnel(matriculeToDelete);
        loadPersonnel(personnelService);
        $('.sub-personnel').trigger("reset");
    });

    // Intercepter le formulaire d'ajout de site
    $('#add-caserne').submit(async function (event) 
    {
        event.preventDefault();
        await addCaserne(caserneService);
        loadCasernes(caserneService);
        $('#add-caserne').trigger("reset");
    });

    // Intercepter le formulaire de suppression de site
    $('#sitesuppr').submit(async function (event) 
    {
        event.preventDefault();
        var siteNameToDelete = $('#siteNameToDelete').val();
        await caserneService.deleteCaserne(siteNameToDelete);
        loadCasernes(caserneService);
        $('#sitesuppr').trigger("reset");
    });

    // Intercepter le formulaire d'ajout de personnel
    $('.add-form').submit(function (event) 
    {
        event.preventDefault();
        var formData = $(this).serialize();
        simulateSuccessfulAddition(formData);
        // Enregistrement dans le localStorage
        saveToLocalStorage();
        $('.add-form').trigger("reset");
    });

    $("#login").submit(async function (event) 
    {
        event.preventDefault();
        const formData = $(this).serializeArray();
        await authenticationService.logIn(convertFormDataToArray(formData));
        $('#login').trigger("reset");
    });
    
     // Intercepter le formulaire d'ajout d'équipement
    $('.addequi').submit(async function (event) 
    {
        event.preventDefault();
        await addequipement(typeEquipmentService);
        // Appeler la fonction pour charger et afficher les équipements après l'ajout
        loadequipement(typeEquipmentService);
        $('.addequi').trigger("reset");
    });

    // Intercepter le formulaire de suppression d'équipement
    $('.subequi').submit(async function (event) 
    {
        event.preventDefault();
        var equipementNameToDelete = $('#equipementNameToDelete').val();
        await typeEquipmentService.deleteTypes(equipementNameToDelete);
        loadequipement(typeEquipmentService);
        $('.subequi').trigger("reset");
    });

     // Intercepter le formulaire d'ajout d'équipement
    $('.addteam').submit(async function (event) 
    {
        event.preventDefault();
        await addateam(equipeServiceInstance);
        // Appeler la fonction pour charger et afficher les équipements après l'ajout
        loadteam(equipeServiceInstance );
        $('.addteam').trigger("reset");
    });

    // Intercepter le formulaire de suppression d'équipement
    $('.subteam').submit(async function (event) {
        event.preventDefault();
        var idTeamToDelete = $('#idTeamToDelete').val();
    
        try {
            await equipeServiceInstance.deleteTeams(idTeamToDelete);
            console.log('Équipe supprimée avec succès.');
            loadteam(equipeServiceInstance);
            $('.subteam').trigger("reset");
        } catch (error) {
            console.error('Erreur lors de la suppression de l\'équipe :', error);
            alert("Une erreur est survenue lors de la suppression de l'équipe");
        }
    });

    // Intercepter le formulaire d'ajout d'équipement
    $('.addPersonTeam').submit(async function (event) 
    {
        event.preventDefault();
        await addpersontoteam(equipeServiceInstance);
        // Appeler la fonction pour charger et afficher les équipements après l'ajout
        loadteam(equipeServiceInstance );
        $('.addPersonTeam').trigger("reset");
    });

    // Intercepter le formulaire de suppression d'équipement
    $('.subPersonTeam').submit(async function (event) 
    {
        event.preventDefault();
        var idTeamToDelete = $('#idTeamToDelete').val();
        await equipeServiceInstance.deleteTeams(idTeamToDelete);
        loadteam(equipeServiceInstance );
        $('.subPersonTeam').trigger("reset");
    });
});