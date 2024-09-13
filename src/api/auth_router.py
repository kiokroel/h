from jwt.exceptions import InvalidTokenError
from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from core.repositories.user_repository import SQLAlchemyUserRepository
from core.schemas.token_info import TokenInfo
from core.schemas.user_schema import UserCreate, User


from core.services.user_service import UserService
from core.utils import auth_utils
from core.utils.auth_utils import hash_password

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login/")


router = APIRouter(prefix="/auth", tags=["Авторизация"])


user_service = UserService(SQLAlchemyUserRepository())


async def validate_auth_user(
    username: str = Form(),
    password: str = Form(),
) -> User | Exception:
    email = username
    unauthed_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="invalid email or password",
    )
    if not (user := await user_service.get_user_by_email(email=email)):
        raise unauthed_exc

    if not auth_utils.validate_password(
        password=password, hashed_password=user.password
    ):
        raise unauthed_exc

    return user


def get_current_token_payload(token: str = Depends(oauth2_scheme)) -> dict:
    try:
        payload = auth_utils.decode_jwt(token=token)
    except InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=f"invalid token error: {e}"
        )
    return payload


async def get_current_auth_user(
    payload: dict = Depends(get_current_token_payload),
) -> User:
    email: str | None = payload.get("sub")
    if user := await user_service.get_user_by_email(email):
        return user
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="token invalid (user not found)",
    )


@router.post("/login/", response_model=TokenInfo)
async def auth_user_issue_jwt(user: UserCreate = Depends(validate_auth_user)):
    jwt_payload = {"sub": user.email, "username": user.username, "email": user.email}
    token = auth_utils.encode_jwt(jwt_payload)
    return TokenInfo(access_token=token, token_type="Bearer")


@router.get("/users/me/")
async def auth_user_check_self_info(
    payload: dict = Depends(get_current_token_payload),
    user: User = Depends(get_current_auth_user),
):
    iat = payload.get("iat")
    return {
        "username": user.username,
        "email": user.email,
        "logged_in_at": iat,
        "id": user.id,
    }


@router.post("/register", response_model=User)
async def create_user(user: UserCreate = Depends()):
    user_from_db = await user_service.get_user_by_email(email=user.email)
    if user_from_db:
        raise HTTPException(status_code=400, detail="Email already registered")
    user.password = hash_password(user.password)
    new_user = await user_service.create_user(user)
    return new_user
