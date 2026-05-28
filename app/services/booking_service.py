

from app.repositories.booking_repository import BookingRepository

class BookingService:
    def __init__(self, db):
        self.repo = BookingRepository(db)