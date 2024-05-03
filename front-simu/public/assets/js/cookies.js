export function getCookie(name) 
{
    // Récupère tous les cookies
    const cookies = document.cookie.split(';');
  
    // Cherche le cookie avec le nom spécifié
    for (let i = 0; i < cookies.length; i++) 
    {
      const cookie = cookies[i].trim();
      // Vérifie si le cookie commence par le nom recherché
      if (cookie.startsWith(name + '=')) 
      {
        // Retourne la valeur du cookie
        return cookie.substring(name.length + 1);
      }
    }
    // Si le cookie n'est pas trouvé, on retourne null
    return null;
}

export function getHeader() 
{
  const tokenType = getCookie("tokenType");
  const tokenValue = getCookie("tokenValue");
  if(tokenType == null || tokenValue == null) 
  {
    return null;
  }
  return tokenType + " " + tokenValue;
}

export function createCookie(name, value) 
{
  let cookie = `${encodeURIComponent(name)}=${encodeURIComponent(value)}`;

  // Définir la date d'expiration à 3 heures plus tard
  const expirationDate = new Date();
  expirationDate.setTime(expirationDate.getTime() + (3 * 60 * 60 * 1000)); // 3 heures en millisecondes
  cookie += `; expires=${expirationDate.toUTCString()}`;

  document.cookie = cookie;
}