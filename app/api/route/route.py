from fastapi import APIRouter 
from app.service.scrap import get_recipe_scrap,get_recipe_id
from app.service.search import search_recipes_by_text
from app.service.llm import generate_response
router = APIRouter()


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

@router.get("/recipes/search")
def search_recipes(query: str):
    return search_recipes_by_text(query)

@router.get("/recipes/llm")
def generate_recipe(query: str):
    search_response = search_recipes_by_text(query)
    return generate_response(query,search_response)