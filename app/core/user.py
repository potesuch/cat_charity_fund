from typing import Union

from fastapi import Depends

from fastapi_users import (
    IntegerIDMixin, BaseUserManager, InvalidPasswordException, FastAPIUsers
)
from fastapi_users.authentication import (
    AuthenticationBackend, BearerTransport, JWTStrategy
)

from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.config import settings
from app.models import User
from app.schemas.user import UserCreate


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """
    Асинхронный генератор, предоставляющий доступ к базе данных пользователей.

    Args:
        session (AsyncSession): Асинхронная сессия SQLAlchemy.

    Yields:
        SQLAlchemyUserDatabase: База данных пользователей.
    """
    yield SQLAlchemyUserDatabase(session, User)


bearer_transport = BearerTransport(tokenUrl='auth/jwt/login')


def get_jwt_strategy() -> JWTStrategy:
    """
    Возвращает стратегию JWT.

    Returns:
        JWTStrategy: Стратегия JWT с заданным секретом и временем жизни токена.
    """
    return JWTStrategy(secret=settings.secret, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name='jwt',
    transport=bearer_transport,
    get_strategy=get_jwt_strategy
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """
    Менеджер пользователей, расширяющий базовый менеджер с проверкой паролей.
    """

    async def validate_password(
            self,
            password: str,
            user: Union[UserCreate, User]
    ):
        """
        Проверяет допустимость пароля.

        Args:
            password (str): Пароль пользователя.
            user (Union[UserCreate, User]): Пользователь.

        Raises:
            InvalidPasswordException: Если пароль менее 3 символов или содержит email пользователя.
        """
        if len(password) < 3:
            raise InvalidPasswordException(
                reason='Password should be at least 3 characters'
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason='Password should not contain e-mail'
            )


async def get_user_manager(user_db=Depends(get_user_db)):
    """
    Асинхронный генератор, предоставляющий менеджер пользователей.

    Args:
        user_db: Зависимость для получения базы данных пользователей.

    Yields:
        UserManager: Менеджер пользователей.
    """
    yield UserManager(user_db)


fastapi_users = FastAPIUsers(
    get_user_manager,
    [auth_backend]
)

current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
