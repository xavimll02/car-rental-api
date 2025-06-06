import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.services.car_service import CarService
from app.services.booking_service import BookingService
from app.dtos.car_dto import CarDTO
from app.dtos.booking_dto import BookingDTO
import datetime
import json
import os
import shutil
from pathlib import Path

# Define test data directory
TEST_DATA_DIR = Path("test_data")

@pytest.fixture(autouse=True)
def setup_test_environment(monkeypatch):
    # Setup: create test data directory
    TEST_DATA_DIR.mkdir(parents=True, exist_ok=True)
    test_cars_path = TEST_DATA_DIR / "cars.json"
    test_bookings_path = TEST_DATA_DIR / "bookings.json"
    
    # Create empty JSON files for tests
    with open(test_cars_path, "w") as f:
        json.dump([], f)
    with open(test_bookings_path, "w") as f:
        json.dump([], f)
    
    # Patch the file paths in repositories
    monkeypatch.setattr('app.repositories.car_repository.CARS_FILE_PATH', test_cars_path)
    monkeypatch.setattr('app.repositories.booking_repository.BOOKINGS_FILE_PATH', test_bookings_path)
    
    yield
    
    # Cleanup: remove test data directory after tests
    if TEST_DATA_DIR.exists():
        shutil.rmtree(TEST_DATA_DIR)

@pytest.fixture
def test_client():
    return TestClient(app)

@pytest.fixture
def car_service():
    return CarService()

@pytest.fixture
def booking_service():
    return BookingService()

@pytest.fixture
def sample_car_data() -> CarDTO:
    return CarDTO(
        brand="Toyota",
        model="Camry",
        year=2022,
        daily_rate=50.0
    )

@pytest.fixture
def sample_booking_data() -> BookingDTO:
    today = datetime.date.today()
    return BookingDTO(
        car_id="1",
        customer_name="John Doe",
        customer_email="johndoe@gmail.com",
        start_date=today,
        end_date=today + datetime.timedelta(days=2)
    ) 