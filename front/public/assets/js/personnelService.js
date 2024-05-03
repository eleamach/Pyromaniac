// Classe pour gérer les opérations liées au personnel
export class PersonnelService 
{
    constructor(apiService) 
    {
        this.apiService = apiService;
    }

    async addPersonnel(firstname, lastname, matricule, age, formed, password) 
    {
        try 
        {
            // Appeler l'API pour traiter les données
            let personnel = await this.apiService.makeRequest('/api/v1/employees', 'POST', 
            {
                employee_first_name: firstname,
                employee_last_name: lastname,
                employee_number: matricule,
                employee_disable: false,
                employee_password: password,
            });
            if(formed != "null") 
            {
                await this.apiService.makeRequest('/api/v1/type-equipment-employee', 'POST', 
                {
                    id_type_equipment: formed,
                    employee_number: personnel.employee_number,
                });
            }
        } 
        catch (error) 
        {
            // Gérer les erreurs
            console.error('Erreur lors de l\'ajout du personnel :', error);
            alert("Une erreur est survenue lors de l'ajout du personnel");
        }
    }

    async getPersonnels() 
    {
        try 
        {
            return await this.apiService.makeRequest('/api/v1/employees', 'GET', null);
        } 
        catch (error) 
        {
            // Gérer les erreurs
            console.error('Erreur lors de la récupération des données du personnel :', error);
            alert("Problème de connexion au serveur");
        }
    }

    async deletePersonnel(id) 
    {
        try 
        {
            await this.apiService.makeRequest('/api/v1/employees/' + id, 'DELETE', {});
        } 
        catch (error) 
        {
            // Gérer les erreurs
            console.error('Erreur lors de la suppression du personnel :', error);
            alert("Une erreur est survenue lors de la suppression du personnel");
        }
    }
}
