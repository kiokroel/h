import datetime

from pydantic import BaseModel


class ParkingSpotBase(BaseModel):
    id: int
    floor: int | None = None

    class Config:
        from_attributes = True


class ParkingCreate(BaseModel):
    floor: int | None = None

    class Config:
        from_attributes = True


class TimeDelta(BaseModel):
    start_time: datetime.datetime
    end_time: datetime.datetime

    class Config:
        from_attributes = True


class ReserveParkingSpace(TimeDelta):
    user_id: int | None
    spot_id: int

    class Config:
        from_attributes = True


class ReserveParkingSpaceReturn(ReserveParkingSpace):
    id: int

    class Config:
        from_attributes = True


class CancelReserveParkingSpace(BaseModel):
    user_id: int
    spot_id: int

    class Config:
        from_attributes = True


class CancelReserveParkingSpaceReturn(CancelReserveParkingSpace, TimeDelta):

    class Config:
        from_attributes = True
