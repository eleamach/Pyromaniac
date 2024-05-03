// Classe pour gérer les opérations liées aux casernes
export class WeatherService
{
    constructor(apiService) 
    {
        this.apiService = apiService;
    }

    async getAllWeather() 
    {
        try 
        {
            return await this.apiService.makeRequest('/weather/', 'GET', null);
        } 
        catch (error) 
        {
            // Gérer les erreurs
            console.error('Erreur lors de la récupération des données des capteurs :', error);
            alert("Problème de connexion au serveur");
        }
    }

}