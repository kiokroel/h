from fastapi import APIRouter


from .auth_router import router as auth_router
from .parking_router import router as parking_router


router = APIRouter()

router.include_router(
    auth_router,
)

router.include_router(parking_router)
