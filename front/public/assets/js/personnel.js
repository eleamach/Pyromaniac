function loadPersonnel(personnelService, typeEquipmentService) 
{
    personnelService.getPersonnels()
        .then((personnels) => 
        {
            // Afficher les données dans la page
            displayPersonnel(personnels);
        })
        .catch((error) => 
        {
            console.error('Erreur lors de la récupération des données du personnel :', error);
            alert("Problème de connexion au serveur");
        });
    typeEquipmentService.getTypes()
        .then((types) => 
        {
            // Afficher les données dans la page
            displayTypes(types);
        })
        .catch((error) => 
        {
            console.error('Erreur lors de la récupération des données des types d\'équipement :', error);
            alert("Problème de connexion au serveur");
        });
}

function displayPersonnel(personnels) 
{
    $('#affichagePersonnel').empty();
    for (var personnel of personnels) 
    {
        var personnelElement = document.createElement('div');
        // Afficher les données dans la page
        personnelElement.classList.add('personnel');
        personnelElement.classList.add('personnel-' + personnel.employee_number.toLowerCase());
        personnelElement.innerHTML = `<strong>${personnel.employee_last_name} ${personnel.employee_first_name}</strong>, matricule : ${personnel.employee_number}`;
        $('#affichagePersonnel').append(personnelElement);
    }
}

function displayTypes(types) 
{
    var formedSelect = document.getElementById("formed");
    // Ajouter chaque option à la liste déroulante
    for (var type of types) 
    {
        var option = document.createElement("option");
        option.value = type.id_type_equipment;
        option.text = type.type_equipment_name;
        formedSelect.appendChild(option);
    }
}

async function addPersonnel(personnelService)
{
    var firstname = $('#firstname').val();
    var lastname = $('#lastname').val();
    var matricule = $('#matricule').val();
    var age = $('#age').val();
    var formed = $('#formed').val();
    var password = $('#password').val();

    if(firstname == "" || lastname == "" || matricule == "" || password == "")
    {
        alert("Veuillez remplir tous les champs");
        return;
    }
    $('.add-personnel').trigger("reset");
    await personnelService.addPersonnel(firstname, lastname, matricule, age, formed, password);
    loadPersonnel(personnelService);
}