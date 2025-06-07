from pathlib import Path
import json
from datetime import date
from app.models.booking import Booking

DATA_DIR = Path("data")
BOOKINGS_FILE_PATH = DATA_DIR / "bookings.json"

class BookingRepository:
    def __init__(self):
        self.bookings_file = BOOKINGS_FILE_PATH
        self._initialize_storage()

    def _initialize_storage(self):
        self.bookings_file.parent.mkdir(parents=True, exist_ok=True)
        if not self.bookings_file.exists():
            self._save_bookings([])

    def _load_bookings(self) -> list[Booking]:
        with open(self.bookings_file, 'r') as f:
            bookings_data = json.load(f)
            return [Booking(**booking) for booking in bookings_data]

    def _save_bookings(self, bookings: list[Booking]):
        bookings_data = []
        for booking in bookings:
            booking_dict = booking.model_dump()
            booking_dict['start_date'] = booking_dict['start_date'].isoformat()
            booking_dict['end_date'] = booking_dict['end_date'].isoformat()
            bookings_data.append(booking_dict)
            
        with open(self.bookings_file, 'w') as f:
            json.dump(bookings_data, f, indent=2)

    def create_booking(self, booking: Booking) -> Booking:
        bookings = self._load_bookings()
        bookings.append(booking)
        self._save_bookings(bookings)
        return booking

    def get_bookings_by_date_range(self, start_date: date, end_date: date) -> list[Booking]:
        bookings = self._load_bookings()
        filtered_bookings = []
        
        for booking in bookings:
            if (booking.start_date <= end_date and booking.end_date >= start_date):
                filtered_bookings.append(booking)
        
        return filtered_bookings