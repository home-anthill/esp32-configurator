from typing import Annotated

from pydantic import AfterValidator, BaseModel, Field


def printable_ascii(value: str) -> str:
    if not all(' ' <= char <= '~' for char in value):
        raise ValueError('must contain only printable ASCII characters')
    return value


ModelName = Annotated[str, Field(min_length=2, max_length=50), AfterValidator(printable_ascii)]
Manufacturer = Annotated[str, Field(min_length=3, max_length=50), AfterValidator(printable_ascii)]


class DeviceIdentity(BaseModel):
    model_name: ModelName
    manufacturer: Manufacturer
