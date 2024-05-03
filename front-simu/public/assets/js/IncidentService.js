
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
            return await this.apiService.makeRequest('/incident/', 'GET', null);
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
            return await this.apiService.makeRequest('/incident_sensor_histo/incident_id/'+id, 'GET', null);
        } 
        catch (error) 
        {
            // Gérer les erreurs
            console.error('Erreur lors de la récupération des données des capteurs :', error);
            toaster.error("Problème de connexion au serveur");
        }
    }
}

export class IncidentSimulationService
{
    constructor(apiService) 
    {
        this.apiService = apiService;
    }

    async getIncidentBySimu(id) 
    {
        try 
        {
            return await this.apiService.makeRequest('/incident_simulation/simulation_id/'+id, 'GET', null);
        } 
        catch (error) 
        {
            // Gérer les erreurs
            console.error('Erreur lors de la récupération des données des capteurs :', error);
            toaster.error("Problème de connexion au serveur");
        }
    }
}