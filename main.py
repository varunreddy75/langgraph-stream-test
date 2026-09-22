from typing import TypedDict

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from dotenv import load_dotenv

from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq

load_dotenv()

app = FastAPI()


class State(TypedDict):
    prompt: str
    generated_text: str


class PromptRequest(BaseModel):
    prompt: str


llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
)


@app.post("/stream")
async def stream(req: PromptRequest):

    def token_generator():
        for chunk in llm.stream(
            f"Write exactly 100 lines about {req.prompt}"
        ):
            if chunk.content:
                yield chunk.content

    return StreamingResponse(
        token_generator(),
        media_type="text/plain"
    )