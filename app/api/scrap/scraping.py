import requests, random, time
from bs4 import BeautifulSoup

def crawl_recipe():
    while True:
        recipe_id = random.randint(6803892, 7037297)  # 1000000부터 10000000 사이의 랜덤 ID 생성
        url = f"http://www.10000recipe.com/recipe/{recipe_id}"
        page = requests.get(url)
        
        # 페이지가 정상적으로 로드되지 않은 경우 예외 처리
        if page.status_code != 200:
            print(f"ID {recipe_id}에 대한 페이지를 불러오지 못했습니다.")
            # 랜덤한 시간 동안 대기
            wait_time = random.uniform(1, 3)
            print(f"{wait_time:.2f}초 동안 대기합니다...")
            time.sleep(wait_time)
            continue  # 다른 ID 시도
        
        soup = BeautifulSoup(page.content, 'html.parser')
        
        # "레시피 정보가 없습니다" 메시지 확인
        if soup.find(string="레시피 정보가 없습니다"):
            print(f"ID {recipe_id}에 대한 레시피 정보가 없습니다. 다른 ID를 시도합니다.")
            # 랜덤한 시간 동안 대기
            wait_time = random.uniform(1, 3)
            print(f"{wait_time:.2f}초 동안 대기합니다...")
            time.sleep(wait_time)
            continue  # 다른 ID 시도
        
        recipe_data = {}
        
        # 레시피 제목 추출
        title_div = soup.find('div', class_='view2_summary')
        if title_div:
            title = title_div.find('h3').get_text(strip=True)
            recipe_data['title'] = title
        else:
            print(f"ID {recipe_id}에 대한 레시피 제목을 찾을 수 없습니다. 다른 ID를 시도합니다.")
            wait_time = random.uniform(1, 3)
            print(f"{wait_time:.2f}초 동안 대기합니다...")
            time.sleep(wait_time)
            continue  # 다른 ID 시도
        
        # 재료 추출
        ingredients = {}
        ingredient_div = soup.find('div', class_='ready_ingre3')
        if ingredient_div:
            for ul in ingredient_div.find_all('ul'):
                category = ul.find('b').get_text(strip=True)
                items = [li.get_text(strip=True).replace("구매", "").strip() for li in ul.find_all('li')]
                ingredients[category] = items
        else:
            print(f"ID {recipe_id}에 대한 재료 정보를 찾을 수 없습니다. 다른 ID를 시도합니다.")
            wait_time = random.uniform(1, 3)
            print(f"{wait_time:.2f}초 동안 대기합니다...")
            time.sleep(wait_time)
            continue  # 다른 ID 시도
        recipe_data['ingredients'] = ingredients
        
        # 조리 단계 추출
        steps = []
        step_div = soup.find('div', class_='view_step')
        if step_div:
            for i, step in enumerate(step_div.find_all('div', class_='view_step_cont'), 1):
                steps.append(f"Step {i}: {step.get_text(strip=True)}")
        else:
            print(f"ID {recipe_id}에 대한 조리 단계를 찾을 수 없습니다. 다른 ID를 시도합니다.")
            wait_time = random.uniform(1, 3)
            print(f"{wait_time:.2f}초 동안 대기합니다...")
            time.sleep(wait_time)
            continue  # 다른 ID 시도
        recipe_data['steps'] = steps
        
        # 레시피 데이터를 찾은 경우 출력하고 계속 진행
        print(f"레시피 ID {recipe_id}를 찾았습니다:\n", recipe_data)
        
        # 다음 레시피 검색을 위해 랜덤한 시간 동안 대기
        wait_time = random.uniform(1, 3)
        print(f"{wait_time:.2f}초 동안 대기 후 다음 레시피 검색을 시작합니다...")
        time.sleep(wait_time)

# 테스트 실행
crawl_recipe()