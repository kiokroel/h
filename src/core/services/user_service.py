import core.schemas.user_schema as schemas


class UserService:
    def __init__(self, user_repository):
        self.__user_repository = user_repository

    async def create_user(self, user_schema) -> schemas.User:
        return await self.__user_repository.create_user(user_schema)

    async def get_user(self, user_id) -> schemas.User:
        return await self.__user_repository.get_user(user_id)

    async def get_user_by_email(self, email: str) -> schemas.User:
        return await self.__user_repository.get_user_by_email(email)
