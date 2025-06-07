from datetime import date

from app.dtos.car_dto import CarDTO
from app.services.car_service import CarService

def test_add_car(car_service: CarService, sample_car_data: CarDTO):
    car = car_service.add_car(sample_car_data)
    
    assert car.brand == sample_car_data.brand
    assert car.model == sample_car_data.model
    assert car.year == sample_car_data.year
    assert car.daily_rate == sample_car_data.daily_rate
    assert car.id is not None

def test_get_available_cars_empty(car_service: CarService):
    available_cars = car_service.get_available_cars(date.today())
    assert len(available_cars) == 0

def test_get_available_cars_with_data(car_service: CarService, sample_car_data: CarDTO):
    # Add a car first
    car = car_service.add_car(sample_car_data)
    
    # Check availability
    available_cars = car_service.get_available_cars(date.today())
    assert len(available_cars) == 1
    assert available_cars[0].id == car.id