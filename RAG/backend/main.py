import uuid
from fastapi import FastAPI
import ollama
import chromadb
from langchain_text_splitters import RecursiveCharacterTextSplitter
import uvicorn
import schemas

app = FastAPI()

chroma_client = chromadb.Client()
ollama_client = ollama.Client(host="http://ollama:11434")

vectordb = chroma_client.get_or_create_collection(name="docs")

def get_embedding(prompt : str):
    embeddings = ollama_client.embeddings(model="mxbai-embed-large",prompt=prompt)
    return embeddings["embedding"]

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=700,
    chunk_overlap=200,
    separators=["\n\n", "\n", ".", " ", ""]
)
def chunk_text(text):
    return text_splitter.split_text(text)

def load_document():
    with open("document.txt", "r", encoding="utf-8") as f:
        text = f.read()
    chunks = chunk_text(text=text)

    for chunk in chunks:
        embedding = get_embedding(chunk)
        
        vectordb.add(
            documents=[chunk],
            embeddings=[embedding],
            ids=[str(uuid.uuid4())]
        )

@app.post("/askLLM")
def ask_question(request:schemas.askllm):
    
    query_embedding = get_embedding(request.user_input)
    results = vectordb.query(
        query_embeddings=[query_embedding],
        n_results=2
    )
    context = "\n".join(results["documents"][0])
    prompt = f"Answer only using context. Say I don't know if not in context. Context: {context} Question: {request.user_input}"
    response = ollama_client.chat(model="llama3.1:8b",
        messages=[{"role": "user", "content": prompt}]
    )
    return {
        "answer": response["message"]["content"],
        "context chunk": context
    }

if __name__ == "__main__":
    load_document()
    uvicorn.run(app=app,host="0.0.0.0",port=8000)