from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.future import select
from starlette.middleware.cors import CORSMiddleware

from cruid import cat_router, mission_router, target_router
from database import get_session, engine, Base
from models import SpyCat

app = FastAPI()


origins = [
    # "http://127.0.0.1:3000"
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(cat_router)
app.include_router(mission_router)
app.include_router(target_router)


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

if __name__ == "__main__":
    pass