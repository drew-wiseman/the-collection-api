from database import Base
from sqlalchemy import Column, Integer, String, Float, Boolean

class GameDB(Base):
    __tablename__ = "games"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    platform = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    year_released = Column(Integer, nullable=False)
    current_market_price = Column(Float, nullable=False)
    played = Column(Boolean, nullable=False)
    condition = Column(String, nullable=True)
    cover_image_url = Column(String, nullable=True)
    tub_number = Column(Integer, nullable=False)

class MovieDB(Base):
    __tablename__ = "movies"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    year_released = Column(Integer, nullable=False)
    studio = Column(String, nullable=False)
    runtime_minutes = Column(Integer, nullable=False)
    format = Column(String, nullable=False)
    actors = Column(String, nullable=False)
    current_market_price = Column(Float, nullable=False)
    cover_image_url = Column(String, nullable=True)
    tub_number = Column(Integer, nullable=False)

class MusicDB(Base):
    __tablename__ = "music"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    artist = Column(String, nullable=False)
    genre = Column(String, nullable=False)
    year_released = Column(Integer, nullable=False)
    format = Column(String, nullable=False)
    track_count = Column(Integer, nullable=False)
    current_market_price = Column(Float, nullable=False)
    cover_image_url = Column(String, nullable=True)
    tub_number = Column(Integer, nullable=False)