/*
 * Copyright (c) 2023.
 * Autheur : Adrien JAUFRE
 */

package fr.cpe.emergencymanager.Client;

import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.databind.ObjectMapper;
import fr.cpe.emergencymanager.Config.ConfigLoader;
import org.apache.http.HttpResponse;
import org.apache.http.NameValuePair;
import org.apache.http.auth.AuthenticationException;
import org.apache.http.client.HttpClient;
import org.apache.http.client.entity.UrlEncodedFormEntity;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.impl.client.HttpClientBuilder;
import org.apache.http.message.BasicNameValuePair;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

public class ApiToken {
    private Logger log = LoggerFactory.getLogger(ApiToken.class);
    private HttpClient httpClient;
    private ObjectMapper objectMapper;
    private static ApiToken TOKEN = null;

    private String token;

    private String tokenType;

    private ApiToken() {
        this.httpClient = HttpClientBuilder.create().build();
        this.objectMapper = new ObjectMapper();
    }

    @JsonCreator
    public ApiToken(@JsonProperty("access_token") String token, @JsonProperty("token_type") String tokenType) {
        this.token = token;
        this.tokenType = tokenType;
    }

    @JsonIgnore
    public String getHeader(){
        return TOKEN.tokenType + " " + TOKEN.token;
    }

    @JsonIgnore
    protected static String getHeaderToken() {
        if(ConfigLoader.getConfig().getApiConfig().getUsername().isEmpty()) {
            return null;
        }
        if(TOKEN == null) {
            TOKEN = new ApiToken().token();
        }
        return TOKEN.getHeader();
    }

    private ApiToken token() {
        if(!ConfigLoader.getConfig().getApiConfig().getUsername().isEmpty() && ApiToken.TOKEN == null) {
            log.debug("Authentification auprès de l'API en cours...");
            List<NameValuePair> pairs = new ArrayList<NameValuePair>();
            pairs.add(new BasicNameValuePair("grant_type", ""));
            pairs.add(new BasicNameValuePair("username", ConfigLoader.getConfig().getApiConfig().getUsername()));
            pairs.add(new BasicNameValuePair("password", ConfigLoader.getConfig().getApiConfig().getPassword()));
            pairs.add(new BasicNameValuePair("scope", ""));
            pairs.add(new BasicNameValuePair("client_id", ""));
            pairs.add(new BasicNameValuePair("client_secret", ""));
            try {
                HttpPost request = new HttpPost(ConfigLoader.getConfig().getApiConfig().getUrlToken());
                request.setEntity(new UrlEncodedFormEntity(pairs));
                request.addHeader("accept", "application/json");
                request.addHeader("Content-Type", "application/x-www-form-urlencoded");

                HttpResponse httpResponse = httpClient.execute(request);
                if(httpResponse.getStatusLine().getStatusCode() != 200) {
                    log.error("Echec d'authentification auprès de l'API");
                    log.warn("Veuillez vérifier les identifiants saisis dans le fichier de configuration !");
                    throw new AuthenticationException("Authentication failure");
                }

                BufferedReader reader = new BufferedReader(new InputStreamReader(httpResponse.getEntity().getContent()));
                String line;
                StringBuilder result = new StringBuilder();
                while ((line = reader.readLine()) != null) {
                    result.append(line);
                }
                return objectMapper.readValue(result.toString(), ApiToken.class);
            } catch (IOException e) {
                throw new RuntimeException(e);
            } catch (AuthenticationException e) {
                throw new RuntimeException(e);
            }
        }
        return null;
    }
}