import chromadb
import uuid
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer


embedding = SentenceTransformer("all-mpnet-base-v2")
dimensions = 768
faiss_index = faiss.IndexFlatIP(dimensions)
recent_embeddings = []

class Localembed:
    def __call__(self, input):
        return embedding.encode(input).tolist()
    def name(self):
        return "Localembed"

embed = Localembed()
client = chromadb.PersistentClient(path=r"/Users/ravisharma/PycharmProjects/Newsly_remastered/Vectorbase")

base = client.get_or_create_collection("vectordata",embedding_function=embed)

def add_data(para,metadata):
    try:
        id = (str(uuid.uuid4()))
        base.add(documents=para, metadatas=metadata, ids=id)
        print("Added data to Vector Database!" )
    except Exception as e:
        print("ERROR :",e)

def delete_existing(metadata):
    try:
        base.delete(where={"doc_id":metadata["doc_id"]})
    except Exception as e:
        print("ERROR :",e)

def query_base(query,n = 2,where = None):
    if where != None:
        results = base.query(query_texts=query, n_results=n,where=where)
    else:
        results = base.query(query_texts=query,n_results=n)

    return results

def probability_calculator(results):
    if not results or not results.get('metadatas'):
        return 0

    metadatas = results['metadatas'][0]
    distances = results['distances'][0]

    if not metadatas or not distances:
        return 0

    score = 0
    total_weight = 0
    has_like = False
    has_dislike = False

    for prefer, dist in zip(metadatas, distances):
        weight = 1 / (dist + 1e-6)
        feedback = prefer.get("feedback", "").lower()
        if feedback == "like":
            score += weight
            has_like = True
        elif feedback == "dislike":
            score -= weight
            has_dislike = True
        total_weight += weight

    if total_weight == 0:
        return 0

    if has_like and has_dislike:
        # Mixed feedback – use full normalized formula
        probability = (score / total_weight + 1) / 2
    elif has_like:
        # Only positive feedback: estimate probability from weighted closeness
        probability = min(1.0, total_weight / (total_weight + 5))  # tunable
    elif has_dislike:
        # Only negative feedback: invert closeness
        probability = max(0.0, 1 - (total_weight / (total_weight + 5)))  # tunable
    else:
        probability = 0.5  # fallback

    return probability

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


if __name__ == '__main__':
    result = query_base(["heloooo"],n=3,where={"user_id":'7805cd98-58e6-421b-a561-8a24429cd421'})
    print(probability_calculator(result))


