
import { toaster } from "./toaster.js";

// Classe pour gérer les opérations liées aux casernes
export class EquipmentService 
{
    constructor(apiService) 
    {
        this.apiService = apiService;
    }

    async getEquipment() 
    {
        try 
        {
            return await this.apiService.makeRequest('/api/v1/equipment/', 'GET', null);
        } 
        catch (error) 
        {
            // Gérer les erreurs
            console.error('Erreur lors de la récupération des données des casernes :', error);
            toaster.error("Problème de connexion au serveur");
        }
    }
}
