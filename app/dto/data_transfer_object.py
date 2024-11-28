from app.repositorie.db_connection import DatabaseConnection
from app.service.preprocess.data_embedding import EmbeddingService
from app.model.recipe_model import Recipe
from typing import List

class RecipeService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.pinecone_repository = DatabaseConnection()

    async def add_recipe(self,recipe_id,recipe_data):
        print("레시피추가중")
        if "error" in recipe_data:
            return {"error": recipe_data["error"]}

        # 레시피 객체 생성
        recipe = Recipe(recipe_id=recipe_id,**recipe_data)

        # 메타데이터 생성 전에 재료 전처리
        metadata = recipe.to_metadata()
        processed_ingredients = self.pinecone_repository.process_ingredients(metadata)
        cleaned_ingredients = self.pinecone_repository.strip_quantities(processed_ingredients)
        # 텍스트 준비
        ingredients_text = ", ".join(cleaned_ingredients)

        # 임베딩 생성
        embedding = self.embedding_service.embed_text([ingredients_text])[0]

        metadata['ingredients'] = cleaned_ingredients

        # 벡터 및 메타데이터 저장
        try:
            result = await self.pinecone_repository.upsert_recipe(recipe.recipe_id, embedding, metadata)
            print(f"레시피 {recipe_id} {result['status']}")
            print(metadata['ingredients'])
            print(metadata)
        except Exception as e:
            print(f"업서트 실패: {e}")
            return {"error": str(e)}

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