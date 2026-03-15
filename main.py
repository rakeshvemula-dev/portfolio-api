from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import httpx
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = FastAPI(title="Portfolio Chat API")

# ===== CORS SETUP =====
# This allows your portfolio frontend to call this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",  # Live Server local dev
        "http://localhost:5500",  # Localhost dev
        "https://rakeshvemula.vercel.app",  # Production (update later)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===== REQUEST MODEL =====
class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]


# ===== RESPONSE MODEL =====
class ChatResponse(BaseModel):
    reply: str


# ===== SYSTEM CONTEXT =====
SYSTEM_CONTEXT = """
You are an AI assistant embedded in Rakesh Vemula's portfolio website.
Answer questions about Rakesh in a helpful, concise and conversational tone.
IMPORTANT: Never use markdown formatting — no bold, no bullet points, no dashes, no headers.
Write in plain natural sentences only, like you're having a conversation.
Keep answers brief and to the point — 3 to 5 sentences maximum.
Only answer questions related to Rakesh's background, skills, projects, and experience.
If asked something unrelated, politely redirect.

NAME: Rakesh Vemula
LOCATION: Hyderabad, Telangana, India
EMAIL: rakeshvemula14300@gmail.com
LINKEDIN: linkedin.com/in/iamrakeshvemula
GITHUB: github.com/rakeshvemula-dev

SUMMARY:
CS Graduate (2025) specializing in AI/GenAI application development.
Focused on building LLM-powered backends, RAG systems, and Agentic Workflows using Python.

SKILLS:
- AI/LLM: LLMs (Gemini, OpenAI), RAG Systems, Prompt Engineering, LangChain, Google Vertex AI
- Backend: Python, FastAPI, Flask, REST APIs, SQL
- Tools: Git/GitHub, VS Code, Postman, Docker (learning), Google Cloud

PROJECTS:
1. Artisan AI — Full-stack GenAI app that automates marketing content for artisans.
   Stack: Python, Flask, React, Google Gemini API, Cloudinary

2. Spotify Song Segmentation — Unsupervised ML pipeline clustering songs by audio features.
   Stack: Python, K-Means, Scikit-learn

3. Cardiovascular Disease Prediction — Compared five ML classifiers for heart disease detection.
   Stack: Python, Random Forest, SVM, Scikit-learn

CURRENTLY BUILDING:
- RAG Chatbot (LangChain + FastAPI + vector embeddings)
- LangGraph Agent (multi-step agentic workflows)

EXPERIENCE:
- Data Research Analyst at Concentrix Daksh Services (Aug-Sep 2024)
- AI Intern at Corizo.in (Jun-Jul 2023)

EDUCATION:
- B.Tech Computer Science, Geethanjali College (2021-2025), CGPA: 8.24

CERTIFICATIONS:
- Generative AI Academy — Google Cloud
- Google Data Analytics Professional Certificate

AVAILABILITY:
Open to AI Backend and LLM App Developer roles in Hyderabad or remote.
"""


# ===== HEALTH CHECK ROUTE =====
@app.get("/")
async def root():
    return {"status": "Portfolio API is running"}


# ===== CHAT ROUTE =====
@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise HTTPException(status_code=500, detail="API key not configured")

    # Build messages with system context prepended
    messages = [{"role": "system", "content": SYSTEM_CONTEXT}] + [
        msg.model_dump() for msg in request.messages
    ]

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {api_key}",
                },
                json={
                    "model": "llama-3.1-8b-instant",
                    "messages": messages,
                    "max_tokens": 500,
                },
                timeout=30.0,
            )

        data = response.json()

        if "error" in data:
            raise HTTPException(status_code=400, detail=data["error"]["message"])

        reply = data["choices"][0]["message"]["content"]
        return ChatResponse(reply=reply)

    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Request timed out")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
