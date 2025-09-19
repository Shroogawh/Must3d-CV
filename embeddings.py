from sentence_transformers import SentenceTransformer


embed_model = SentenceTransformer("sentence-transformers/intfloat/multilingual-e5-base")

def get_embedding(text: str):
    """
    تحويل النص إلى vector representation.
    """
    return embed_model.encode(text)
