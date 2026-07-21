from fastapi import FastAPI
from database import engine, Base
from routers import games

app = FastAPI(
    title="The Collection API",
    description="A REST API for tracking a retro video game collection.",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)

app.include_router(games.router)