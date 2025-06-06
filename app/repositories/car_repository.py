from pathlib import Path
import json
from typing import Optional
from app.models.car import Car

DATA_DIR = Path("data")
CARS_FILE_PATH = DATA_DIR / "cars.json"

class CarRepository:
    def __init__(self):
        self.cars_file = CARS_FILE_PATH
        self._initialize_storage()

    def _initialize_storage(self):
        self.cars_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.cars_file.exists():
            self._save_cars([])

    def _load_cars(self) -> list[Car]:
        with open(self.cars_file, 'r') as f:
            return json.load(f)

    def _save_cars(self, cars: list[Car]):
        with open(self.cars_file, 'w') as f:
            json.dump(cars, f, indent=2)

    def get_all_cars(self) -> list[Car]:
        cars_data = self._load_cars()
        return [Car(**car) for car in cars_data]

    def get_car_by_id(self, car_id: str) -> Optional[Car]:
        cars = self.get_all_cars()
        for car in cars:
            if car.id == car_id:
                return car
        return None

    def add_car(self, car: Car) -> Car:
        cars = self._load_cars()
        car_dict = car.model_dump()
        cars.append(car_dict)
        self._save_cars(cars)
        return car