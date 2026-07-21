from typing import List, Literal, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from auth import verify_api_key
from database import get_db
from models import MusicDB
from schemas import DeleteResponse, Music, MusicCreate, MusicStats

router = APIRouter(prefix="/music", tags=["music"])

@router.get("/", response_model=List[Music])
def get_albums(
    title: Optional[str] = None,
    artist: Optional[str] = None, 
    genre: Optional[str] = None, 
    start_year: Optional[int] = None,
    end_year: Optional[int] = None,
    format: Optional[Literal["vinyl", "cassette", "CD", "8-track"]] = None,
    min_track_count: Optional[int] = None,
    max_track_count: Optional[int] = None,
    min_curr_price: Optional[float] = None,
    max_curr_price: Optional[float] = None,
    db: Session = Depends(get_db)
):
    """Retrieve a filtered list of albums."""
    query = db.query(MusicDB)
    if title is not None:
        query = query.filter(MusicDB.title == title)
    if artist is not None:
        query = query.filter(MusicDB.artist == artist)
    if genre is not None:
        query = query.filter(MusicDB.genre == genre)
    if start_year is not None:
        query = query.filter(MusicDB.year_released >= start_year)
    if end_year is not None:
        query = query.filter(MusicDB.year_released <= end_year)
    if format is not None:
        query = query.filter(MusicDB.format == format)
    if min_track_count is not None:
        query = query.filter(MusicDB.track_count >= min_track_count)
    if max_track_count is not None:
        query = query.filter(MusicDB.track_count <= max_track_count)  
    if min_curr_price is not None:
        query = query.filter(MusicDB.current_market_price >= min_curr_price)
    if max_curr_price is not None:
        query = query.filter(MusicDB.current_market_price <= max_curr_price)
    return query.all()

@router.get("/stats", response_model=MusicStats)
def get_music_stats(db: Session = Depends(get_db)):
    """Retrieve statistics about the albums within the collection"""
    stats = {
        "total_albums" : db.query(func.count(MusicDB.id)).scalar(),
        "total_market_value" : db.query(func.coalesce(func.sum(MusicDB.current_market_price), 0)).scalar(),
        "most_expensive_album" : db.query(MusicDB).order_by(MusicDB.current_market_price.desc()).first()
    }
    return stats

@router.post("/", response_model=Music)
def create_album(album: MusicCreate, db: Session = Depends(get_db), auth: None = Depends(verify_api_key)):
    """Add an album into the collection."""
    album_data = album.model_dump()
    a = MusicDB(**album_data)
    db.add(a)
    db.commit()
    db.refresh(a)
    return a

@router.get("/{id}", response_model=Music)
def get_album(id: int, db: Session = Depends(get_db)):
    """Retrieve a single album by its id."""
    result = db.query(MusicDB).filter(MusicDB.id == id).first()
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Album ID '{id}' not found."
        )
    return result

@router.delete("/{id}", response_model=DeleteResponse)
def del_album(id: int, db: Session = Depends(get_db), auth: None = Depends(verify_api_key)):
    """Remove a single album by its id."""
    result = db.query(MusicDB).filter(MusicDB.id == id).first()
    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Album ID '{id}' not found."
        )
    db.delete(result)
    db.commit()
    return {"message": f"Album ID '{id}' deleted."}