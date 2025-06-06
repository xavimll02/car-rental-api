import uuid
from datetime import date
from app.repositories.car_repository import CarRepository
from app.repositories.booking_repository import BookingRepository
from app.models.car import Car
from app.models.booking import Booking
from app.dtos.car_dto import CarDTO
import logging

logger = logging.getLogger(__name__)

class CarService:
    def __init__(self):
        self.car_repo = CarRepository()
        self.booking_repo = BookingRepository()

    def get_available_cars(self, target_date: date) -> list[Car]:
        
        # Get all cars and bookings for the date
        all_cars = self.car_repo.get_all_cars()
        bookings = self.booking_repo.get_bookings_by_date_range(target_date, target_date)
        
        # Filter out booked cars
        booked_car_ids = {booking.car_id for booking in bookings}
        available_cars = [car for car in all_cars if car.id not in booked_car_ids]
        logger.info(f"{len(available_cars)} car/s available for date {target_date}")
        return available_cars

    def add_car(self, car_dto: CarDTO) -> Car:
        car = Car(
            id=str(uuid.uuid4()),
            brand=car_dto.brand,
            model=car_dto.model,
            year=car_dto.year,
            daily_rate=car_dto.daily_rate,
            description=car_dto.description
        )
        logger.info(f"Car successfully added to the system with id: {car.id}")
        return self.car_repo.add_car(car)