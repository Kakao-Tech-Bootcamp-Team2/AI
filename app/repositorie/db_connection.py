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

    def upsert_recipe(self, embedding, metadata):
        unique_id = str(uuid.uuid4())
        # 벡터 업서트
        self.index.upsert(vectors=[
            {
                'id': unique_id,
                'values': embedding,
                'metadata': metadata
            }
        ])

    def extract_ingredient_name(self,ingredient:str) -> str : #재료 데이터에서 ()등 제거
        return re.match(r'([^(]+)', ingredient).group(1).strip()
    
    def process_ingredients(self, recipe_metadata: Dict) -> List[str]: #메타데이터에서 재료만 추출
        return [self.extract_ingredient_name(ing) for ing in recipe_metadata['ingredients']]

    def get_filtered_recipes(self, query_embedding, query_ingredients: List[str], top_k=100):
        # Pinecone에서 검색
        print("Query Embedding:", query_embedding)  # Query Embedding 확인
        print("Query Ingredients:", query_ingredients)  # Query Ingredients 확인

        results = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )

        # Pinecone에서 반환된 결과 확인
        print("Raw Results:", results)
        if not results["matches"]:
            print("No matches found in Pinecone index.")
            return []

        # 결과 필터링: query_ingredients에 포함된 재료만 있는 레시피 반환
        filtered_results = []
        for match in results["matches"]:
            match_ingredients = match["metadata"].get("ingredients", [])
            print("Match Title:", match["metadata"].get("title", ""))
            print("Match Ingredients:", match_ingredients)

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