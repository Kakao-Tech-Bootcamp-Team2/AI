from fastapi import APIRouter
from app.api.request import get_spoonacular,get_edam

router = APIRouter()

@router.get("/recipes/{query}")
def get_recipes(query: str):
    return get_spoonacular(query)

@router.get("/recipes2/{query}")
def get_recipes2(query:str):
    return get_edam(query)