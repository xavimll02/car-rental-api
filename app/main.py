from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.car_router import router as car_router
from app.routers.booking_router import router as booking_router
import logging
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('app.log')
    ]
)

app = FastAPI(
    title="Car Rental API",
    description="A REST API for a car rental service"
)

# Include routers
app.include_router(car_router)
app.include_router(booking_router)

@app.get("/health")
async def health():
    return {"status": "ok"}