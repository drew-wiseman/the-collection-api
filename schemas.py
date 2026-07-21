from pydantic import BaseModel, Field
from typing import Literal, Optional, List

class GameCreate(BaseModel):
    title: str
    platform: str
    genre: str
    year_released: int
    current_market_price: float = Field(gt=0, description="Market price must be greater than zero.")
    played: bool
    condition: Optional[Literal["loose", "CIB", "sealed"]] = None

class Game(GameCreate):
    id: int

class GameStats(BaseModel):
    total_games: int
    total_market_value: float
    most_expensive_game: Optional[Game] = None

class MovieCreate(BaseModel):
    title: str
    genre: str
    year_released: int
    studio: str
    runtime_minutes: int
    format: Literal["VHS", "DVD", "blu-ray", "videodisc"]
    actors: str
    current_market_price: float = Field(gt=0, description="Market price must be greater than zero.")

class Movie(MovieCreate):
    id: int

class MovieStats(BaseModel):
    total_movies: int
    total_market_value: float
    most_expensive_movie: Optional[Movie] = None

class MusicCreate(BaseModel):
    title: str
    artist: str
    genre: str
    year_released: int
    format: Literal["vinyl", "cassette", "CD", "8-track"]
    track_count: int
    current_market_price: float = Field(gt=0, description="Market price must be greater than zero.")

class Music(MusicCreate):
    id: int

class MusicStats(BaseModel):
    total_albums: int
    total_market_value: float
    most_expensive_album: Optional[Music] = None

class DeleteResponse(BaseModel):
    message: str