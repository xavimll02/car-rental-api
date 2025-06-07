import pytest
from datetime import date, timedelta
from app.dtos.booking_dto import BookingDTO
from app.dtos.car_dto import CarDTO
from app.exceptions.booking_exceptions import BookingConflictError
from app.exceptions.car_exceptions import CarNotFoundError
from app.services.booking_service import BookingService
from app.services.car_service import CarService

def test_create_booking(booking_service: BookingService, car_service: CarService, 
                        sample_car_data: CarDTO, sample_booking_data: BookingDTO):
    # First add a car
    car = car_service.add_car(sample_car_data)
    
    # Update booking data with the new car id
    new_booking_data = BookingDTO(
        car_id=car.id,
        customer_name=sample_booking_data.customer_name,
        customer_email=sample_booking_data.customer_email,
        start_date=sample_booking_data.start_date,
        end_date=sample_booking_data.end_date
    )
    
    # Create booking
    booking = booking_service.create_booking(new_booking_data)
    
    assert booking.car_id == car.id
    assert booking.customer_name == new_booking_data.customer_name
    assert booking.start_date == new_booking_data.start_date
    assert booking.end_date == new_booking_data.end_date
    assert booking.id is not None

def test_create_booking_car_not_found(booking_service: BookingService, sample_booking_data: BookingDTO):
    with pytest.raises(CarNotFoundError):
        booking_service.create_booking(sample_booking_data)

def test_create_booking_conflict(booking_service: BookingService, car_service: CarService, 
                                 sample_car_data: CarDTO, sample_booking_data: BookingDTO):
    # First add a car
    car = car_service.add_car(sample_car_data)
    
    # Update booking data with the new car id
    new_booking_data = BookingDTO(
        car_id=car.id,
        customer_name=sample_booking_data.customer_name,
        customer_email=sample_booking_data.customer_email,
        start_date=sample_booking_data.start_date,
        end_date=sample_booking_data.end_date
    )
    
    # Create first booking
    booking_service.create_booking(new_booking_data)
    
    # Try to create second booking for same dates
    with pytest.raises(BookingConflictError):
        booking_service.create_booking(new_booking_data)

def test_create_booking_different_dates(booking_service: BookingService, car_service: CarService, 
                                        sample_car_data: CarDTO, sample_booking_data: BookingDTO):
    # First add a car
    car = car_service.add_car(sample_car_data)
    
    # Update booking data with the new car id
    new_booking_data = BookingDTO(
        car_id=car.id,
        customer_name=sample_booking_data.customer_name,
        customer_email=sample_booking_data.customer_email,
        start_date=sample_booking_data.start_date,
        end_date=sample_booking_data.end_date
    )
    
    # Create first booking
    booking_service.create_booking(new_booking_data)
    
    # Create second booking for different dates
    future_date = date.today() + timedelta(days=10)
    future_booking_data = BookingDTO(
        car_id=car.id,
        customer_name=sample_booking_data.customer_name,
        customer_email=sample_booking_data.customer_email,
        start_date=future_date,
        end_date=future_date + timedelta(days=2)
    )
    
    booking = booking_service.create_booking(future_booking_data)
    
    assert booking.id is not None
    assert booking.start_date == future_booking_data.start_date 