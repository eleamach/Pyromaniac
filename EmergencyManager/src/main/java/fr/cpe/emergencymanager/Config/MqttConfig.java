 package fr.cpe.emergencymanager.Config;

public class MqttConfig {
    private String broker;
    private String clientId;
    private String username;
    private String password;

    public MqttConfig(String broker, String clientId, String username, String password) {
        this.broker = broker;
        this.clientId = clientId;
        this.username = username;
        this.password = password;
    }

    public String getBroker() {
        return broker;
    }

    public String getClientId() {
        return clientId;
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
        return "MqttConfig{" +
                "broker='" + broker + '\'' +
                ", clientId='" + clientId + '\'' +
                ", username='" + username + '\'' +
                ", password='" + (maskedPassword.toString()) + '\'' +
                '}';
    }
}