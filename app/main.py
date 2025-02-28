from fastapi import FastAPI
from app.dependencies import create_db_and_tables
from app.routers import messages, profiles, users

app = FastAPI()

# Routers
app.include_router(users.router)
app.include_router(profiles.router)
app.include_router(messages.router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables();
