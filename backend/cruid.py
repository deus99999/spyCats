from typing import List

import httpx
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from starlette import status

from database import get_session
from models import SpyCat, Mission, Target
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from schemas import SpyCatCreate, SpyCatRead, UpdateSalaryRequest, MissionCreate, MissionRead, TargetUpdate, TargetRead

cat_router = APIRouter()


async def is_valid_breed(breed_name: str) -> bool:
    async with httpx.AsyncClient() as client:
        response = await client.get("https://api.thecatapi.com/v1/breeds")
        if response.status_code != 200:
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY)

        breeds = response.json()

        for breed in breeds:
            if breed['name'].lower() == breed_name.lower():
                return True
        return False


@cat_router.post("/add_cat", response_model=SpyCatRead)
async def create_cat(cat_data: SpyCatCreate, session: AsyncSession = Depends(get_session)):

    if not await is_valid_breed(cat_data.breed):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,  # Или status.HTTP_422_UNPROCESSABLE_ENTITY
            detail=f"Breed '{cat_data.breed}' is not in API.")

    cat = SpyCat(
        name=cat_data.name,
        years_experience=cat_data.years_experience,
        breed=cat_data.breed,
        salary=cat_data.salary
    )
    session.add(cat)
    await session.commit()
    await session.refresh(cat)
    return cat


@cat_router.get("/cat/{id}")
async def get_cat(id: int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(SpyCat).where(SpyCat.id == id))
    cat = result.scalars().all()
    return cat


@cat_router.get("/cats")
async def get_cats(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(SpyCat))
    cats = result.scalars().all()
    return cats


@cat_router.delete("/delete_cat/{cat_id}")
async def delete_cat(cat_id = int, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(SpyCat).where(SpyCat.id == cat_id))
    cat = result.scalars().one_or_none()

    if not cat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Cat with id {cat_id} not found"
        )
    await session.delete(cat)
    await session.commit()
    return {"message": f"Cat with id {cat_id} deleted successfully"}


@cat_router.patch("/update-cat-salary/{cat_id}")
async def update_cat_salary(cat_id: int, update_data: UpdateSalaryRequest, session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(SpyCat).where(SpyCat.id == cat_id))
    cat = result.scalar_one_or_none()

    if not cat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Spy cat with id {cat_id} not found"
        )

    cat.salary = update_data.salary
    await session.commit()
    await session.refresh(cat)
    return {"message": f"Salary updated to {cat.salary}", "cat": {
        "id": cat.id,
        "name": cat.name,
        "salary": cat.salary
    }}


mission_router = APIRouter()


@mission_router.post("/", response_model=MissionRead)
async def create_mission(mission_data: MissionCreate, session: AsyncSession = Depends(get_session)):
    mission = Mission(name=mission_data.name, is_complete=mission_data.is_complete)

    for target_data in mission_data.targets:
        target = Target(
            name=target_data.name,
            country=target_data.country,
            notes=target_data.notes or "",
            is_complete=target_data.is_complete,
            mission=mission
        )
        session.add(target)

    session.add(mission)
    await session.commit()
    await session.refresh(mission)

    result = await session.execute(
        select(Mission)
        .options(selectinload(Mission.targets))
        .where(Mission.id == mission.id)
    )
    mission_with_targets = result.scalar_one()

    return mission_with_targets


target_router = APIRouter()


@target_router.patch("/targets/{target_id}", response_model=TargetRead)
async def update_target(target_id: int, data: TargetUpdate, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(Target).options(selectinload(Target.mission)).where(Target.id == target_id)
    )
    target = result.scalar_one_or_none()

    if not target:
        raise HTTPException(status_code=404, detail="Target not found")

    if target.is_complete or target.mission.is_complete:
        raise HTTPException(status_code=400, detail="Cannot update completed target or mission")

    if data.notes is not None:
        target.notes = data.notes

    if data.is_complete is not None:
        target.is_complete = data.is_complete

    await session.commit()
    await session.refresh(target)
    return target


@mission_router.post("/missions/{mission_id}/assign_cat/{cat_id}", status_code=status.HTTP_200_OK)
async def assign_cat_to_mission(
    mission_id: int,
    cat_id: int,
    session: AsyncSession = Depends(get_session),
):
    mission = await session.get(Mission, mission_id)
    if not mission:
        raise HTTPException(status_code=404, detail="Mission not found")

    cat = await session.get(SpyCat, cat_id)
    if not cat:
        raise HTTPException(status_code=404, detail="Cat not found")

    if mission.cat_id is not None:
        raise HTTPException(status_code=400, detail="Mission already assigned to a cat")

    mission.cat_id = cat_id
    session.add(mission)
    await session.commit()
    await session.refresh(mission)

    return {"message": f"Cat {cat_id} assigned to mission {mission_id}"}


@mission_router.get("/missions", response_model=List[MissionRead])
async def list_missions(session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(Mission).options(selectinload(Mission.targets))
    )
    missions = result.scalars().all()
    return missions