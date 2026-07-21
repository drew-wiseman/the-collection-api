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
    purchase_price: Optional[float] = None

class Game(GameCreate):
    id: int

class GameStats(BaseModel):
    total_games: int
    total_market_value: float
    most_expensive_game: Optional[Game] = None

class DeleteResponse(BaseModel):
    message: str