import os
import requests
import json
from bs4 import BeautifulSoup

def get_recipe_scrap(recipe_id):
    url = f"http://www.10000recipe.com/recipe/{recipe_id}"
    page = requests.get(url)

    try:
        page = requests.get(url, timeout=10)
    
    # 서버 연결 문제나 요청 실패 시 예외 발생 방지를 위해 예외 처리 
    except requests.RequestException as e:
        return {"error": f"ID {recipe_id}에 대한 페이지 요청 중 오류 발생: {e}"}
    
    # 페이지가 정상적으로 로드되지 않은 경우 예외 처리
    if page.status_code != 200:
        return {"error": f"ID {recipe_id}에 대한 페이지를 불러오지 못했습니다."}
        
    soup = BeautifulSoup(page.content, 'html.parser')
        
    # "레시피 정보가 없습니다" 메시지 확인
    if soup.find(string="레시피 정보가 없습니다"):
        return {"error": f"ID {recipe_id}에 대한 레시피 정보가 없습니다."}
    
        
    recipe_data = {}
        
    # 레시피 제목 추출
    title_div = soup.find('div', class_='view2_summary')
    if title_div:
        title = title_div.find('h3').get_text(strip=True)
        recipe_data['title'] = title
    else:
        return {"error": f"ID {recipe_id}에 대한 레시피 제목을 찾을 수 없습니다."}
        
    # 재료 추출
    ingredients = {}
    ingredient_div = soup.find('div', class_='ready_ingre3')
    if ingredient_div:
        for ul in ingredient_div.find_all('ul'):
            category = ul.find('b').get_text(strip=True)
            items = [li.get_text(strip=True).replace("구매", "").strip() for li in ul.find_all('li')]
            ingredients[category] = items
    else:
        return {"error": f"ID {recipe_id}에 대한 재료 정보를 찾을 수 없습니다."}
    recipe_data['ingredients'] = ingredients
        
    # 조리 단계 추출
    steps = []
    step_div = soup.find('div', class_='view_step')
    if step_div:
        for i, step in enumerate(step_div.find_all('div', class_='view_step_cont'), 1):
            steps.append(f"Step {i}: {step.get_text(strip=True)}")
    else:
        return {"error": f"ID {recipe_id}에 대한 조리 단계를 찾을 수 없습니다."}
    recipe_data['steps'] = steps

    return recipe_data  # 유효한 레시피 데이터 반환

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