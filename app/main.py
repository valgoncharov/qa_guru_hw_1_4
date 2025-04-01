import json
import uvicorn
import os
from fastapi_pagination import add_pagination
from fastapi import FastAPI
from app.database import create_db_and_tables, set_users, engine
from app.routers import status, users
from app.models.User import User
import dotenv
from sqlmodel import Session
from sqlalchemy import text

dotenv.load_dotenv()


app = FastAPI()
add_pagination(app)
app.include_router(status.router)
app.include_router(users.router)


def load_users():
    # Get the absolute path to users.json
    current_dir = os.path.dirname(os.path.abspath(__file__))
    users_file = os.path.join(os.path.dirname(current_dir), "users.json")

    with open(users_file) as f:
        users_data = json.load(f)

    # Create User instances without the id field
    users_list = []
    for user_data in users_data:
        user_dict = {k: v for k, v in user_data.items() if k != 'id'}
        users_list.append(User(**user_dict))

    set_users(users_list)


@app.on_event("startup")
async def startup_event():
    # Create tables first
    create_db_and_tables()

    # Verify database connection
    with Session(engine) as session:
        session.exec(text("SELECT 1"))

    # Then load users
    load_users()


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, reload=True)
