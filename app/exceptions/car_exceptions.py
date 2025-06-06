from app.exceptions.base_exceptions import AppException


class CarNotFoundError(AppException):
    def __init__(self, car_id: int):
        super().__init__(f"Car with ID {car_id} not found.")
