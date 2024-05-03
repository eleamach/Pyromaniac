package fr.cpe.emergencymanager.Repository;


import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.type.CollectionType;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import fr.cpe.emergencymanager.Entities.ManageObjects;
import fr.cpe.emergencymanager.Client.ApiClient;
import org.apache.http.HttpResponse;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.UnsupportedEncodingException;
import java.net.URLEncoder;
import java.util.ArrayList;
import java.util.Collection;
import java.util.List;
import java.util.Optional;

public abstract class Repository<T extends ManageObjects> {
    protected ApiClient API = new ApiClient();
    protected ObjectMapper mapper;
    private Class type;
    private String endpoint;
    private final Logger log = LoggerFactory.getLogger(Repository.class);

    public Repository() {
        mapper = new ObjectMapper();
        mapper.registerModule(new JavaTimeModule());
    }

    protected void setType(Class type) {
        this.type = type;
    }
    protected Class getType() {
        return type;
    }
    protected void setEndpoint(String endpoint) {
        this.endpoint = endpoint;
    }
    protected String getEndpoint() {
        return endpoint;
    }

    public Optional<T> findOneById(Long id) {
        try {
            HttpResponse response = API.getOneById(endpoint, id);
            return httpResponseIsOkay(response) ? Optional.of(httpToObject(response, type)) : Optional.empty();
        } catch (IOException e) {
            errorOnExecution(e);
            return Optional.empty();
        }
    }

    public T findById(Long id) {
        try {
            HttpResponse response = API.getOneById(endpoint, id);
            return httpResponseIsOkay(response) ? httpToObject(response, type) : null;
        } catch (IOException e) {
            errorOnExecution(e);
            return null;
        }
    }

    public List<T> findAll() {
        List<T> retour = new ArrayList<T>();
        try {
            HttpResponse response = API.get(endpoint);
            return httpResponseIsOkay(response) ? (List<T>) httpToObject(response, mapper.getTypeFactory().constructCollectionType(List.class, type)) : retour;
        } catch (IOException e) {
            errorOnExecution(e);
            return retour;
        }
    }

    public boolean delete(T object) {
        try {
            HttpResponse response = null;
            if(object.getIdentify() instanceof String) {
                response = API.delete(endpoint, (String)object.getIdentify());
            } else if(object.getIdentify() instanceof Long) {
                response = API.delete(endpoint, (Long)object.getIdentify());
            }
            return httpResponseIsOkay(response);
        } catch (IOException e) {
            errorOnExecution(e);
            return false;
        }
    }

    public T create(T object) {
        try {
            HttpResponse response = API.post(endpoint, object);
            return httpResponseIsOkay(response) ? httpToObject(response, type) : null;
        } catch (IOException e) {
            errorOnExecution(e);
        }
        return null;
    }

    public boolean update(T object) {
        try {
            HttpResponse response = API.patch(endpoint, object);
            return httpResponseIsOkay(response);
        } catch (IOException e) {
            errorOnExecution(e);
        }
        return false;
    }

    protected T httpToObject(HttpResponse response, Class classe) throws IOException {
        BufferedReader reader = new BufferedReader(new InputStreamReader(response.getEntity().getContent()));
        String line;
        StringBuilder result = new StringBuilder();
        while ((line = reader.readLine()) != null) {
            result.append(line);
        }
        return (T) mapper.readValue(result.toString(), classe);
    }
    protected Collection<T> httpToObject(HttpResponse response, CollectionType collectionType) throws IOException {
        BufferedReader reader = new BufferedReader(new InputStreamReader(response.getEntity().getContent()));
        String line;
        StringBuilder result = new StringBuilder();
        while ((line = reader.readLine()) != null) {
            result.append(line);
        }
        return (Collection<T>) mapper.readValue(result.toString(), collectionType);
    }

    protected String endpointEncoder(String endpoint) throws UnsupportedEncodingException {
        String encodedUrl = URLEncoder.encode(endpoint, "UTF-8");
        return encodedUrl.replace("+", "%20");
    }

    protected boolean httpResponseIsOkay(HttpResponse httpResponse) {
        if(httpResponse.getStatusLine().getStatusCode() != 200) {
            if(httpResponse.getStatusLine().getStatusCode() != 404) {
                log.error("Echec lors de l'exécution d'une requête HTTP (code HTTP != 200)");
                log.error(" de type : " + type.getName());
                log.error(" avec le code HTTP : " + httpResponse.getStatusLine().getStatusCode());
                log.error(" détail : " + httpResponse.getStatusLine().getReasonPhrase());
            }
            return false;
        }
        return true;
    }

    protected void errorOnExecution(Exception e) {
        log.error("Echec de l'exécution de la requête HTTP (errorOnExecution)");
        log.error("  de type : " + type.getName());
        log.error("  avec l'exception : " + e);
    }
}