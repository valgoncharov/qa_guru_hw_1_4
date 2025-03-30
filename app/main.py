import json
import uvicorn
from fastapi_pagination import add_pagination
from fastapi import FastAPI
from routers import status, users
from database import users_db

from app.models.User import User


app = FastAPI()
add_pagination(app)
app.include_router(status.router)
app.include_router(users.router)


def load_users():
    global users_db
    with open("../users.json") as f:
        users_data = json.load(f)
    users_db = [User.model_validate(user) for user in users_data]


@app.on_event("startup")
async def startup_event():
    load_users()


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000, reload=True)
