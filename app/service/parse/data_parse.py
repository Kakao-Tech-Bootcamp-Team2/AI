import xml.etree.ElementTree as ET

def parse_data(xml_string):
    try:
        root = ET.fromstring(xml_string)
    except ET.ParseError as e:
        raise ValueError(f"XML 파싱 오류: {e}")

    recipes = []
    for row in root.findall('row'):
        title = row.find('RCP_NM').text if row.find('RCP_NM') is not None else "제목 없음"
        ingredients_detail = row.find('RCP_PARTS_DTLS').text if row.find('RCP_PARTS_DTLS') is not None else ""
        
        steps = []
        for i in range(1, 21):
            step = row.find(f'MANUAL{i:02d}')
            if step is not None and step.text:
                steps.append(f'Step {i}: {step.text.strip()}')

        recipe = {
            'title': title,
            'ingredients_detail': ingredients_detail,
            'steps': steps
        }
        recipes.append(recipe)
    return recipes

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
