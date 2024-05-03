package fr.cpe.emergencymanager.Client;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import fr.cpe.emergencymanager.Config.ConfigLoader;
import fr.cpe.emergencymanager.Entities.ManageObjects;
import org.apache.http.HttpRequest;
import org.apache.http.HttpResponse;
import org.apache.http.client.methods.*;
import org.apache.http.entity.StringEntity;
import org.apache.http.impl.client.CloseableHttpClient;
import org.apache.http.impl.client.HttpClients;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;


/**
 * Classe ApiClient
 * Classe permettant d'effectuer les requêtes vers l'API
 */
public class ApiClient {
    public static final String RADICALURL = ConfigLoader.getConfig().getApiConfig().getUrl();

    private final ObjectMapper objectMapper;
    private final Logger log = LoggerFactory.getLogger(ApiClient.class);

    public ApiClient() {
        objectMapper = new ObjectMapper();
        objectMapper.registerModule(new JavaTimeModule());
    }

    public HttpResponse getOneById(String endpoint, Long id) throws IOException {
        String url = RADICALURL + endpoint + "/" + id.toString();
        return httpGet(url);
    }
    public HttpResponse getOneById(String endpoint, String id) throws IOException {
        String url = RADICALURL + endpoint + "/" + id;
        return httpGet(url);
    }
    public HttpResponse get(String endpoint) throws IOException {
        String url = RADICALURL + endpoint;
        return httpGet(url);
    }

    public <T extends ManageObjects> HttpResponse post(String endpoint, T requestBody) throws IOException {
        String url = RADICALURL + endpoint;
        HttpPost request = new HttpPost(url);
        String jsonBody = objectMapper.writeValueAsString(requestBody);
        request.setEntity(new StringEntity(jsonBody));
        return httpPost(request);
    }

    public <T extends ManageObjects> HttpResponse patch(String endpoint, T requestBody) throws IOException {
        if(requestBody.getIdentify() == null) {
            throw new IOException("L'objet à modifier n'a pas d'id");
        }
        String url = RADICALURL + endpoint + '/' + requestBody.getIdentify();
        HttpPatch request = new HttpPatch(url);
        String jsonBody = objectMapper.writeValueAsString(requestBody);
        request.setEntity(new StringEntity(jsonBody));
        return httpPatch(request);
    }

    public HttpResponse delete(String endpoint, Long id) throws IOException {
        String url = RADICALURL + endpoint + "/" + id;
        return httpDelete(url);
    }
    public HttpResponse delete(String endpoint, String id) throws IOException {
        String url = RADICALURL + endpoint + "/" + id;
        return httpDelete(url);
    }

    public HttpResponse httpGet(String url) throws IOException {
        try(CloseableHttpClient httpClient = HttpClients.createDefault()) {
            log.debug("Lancement d'un GET sur l'adresse " + url);
            HttpGet request = new HttpGet(url);
            request = addHeaders(request);
            HttpResponse httpResponse = httpClient.execute(request);
            httpClient.close();
            return httpResponse;
        }
    }

    private HttpResponse httpDelete(String url) throws IOException {
        try(CloseableHttpClient httpClient = HttpClients.createDefault()) {
            log.debug("Lancement d'un DELETE sur l'adresse " + url);
            HttpDelete request = new HttpDelete(url);
            request = addHeaders(request);
            HttpResponse httpResponse = httpClient.execute(request);
            httpClient.close();
            return httpResponse;
        }
    }

    private HttpResponse httpPost(HttpPost request) throws IOException {
        try(CloseableHttpClient httpClient = HttpClients.createDefault()) {
            log.debug("Lancement d'une requête POST sur l'adresse " + request.getURI().toString());
            request = addHeaders(request);
            HttpResponse httpResponse = httpClient.execute(request);
            httpClient.close();
            return httpResponse;
        }
    }

    private HttpResponse httpPatch(HttpPatch request) throws IOException {
        try(CloseableHttpClient httpClient = HttpClients.createDefault()) {
            log.debug("Lancement d'une requête PATCH sur l'adresse " + request.getURI().toString());
            request = addHeaders(request);
            HttpResponse httpResponse = httpClient.execute(request);
            httpClient.close();
            return httpResponse;
        }
    }

    private <T extends HttpRequest> T addHeaders(T httpRequest) {
        httpRequest.addHeader("accept", "application/json");
        httpRequest.addHeader("Content-Type", "application/json");
        if(!ConfigLoader.getConfig().getApiConfig().getUsername().isEmpty()) httpRequest.addHeader("Authorization", ApiToken.getHeaderToken());
        return httpRequest;
    }
}