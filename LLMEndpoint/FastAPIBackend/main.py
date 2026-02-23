import json
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from ollama import AsyncClient

import uvicorn
import schemas

messages = [{"role":"system","content":"You are a cinephile and movie expert. Recommend movies as the type user wants."}]

app = FastAPI()
CORSOrigins = [
    "http://localhost:5173"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORSOrigins, 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = AsyncClient(host="http://ollama:11434")

@app.post("/LLMChat")
async def LLM_Chat(Request:schemas.ChatRequest):
    messages.append({"role":"user","content":Request.user_input})
    async def generate():
        assistant_reply = ""
        async for chunk in await client.chat(model="llama3.1:8b",messages=messages,options={"temperature":1},stream=True):
            content = chunk["message"]["content"]
            yield json.dumps({"text":content})+"\n"
            assistant_reply += content
        messages.append({"role":"assistant","content":assistant_reply})
    return StreamingResponse(generate(),media_type="text/event-stream")

if __name__ == "__main__":
    uvicorn.run(app=app,host="0.0.0.0",port=8000)