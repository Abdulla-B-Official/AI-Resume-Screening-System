import numpy as np
import torch
from sentence_transformers import SentenceTransformer

# Using a lightweight, ultra-fast model or optimized BGE model for real-time inference
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
QUERY_PREFIX = ""

device = "cuda" if torch.cuda.is_available() else "cpu"
_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME, device=device)
        _model.eval()
    return _model

def chunk_text(text, max_words=100):
    chunks, buffer, count = [], [], 0
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue
        n = len(line.split())
        if count + n > max_words and buffer:
            chunks.append(" ".join(buffer))
            buffer, count = [], 0
        buffer.append(line)
        count += n
    if buffer:
        chunks.append(" ".join(buffer))
    return chunks if chunks else [text]

def embed(texts, is_query=False):
    model = get_model()
    if not texts:
        return np.zeros((0, model.get_sentence_embedding_dimension()), dtype="float32")
    
    with torch.no_grad():
        embeddings = model.encode(
            texts,
            batch_size=64,
            normalize_embeddings=True,
            convert_to_numpy=True,
            show_progress_bar=False
        )
    return embeddings