// Local WiFi credentials
#define SECRET_SSID "{{ secrets.wifi_ssid }}"
#define SECRET_PASS "{{ secrets.wifi_password.get_secret_value() }}"

#define MANUFACTURER "{{ secrets.manufacturer }}"
#define MODEL "{{ model_name }}"
#define API_TOKEN "{{ secrets.api_token.get_secret_value() }}"

// enable both HTTPS and MQTTS you should change PORTS accordingly
// https port: 443 | mqtts port: 8883
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

// OLED display support. When false, OLED code is not compiled.
#define OLED_DISPLAY {{ 'true' if secrets.oled_display else 'false' }}
// Optional GPIO button for display power saving/restart controls.
// When false, the display stays on and the button pin is not configured.
#define DISPLAY_BUTTON_ENABLED {{ 'true' if secrets.display_button_enabled else 'false' }}

{% if model_name == 'thermostat' %}
// ------------------------------------ THERMOSTAT ONLY ------------------------------------
// Thermostat operating mode: 0 = cooling, 1 = heating.
#ifndef OPERATING_MODE
#define OPERATING_MODE {{ secrets.operating_mode }}
#endif

// Relay/output polarity. true = active LOW, false = active HIGH.
#define HOT_ACTIVE_LOW {{ 'true' if secrets.hot_active_low else 'false' }}
#define COLD_ACTIVE_LOW {{ 'true' if secrets.cold_active_low else 'false' }}
#define FAN_ACTIVE_LOW {{ 'true' if secrets.fan_active_low else 'false' }}
#define PUMP_ACTIVE_LOW {{ 'true' if secrets.pump_active_low else 'false' }}

// specific thermostat config
#define THERMOCOUPLE_TYPE "{{ secrets.thermocouple_type }}"

// Keep FAN physically on for this many seconds after thermostat logic turns it off.
#define FAN_TURN_OFF_DELAY_SECONDS {{ secrets.fan_turn_off_delay_seconds }}

// Cooling safety checks used only when OPERATING_MODE is 0. These checks do
// not require a specific cooling rate. They only stop COLD if temperature has
// risen since cooling started or during a later wide monitoring window.
#define COOLING_SHORT_RISE_CHECK_SECONDS {{ secrets.cooling_short_rise_check_seconds }}
#define COOLING_WIDE_RISE_CHECK_SECONDS {{ secrets.cooling_wide_rise_check_seconds }}
// ------------------------------------------------------------------------------------------
{% endif %}
