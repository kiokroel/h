from sqlalchemy import select, and_, delete

import core.schemas.parking_schema as schemas
from core.database.db_helper import db_helper
from core.database.models.booking_history import BookingHistory
from core.database.models.parking_spot import ParkingSpot


class SQLAlchemyParkingRepository:
    def __init__(self):
        self.__db_helper = db_helper

    async def get_free_parking_spaces(self, time_schema: schemas.TimeDelta) -> list[schemas.ParkingSpotBase]:
        db = await self.__db_helper.session_getter()
        stmt = select(ParkingSpot.id)
        result = await db.execute(stmt)
        ids = [parking_spaces_id for parking_spaces_id in result.scalars()]

        stmt = select(BookingHistory).select_from(BookingHistory)
        result = await db.execute(stmt)
        all_book_history = result.scalars().all()

        for history in all_book_history:
            if history.start_time <= time_schema.end_time and history.end_time >= time_schema.start_time:
                ids.remove(history.spot_id)

        return ids

    async def reservation_parking_space(self, reserve_parking_space: schemas.ReserveParkingSpace):
        db = await self.__db_helper.session_getter()
        db_booking_history = BookingHistory(**reserve_parking_space.model_dump())
        db.add(db_booking_history)
        await db.commit()
        await db.refresh(db_booking_history)
        return schemas.ReserveParkingSpaceReturn.model_validate(db_booking_history)

    async def cancel_reservation_parking_space(self, reserve_parking_space: schemas.ReserveParkingSpace):
        db = await self.__db_helper.session_getter()
        stmt = select(BookingHistory).where(and_(BookingHistory.user_id==reserve_parking_space.user_id, BookingHistory.spot_id==reserve_parking_space.spot_id))
        result = await db.execute(stmt)
        history: BookingHistory | None = result.scalar_one_or_none()
        if not history:
            return
        stmt = delete(BookingHistory).where(BookingHistory.id == history.id)
        await db.execute(stmt)
        return history

    async def create_parking_spaces(self, count: int) -> list[schemas.ParkingSpotBase]:
        db = await self.__db_helper.session_getter()
        parking_spaces = list()
        for _ in range(count):
            db_parking_space = ParkingSpot(**schemas.ParkingCreate().model_dump())
            db.add(db_parking_space)
            parking_spaces.append(db_parking_space)
        await db.commit()
        for i in range(count):
            await db.refresh(parking_spaces[i])
            parking_spaces[i] = schemas.ParkingSpotBase.model_validate(parking_spaces[i])
        return parking_spaces
