from pydantic import BaseModel
from typing import Optional

class CarDTO(BaseModel):
    brand: str
    model: str
    year: int
    daily_rate: float
    description: Optional[str] = None

