from pydantic import BaseModel,Field

class CookiePayload(BaseModel):
    employee_id: int = Field(gt=0)
    employee_name: str = Field(min_length=2)
    age: int = Field(gt=0, lt=120)
