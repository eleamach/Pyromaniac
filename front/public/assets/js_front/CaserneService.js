// Classe pour gérer les opérations liées aux casernes

import { toaster } from "./toaster.js";

export class CaserneService 
{
    constructor(apiService) 
    {
        this.apiService = apiService;
    }

    async getCasernes() 
    {
        try 
        {
            return await this.apiService.makeRequest('/api/v1/firestation/', 'GET', null);
        } 
        catch (error) 
        {
            // Gérer les erreurs
            console.error('Erreur lors de la récupération des données des casernes :', error);
            toaster.error("Problème de connexion au serveur");
        }
    }
}
