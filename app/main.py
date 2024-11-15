from fastapi import FastAPI
from app.api.route.route import router
from contextlib import asynccontextmanager
from app.controller.controller import add_recipe
import asyncio

@asynccontextmanager
async def lifespan(app : FastAPI) :
    print("start")
    asyncio.create_task(add_recipe())
    yield

    print("end")

app = FastAPI(lifespan=lifespan)
app.include_router(router)
