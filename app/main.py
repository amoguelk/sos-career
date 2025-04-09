from fastapi import FastAPI
from app.dependencies import create_db_and_tables
from app.routers import messages, profiles, users
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(users.router)
app.include_router(profiles.router)
app.include_router(messages.router)


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
