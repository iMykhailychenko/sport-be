import uvicorn
import db

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.users import users
from app.dates import dates
from app.exercises import exercises
from app.trainings import trainings

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(dates.router)
app.include_router(exercises.router)
app.include_router(trainings.router)


@app.on_event("startup")
async def startup() -> None:
    await db.connect()


@app.on_event("shutdown")
async def shutdown() -> None:
    await db.disconnect()


if __name__ == '__main__':
    uvicorn.run("main:app", port=8000, host="0.0.0.0", reload=True, env_file=".env.dev")
