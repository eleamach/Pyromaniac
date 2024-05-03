function loadequipement(TypeEquipmentService) 
{
    TypeEquipmentService.getTypes()
        .then((equipement) => 
        {
            // Afficher les données dans la page
            displayequipement(equipement);
            console.log('Equipements chargés avec succès.');
        })
        .catch((error) => 
        {
            console.error('Erreur lors de la récupération des données des equipement :', error);
            alert("Problème de connexion au serveur");
        });
}

function displayequipement(equipement) 
{
    $('#equipementContainer').empty();
    for (var type of equipement) 
    {
        var equipementElement = document.createElement('div');
        equipementElement.classList.add('equipement');
        equipementElement.classList.add('equipement-' + type.id_type_equipment);
        equipementElement.innerHTML = `${type.id_type_equipment} : <strong>${type.type_equipment_name}</strong>, capacité : ${type.type_equipment_capacity_pers}, level : ${type.type_equipment_level_incident}<br>`;
        $('#equipementContainer').append(equipementElement);
    }
}

async function addequipement(equipementService) 
{
    var equipementName = $('#equipementName').val();
    var equipementCapacity = $('#capacity').val();
    var equipementLevel = $('#levelincident').val();

    if (equipementName == "" || equipementCapacity == "" || equipementLevel == "") 
    {
        alert("Veuillez remplir tous les champs");
        return;
    }

    // Utilisez le sélecteur d'id pour réinitialiser le formulaire complet
    $('#add-equipement').trigger("reset");

    try 
    {
        await equipementService.addType(equipementName, equipementCapacity, equipementLevel);
        console.log('Equipement ajouté avec succès.');
        loadequipement(equipementService);
    } 
    catch (error) 
    {
        console.error('Erreur lors de l\'ajout de l\'équipement :', error);
        alert("Une erreur est survenue lors de l'ajout de l'équipement");
    }
}