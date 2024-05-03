function loadCasernes(caserneService) 
{
    caserneService.getCasernes()
        .then((casernes) => 
        {
            // Afficher les données dans la page
            displayCasernes(casernes);
        })
        .catch((error) => 
        {
            console.error('Erreur lors de la récupération des données des casernes :', error);
            alert("Problème de connexion au serveur");
        });
}

function displayCasernes(casernes) 
{
    $('#sitesContainer').empty();
    for (var caserne of casernes) 
    {
        var siteElement = document.createElement('div');
        siteElement.classList.add('site');
        siteElement.classList.add('site-' + caserne.id_fire_station);
        siteElement.innerHTML = `<strong>${caserne.fire_station_name}</strong><br>Coordonnées : (${caserne.fire_station_longitude}, ${caserne.fire_station_latitude})`;
        $('#sitesContainer').append(siteElement);
    }
}

async function addCaserne(caserneService) 
{
    var siteName = $('#siteName').val();
    var siteX = $('#siteX').val();
    var siteY = $('#siteY').val();

    if(siteName == "" || siteX == "" || siteY == "")
    {
        alert("Veuillez remplir tous les champs");
        return;
    }
    $('#add-caserne').trigger("reset");
    await caserneService.addCaserne(siteName, siteX, siteY);
    loadCasernes(caserneService);
}