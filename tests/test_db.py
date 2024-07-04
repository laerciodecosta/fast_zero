from sqlalchemy import select

from fast_zero.models import User


def test_create_user(session):
    new_user = User(
        username='testusername', password='testtest', email='teste@test'
    )
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'testusername'))

    assert user.username == 'testusername'
