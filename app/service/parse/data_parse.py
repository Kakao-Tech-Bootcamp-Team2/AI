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