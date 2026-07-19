from database import SessionLocal, engine, Base
from fastapi import FastAPI, HTTPException, status, Depends
from models import GameDB
from pydantic import BaseModel, Field
from typing import Literal, Optional
from sqlalchemy.orm import Session

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
Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

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
    db: Session = Depends(get_db)
):
    query = db.query(GameDB)
    if title is not None:
        query = query.filter(GameDB.title == title)
    if platform is not None:
        query = query.filter(GameDB.platform == platform)
    if genre is not None:
        query = query.filter(GameDB.genre == genre)
    if min_curr_price is not None:
        query = query.filter(GameDB.current_market_price >= min_curr_price)
    if max_curr_price is not None:
        query = query.filter(GameDB.current_market_price <= max_curr_price)
    if start_year is not None:
        query = query.filter(GameDB.year_released >= start_year)
    if end_year is not None:
        query = query.filter(GameDB.year_released <= end_year)
    if condition is not None:
        query = query.filter(GameDB.condition == condition)
    if max_purchase_price is not None:
        query = query.filter(GameDB.purchase_price <= max_purchase_price)
    if min_purchase_price is not None:
        query = query.filter(GameDB.purchase_price >= min_purchase_price)
    return query.all()

@app.post("/games")
def create_game(game: GameCreate, db: Session = Depends(get_db)):
    game_data = game.model_dump()
    g = GameDB(**game_data)
    db.add(g)
    db.commit()
    db.refresh(g)
    return g

@app.get("/games/{id}")
def get_game(id: int, db: Session = Depends(get_db)):
    result = db.query(GameDB).filter(GameDB.id == id).first()
    if result is None:
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game ID '{id}' not found."
        )
    return result


@app.delete("/games/{id}")
def del_game(id: int, db: Session = Depends(get_db)):
    result = db.query(GameDB).filter(GameDB.id == id).first()
    if result is None:
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game ID '{id}' not found."
        )
    db.delete(result)
    db.commit()
    return {"message": f"Game ID '{id}' deleted."}