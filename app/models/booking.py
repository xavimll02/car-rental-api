from pydantic import BaseModel
from datetime import date

class Booking(BaseModel):
    id: str
    car_id: str
    start_date: date
    end_date: date
    customer_name: str
    customer_email: str
    total_price: float