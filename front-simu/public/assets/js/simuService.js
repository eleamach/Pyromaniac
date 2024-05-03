
import { toaster } from "./toaster.js";

// Classe pour gérer les opérations liées aux casernes
export class SimuService
{
    constructor(apiService) 
    {
        this.apiService = apiService;
    }

    async getCurrentSimu() 
    {
        try 
        {
            return await this.apiService.makeRequest('/simulation/', 'GET', null);
        } 
        catch (error) 
        {
            // Gérer les erreurs
            console.error('Erreur lors de la récupération des données des capteurs :', error);
            toaster.error("Problème de connexion au serveur");
        }
    }

    async startSimu(weather, difficulty, speed) 
    {
        try 
        {
            
            return await this.apiService.makeRequest('/simulation/', 'POST', {
                difficulty_id: difficulty,
                simulation_speed: speed
            });
        } 
        catch (error) 
        {
            // Gérer les erreurs
            console.error('Erreur lors de la récupération des données des capteurs :', error);
            toaster.error("Problème de connexion au serveur");
        }
    }

    async deleteSimu(id) 
    {
        try {
            await this.apiService.makeRequest('/simulation/' + id, 'DELETE', {});
        } 
        catch (error) 
        {
            console.error('Erreur lors de la suppression de la simulation :', error);
            toaster.error("Une erreur est survenue lors de la suppression de la simulation");
        }
    }


}