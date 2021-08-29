from app import app
from tests.factories import faker, UserFactory
from conftest import logged_in_client  # type: ignore
from werkzeug.security import generate_password_hash


class TestRegister:
    def test_register(self) -> None:
        with app.test_client() as client:
            email = faker.safe_email()
            password = faker.password()
            # register a user
            resp = client.post("/register", json=dict(email=email, password=password))
            assert resp.status_code == 200

    def test_register_bad_email(self) -> None:
        with app.test_client() as client:
            email = "something@"
            password = faker.password()
            resp = client.post("/register", json=dict(email=email, password=password))
            assert resp.status_code == 400

    def test_register_no_password(self) -> None:
        with app.test_client() as client:
            email = "something@something1.com"
            password = None
            resp = client.post("/register", json=dict(email=email, password=password))
            assert resp.status_code == 400

    def test_register_no_email(self) -> None:
        with app.test_client() as client:
            email = None
            password = faker.password()
            resp = client.post("/register", json=dict(email=email, password=password))
            assert resp.status_code == 400

    def test_register_same_email(self) -> None:
        with app.test_client() as client:
            email = faker.safe_email()
            password = faker.password()
            user = UserFactory.create(email=email)
            resp = client.post("/register", json=dict(email=email, password=password))
            assert resp.status_code == 409


class TestLogin:
    def test_login(self) -> None:
        with app.test_client() as client:
            email = faker.safe_email()
            password = faker.password()
            hashed_password = generate_password_hash(password)
            user = UserFactory.create(email=email, password=hashed_password)
            # login a user
            resp = client.post("/login", json=dict(email=email, password=password))
            assert resp.status_code == 200

    def test_login_bad_email(self) -> None:
        with app.test_client() as client:
            email = "something@"
            password = faker.password()
            # login a user
            resp = client.post("/login", json=dict(email=email, password=password))
            assert resp.status_code == 400

    def test_email_not_registered(self) -> None:
        with app.test_client() as client:
            email = faker.safe_email()
            password = faker.password()
            # login a user
            resp = client.post("/login", json=dict(email=email, password=password))
            assert resp.status_code == 404

    def test_bad_password(self) -> None:
        with app.test_client() as client:
            email = faker.safe_email()
            password = faker.password()
            hashed_password = generate_password_hash(password)
            bad_password = password + "bad"
            user = UserFactory.create(email=email, password=hashed_password)
            # login a user
            resp = client.post("/login", json=dict(email=email, password=bad_password))
            assert resp.status_code == 403


class TestLogOut:
    def test_logout(self) -> None:
        user = UserFactory.create()
        with logged_in_client(user) as client:
            resp = client.get("/logout")
            assert resp.status_code == 200

    def test_logout_unauthenticated_user(self) -> None:
        with app.test_client() as client:
            resp = client.get("/logout")
            assert resp.status_code == 401
