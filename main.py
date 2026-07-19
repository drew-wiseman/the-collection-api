from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import Literal, Optional

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

app = FastAPI() # create app instance
games = [] #in memory list to hold games

@app.get("/games")
def get_games(
    title: Optional[str] = None, 
    platform: Optional[str] = None,
    genre: Optional[str] = None,
    min_curr_price: Optional[float] = None,
    max_curr_price: Optional[float] = None,
    start_year: Optional[int] = None,
    end_year: Optional[int] = None,
    condition: Optional[Literal["loose", "CIB", "sealed"]] = None,
    max_purchase_price: Optional[float] = None,
    min_purchase_price: Optional[float] = None,
):
    result = games
    if title is not None:
        result = [g for g in result if g.title == title]
    if platform is not None:
        result = [g for g in result if g.platform == platform]
    if genre is not None:
        result = [g for g in result if g.genre == genre]
    if min_curr_price is not None:
        result = [g for g in result if g.current_market_price >= min_curr_price]
    if max_curr_price is not None:
        result = [g for g in result if g.current_market_price <= max_curr_price]
    if start_year is not None:
        result = [g for g in result if g.year_released >= start_year]
    if end_year is not None:
        result = [g for g in result if g.year_released <= end_year]
    if condition is not None:
        result = [g for g in result if g.condition == condition]
    if max_purchase_price is not None:
        result = [g for g in result if g.purchase_price <= max_purchase_price]
    if min_purchase_price is not None:
        result = [g for g in result if g.purchase_price >= min_purchase_price]
    return result

@app.post("/games")
def create_game(game: GameCreate):
    game_data = game.model_dump()
    g = Game(id=len(games) + 1, **game_data)
    games.append(g)
    return g

@app.get("/games/{id}")
def get_game(id: int):
    for g in games:
        if g.id == id:
            return g
    raise HTTPException (
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Game ID '{id}' not found."
    )

@app.delete("/games/{id}")
def del_game(id: int):
    target = -1
    for i, g in enumerate(games):
        if g.id == id:
            target = i
            break
    if target == -1:
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game ID '{id}' not found."
        )
    else:
        games.pop(target)