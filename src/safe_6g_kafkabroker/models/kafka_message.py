from pydantic import BaseModel, Field
from enum import Enum

class FunctionType(str, Enum):
    SAFETY = "SAFETY"
    SECURITY = "SECURITY"
    PRIVACY = "PRIVACY"
    RELIABILITY = "RELIABILITY"
    RESILIENCE = "RESILIENCE"


class KafkaMessage(BaseModel):
    cLoTW: float = Field(..., description="Confidence Level of Trustworthiness")
    function: FunctionType = Field(..., description="Function topic category")
    targetApplicationIP: str = Field(..., description="Target application IP address")
    IMSI: str = Field(..., description="International Mobile Subscriber Identity")
    MSISDN: str = Field(..., description="Mobile Station International Subscriber Directory Number")
    IMEI: str = Field(..., description="International Mobile Equipment Identity")
