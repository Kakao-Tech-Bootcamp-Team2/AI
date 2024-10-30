from langchain.embeddings import HuggingFaceEmbeddings

model_name = "intfloat/multilingual-e5-large-instruct" #허깅페이스 기본
hf_embeddings = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs={"device": "cuda"},  
    encode_kwargs={"normalize_embeddings": True}
)

def prepare_text_for_embedding(recipe):
    title = recipe['title']
    ingredients_text = '\n'.join([
        f"{category}: {', '.join(items)}"
        for category, items in recipe['ingredients'].items()
    ])
    steps_text = '\n'.join([
        f"단계 {i+1}: {step}"
        for i, step in enumerate(recipe['steps'])
    ])
    full_text = f"{title}\n\n재료:\n{ingredients_text}\n\n조리 단계:\n{steps_text}"
    return full_text

def embed_text(texts):
    return hf_embeddings.embed_documents(texts)