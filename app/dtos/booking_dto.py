from pydantic import BaseModel, model_validator
from datetime import date

class BookingDTO(BaseModel):
    car_id: str
    start_date: date
    end_date: date
    customer_name: str
    customer_email: str

    @model_validator(mode='after')
    def check_dates(self):
        if self.start_date > self.end_date:
            raise ValueError('start_date must be before or equal to end_date')
        return self