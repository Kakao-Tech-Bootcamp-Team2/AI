from fastapi import FastAPI
from app.api.route.route import router
app = FastAPI()

app.include_router(router)