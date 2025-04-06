from typing import Iterable
from fastapi import HTTPException
from fastapi import status
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
        existing_user = session.get(User, user_id)
        if not existing_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with id {user_id} not found"
            )
        for key, value in user.model_dump(exclude_unset=True).items():
            setattr(existing_user, key, value)
        session.commit()
        session.refresh(existing_user)
        return existing_user
