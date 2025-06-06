from pydantic import BaseModel
from typing import Optional

class Car(BaseModel):
    id: str
    model: str
    brand: str
    year: int
    daily_rate: float
    description: Optional[str] = None