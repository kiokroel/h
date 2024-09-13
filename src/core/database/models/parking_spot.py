from sqlalchemy import Column, Integer

from core.database.db_helper import Base


class ParkingSpot(Base):
    __tablename__ = "parking_spots"

    id = Column(Integer, primary_key=True)
    floor = Column(Integer, nullable=True)
