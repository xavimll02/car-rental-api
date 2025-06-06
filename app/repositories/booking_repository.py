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
            return json.load(f)

    def _save_bookings(self, bookings: list[Booking]):
        with open(self.bookings_file, 'w') as f:
            json.dump(bookings, f, indent=2)

    def create_booking(self, booking: Booking) -> Booking:
        bookings = self._load_bookings()
        booking_dict = booking.model_dump()
        booking_dict['start_date'] = booking.start_date.isoformat()
        booking_dict['end_date'] = booking.end_date.isoformat()
        bookings.append(booking_dict)
        self._save_bookings(bookings)
        return booking

    def get_bookings_by_date_range(self, start_date: date, end_date: date) -> list[Booking]:
        bookings = self._load_bookings()
        filtered_bookings = []
        
        for booking in bookings:
            booking_start = date.fromisoformat(booking['start_date'])
            booking_end = date.fromisoformat(booking['end_date'])
            
            if (booking_start <= end_date and booking_end >= start_date):
                filtered_bookings.append(Booking(**booking))
        
        return filtered_bookings