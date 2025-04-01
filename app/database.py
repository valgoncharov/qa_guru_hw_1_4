from app.models.User import User

# Initialize empty list
users_db: list[User] = []


def get_users() -> list[User]:
    return users_db


def set_users(users: list[User]) -> None:
    global users_db
    users_db = users
