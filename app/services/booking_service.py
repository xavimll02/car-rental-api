from app.exceptions.booking_exceptions import BookingConflictError
from app.exceptions.car_exceptions import CarNotFoundError
from app.repositories.booking_repository import BookingRepository
from app.repositories.car_repository import CarRepository
from app.models.booking import Booking
from app.dtos.booking_dto import BookingDTO
import logging
import uuid

logger = logging.getLogger(__name__)

class BookingService:
    def __init__(self):
        self.booking_repo = BookingRepository()
        self.car_repo = CarRepository()

    def create_booking(self, dto: BookingDTO) -> Booking:
        # Check car exists
        car = self.car_repo.get_car_by_id(dto.car_id)
        if not car:
            logger.error(f"Booking failed: Car ID {dto.car_id} does not exist")
            raise CarNotFoundError(dto.car_id)

        # Check availability
        bookings = self.booking_repo.get_bookings_by_date_range(dto.start_date, dto.end_date)
        if any(b.car_id == dto.car_id for b in bookings):
            logger.error(f"Booking failed: Car ID {dto.car_id} already booked for the selected dates")
            raise BookingConflictError(dto.car_id)

        # Calculate total price (number of days * daily rate)
        days = (dto.end_date - dto.start_date).days + 1
        total_price = car.daily_rate * days

        booking = Booking(
            id=str(uuid.uuid4()),
            car_id=dto.car_id,
            start_date=dto.start_date,
            end_date=dto.end_date,
            customer_name=dto.customer_name,
            customer_email=dto.customer_email,
            total_price=total_price
        )
        self.booking_repo.create_booking(booking)
        logger.info(f"Booking successful: {booking.model_dump()}")
        return booking