import requests
from bs4 import BeautifulSoup

def get_recipe_scrap(recipe_id):
    url = f"http://www.10000recipe.com/recipe/{recipe_id}"
    page = requests.get(url)
        
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

