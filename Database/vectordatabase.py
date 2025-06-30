import chromadb
import uuid

client = chromadb.PersistentClient(path=r"F:\GraphNewsly\Database\Vectorbase")

base = client.get_or_create_collection("vectordata")

def add_data():
    try:
        with open('temp.txt', 'r', encoding='utf-8') as f:
            data = f.read()
        data = eval(data)
        para = []
        metadata = []
        for i in data:
            points = '.'.join(i["Paragraphs"])
            para.append(points)
            del i['Paragraphs']
            metadata.append(i)
        id = [str(uuid.uuid4()) for _ in range(len(data))]
        base.add(documents=para, metadatas=metadata, ids=id)
        print("Added data to Vector Database!" )
    except Exception as e:
        print("ERROR :",e)


def query_base(query,n = 2,where = None):
    if where != None:
        results = base.query(query_texts=query, n_results=n,where=where)
    else:
        results = base.query(query_texts=query,n_results=n)

    return results

if __name__ == '__main__':
    print(query_base(["Indian Railways is set to revamp its"]))