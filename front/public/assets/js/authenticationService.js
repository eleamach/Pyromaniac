import { getCookie, createCookie } from './cookies.js';

// Classe pour gérer les opérations liées au personnel
export class AuthenticationService 
{
    user;
    apiService;
    
    constructor(apiService) 
    {
        this.apiService = apiService;
    }

    async isConnected() 
    {
        try 
        {
            const tokenType = getCookie("tokenType");
            const tokenValue = getCookie("tokenValue");
            const urlLogin = "/login.html";
            if((tokenType == null || tokenValue == null) && !window.location.href.endsWith(urlLogin)) 
            {
                window.location.href = "../" + urlLogin;
                return false;
            }
            let resp = await this.apiService.makeRequest('/api/v1/employees/me/', 'GET', null, true); //TODO
            if(resp.status != 200) 
            {
                return false;
            }
            return resp.status == 200;
        } 
        catch (error) 
        {
            // Gérer les erreurs
            console.error('Erreur lors de la récupération des données du personnel :', error);
            alert("Problème de connexion au serveur");
        }
    }

    async logIn(formData) 
    {
        try 
        {
            const data = new URLSearchParams();
            data.append('username', formData["username"]);
            data.append('password', formData["password"]);
            let resp = await this.apiService.makeRequest('/token', 'POST', data, true);
            if(resp.status != 200) 
            {
                alert("Identifiant / Mot de passe invalide");
                return false;
            }
            let r = await resp.json();
            createCookie("tokenValue", r.access_token);
            createCookie("tokenType", r.token_type);
            window.location.href = "./Gestion/gestionPersonnel.html";
        } 
        catch (error) 
        {
            // Gérer les erreurs
            console.error('Erreur lors de la récupération des données du personnel :', error);
            alert("Problème de connexion au serveur");
        }
    }
}