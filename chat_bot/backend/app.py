from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from groq_agent import chat

app = FastAPI()


class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
async def chat_api(req: ChatRequest):
    result = await chat(req.message)
    return {"response": result}


app.mount("/", StaticFiles(directory="../frontend", html=True), name="frontend")
