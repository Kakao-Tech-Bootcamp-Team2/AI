from fastapi import APIRouter
from app.api.request import get_spoonacular,get_edam
from app.api.scrap import get_recipe_scrap
import random

router = APIRouter()

@router.get("/recipes/{query}")
def get_recipes(query: str):
    return get_spoonacular(query)

@router.get("/recipes2/{query}")
def get_recipes2(query:str):
    return get_edam(query)

@router.get("/scrap")
async def get_scrap() :
    max_attempts = 5
    recipe_id = random.randint(6803892, 7037297)  # 랜덤 ID 생성
    recipe_data = get_recipe_scrap(recipe_id)
    for _ in range(max_attempts):
        recipe_id = random.randint(6803892, 7037297)  # 랜덤 ID 생성
        recipe_data = get_recipe_scrap(recipe_id)
        
        # 유효한 레시피 데이터가 있으면 반환
        if "error" not in recipe_data:
            return recipe_data
        
    # 모든 시도가 실패한 경우 에러 메시지 반환
    return {"error": "유효한 레시피를 찾을 수 없습니다. 다시 시도해 주세요."}