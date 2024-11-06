import aiohttp
import ssl
from bs4 import BeautifulSoup
from app.service.parse import parse_scrap_data  # parse.py에서 파싱 함수 임포트

async def get_recipe_scrap(recipe_id):
    url = f"https://www.10000recipe.com/recipe/{recipe_id}"
    
    # SSL 컨텍스트 설정 (비동기 방식으로 인한 SSL 인증서 오류 해결)
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    
    try:
        # SSL 컨텍스트를 connector에 적용
        connector = aiohttp.TCPConnector(ssl=ssl_context)
        async with aiohttp.ClientSession(connector=connector) as session:
            async with session.get(url, timeout=10) as response:
                if response.status != 200:
                    return {"error": f"ID {recipe_id}에 대한 페이지를 불러오지 못했습니다."}
                content = await response.text()
    except aiohttp.ClientError as e:
        return {"error": f"ID {recipe_id}에 대한 페이지 요청 중 오류 발생: {e}"}
    
    soup = BeautifulSoup(content, 'html.parser')
    
    if soup.find(string="레시피 정보가 없습니다"):
        return {"error": f"ID {recipe_id}에 대한 레시피 정보가 없습니다."}
    
    # 파싱 함수 호출
    recipe_data = parse_scrap_data(soup, recipe_id)
    
    return recipe_data
'''
# 레시피 데이터 json 파일로 저장
download_folder = os.path.join(os.path.expanduser("~"), "Downloads")
filename = os.path.join(download_folder, "crawled_recipes.json")

def crawl_recipes_to_json(start_id, end_id, filename=filename):
    # 파일이 존재하면 기존 데이터를 불러오기
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            recipe_list = json.load(f)
            existing_ids = {recipe["recipe_id"] for recipe in recipe_list}  # 기존 recipe_id를 집합으로 저장
    else:
        recipe_list = []  # 파일이 없으면 빈 리스트로 시작
        existing_ids = set()  # 빈 집합으로 시작
    
    
    for recipe_id in range(start_id, end_id + 1):
        if recipe_id in existing_ids:  # 중복된 recipe_id 건너뛰기
            print(f"ID {recipe_id}은 이미 존재합니다. 건너뜁니다.")
            continue
        
        recipe = get_recipe_scrap(recipe_id)
        if "error" not in recipe:
            # 레시피 정보를 딕셔너리로 변환하여 리스트에 추가
            recipe_info = {
                "recipe_id": recipe_id,
                "title": recipe['title'],
                "ingredients": recipe['ingredients'],
                "steps": recipe['steps']
            }
            recipe_list.append(recipe_info)  # 레시피 정보를 리스트에 추가
            print(f"ID {recipe_id} 레시피 수집 완료: {recipe['title']}")
        else:
            print(recipe["error"])
    
    # 리스트를 JSON 파일로 저장
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(recipe_list, f, ensure_ascii=False, indent=4)
    print(f"수집된 레시피 데이터를 {filename}에 저장했습니다.")


# 레시피 크롤링 실행 코드
crawl_recipes_to_json(7035599, 7035610)  # 테스트할 때는 이 구간 근처로 설정해보세요

# 데이터 반환 확인용 코드 (오류 발생 시 테스트용))
# print(get_recipe_scrap(128671))
'''