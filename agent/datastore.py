import json, glob, os
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from config import emb

RAW, VDB = {}, None

def _as_records(data):
    if isinstance(data, list):
        return [r for r in data if isinstance(r, dict)]
    if isinstance(data, dict):
        recs = [r for v in data.values() if isinstance(v, list)
                for r in v if isinstance(r, dict)]
        return recs or [data]
    return []

def build(folder="data"):
    global VDB
    docs = []
    for path in glob.glob(f"{folder}/*.json"):
        name = os.path.basename(path)
        for i, rec in enumerate(_as_records(json.load(open(path)))):
            tag = f"{name}#{i}"
            RAW[tag] = rec
            sentence = f"{name} record: " + ", ".join(f"{k}={v}" for k, v in rec.items())
            docs.append(Document(page_content=sentence, metadata={"source": tag}))
    VDB = FAISS.from_documents(docs, emb)
    print(f"Indexed {len(docs)} records from {folder}/")

def search(query, k=8):
    return [{"source": d.metadata["source"], "record": d.page_content}
            for d in VDB.similarity_search(query, k=k)]