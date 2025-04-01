from typing import Iterable

from ..models.User import User
from .engins import engine
from sqlmodel import Session, select


def get_user(user_id: int) -> User | None:
    with Session(engine) as session:
        return session.get(User, user_id)


def get_users() -> Iterable[User] | None:
    with Session(engine) as session:
        statement = select(User)
        return session.exec(statement).all()


def create_user(user: User) -> User:
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user


def delete_user(user_id: int) -> None:
    with Session(engine) as session:
        user = session.get(User, user_id)
        session.delete(user)
        session.commit()


def update_user(user_id: int, user: User) -> User:
    with Session(engine) as session:
        user = session.get(User, user_id)
        user.update(user)
        session.commit()
        session.refresh(user)
        return user
