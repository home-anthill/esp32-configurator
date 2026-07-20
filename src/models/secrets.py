from typing import Literal

from pydantic import BaseModel, Field, SecretStr


class Secrets(BaseModel):
    # Required fields
    wifi_ssid: str
    wifi_password: SecretStr
    api_token: SecretStr
    server_domain: str
    mqtt_domain: str
    mqtt_username: str
    mqtt_password: SecretStr

    # Optional fields with defaults
    manufacturer: str = 'ks89'
    ssl: bool = True
    server_port: int = 443
    server_path: str = '/admission/register'
    mqtt_port: int = 8883
    mqtt_auth: bool = True

    oled_display: bool = False
    display_button_enabled: bool = True

    # Thermostat-only fields
    operating_mode: Literal[0, 1] = 0
    hot_active_low: bool = False
    cold_active_low: bool = False
    fan_active_low: bool = False
    pump_active_low: bool = False
    thermocouple_type: str = 'K'
    fan_turn_off_delay_seconds: int = Field(default=0, ge=0)
    cooling_short_rise_check_seconds: int = Field(default=120, ge=0)
    cooling_wide_rise_check_seconds: int = Field(default=600, ge=0)
