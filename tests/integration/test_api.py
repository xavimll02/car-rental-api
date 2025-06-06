from datetime import date
from fastapi import status
from fastapi.testclient import TestClient

from app.dtos.booking_dto import BookingDTO
from app.dtos.car_dto import CarDTO

def test_add_car(test_client: TestClient, sample_car_data: CarDTO):
    response = test_client.post("/cars", json=sample_car_data.model_dump())
    assert response.status_code == status.HTTP_200_OK
    
    car = response.json()
    assert car["brand"] == sample_car_data.brand
    assert car["model"] == sample_car_data.model
    assert car["year"] == sample_car_data.year
    assert car["daily_rate"] == sample_car_data.daily_rate
    assert "id" in car

def test_get_available_cars_empty(test_client: TestClient):
    today = date.today().isoformat()
    response = test_client.get(f"/cars?date={today}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == []

def test_get_available_cars_with_data(test_client: TestClient, sample_car_data: CarDTO):
    # First add a car
    car_response = test_client.post("/cars", json=sample_car_data.model_dump())
    assert car_response.status_code == status.HTTP_200_OK
    
    # Check availability
    today = date.today().isoformat()
    response = test_client.get(f"/cars?date={today}")
    assert response.status_code == status.HTTP_200_OK
    
    cars = response.json()
    assert len(cars) == 1
    assert cars[0]["brand"] == sample_car_data.brand

def test_create_booking(test_client: TestClient, sample_car_data: CarDTO, sample_booking_data: BookingDTO):
    # First add a car
    car_response = test_client.post("/cars", json=sample_car_data.model_dump())
    assert car_response.status_code == status.HTTP_200_OK
    car = car_response.json()
    
    # Update booking with created car id
    booking_data = sample_booking_data.model_dump()
    booking_data["car_id"] = car["id"]
    booking_data["start_date"] = booking_data["start_date"].isoformat()
    booking_data["end_date"] = booking_data["end_date"].isoformat()
    
    response = test_client.post("/bookings", json=booking_data)
    assert response.status_code == status.HTTP_200_OK
    
    booking = response.json()
    assert booking["car_id"] == booking_data["car_id"]
    assert booking["customer_name"] == booking_data["customer_name"]
    assert booking["customer_email"] == booking_data["customer_email"]
    assert booking["start_date"] == booking_data["start_date"]
    assert booking["end_date"] == booking_data["end_date"]
    assert "id" in booking

def test_create_booking_car_not_found(test_client: TestClient, sample_booking_data: BookingDTO):
    booking_data = sample_booking_data.model_dump()
    booking_data["start_date"] = booking_data["start_date"].isoformat()
    booking_data["end_date"] = booking_data["end_date"].isoformat()
    
    response = test_client.post("/bookings", json=booking_data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_create_booking_conflict(test_client: TestClient, sample_car_data: CarDTO, sample_booking_data: BookingDTO):
    # First add a car
    car_response = test_client.post("/cars", json=sample_car_data.model_dump())
    assert car_response.status_code == status.HTTP_200_OK
    car = car_response.json()
    
    # Update booking with created car id
    booking_data = sample_booking_data.model_dump()
    booking_data["car_id"] = car["id"]
    booking_data["start_date"] = booking_data["start_date"].isoformat()
    booking_data["end_date"] = booking_data["end_date"].isoformat()
    
    response1 = test_client.post("/bookings", json=booking_data)
    assert response1.status_code == status.HTTP_200_OK
    
    # Try to create second booking for same dates
    response2 = test_client.post("/bookings", json=booking_data)
    assert response2.status_code == status.HTTP_400_BAD_REQUEST

def test_get_available_cars_invalid_date(test_client: TestClient):
    response = test_client.get("/cars?date=invalid-date")
    assert response.status_code == status.HTTP_400_BAD_REQUEST 