from pydantic import BaseModel, Field

class FunctionResponse(BaseModel):
    cLotw: float = Field(..., description="Achieved Confidence Level of Trustworthiness")
    actions: list[str] = Field(..., description="List of actions to be taken")