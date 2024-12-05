import json
from app.core import setting
from langchain_openai import ChatOpenAI

def generate_response(user_query, search_response, model="gpt-4o-mini", temperature=0.5, max_tokens=1000, timeout=30, max_retries=3):
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
    
    prompt = f"""
    사용자가 소지한 재료: {user_query}
    관련 문서:
    {search_response}
    위의 사용자가 소지한 재료와 관련 문서를 참고하여 **레시피를 1개에서 5개 추천해주세요**.

    가능하다면, 추가적인 재료를 최소화하여 추천해 주세요.
    각 재료는 반드시 '재료명'과 '양'을 포함해야 합니다.

    다음과 같은 JSON 형식으로 답변해 주세요:

    {{
      "레시피 목록": [
        {{
          "레시피 id": "관련 문서의 recipe_id",
          "레시피 이름": "레시피 이름",
          "재료": [
            {{"재료명": "재료1", "양": "양1"}},
            {{"재료명": "재료2", "양": "양2"}}
          ],
          "조리 방법": ["조리 단계1", "조리 단계2"]
        }},
        ...
      ]
    }}

    위의 형식을 엄격히 따라주시고, 응답을 코드 블록으로 감싸지 말아주세요.
    """

    # 모델 호출 및 응답 생성
    response = llm.invoke([{"role": "user", "content": prompt}])
    assistant_content = response.content

    # JSON 내용 파싱
    try:
        recipe = json.loads(assistant_content)
    except json.JSONDecodeError as e:
        print("JSON 파싱 실패:", e)
        recipe = None

    return recipe