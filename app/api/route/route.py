from fastapi import APIRouter 
from app.service.scrap import get_recipe_scrap,get_recipe_id
from app.service.search import search_recipes_by_text
from app.service.llm import generate_response
from app.controller.controller import stop_crawling, is_crawling, resume_crawling, reset_crawling
import asyncio

router = APIRouter()


"""recipes 관련 route"""

@router.get("/scrap/{recipe_id}", tags=["recipes"]) #레시피 크롤링 예시 route
async def get_scrap(recipe_id) :
    recipe_data = await get_recipe_scrap(recipe_id)
        # 유효한 레시피 데이터가 있으면 반환
    if "error" not in recipe_data:
        return recipe_data
    # 모든 시도가 실패한 경우 에러 메시지 반환
    return {"error": "유효한 레시피를 찾을 수 없습니다. 다시 시도해 주세요."}

@router.get("/recipe_id/{num}", tags=["recipes"]) #레시피 id 크롤링 예시 route
async def get_scrap_id(num) :
    recipe_id = await get_recipe_id(num)
    # 유효한 레시피 데이터가 있으면 반환
    if "error" not in recipe_id:
        return recipe_id
    # 모든 시도가 실패한 경우 에러 메시지 반환
    return {"error": "유효한 레시피를 찾을 수 없습니다. 다시 시도해 주세요."}

@router.get("/recipes/search", tags=["recipes"])
def search_recipes(query: str):
    return search_recipes_by_text(query)

@router.get("/recipes/llm", tags=["recipes"])
def generate_recipe(query: str):
    search_response = search_recipes_by_text(query)
    return generate_response(query,search_response)


""" admin 관련 route"""

@router.get("/admin/crawling/status", tags=["admin"])  # 현재 크롤링 상태 확인 (True/False)
async def get_crawling_status():
    return {"is_crawling": is_crawling()}

@router.post("/admin/crawling/stop", tags=["admin"])  # 크롤링 일시정지
async def stop_crawling_endpoint():
    stop_crawling()
    return {"message": "크롤링 중지가 요청되었습니다."}

@router.post("/admin/crawling/resume", tags=["admin"])  # 크롤링 재개
async def resume_crawling_endpoint():
    success = await resume_crawling()
    if success:
        return {"message": "크롤링이 재개되었습니다."}
    return {"message": "크롤링이 이미 실행 중입니다."}

@router.post("/admin/crawling/reset", tags=["admin"])  # 크롤링 중단 지점 초기화 및 시작 (1페이지부터 다시 크롤링)
async def reset_crawling_endpoint():
    success = await reset_crawling()
    if success:
        return {"message": "크롤링이 처음부터 다시 시작되었습니다."}
    return {"message": "크롤링이 이미 실행 중입니다."}