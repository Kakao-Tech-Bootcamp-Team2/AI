from fastapi import HTTPException
from app.service.request import get_recipe_api
from app.service.scrap import get_recipe_scrap
from app.dto.data_transfer_object import RecipeService
import asyncio
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
recipe_service = RecipeService()


async def get_recipes(num:int):
    recipe_data = await get_recipe_api(num,num)
        # 유효한 레시피 데이터가 있으면 반환
    await asyncio.sleep(1)
    print("task 1")
    if "error" not in recipe_data:
        return recipe_data

    # 모든 시도가 실패한 경우 에러 메시지 반환
    return {"error": "유효한 레시피를 찾을 수 없습니다. 다시 시도해 주세요."}

async def get_scrap(recipe_id:int) :
    recipe_data = await get_recipe_scrap(recipe_id)
    await asyncio.sleep(1)
    print("task 2")
        
    # 유효한 레시피 데이터가 있으면 반환
    if "error" not in recipe_data:
        return recipe_data
        
    # 모든 시도가 실패한 경우 에러 메시지 반환
    return {"error": "유효한 레시피를 찾을 수 없습니다. 다시 시도해 주세요."}

async def process_recipes():
    tasks = []
    num = 1
    while True:
        recipe_data = await get_recipes(num)
        if recipe_data:
            task = asyncio.create_task(recipe_service.add_recipe(recipe_data))
            tasks.append(task)
            num += 1
        else:
            break
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results

async def process_scraps():
    tasks = []
    recipe_id = 6803892
    while True:
        recipe_data = await get_scrap(recipe_id)
        if recipe_data:
            task = asyncio.create_task(recipe_service.add_recipe(recipe_data))
            tasks.append(task)
            recipe_id += 1        
        else:
            break
    results = await asyncio.gather(*tasks, return_exceptions=True)
    return results

async def ad_recipe():
    # 두 작업을 동시에 실행
    try :
        results = await asyncio.gather(
            process_recipes(),
            process_scraps()
        )

        for result in results:
            if isinstance(result, Exception):
                logger.error(f"레시피 추가 중 오류 발생: {result}")
            elif result.get("error"):
                logger.error(f"레시피 추가 중 오류 발생: {result['error']}")

        logger.info("모든 레시피 추가 작업이 완료되었습니다.")
    except Exception as e:
        logger.error(f"ad_recipe 함수 실행 중 예외 발생: {e}")



async def add_recipe():
    recipe_data = await get_recipe_api(2,3) # api에서 불러올때 데이터 형식
    #recipe_data = await get_scrap() -> 스크랩시에 데이터 형식
    result = await recipe_service.add_recipe(recipe_data)
    if result.get("error"):
        raise HTTPException(status_code=404, detail=result["error"])
    return {"message": "레시피가 성공적으로 추가되었습니다."}

async def search_recipes(query: str):
    results = await recipe_service.search_recipes(query)
    return results
