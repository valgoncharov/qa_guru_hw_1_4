from sqlmodel import create_engine, SQLModel, Session, text, select
import os
from app.models.User import User


# Default database URL if environment variable is not set
DEFAULT_DATABASE_URL = "postgresql+psycopg2://postgres:example@localhost:5432/postgres"

# Get database URL from environment or use default
database_url = os.getenv("DATABASE_ENGINE", DEFAULT_DATABASE_URL)

# Create engine with the database URL
engine = create_engine(database_url,
                       pool_size=os.getenv("DATABASE_POOL_SIZE", 10))


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_database_status() -> bool:
    try:
        with Session(engine) as session:
            session.exec(text("SELECT 1"))
            return True
    except Exception as e:
        print(e)
        return False


def get_users() -> list[User]:
    with Session(engine) as session:
        statement = select(User)
        return session.exec(statement).all()


def set_users(users: list[User]) -> None:
    with Session(engine) as session:
        # Clear existing users
        session.exec(text('DELETE FROM "user"'))
        # Add new users
        for user in users:
            session.add(user)
        session.commit()
