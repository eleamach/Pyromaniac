
import { toaster } from "./toaster.js";

// Classe pour gérer les opérations liées aux casernes
export class SettingService 
{
    constructor(apiService) 
    {
        this.apiService = apiService;
    }

    async getGap() 
    {
        try 
        {
            return await this.apiService.makeRequest('/parameters/neighbor-longitude', 'GET', null);
        } 
        catch (error) 
        {
            // Gérer les erreurs
            console.error('Erreur lors de la récupération des données des casernes :', error);
            toaster.error("Problème de connexion au serveur");
        }
    }
}
