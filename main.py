from typing import TypedDict

from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

from langgraph.graph import StateGraph, START, END
from langchain_groq import ChatGroq

load_dotenv()

app = FastAPI()


# ----------------------------
# Request Schema
# ----------------------------

class PromptRequest(BaseModel):
    prompt: str


# ----------------------------
# LangGraph State
# ----------------------------

class State(TypedDict):
    prompt: str
    generated_text: str


# ----------------------------
# LLM
# ----------------------------

llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
)


# ----------------------------
# Node
# ----------------------------

def generate_text(state: State):
    full_text = ""

    print("\n--- STREAM START ---\n")

    for chunk in llm.stream(
        f"Write exactly 10 lines about {state['prompt']}"
    ):
        if chunk.content:
            print(chunk.content, end="", flush=True)
            full_text += chunk.content

    print("\n\n--- STREAM END ---\n")

    return {
        "generated_text": full_text
    }


# ----------------------------
# Build Graph
# ----------------------------

builder = StateGraph(State)

builder.add_node("generate_text", generate_text)

builder.add_edge(START, "generate_text")
builder.add_edge("generate_text", END)

graph = builder.compile()


# ----------------------------
# API
# ----------------------------

@app.get("/")
def health():
    return {"status": "running"}


@app.post("/generate")
def generate(req: PromptRequest):

    result = graph.invoke(
        {
            "prompt": req.prompt,
            "generated_text": ""
        }
    )

    return {
        "prompt": req.prompt,
        "generated_text": result["generated_text"]
    }