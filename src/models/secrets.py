from pydantic import BaseModel, SecretStr

from src.models.device_identity import Manufacturer


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
    manufacturer: Manufacturer = 'ks89'
    ssl: bool = True
    server_port: int = 443
    server_path: str = '/admission/register'
    mqtt_port: int = 8883
    mqtt_auth: bool = True
