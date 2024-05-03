// Classe pour gérer les opérations liées aux casernes
export class CaserneService 
{
    constructor(apiService) 
    {
        this.apiService = apiService;
    }

    async addCaserne(nom, longitude, latitude) 
    {
        try {
            // Appeler l'API pour traiter les données
            await this.apiService.makeRequest('/api/v1/firestation', 'POST', 
            {
                fire_station_name: nom,
                fire_station_longitude: longitude,
                fire_station_latitude: latitude,
            });
        } 
        catch (error) 
        {
            // Gérer les erreurs
            console.error('Erreur lors de l\'ajout de la caserne :', error);
            alert("Une erreur est survenue lors de l'ajout de la caserne");
        }
    }

    async getCasernes() 
    {
        try 
        {
            return await this.apiService.makeRequest('/api/v1/firestation', 'GET', null);
        } 
        catch (error) 
        {
            // Gérer les erreurs
            console.error('Erreur lors de la récupération des données des casernes :', error);
            alert("Problème de connexion au serveur");
        }
    }

    async deleteCaserne(nom) 
    {
        try 
        {
            let caserne = await this.apiService.makeRequest('/api/v1/firestation/name/' + nom, 'GET', {});
            await this.apiService.makeRequest('/api/v1/firestation/' + caserne.id_fire_station, 'DELETE', {});
        } catch (error) 
        {
            // Gérer les erreurs
            console.error('Erreur lors de la suppression de la caserne :', error);
            alert("Une erreur est survenue lors de la suppression de la caserne");
        }
    }
}
