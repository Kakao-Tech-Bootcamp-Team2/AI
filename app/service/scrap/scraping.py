import aiohttp
import ssl
from bs4 import BeautifulSoup
from app.service.parse import parse_scrap_data,parse_scrap_id

# SSL 컨텍스트 설정 (비동기 방식으로 인한 SSL 인증서 오류 해결)
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

    
async def get_recipe_id(page_number):
    url = f"https://www.10000recipe.com/recipe/list.html?order=date&page={page_number}"
    try:
        # SSL 컨텍스트를 connector에 적용
        connector = aiohttp.TCPConnector(ssl=ssl_context)
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(url, timeout=10) as response:
                if response.status != 200:
                    return {"error": f"페이지 {page_number}를 불러오지 못했습니다."}
                content = await response.text()
    except aiohttp.ClientError as e:
        return {"error": f"페이지 요청 중 오류 발생: {e}"}
    
    soup = BeautifulSoup(content, 'html.parser')
    
    if soup.find(string="레시피 정보가 없습니다"):
        return {"error": f"페이지 {page_number}에 레시피 정보가 없습니다."}

    # 파싱 함수 호출
    recipe_ids = parse_scrap_id(soup)
    soup.decompose()

    return recipe_ids



async def get_recipe_scrap(recipe_id):
    url = f"https://www.10000recipe.com/recipe/{recipe_id}"
    try:
        # SSL 컨텍스트를 connector에 적용
        connector = aiohttp.TCPConnector(ssl=ssl_context)
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(url, timeout=10) as response:
                if response.status != 200:
                    return {"error": f"ID {recipe_id}에 대한 페이지를 불러오지 못했습니다."}
                content = await response.text(errors='ignore')  # 오류 무시
    except aiohttp.ClientError as e:
        return {"error": f"ID {recipe_id}에 대한 페이지 요청 중 오류 발생: {e}"}

    try:
        soup = BeautifulSoup(content, 'html.parser')
        if soup.find(string="레시피 정보가 없습니다"):
            return {"error": f"ID {recipe_id}에 대한 레시피 정보가 없습니다."}
        recipe_data = parse_scrap_data(soup, recipe_id)
        return recipe_data
    finally:
        if 'soup' in locals():
            soup.decompose()