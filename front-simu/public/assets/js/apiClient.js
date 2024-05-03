import { getHeader } from "./cookies.js";

// Classe pour gérer les requêtes API
export class ApiClient 
{
    constructor(baseUrl) 
    {
        this.baseUrl = baseUrl;
    }

    async makeRequest(url, method, data, isToken = false) 
    {
        try 
        {
            var response = null;
            if(isToken) 
            {
                var headers = 
                {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'accept': 'application/json',
                }
            } 
            else 
            {
                var headers = 
                {
                    'Content-Type': 'application/json',
                    'accept': 'application/json',
                }
            }

            const token = getHeader();
            if(token != null) 
            {
                headers["Authorization"] = token;
            }
            if(isToken) 
            {
                response = await fetch(this.baseUrl + url, {
                    method: method,
                    headers: headers,
                    body: data
                });
            }

            if(response == null) 
            {
                if(method == 'GET' || method == 'DELETE') 
                {
                    response = await fetch(this.baseUrl + url, 
                        {
                        method: method,
                        headers: headers,
                    });
                } 
                else 
                {
                    response = await fetch(this.baseUrl + url, 
                        {
                        method: method,
                        headers: headers,
                        body: JSON.stringify(data),
                    });
                }
            }

            if(isToken) 
            {
                return response;
            }
            return response.json();
        } catch (error) 
        {
            console.error('Erreur lors de la requête API :', error);
            throw error;
        }
    }
}