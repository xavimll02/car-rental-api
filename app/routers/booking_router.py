from fastapi import APIRouter, HTTPException, Depends
from app.exceptions.booking_exceptions import BookingConflictError
from app.exceptions.car_exceptions import CarNotFoundError
from app.models.booking import Booking
from app.services.booking_service import BookingService
from app.dtos.booking_dto import BookingDTO
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/bookings", tags=["bookings"])

def get_booking_service() -> BookingService:
    return BookingService()

@router.post("/", response_model=Booking)
async def create_booking(
    request: BookingDTO,
    service: BookingService = Depends(get_booking_service)
) -> Booking:
    logger.info(f"Received request to create booking for car_id: {request.car_id}, customer: {request.customer_name}")
    try:
        return service.create_booking(request)
    except (CarNotFoundError, BookingConflictError) as e:
        raise HTTPException(status_code=400, detail=e.message)
    except Exception as e:
        logger.error(f"Error creating booking: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")