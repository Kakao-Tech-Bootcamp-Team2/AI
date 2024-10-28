import requests
from bs4 import BeautifulSoup

def crawl_recipe(recipe_id):
    url = f"http://www.10000recipe.com/recipe/{recipe_id}"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    recipe_data = {}
    
    # 레시피 제목 추출
    title = soup.find('div', class_='view2_summary').find('h3').get_text(strip=True)
    recipe_data['title'] = title
    
    # 재료 추출
    ingredients = {}
    ingredient_div = soup.find('div', class_='ready_ingre3')
    for ul in ingredient_div.find_all('ul'):
        category = ul.find('b').get_text(strip=True)
        items = [li.get_text(strip=True).replace("구매", "").strip() for li in ul.find_all('li')]
        ingredients[category] = items
    recipe_data['ingredients'] = ingredients
    
    # 조리 단계 추출
    steps = []
    step_div = soup.find('div', class_='view_step')
    for i, step in enumerate(step_div.find_all('div', class_='view_step_cont'), 1):
        steps.append(f"Step {i}: {step.get_text(strip=True)}")
    recipe_data['steps'] = steps
    
    return recipe_data

print(crawl_recipe(7035836))