
import { toaster } from "./toaster.js";

// Classe pour gérer les opérations liées aux casernes
export class IncidentService
{
    constructor(apiService) 
    {
        this.apiService = apiService;
    }

    async getAllIncident() 
    {
        try 
        {
            return await this.apiService.makeRequest('/api/v1/incidents/', 'GET', null);
        } 
        catch (error) 
        {
            // Gérer les erreurs
            console.error('Erreur lors de la récupération des données des capteurs :', error);
            toaster.error("Problème de connexion au serveur");
        }
    }
}

export class IncidentSensorHistoService
{
    constructor(apiService) 
    {
        this.apiService = apiService;
    }

    async getIncidentHistoById(id) 
    {
        try 
        {
            return await this.apiService.makeRequest('/api/v1/incident-sensor-histo/incident/'+id, 'GET', null);
        } 
        catch (error) 
        {
            // Gérer les erreurs
            console.error('Erreur lors de la récupération des données des capteurs :', error);
            toaster.error("Problème de connexion au serveur");
        }
    }
}

