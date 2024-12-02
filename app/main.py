from fastapi import FastAPI
from app.api.route.route import router
from contextlib import asynccontextmanager
from app.controller.controller import add_recipe
import asyncio

_startup_task = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    global _startup_task
    if _startup_task is None:
        _startup_task = asyncio.create_task(add_recipe())
    yield
    if _startup_task:
        _startup_task.cancel()
        try:
            await _startup_task
        except asyncio.CancelledError:
            pass

app = FastAPI(lifespan=lifespan)
app.include_router(router)