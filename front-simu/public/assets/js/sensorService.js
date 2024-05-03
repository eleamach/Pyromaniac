
import { toaster } from "./toaster.js";

// Classe pour gérer les opérations liées aux casernes
export class SensorService
{
    constructor(apiService) 
    {
        this.apiService = apiService;
    }

    async getAllSensor() 
    {
        try 
        {
            return await this.apiService.makeRequest('/sensor/', 'GET', null);
        } 
        catch (error) 
        {
            // Gérer les erreurs
            console.error('Erreur lors de la récupération des données des capteurs :', error);
            toaster.error("Problème de connexion au serveur");
        }
    }

}