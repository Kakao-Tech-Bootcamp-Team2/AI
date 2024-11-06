from fastapi import APIRouter , HTTPException
from app.service.request import get_spoonacular,get_edam
from app.service.scrap import get_recipe_scrap
from app.dto.data_transfer_object import RecipeService
from app.model.recipe_model import Recipe
from typing import List
import random

router = APIRouter()
recipe_service = RecipeService()


@router.get("/recipes/{query}")
def get_recipes(query: str):
    return get_spoonacular(query)

@router.get("/recipes2/{query}")
def get_recipes2(query:str):
    return get_edam(query)

@router.get("/scrap")
async def get_scrap() :
    max_attempts = 5
    for _ in range(max_attempts):
        recipe_id = random.randint(6803892, 7037297)  # 랜덤 ID 생성
        recipe_data = get_recipe_scrap(recipe_id)
        
        # 유효한 레시피 데이터가 있으면 반환
        if "error" not in recipe_data:
            return recipe_data
        
    # 모든 시도가 실패한 경우 에러 메시지 반환
    return {"error": "유효한 레시피를 찾을 수 없습니다. 다시 시도해 주세요."}

@router.post("/recipes/{recipe_id}", response_model=dict)
async def add_recipe(recipe_id: int):
    result = await recipe_service.add_recipe(recipe_id)
    if result.get("error"):
        raise HTTPException(status_code=404, detail=result["error"])
    return {"message": f"레시피 {recipe_id}가 성공적으로 추가되었습니다."}

@router.get("/recipes/search", response_model=List[Recipe])
async def search_recipes(query: str):
    results = await recipe_service.search_recipes(query)
    return results