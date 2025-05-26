from typing import List, Optional

from pydantic import BaseModel, Field, validator


class SpyCatRead(BaseModel):
    name: str
    years_experience: int
    breed: str
    salary: float


class SpyCatCreate(BaseModel):
    name: str
    years_experience: int = Field(0, ge=0)  # minimum 0
    breed: str
    salary: float = Field(0, ge=0)

    @validator('breed')
    def validate_breed(cls, breed_name):
        if not breed_name:
            raise ValueError("Breed is required")
        return breed_name


class UpdateSalaryRequest(BaseModel):
    salary: int | float


class TargetCreate(BaseModel):
    name: str
    country: str
    notes: str = ''
    is_complete: bool = False


class MissionCreate(BaseModel):
    name: str
    targets: List[TargetCreate]
    is_complete: bool = False


class MissionRead(BaseModel):
    id: int
    name: str
    is_complete: bool
    targets: List[TargetCreate]


class TargetUpdate(BaseModel):
    notes: Optional[str] = None
    is_complete: Optional[bool] = None


class TargetRead(BaseModel):
    id: int
    name: str
    country: str
    notes: Optional[str]
    is_complete: bool
    mission_id: int

    class Config:
        from_attributes = True