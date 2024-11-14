from app.core import setting
from pinecone import Pinecone, ServerlessSpec
import uuid

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

    def search_recipes(self, query_embedding, top_k=5):  # 임시 검색 기능
        results = self.index.query(
            vector=query_embedding,
            top_k=top_k,
            include_metadata=True
        )
        return [match['metadata'] for match in results['matches']]