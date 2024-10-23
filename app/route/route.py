from fastapi import APIRouter
from app.api.request import get_spoonacular

router = APIRouter()

@router.get("/recipes/{query}")
def get_recipes(query: str):
    return get_spoonacular(query)