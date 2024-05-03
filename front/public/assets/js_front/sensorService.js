
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
            return await this.apiService.makeRequest('/api/v1/sensor/', 'GET', null);
        } 
        catch (error) 
        {
            // Gérer les erreurs
            console.error('Erreur lors de la récupération des données des capteurs :', error);
            toaster.error("Problème de connexion au serveur");
        }
    }

    async getSensorById(id) 
    {
        try 
        {
            return await this.apiService.makeRequest('/api/v1/sensor/'+id, 'GET', null);
        } 
        catch (error) 
        {
            // Gérer les erreurs
            console.error('Erreur lors de la récupération des données des capteurs :', error);
            toaster.error("Problème de connexion au serveur");
        }
    }

    async getSensorOff() 
    {
        try 
        {
            return await this.apiService.makeRequest('/api/v1/sensor/status/false', 'GET', null);
        } 
        catch (error) 
        {
            // Gérer les erreurs
            console.error('Erreur lors de la récupération des données des capteurs :', error);
            toaster.error("Problème de connexion au serveur");
        }
    }

}

export class SensorHistoService
{
    constructor(apiService) 
    {
        this.apiService = apiService;
    }

    async getSensorHistoByIncidentService(id) 
    {
        try 
        {
            return await this.apiService.makeRequest('/api/v1/sensor-histo/'+id, 'GET', null);
        } 
        catch (error) 
        {
            // Gérer les erreurs
            console.error('Erreur lors de la récupération des données des capteurs :', error);
            toaster.error("Problème de connexion au serveur");
        }
    }

}