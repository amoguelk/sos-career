from fastapi import FastAPI
from app.routers import messages, profiles, users

app = FastAPI()

app.include_router(users.router)
app.include_router(profiles.router)
app.include_router(messages.router)
