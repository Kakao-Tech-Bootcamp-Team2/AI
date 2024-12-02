from langchain_huggingface import HuggingFaceEmbeddings

class EmbeddingService:
    _instance = None
    _embedding_model = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.model_name = "intfloat/multilingual-e5-large-instruct"
            cls._instance._embedding_model = HuggingFaceEmbeddings(model_name=cls._instance.model_name)
        return cls._instance

    def __init__(self):
        pass

    def embed_text(self, texts):
        return self._embedding_model.embed_documents(texts)

    def embed_query(self, query):
        return self._embedding_model.embed_query(query)