from fastapi import Depends
from sqlalchemy import select


import core.schemas.user_schema as schemas
from core.database.db_helper import db_helper
from core.database.models.user import User


class SQLAlchemyUserRepository:
    def __init__(self):
        self.__db_helper = db_helper

    async def get_user(self, user_id: int) -> schemas.User | None:
        db = await self.__db_helper.session_getter()
        stmt = select(User).where(User.id == user_id)
        result = await db.execute(stmt)
        user: User | None = result.scalar_one_or_none()
        return user

    async def get_user_by_email(self, email: str) -> schemas.User | None:
        db = await self.__db_helper.session_getter()
        stmt = select(User).where(User.email == email)
        result = await db.execute(stmt)
        user: User | None = result.scalar_one_or_none()
        return user

    async def create_user(self, user: schemas.UserCreate) -> schemas.User:
        db = await self.__db_helper.session_getter()
        db_user = User(**user.model_dump())
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user
