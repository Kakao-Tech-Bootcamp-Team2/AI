from typing import List, Dict
from app.repositorie.db_connection import DatabaseConnection
from app.service.preprocess.data_embedding import EmbeddingService

def search_recipes_by_text(query: str, top_k: int = 50) -> List[Dict]:
    # 쿼리 전처리
    if "," not in query:
        query_ingredients = [query.strip()]
    else:
        query_ingredients = [ingredient.strip() for ingredient in query.split(",")]
    
    print(f"전처리된 쿼리 재료: {query_ingredients}")  # 디버깅 로그 

    # 쿼리 임베딩 생성
    embedding_service = EmbeddingService()
    query_text = " ".join(query_ingredients)
    print(f"임베딩할 텍스트: {query_text}")  # 디버깅 로그 2
    
    query_embedding = embedding_service.embed_query(query_text)
    print(f"임베딩 벡터 길이: {len(query_embedding)}")  # 디버깅 로그
    
    return search_recipes(query_embedding, query_ingredients, top_k)

def search_recipes(query_embedding: List[float], query_ingredients: List[str], top_k: int = 50) -> List[Dict]:
    db = DatabaseConnection()
    
    # 디버깅 로그
    print(f"\n=== 검색 시작 ===")
    print(f"검색할 재료: {query_ingredients}")
    print(f"임베딩 벡터 샘플: {query_embedding[:5]}...")  # 처음 5개 값만 출력

    results = db.index.query(
        vector=query_embedding,
        top_k=top_k,
        include_metadata=True
    )

    print(f"\n=== 검색 결과 ===")
    print(f"총 매치 수: {len(results['matches'])}")

    if not results["matches"]:
        print("검색 결과가 없습니다.")
        return []

    # 'score'를 기준으로 매칭 결과 정렬
    sorted_matches = sorted(results["matches"], key=lambda x: x['score'], reverse=True)
    
    filtered_results = []

    for match in sorted_matches:
        match_id = match['id'] 
        match_ingredients = match["metadata"].get("ingredients", [])
        match_title = match["metadata"].get("title", "")
        raw_ingredients = match["metadata"].get("raw_ingredients", [])
        print(f"\n매칭 항목:")
        print(f"id : {match_id}")
        print(f"제목: {match_title}")
        print(f"재료: {match_ingredients}")
        print(f"날것의 재료: {raw_ingredients}")
        print(f"점수: {match['score']}")
        
        # 결과 딕셔너리에 'score'를 포함하지 않고 필요한 정보만 추가
        filtered_results.append({
            "id" : match_id,
            "title": match_title,
            "ingredients": raw_ingredients,
            "steps": match["metadata"].get("steps", [])
        })

    print(f"\n=== 최종 결과 ===")
    print(f"필터링된 결과 수: {len(filtered_results)}")
    
    return filtered_results
