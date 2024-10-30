from app.core import setting
from pinecone import Pinecone, ServerlessSpec

class DatabaseConnection :
    def __init__(self) :
        pc = Pinecone(api_key = setting.PINECONE_API_KEY)
        index_name = "recipes"
        pc.create_index(
        name=index_name,
        dimension=1024,
        metric='cosine',
        spec=ServerlessSpec(
            cloud="aws",
            region="us-east-1"
            )
        )
        self.index = pc.Index(index_name)
        self.vector_store = Pinecone(self.index,setting.PINECONE_HOST_URL,"text")

    def upsert_recipe(self, recipe_id,embedding,metadata) :
        self.index.upsert([(str(recipe_id), embedding, metadata)])

    def search_recipes(self, query_embedding, top_k=5): #임시 찾는 기능
        results = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )
        return [match['metadata'] for match in results['matches']]