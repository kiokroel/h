from sqlalchemy import (
    Column,
    Integer,
    TIMESTAMP,
)

from core.database.db_helper import Base


from sqlalchemy import ForeignKey


class BookingHistory(Base):
    __tablename__ = "booking_history"

    id = Column(Integer, primary_key=True)
    spot_id = Column(Integer, ForeignKey("parking_spots.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    start_time = Column(TIMESTAMP, nullable=False)
    end_time = Column(TIMESTAMP, nullable=False)
