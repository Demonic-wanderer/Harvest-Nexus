"""
SQLAlchemy models for the future API layer (Buyer Linkage Engine).
Not used by the current CLI tool, which talks to sqlite directly via
db/database.py. Use these once you move to the FastAPI service.
"""
from datetime import datetime

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class MarketPrice(Base):
    __tablename__ = "market_prices"

    id = Column(Integer, primary_key=True, index=True)
    crop_type = Column(String, index=True, nullable=False)
    region = Column(String, index=True, nullable=False)
    price_per_quintal = Column(Float, nullable=False)
    recorded_at = Column(DateTime, default=datetime.utcnow, index=True)


class Mandi(Base):
    __tablename__ = "mandis"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    location = Column(String, index=True, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    contact_number = Column(String, nullable=True)

    buyers = relationship("Buyer", back_populates="mandi")


class Buyer(Base):
    __tablename__ = "buyers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    crop_types = Column(String, nullable=False)
    location = Column(String, index=True, nullable=False)
    contact_number = Column(String, nullable=True)
    mandi_id = Column(Integer, ForeignKey("mandis.id"), nullable=True)

    mandi = relationship("Mandi", back_populates="buyers")
