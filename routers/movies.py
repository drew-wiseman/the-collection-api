from typing import List, Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from auth import verify_api_key
from database import get_db
from models import MovieDB
from schemas import DeleteResponse, Movie, MovieCreate, MovieStats

router = APIRouter(prefix="/movies", tags=["movies"])

@router.get("/", response_model=List[Movie])
def get_movies(
    title: Optional[str] = None, 
    genre: Optional[str] = None,
    start_year: Optional[int] = None,
    end_year: Optional[int] = None,
    studio: Optional[str] = None,
    min_runtime: Optional[int] = None,
    max_runtime: Optional[int] = None,
    format: Optional[Literal["VHS", "DVD", "blu-ray", "videodisc"]] = None,
    min_curr_price: Optional[float] = None,
    max_curr_price: Optional[float] = None,
    db: Session = Depends(get_db)
):
    """Retrieve a filtered list of movies."""
    query = db.query(MovieDB)
    if title is not None:
        query = query.filter(MovieDB.title == title)
    if genre is not None:
        query = query.filter(MovieDB.genre == genre)
    if start_year is not None:
        query = query.filter(MovieDB.year_released >= start_year)
    if end_year is not None:
        query = query.filter(MovieDB.year_released <= end_year)
    if studio is not None:
        query = query.filter(MovieDB.studio == studio)
    if min_runtime is not None:
        query = query.filter(MovieDB.runtime_minutes >= min_runtime)
    if max_runtime is not None:
        query = query.filter(MovieDB.runtime_minutes <= max_runtime)
    if format is not None:
        query = query.filter(MovieDB.format == format)
    if min_curr_price is not None:
        query = query.filter(MovieDB.current_market_price >= min_curr_price)
    if max_curr_price is not None:
        query = query.filter(MovieDB.current_market_price <= max_curr_price)
    return query.all()

@router.get("/stats", response_model=MovieStats)
def get_movies_stats(db: Session = Depends(get_db)):
    """Retrieve statistics about the movies within the collection"""
    stats = {
        "total_movies" : db.query(func.count(MovieDB.id)).scalar(),
        "total_market_value" : db.query(func.coalesce(func.sum(MovieDB.current_market_price), 0)).scalar(),
        "most_expensive_movie" : db.query(MovieDB).order_by(MovieDB.current_market_price.desc()).first()
    }
    return stats

@router.post("/", response_model=Movie)
def create_movie(movie: MovieCreate, db: Session = Depends(get_db), auth: None = Depends(verify_api_key)):
    """Add a movie into the collection."""
    movie_data = movie.model_dump()
    m = MovieDB(**movie_data)
    db.add(m)
    db.commit()
    db.refresh(m)
    return m

@router.get("/{id}", response_model=Movie)
def get_movie(id: int, db: Session = Depends(get_db)):
    """Retrieve a single movie by its id."""
    result = db.query(MovieDB).filter(MovieDB.id == id).first()
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie ID '{id}' not found."
        )
    return result

@router.delete("/{id}", response_model=DeleteResponse)
def del_movie(id: int, db: Session = Depends(get_db), auth: None = Depends(verify_api_key)):
    """Remove a single movie by its id."""
    result = db.query(MovieDB).filter(MovieDB.id == id).first()
    if result is None:
        raise HTTPException (
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Movie ID '{id}' not found."
        )
    db.delete(result)
    db.commit()
    return {"message": f"Movie ID '{id}' deleted."}