// Classe pour gérer les opérations liées aux casernes
export class equipeService 
{
    constructor(apiService) 
    {
        this.apiService = apiService;
    }

    async addTeam(nom, idfeu) 
    {
        try 
        {
            // Appeler l'API pour traiter les données
            await this.apiService.makeRequest('/api/v1/teams', 'POST', 
            {
                team_name: nom,
                id_fire_station: idfeu
            });

            // Effacer les champs du formulaire
            $('.addteam').trigger("reset");
            
            console.log('DEBUG');
        } 
        catch (error) 
        {
            // Gérer les erreurs
            console.error('Erreur lors de l\'ajout de la caserne :', error);
            alert("Une erreur est survenue lors de l'ajout de la caserne");
        }
    }

    async addPersonToTeam(idteam, matricule) 
    {
        try 
        {
            // Appeler l'API pour traiter les données
            await this.apiService.makeRequest('/api/v1/team-employee', 'POST', 
            {
                id_team: idteam,
                employee_number: matricule
            });

            // Effacer les champs du formulaire
            $('.addPersonTeam').trigger("reset");
            
        } 
        catch (error) 
        {
            // Gérer les erreurs
            console.error('Erreur lors de l\'ajout de la caserne :', error);
            alert("Une erreur est survenue lors de l'ajout de la caserne");
        }
    }

    async getTeams() 
    {
        try 
        {
            return await this.apiService.makeRequest('/api/v1/teams', 'GET', null);
        } 
        catch (error) 
        {
            // Gérer les erreurs
            console.error('Erreur lors de la récupération des données des casernes :', error);
            alert("Problème de connexion au serveur");
        }
    }

    async deleteTeams(id) 
    {
        try {
            // Appeler l'API pour traiter les données
            await this.apiService.makeRequest('/api/v1/teams/' + id, 'DELETE', {});
        } 
        catch (error) 
        {
            // Gérer les erreurs
            console.error('Erreur lors de la suppression de l\'équipement :', error);
            alert("Une erreur est survenue lors de la suppression de l'équipement");
        }
    }

    // Modifiez votre equipeService pour ajouter une méthode getEmployeesByTeam
    async getEmployeesByTeam(teamId) {
        try {
            return await this.apiService.makeRequest(`/api/v1/team-employee/teams_id/${teamId}/employees`, 'GET', null);
        } catch (error) {
            console.error('Erreur lors de la récupération des employés de l\'équipe :', error);
            alert("Problème de connexion au serveur");
        }
    }

}