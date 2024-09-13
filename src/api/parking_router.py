from typing import List

from fastapi import APIRouter, Depends

from api.auth_router import get_current_auth_user
from core.repositories.parking_repository import SQLAlchemyParkingRepository
from core.schemas.parking_schema import (
    ParkingSpotBase,
    TimeDelta,
    ReserveParkingSpace,
    CancelReserveParkingSpace, ReserveParkingSpaceReturn,
)
from core.schemas.user_schema import User
from core.services.parking_service import ParkingService

router = APIRouter(prefix="/parking", tags=["Parking"])


parking_service = ParkingService(SQLAlchemyParkingRepository())


@router.get("/free_spaces", response_model=List[int])
async def get_free_parking_spaces(time_delta: TimeDelta = Depends()):
    return await parking_service.get_free_parking_spaces(time_delta)


@router.post("/create_parking_spaces", response_model=List[ParkingSpotBase])
async def create_parking_spaces(
    count: int,
    # user: User = Depends(get_current_auth_user),
):
    return await parking_service.create_parking_spaces(count)


@router.post("/reservation_parking_space", response_model=ReserveParkingSpaceReturn)
async def reservation_parking_space(
    reserve_parking_space_schema: ReserveParkingSpace,
    user: User = Depends(get_current_auth_user),
):
    reserve_parking_space_schema.user_id = user.id
    return await parking_service.reservation_parking_space(reserve_parking_space_schema)


@router.delete(
    "/cancel_reservation_parking_space", response_model=CancelReserveParkingSpace
)
async def cancel_reservation_parking_space(
    cansel_reserve_parking_space_schema: CancelReserveParkingSpace,
    # user: User = Depends(get_current_auth_user),
):
    # cansel_reserve_parking_space_schema.user_id = user.id
    return await parking_service.cancel_reservation_parking_space(
        cansel_reserve_parking_space_schema
    )
