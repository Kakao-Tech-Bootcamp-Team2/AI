from app.service.request import get_recipe_api
from app.service.scrap import get_recipe_scrap,get_recipe_id
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

async def get_scrap(recipe_id:int):
    recipe_data = await get_recipe_scrap(recipe_id)
    await asyncio.sleep(1)
    print(f"task {recipe_id}")
    if "error" not in recipe_data:
        return recipe_data
    return None

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
    page_num = 1
    tasks = []
    while True:
        recipe_ids = await get_recipe_id(page_num)
        if 'error' in recipe_ids:
            logger.info(recipe_ids['error'])
            break
        for recipe_id in recipe_ids:  # 한 번에 40개씩 처리
            recipe_data = await get_scrap(recipe_id)
            if recipe_data:
                task = asyncio.create_task(recipe_service.add_recipe(recipe_data))
                tasks.append(task)
            else:
                logger.info(f"레시피 ID {recipe_id}에서 데이터를 찾을 수 없습니다.")
        if tasks:
            try:
                results = await asyncio.gather(*tasks, return_exceptions=True)
                for result in results:
                    if isinstance(result, Exception):
                        logger.error(f"레시피 추가 중 오류 발생: {result}")
            except Exception as e:
                logger.error(f"태스크 실행 중 예외 발생: {e}")
        else:
            logger.info("유효한 태스크가 없습니다. 1초 대기 후 재시도합니다.")
            await asyncio.sleep(1)  # 데이터가 없을 경우 잠시 대기
        page_num += 1


async def add_recipe():
    try:
        await process_scraps()
        logger.info("모든 레시피 추가 작업이 완료되었습니다.")
    except Exception as e:
        logger.error(f"add_recipe 함수 실행 중 예외 발생: {e}")

