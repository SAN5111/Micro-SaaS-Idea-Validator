from datetime import datetime
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from database import Base


class Software(Base):
    __tablename__ = "software"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    website = Column(String, nullable=True)
    createdAt = Column(DateTime, default=datetime.utcnow)

    reviews = relationship("Review", back_populates="software", cascade="all, delete-orphan")


class Review(Base):
    __tablename__ = "reviews"

    id = Column(String, primary_key=True)
    softwareId = Column(String, ForeignKey("software.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    rating = Column(Integer, nullable=False)
    comment = Column(Text, nullable=False)
    createdAt = Column(DateTime, default=datetime.utcnow)

    software = relationship("Software", back_populates="reviews")
