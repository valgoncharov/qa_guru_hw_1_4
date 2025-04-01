import json
import uvicorn
import os
from fastapi_pagination import add_pagination
from fastapi import FastAPI
from app.routers import status, users
from app.database import set_users

from app.models.User import User


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
    users_list = [User.model_validate(user) for user in users_data]
    set_users(users_list)


@app.on_event("startup")
async def startup_event():
    load_users()


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, reload=True)
