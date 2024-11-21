import xml.etree.ElementTree as ET

def parse_api_data(xml_string):
    recipe_data = {}

    try:
        root = ET.fromstring(xml_string)
    except ET.ParseError as e:
        return {"error": f"XML 파싱 오류: {e}"}

    # 첫 번째 레시피 정보를 가져옵니다.
    row = root.find('.//row')
    if row is None:
        return {"error": "레시피 정보를 찾을 수 없습니다."}

    # 레시피 제목 추출
    title_element = row.find('RCP_NM')
    if title_element is not None and title_element.text:
        recipe_data['title'] = title_element.text.strip()
    else:
        return {"error": "레시피 제목을 찾을 수 없습니다."}

    # 재료 추출
    ingredients_detail = row.find('RCP_PARTS_DTLS')
    if ingredients_detail is not None and ingredients_detail.text:
        # 재료를 딕셔너리 형태로 변환
        ingredients_list = [ingredient.strip() for ingredient in ingredients_detail.text.split(',')]
        ingredients = {'재료': ingredients_list}
        recipe_data['ingredients'] = ingredients
    else:
        return {"error": "재료 정보를 찾을 수 없습니다."}

    # 조리 단계 추출
    steps = []
    for i in range(1, 21):
        step_element = row.find(f'MANUAL{i:02d}')
        if step_element is not None and step_element.text:
            steps.append(f'Step {i}: {step_element.text.strip()}')
    if steps:
        recipe_data['steps'] = steps
    else:
        return {"error": "조리 단계를 찾을 수 없습니다."}

    return recipe_data

def parse_scrap_data(soup, recipe_id):
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
            b_tag = ul.find('b')
            category = b_tag.get_text(strip=True) if b_tag else "재료"
            items = [li.get_text(strip=True).replace("구매", "").strip() for li in ul.find_all('li')]
            ingredients[category] = items
        recipe_data['ingredients'] = ingredients
    else:
        return {"error": f"ID {recipe_id}에 대한 재료 정보를 찾을 수 없습니다."}
    
    # 조리 단계 추출
    steps = []
    step_div = soup.find('div', class_='view_step')
    if step_div:
        for i, step in enumerate(step_div.find_all('div', class_='view_step_cont'), 1):
            steps.append(f"Step {i}: {step.get_text(strip=True)}")
        recipe_data['steps'] = steps
    else:
        return {"error": f"ID {recipe_id}에 대한 조리 단계를 찾을 수 없습니다."}
    
    return recipe_data

def parse_scrap_id(soup):
    # 레시피 링크를 선택
    recipe_links = soup.select('a.common_sp_link')
    # 각 링크에서 레시피 ID 추출
    recipe_ids = [link['href'].split('/')[-1] for link in recipe_links]
    return recipe_ids
