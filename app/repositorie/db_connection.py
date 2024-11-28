from app.core import setting
from pinecone import Pinecone, ServerlessSpec
import uuid
import re
from typing import List,Dict

class DatabaseConnection:
    def __init__(self):
        # Pinecone 인스턴스 생성
        pc = Pinecone(api_key=setting.PINECONE_API_KEY)

        index_name = "recipes"
        dimension = 1024  # 벡터의 차원 수

        # 인덱스 존재 여부 확인
        if index_name not in pc.list_indexes().names():
            # 인덱스 생성
            pc.create_index(
                name=index_name,
                dimension=dimension,
                metric='cosine',
                spec=ServerlessSpec(
                    cloud='aws',
                    region='us-east-1'
                )
            )
            print(f"인덱스 '{index_name}'가 생성되었습니다.")
        else:
            print(f"인덱스 '{index_name}'는 이미 존재합니다. 기존 인덱스를 사용합니다.")

        # 인덱스 불러오기
        self.index = pc.Index(index_name)

    async def upsert_recipe(self, recipe_id, embedding, metadata):
        # ID로 기존 데이터 검색
        existing_data = self.index.fetch(ids=[str(recipe_id)])
        
        if existing_data.vectors:
            # 기존 데이터가 있으면 업데이트
            print(f"레시피 {recipe_id} 업데이트 중...")
            self.index.update(
                id=str(recipe_id),
                values=embedding,
                metadata=metadata
            )
            return {"status": "updated"}
        else:
            # 새로운 데이터 삽입
            print(f"새로운 레시피 {recipe_id} 추가 중...")
            self.index.upsert(vectors=[{
                'id': str(recipe_id),
                'values': embedding,
                'metadata': metadata
            }])
            return {"status": "inserted"}

    # 재료 이름에서 양과 단위를 제거하는 함수
    def strip_quantities(self, ingredients: List[str]) -> List[str]:
        cleaned_ingredients = []
        for ingredient in ingredients:
            # 숫자와 단위 제거를 위한 더 포괄적인 패턴
            ingredient = re.sub(r'\d+\.?\d*[a-zA-Z가-힣]*', '', ingredient)
            # 분수 형태 제거
            ingredient = re.sub(r'\d+\/\d+', '', ingredient)
            # 측정 단위 제거
            ingredient = re.sub(r'(약간|T|t|컵|큰술|작은술|숟가락|스푼|g|kg|ml|L)', '', ingredient)
            # 남은 숫자들 제거
            ingredient = re.sub(r'\d+', '', ingredient)
            # 특수문자 제거 (슬래시, 물결표 등)
            ingredient = re.sub(r'[/~]+', '', ingredient)
            # 양쪽 공백 제거하고 결과 추가
            cleaned = ingredient.strip()
            if cleaned:  # 빈 문자열이 아닌 경우만 추가
                cleaned_ingredients.append(cleaned)
        return cleaned_ingredients
    
    def extract_ingredient_name(self, ingredient:str) -> str:
        # 괄호와 슬래시, 물결표 등 불필요한 문자 제거
        return re.match(r'([^(/~]+)', ingredient).group(1).strip()
    
    def process_ingredients(self, recipe_metadata: Dict) -> List[str]: #메타데이터에서 재료만 추출
        return [self.extract_ingredient_name(ing) for ing in recipe_metadata['ingredients']]

    def get_filtered_recipes(self, query_embedding, query_ingredients: List[str], top_k=100):
        # Pinecone에서 검색
        print("쿼리 임베딩 :", query_embedding)  # Query Embedding 확인
        print("쿼리 재료 : :", query_ingredients)  # Query Ingredients 확인

        results = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )

        # Pinecone에서 반환된 결과 확인
        print("pinecone 정보:", results)
        if not results["matches"]:
            print("No matches found in Pinecone index.")
            return []

        # 결과 필터링: query_ingredients에 포함된 재료만 있는 레시피 반환
        filtered_results = []
        for match in results["matches"]:
            match_ingredients = match["metadata"].get("ingredients", [])
            print("매칭 타이틀:", match["metadata"].get("title", ""))
            print("매칭 재료:", match_ingredients)

            # 필터링 조건 확인
            if all(ingredient in match_ingredients for ingredient in query_ingredients):
                print("Match Passed Filter:", match["metadata"].get("title", ""))
                filtered_results.append({
                    "title": match["metadata"].get("title", ""),
                    "ingredients": {"all": match_ingredients},
                    "steps": match["metadata"].get("steps", [])
                })
            else:
                print("Match Failed Filter:", match["metadata"].get("title", ""))

        print("Filtered Results:", filtered_results)  # 최종 필터링된 결과 확인
        return filtered_results