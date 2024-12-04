import json
from app.core import setting
from langchain_openai import ChatOpenAI
from langchain.output_parsers import StructuredOutputParser, ResponseSchema

def generate_response(user_query, search_response, model="gpt-4o-mini", temperature=0.7, max_tokens=500, timeout=30, max_retries=3):
    api_key = setting.OPENAI_API_KEY
    if not api_key:
        raise ValueError("OPENAI_API_KEY 환경 변수가 설정되지 않았습니다.")
    
    llm = ChatOpenAI(
        model=model,
        temperature=temperature,
        max_tokens=max_tokens,
        timeout=timeout,
        max_retries=max_retries,
        api_key=api_key
    )

    # 후처리 설정
    response_schemas = [
        ResponseSchema(name="레시피 이름", description="레시피의 이름"),
        ResponseSchema(
            name="재료",
            description="재료 목록. 각 재료는 '재료명'과 '양'을 포함하는 객체입니다.",
            type="list",
            items={
                "type": "object",
                "properties": {
                    "재료명": {"type": "string", "description": "재료의 이름"},
                    "양": {"type": "string", "description": "재료의 양"}
                }
            }
        ),
        ResponseSchema(name="조리 방법", description="조리 방법에 대한 순서별 설명", type="list"),
    ]
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
    format_instructions = output_parser.get_format_instructions()

    prompt = f"""
    사용자가 소지한 재료: {user_query}
    관련 문서:
    {search_response}
    위의 사용자가 소지한 재료와 관련 문서를 참고하여 레시피를 추천해주세요.

    {format_instructions}

    가능하다면, 추가적인 재료를 최소화하여 추천해 주세요.
    """

    # 모델 호출 및 응답 생성
    response = llm.invoke([{"role": "user", "content": prompt}])
    assistant_content = response.content

    # 코드 블록 마크다운 제거
    if assistant_content.startswith("```json"):
        assistant_content = assistant_content.strip("```json").strip("```").strip()

    # JSON 내용 파싱
    try:
        recipe = json.loads(assistant_content)
    except json.JSONDecodeError as e:
        print("JSON 파싱 실패:", e)
        recipe = None

    return recipe