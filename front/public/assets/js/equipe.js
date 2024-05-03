async function loadteam(equipeService, personnelService) {
    try {
        // Clear existing content
        $('#teamContainer').empty();
        const teams = await equipeService.getTeams();
        for (const team of teams) {
            const employees = await equipeService.getEmployeesByTeam(team.id_team);

            // Afficher les données dans la page, y compris les employés
            displayteam(team, employees);
        }
        console.log('Équipes et employés chargés avec succès.');
    } catch (error) {
        console.error('Erreur lors de la récupération des données des équipes et employés :', error);
        alert("Problème de connexion au serveur");
    }
}

function displayteam(team, employees) {
    var teamElement = document.createElement('div');
    teamElement.classList.add('team');
    teamElement.classList.add(`team-${team.id_fire_station}-${team.id_team}`);
    teamElement.innerHTML = `<strong>${team.team_name}</strong>, agenda : ${team.team_schedule}, id caserne : ${team.id_fire_station}, id team :  ${team.id_team}<br>`;

    // Ajoutez les employés à l'élément de l'équipe
    if (employees.length > 0) {
        for (const employee of employees) {
            teamElement.innerHTML += `<span>${employee.employee_first_name} ${employee.employee_last_name}, Matricule: ${employee.employee_number}</span><br>`;
        }
    } else {
        // Si l'équipe n'a pas de membres, vous pouvez ajouter un message indiquant l'absence de membres
        teamElement.innerHTML += '<span>Aucun membre dans cette équipe.</span><br>';
    }

    $('#teamContainer').append(teamElement);
}

async function addateam(equipeService) {
    var teamname = $('#teamName').val();
    var idcaserne = $('#idFireStation').val();

    if (teamname == "" || idcaserne == "") {
        alert("Veuillez remplir tous les champs");
        return;
    }

    try {
        await equipeService.addTeam(teamname, idcaserne);
        console.log('Équipe ajoutée avec succès.');
        // Reset form only after successful addition
        $('#addteam').trigger("reset");

        // Load only the newly added team instead of all teams
        const newTeam = await equipeService.getTeams().then(teams => teams.pop());
        displayteam(newTeam, []);

    } catch (error) {
        console.error('Erreur lors de l\'ajout de l\'équipe :', error);
        alert("Une erreur est survenue lors de l'ajout de l'équipe");
    }
}


async function addpersontoteam(equipeService) {
    var idteam = $('#idTeamPerson').val();
    var employnb = $('#employeenumber').val();

    if (idteam == "" || employnb == "") {
        alert("Veuillez remplir tous les champs");
        return;
    }

    // Utilisez le sélecteur d'id pour réinitialiser le formulaire complet
    $('#addPersonTeam').trigger("reset");

    try {
        await equipeService.addPersonToTeam(idteam, employnb);
        console.log('Personne ajoutée avec succès.');

        // Ajouter une vérification avant de charger l'équipe à nouveau
        const teamElement = $(`.team-${idteam}`);
        if (!teamElement.length) {
            await loadteam(equipeService);
        }
    } catch (error) {
        console.error('Erreur lors de l\'ajout de l\'équipe :', error);
        alert("Une erreur est survenue lors de l'ajout de l'équipe");
    }
}