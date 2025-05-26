from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Text, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from database import Base


class SpyCat(Base):
    __tablename__ = "spy_cats"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    years_experience = Column(Integer, nullable=False)
    breed = Column(String, nullable=False)
    salary = Column(Integer, nullable=False)


class Mission(Base):
    __tablename__ = "missions"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    cat_id = Column(Integer, ForeignKey("spy_cats.id"), nullable=True)
    is_complete = Column(Boolean, default=False)
    targets = relationship("Target", back_populates="mission")


class Target(Base):
    __tablename__ = "targets"
    id = Column(Integer, primary_key=True)
    mission_id = Column(Integer, ForeignKey("missions.id"))
    name = Column(String, nullable=False)
    country = Column(String, nullable=False)
    notes = Column(String)
    is_complete = Column(Boolean, default=False)

    mission = relationship("Mission", back_populates="targets")


class TargetRead(BaseModel):
    id: int
    name: str
    country: str
    notes: Optional[str]
    is_complete: bool
    mission_id: int

    class Config:
        from_attributes = True