from typing import List, Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from auth import verify_api_key
from database import get_db
from models import GameDB
from schemas import DeleteResponse, Game, GameCreate, GameStats

router = APIRouter(prefix="/games", tags=["games"])

@router.get("/", response_model=List[Game])
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
    """Retrieve a filtered list of games."""
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

@router.get("/stats", response_model=GameStats)
def get_games_stats(db: Session = Depends(get_db)):
    """Retrive statistics about the collection."""
    stats = {
        "total_games" : db.query(func.count(GameDB.id)).scalar(),
        "total_market_value" : db.query(func.coalesce(func.sum(GameDB.current_market_price), 0)).scalar(),
        "total_spent" : db.query(func.coalesce(func.sum(GameDB.purchase_price), 0)).scalar(),
        "most_expensive_game" : db.query(GameDB).order_by(GameDB.current_market_price.desc()).first()
    }
    return stats

@router.post("/", response_model=Game)
def create_game(game: GameCreate, db: Session = Depends(get_db), auth: None = Depends(verify_api_key)):
    """Add a game into the collection."""
    game_data = game.model_dump()
    g = GameDB(**game_data)
    db.add(g)
    db.commit()
    db.refresh(g)
    return g

@router.get("/{id}", response_model=Game)
def get_game(id: int, db: Session = Depends(get_db)):
    """Retrive a single game by its id."""
    result = db.query(GameDB).filter(GameDB.id == id).first()
    if result is None:
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game ID '{id}' not found."
        )
    return result

@router.delete("/{id}", response_model=DeleteResponse)
def del_game(id: int, db: Session = Depends(get_db), auth: None = Depends(verify_api_key)):
    """Remove a single game by its id."""
    result = db.query(GameDB).filter(GameDB.id == id).first()
    if result is None:
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game ID '{id}' not found."
        )
    db.delete(result)
    db.commit()
    return {"message": f"Game ID '{id}' deleted."}