from datetime import date

from app.exceptions.base_exceptions import AppException


class BookingConflictError(AppException):
    def __init__(self, car_id: int):
        super().__init__(f"Car with ID {car_id} is already booked during the date range provided.")