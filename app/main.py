from fastapi import FastAPI
from app.api.route.route import router
from contextlib import asynccontextmanager
from app.controller.controller import ad_recipe


@asynccontextmanager
async def lifespan(app : FastAPI) :
    print("start")
    await ad_recipe()
    yield

    print("end")

app = FastAPI(lifespan=lifespan)
app.include_router(router)
