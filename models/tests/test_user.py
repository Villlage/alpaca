from models.user import User
from tests.factories import UserFactory


class TestUser:
    def test_get_user(self) -> None:
        user = UserFactory.create()
        res = User.get_user(user.id)
        assert user == res

    def test_create_user(self) -> None:
        email = "email@gmail.com"
        password = "password"
        args = dict(email=email, password=password)
        user = User.create_user(**args)
        assert user.email == email
        assert user.password == password

    def test_get_users(self) -> None:
        user1 = UserFactory.create()
        user2 = UserFactory.create()
        UserFactory.create()
        res = User.get_users([user1.id, user2.id])
        assert res
        assert len(res) == 2
        assert set([user1.id, user2.id]) == set(u.id for u in res)

    def test_is_active(self) -> None:
        user = UserFactory.create()
        assert user.is_active == True
        user.deactivate()
        assert user.is_active == False

    def test_is_admin(self) -> None:
        user = UserFactory.create()
        assert user.is_admin() == False
