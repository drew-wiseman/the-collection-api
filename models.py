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