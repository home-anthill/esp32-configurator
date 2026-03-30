// Local WiFi credentials
#define SECRET_SSID "{{ secrets.wifi_ssid }}"
#define SECRET_PASS "{{ secrets.wifi_password.get_secret_value() }}"

#define MANUFACTURER "{{ secrets.manufacturer }}"
#define MODEL "{{ model_name }}"
#define API_TOKEN "{{ secrets.api_token.get_secret_value() }}"

// enable both HTTPS and MQTTS
// you should change PORTS accordingly
// https port: 443
// mqtts port: 8883
#define SSL {{ 'true' if secrets.ssl else 'false' }}

// HTTP server
#define SERVER_DOMAIN "{{ secrets.server_domain }}"
#define SERVER_PORT {{ secrets.server_port }}
#define SERVER_PATH "{{ secrets.server_path }}"
// MQTT server
#define MQTT_URL "{{ secrets.mqtt_domain }}"
#define MQTT_PORT {{ secrets.mqtt_port }}
#define MQTT_AUTH {{ 'true' if secrets.mqtt_auth else 'false' }}
#define MQTT_USERNAME "{{ secrets.mqtt_username }}"
#define MQTT_PASSWORD "{{ secrets.mqtt_password.get_secret_value() }}"
