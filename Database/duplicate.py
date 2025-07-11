import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


embedding = SentenceTransformer("all-mpnet-base-v2")
dimensions = 768
faiss_index = faiss.IndexFlatIP(dimensions)
recent_embeddings = []


def check_for_duplicate(text,threshold=0.77):
    emb = embedding.encode(text,normalize_embeddings=True)
    emb_np = np.array([emb]).astype('float32')

    if len(recent_embeddings) == 0:
        recent_embeddings.append(emb_np)
        faiss_index.add(emb_np)
        return False

    d,_ = faiss_index.search(emb_np,1)
    if d[0][0] > threshold:
        return True

    faiss_index.add(emb_np)
    recent_embeddings.append(emb_np)

    if len(recent_embeddings) > 1000:
        faiss_index.reset()
        recent_embeddings[:] = recent_embeddings[-1000:]
        faiss_index.add(np.vstack(recent_embeddings))

    return False
