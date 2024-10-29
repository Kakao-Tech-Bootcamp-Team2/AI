from fastapi import FastAPI
from app.route.route import router
app = FastAPI()

app.include_router(router)