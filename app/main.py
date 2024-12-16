from fastapi import FastAPI
from app.api.route.route import router
from contextlib import asynccontextmanager
from app.controller.controller import stop_crawling, resume_crawling
import asyncio

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 서버 시작 시 크롤링 시작
    await resume_crawling()
    yield
    # 서버 종료 시 크롤링 중지
    stop_crawling()

app = FastAPI(lifespan=lifespan)
app.include_router(router)