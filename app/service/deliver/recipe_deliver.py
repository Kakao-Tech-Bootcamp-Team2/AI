from app.repositorie.db_connection import DatabaseConnection
from app.service.preprocess.data_embedding import EmbeddingService
from app.model.recipe_model import Recipe
from app.service.scrap import get_recipe_scrap

class RecipeService:
    def __init__(self):
        self.embedding_service = EmbeddingService()
        self.pinecone_repository = DatabaseConnection()

    async def add_recipe(self, recipe_id: int):
        recipe_data = await get_recipe_scrap(recipe_id)
        if "error" in recipe_data:
            return {"error": recipe_data["error"]}

        # 레시피 객체 생성
        recipe = Recipe(**recipe_data)

        # 텍스트 준비
        text = recipe.prepare_text_for_embedding()

        # 임베딩 생성
        embedding = self.embedding_service.embed_text([text])[0]

        # 벡터 및 메타데이터 저장
        await self.pinecone_repository.upsert_recipe(recipe_id, embedding, recipe.to_metadata())

        return {"status": "success"}

    async def search_recipes(self, query: str):
        # 쿼리 임베딩 생성
        query_embedding = self.embedding_service.embed_query(query)

        # Pinecone에서 유사한 레시피 검색
        results = await self.pinecone_repository.search_recipes(query_embedding)

        return results