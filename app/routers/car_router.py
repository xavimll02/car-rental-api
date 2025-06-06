from fastapi import APIRouter, Query, Depends, HTTPException
from app.services.car_service import CarService
from app.dtos.car_dto import CarDTO
from app.models.car import Car
import logging
import datetime

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/cars", tags=["cars"])

def get_car_service() -> CarService:
    return CarService()

@router.post("/", response_model=Car)
def add_car(
    car: CarDTO,
    service: CarService = Depends(get_car_service)
) -> Car:
    logger.info(f"Received request to add car: {car.model} ({car.brand})")
    try:
        return service.add_car(car)
    except Exception as e:
        logger.error(f"Error creating car: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@router.get("/", response_model=list[Car])
def get_available_cars(
    date: str = Query(..., description="Date in YYYY-MM-DD format"),
    service: CarService = Depends(get_car_service)
) -> list[Car]:
    logger.info(f"Received request to list available cars for date: {date}")
    try:
        parsed_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
        return service.get_available_cars(parsed_date)
    except ValueError as e:
        logger.error(f"Invalid date parameter: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error getting available cars: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")