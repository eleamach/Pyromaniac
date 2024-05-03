// Classe pour gérer les opérations liées aux casernes
export class TypeEquipmentService {
    constructor(apiService) {
        this.apiService = apiService;
    }

    async addType(nom, capacitePers, level, image) 
    {
        try {
            // Appeler l'API pour traiter les données
            await this.apiService.makeRequest('/api/v1/type-equipment', 'POST', 
            {
                type_equipment_name: nom,
                type_equipment_capacity_pers: capacitePers,
                type_equipment_level_incident: level,
                type_equipment_image: image
            });

            // Effacer les champs du formulaire
            $('.add-type').trigger("reset");
        } 
        catch (error) 
        {
            // Gérer les erreurs
            console.error('Erreur lors de l\'ajout de la caserne :', error);
            alert("Une erreur est survenue lors de l'ajout de la caserne");
        }
    }

    async getTypes() 
    {
        try 
        {
            return await this.apiService.makeRequest('/api/v1/type-equipment', 'GET', null);
        } 
        catch (error) 
        {
            // Gérer les erreurs
            console.error('Erreur lors de la récupération des données des casernes :', error);
            alert("Problème de connexion au serveur");
        }
    }

    async deleteTypes(id) 
    {
        try 
        {
            // Appeler l'API pour traiter les données
            await this.apiService.makeRequest('/api/v1/type-equipment/' + id, 'DELETE', {});
        } 
        catch (error) 
        {
            // Gérer les erreurs
            console.error('Erreur lors de la suppression de l\'équipement :', error);
            alert("Une erreur est survenue lors de la suppression de l'équipement");
        }
    }
}
