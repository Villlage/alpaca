# type: ignore
import pytest
from werkzeug.security import check_password_hash, generate_password_hash
from common.exceptions import (
    ResourceConflictError,
    ResourceNotFound,
    AuthenticationError,
)
from tests.factories import faker, UserFactory
from services.user_service import create_user, get_user


class TestCreateUser:
    def test_create_user(self) -> None:
        email = "something@something.com"
        password = "something"
        user = create_user(email=email, password=password)
        assert user.email == email
        assert check_password_hash(user.password, password)

    def test_create_user_same_email(self) -> None:
        email = "something@something.com"
        password = "something"
        UserFactory.create(email=email)
        with pytest.raises(ResourceConflictError):
            create_user(email=email, password=password)


class TestGetUser:
    def test_get_user(self) -> None:
        email = faker.safe_email()
        password = faker.password()
        hashed_password = generate_password_hash(password)
        user = UserFactory.create(email=email, password=hashed_password)

        user = get_user(email=email, password=password)
        assert user
        assert user.email == email
        assert user.password == hashed_password

    def test_get_user_email_not_found(self) -> None:
        email = faker.safe_email()
        password = faker.password()
        with pytest.raises(ResourceNotFound):
            get_user(email=email, password=password)

    def test_get_user_bad_password(self) -> None:
        email = faker.safe_email()
        password = faker.password()
        bad_password = password + "bad_password"
        hashed_password = generate_password_hash(password)
        user = UserFactory.create(email=email, password=hashed_password)
        with pytest.raises(AuthenticationError):
            get_user(email=email, password=bad_password)
