from sentence_transformers import SentenceTransformer
import os
from dotenv import load_dotenv

load_dotenv()

EMBED_MODEL = os.getenv("EMBED_MODEL", "intfloat/multilingual-e5-base")
embed_model = SentenceTransformer(EMBED_MODEL)

def get_embedding(text: str):
    """
    تحويل النص إلى تمثيل متجهي.
    """
    return embed_model.encode(text)
