import chromadb
import uuid
from sentence_transformers import SentenceTransformer

embedding = SentenceTransformer("all-mpnet-base-v2")

class Localembed:
    def __call__(self, input):
        return embedding.encode(input).tolist()
    def name(self):
        return "Localembed"

embed = Localembed()
client = chromadb.PersistentClient(path=r"Vectorbase")

base = client.get_or_create_collection("vectordata",embedding_function=embed)

def add_data(para,metadata):
    try:
        id = (str(uuid.uuid4()))
        base.add(documents=para, metadatas=metadata, ids=id)
        print("Added data to Vector Database!" )
    except Exception as e:
        print("ERROR :",e)


def query_base(query,n = 2,where = None):
    print(where)
    if where != None:
        results = base.query(query_texts=query, n_results=n,where=where)
    else:
        results = base.query(query_texts=query,n_results=n)

    return results

def probability_calculator(results):
    probability_list = []
    if not results or not results['metadatas']:
        return 0
    for j in range(len(results['metadatas'])):
        metadatas = results['metadatas'][j]
        distances = results['distances'][j]
        if not metadatas or not distances:
            return 0
        score = 0
        total_weight = 0
        for prefer, dist in zip(metadatas, distances):
            weight = 1 / (dist + 1e-6)
            if prefer["feedback"].lower() == "like":
                score += weight
            elif prefer["feedback"].lower() == "dislike":
                score -= weight
            total_weight += weight

        if total_weight == 0:
            return 0

        probability = (score / total_weight + 1) / 2
        probability_list.append(probability)
    return probability_list


