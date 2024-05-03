package fr.cpe.emergencymanager.Config;

public class ApiConfig {
    private String url;
    private String username;
    private String password;
    private String urlToken;

    public ApiConfig(String url, String username, String password, String urlToken) {
        this.url = url;
        this.username = username;
        this.password = password;
        this.urlToken = urlToken;
    }

    public String getUrl() {
        return url;
    }

    public String getUrlToken() {
        return urlToken;
    }

    public String getUsername() {
        return username;
    }

    public String getPassword() {
        return password;
    }

    @Override
    public String toString() {
        StringBuilder maskedPassword = new StringBuilder();
        for (int i = 0; i < password.length(); i++) {
            maskedPassword.append('*');
        }
        return "ApiConfig{" +
                "url='" + url + '\'' +
                ", urlToken='" + urlToken + '\'' +
                ", username='" + username + '\'' +
                ", password='" + (maskedPassword.toString()) + '\'' +
                '}';
    }
}