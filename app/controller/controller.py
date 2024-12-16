from app.service.scrap import get_recipe_scrap,get_recipe_id
from app.dto.data_transfer_object import RecipeService
import asyncio
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
recipe_service = RecipeService()

# 크롤링 제어를 위한 전역 변수
should_continue_crawling = True
_crawling_task = None
current_page = 1  # 현재 크롤링중인 페이지 번호를 저장

async def get_scrap(recipe_id:int):
    recipe_data = await get_recipe_scrap(recipe_id)
    await asyncio.sleep(1)
    print(f"task {recipe_id}")
    if "error" not in recipe_data:
        return recipe_data
    return None

async def process_scraps():
    global should_continue_crawling, current_page
    page_num = current_page  # 저장된 페이지 번호부터 시작
    tasks = []
    
    while should_continue_crawling:
        recipe_ids = await get_recipe_id(page_num)
        if 'error' in recipe_ids:
            logger.info(recipe_ids['error'])
            break
            
        for recipe_id in recipe_ids:  # 한 번에 40개씩 처리
            if not should_continue_crawling:
                logger.info("크롤링이 중지되었습니다.")
                current_page = page_num  # 중단 시점의 현재 페이지 저장
                return
                
            recipe_data = await get_scrap(recipe_id)
            if recipe_data:
                task = asyncio.create_task(recipe_service.add_recipe(recipe_id,recipe_data))
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
        current_page = page_num  # 페이지 번호 업데이트

async def add_recipe():
    global should_continue_crawling
    should_continue_crawling = True
    try:
        await process_scraps()
        logger.info("모든 레시피 추가 작업이 완료되었습니다.")
    except Exception as e:
        logger.error(f"add_recipe 함수 실행 중 예외 발생: {e}")

# 크롤링 상태 확인 함수 (True/False)
def is_crawling():
    global _crawling_task
    return _crawling_task is not None and not _crawling_task.done()

# 크롤링 일시정지 함수
def stop_crawling():
    global should_continue_crawling
    should_continue_crawling = False
    logger.info("크롤링 중지가 요청되었습니다.")

# 크롤링 재개 함수 (중단된 시점 이후부터)
async def resume_crawling():
    global _crawling_task, should_continue_crawling
    if _crawling_task is None or _crawling_task.done():
        should_continue_crawling = True
        _crawling_task = asyncio.create_task(add_recipe())
        logger.info(f"크롤링이 페이지 {current_page}부터 재개되었습니다.")
        return True
    return False

# 크롤링 중단 지점 초기화 및 시작 함수 (1페이지부터 다시 크롤링)
async def reset_crawling():
    global current_page
    current_page = 1
    return await resume_crawling()