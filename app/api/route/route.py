from fastapi import APIRouter , HTTPException
from app.service.request import get_recipe_api
from app.service.scrap import get_recipe_scrap,get_recipe_id
from app.dto.data_transfer_object import RecipeService
from app.model.recipe_model import Recipe
from typing import List

router = APIRouter()
recipe_service = RecipeService()



@router.get("/recipes/{num}}") #레시피 API 예시 route
async def get_recipes(num:int):
    recipe_data = await get_recipe_api(num,num)
        # 유효한 레시피 데이터가 있으면 반환
    if "error" not in recipe_data:
        return recipe_data

    # 모든 시도가 실패한 경우 에러 메시지 반환
    return {"error": "유효한 레시피를 찾을 수 없습니다. 다시 시도해 주세요."}

@router.get("/scrap/{recipe_id}") #레시피 크롤링 예시 route
async def get_scrap(recipe_id) :
    recipe_data = await get_recipe_scrap(recipe_id)
        # 유효한 레시피 데이터가 있으면 반환
    if "error" not in recipe_data:
        return recipe_data
    # 모든 시도가 실패한 경우 에러 메시지 반환
    return {"error": "유효한 레시피를 찾을 수 없습니다. 다시 시도해 주세요."}

@router.get("/recipe_id/{num}") #레시피 id 크롤링 예시 route
async def get_scrap_id(num) :
    recipe_id = await get_recipe_id(num)
    # 유효한 레시피 데이터가 있으면 반환
    if "error" not in recipe_id:
        return recipe_id
    # 모든 시도가 실패한 경우 에러 메시지 반환
    return {"error": "유효한 레시피를 찾을 수 없습니다. 다시 시도해 주세요."}

@router.get("/recipes/search", response_model=List[Recipe]) #레시피 search 예시 route
async def search_recipes(query: str):
    query_ingredients = [ingredient.strip() for ingredient in query.split(",")]
    # 서비스에 재료 리스트 전달
    results = recipe_service.get_filtered_recipes(query_ingredients)
    return results
