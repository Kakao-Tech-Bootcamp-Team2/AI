from app.repositorie.db_connection import DatabaseConnection
from app.service.preprocess.data_embedding import EmbeddingService
from app.model.recipe_model import Recipe
from typing import List

class RecipeService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.pinecone_repository = DatabaseConnection()

    async def add_recipe(self,recipe_data):
        print("레시피추가중")
        if "error" in recipe_data:
            return {"error": recipe_data["error"]}

        # 레시피 객체 생성
        recipe = Recipe(**recipe_data)

        # 텍스트 준비
        text = recipe.prepare_text_for_embedding()

        # 임베딩 생성
        embedding = self.embedding_service.embed_text([text])[0]

        # 벡터 및 메타데이터 저장
        self.pinecone_repository.upsert_recipe(embedding, recipe.to_metadata())

        return {"status": "success"}

    def get_filtered_recipes(self, query_ingredients: List[str]):
        # 입력 재료를 쉼표로 결합
        query_string = ", ".join(query_ingredients)

        # 임베딩 생성
        query_embedding = self.embedding_service.embed_query(query_string)

        # 저장소 계층에서 필터링된 결과 반환
        results = self.pinecone_repository.get_filtered_recipes(query_embedding, query_ingredients)
        print(results)
        return results