from langchain_huggingface import HuggingFaceEmbeddings
class EmbeddingService:
    def __init__(self):
        self.model_name = "intfloat/multilingual-e5-large-instruct"
        self.embedding_model = HuggingFaceEmbeddings(model_name=self.model_name)

    def embed_text(self, texts):
        return self.embedding_model.embed_documents(texts)

    def embed_query(self, query):
        return self.embedding_model.embed_query(query)