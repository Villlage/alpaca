from typing import Optional
from common.exceptions import (
    ResourceConflictError,
    ResourceNotFound,
    AuthenticationError,
)
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash


def create_user(email: str, password: str) -> User:
    hashed_password = generate_password_hash(password)

    if User.get_user_by_email(email):
        raise ResourceConflictError("Please sign in. This email address is in use")

    return User.create_user(email=email, password=hashed_password)


def get_user(email: str, password: str) -> Optional[User]:
    user = User.get_user_by_email(email=email)
    if not user:
        raise ResourceNotFound("Could not find user. Please Register.")

    if not check_password_hash(user.password, password):  # type: ignore
        raise AuthenticationError("Bad Email or password. Please try again.")

    return user
