# app/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.services.agents import AgentOrchestrator
from app.services.vector_store import vector_store
from app.config import settings
import asyncio

app = FastAPI(title="DataSentience API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://127.0.0.1:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize orchestrator
orchestrator = AgentOrchestrator()

@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    print("🚀 Starting DataSentience Backend...")
    print(f"🔑 API Key loaded: {settings.NVIDIA_API_KEY[:20]}...")
    
    try:
        count = vector_store.collection.count()
        print(f"📚 Vector store contains {count} documents")
    except Exception as e:
        print(f"⚠️ Vector store check failed: {e}")

@app.get("/")
async def root():
    return {"message": "DataSentience API", "status": "healthy", "version": "1.0.0"}

@app.post("/api/analyze")
async def analyze_query(query: str):
    try:
        result = await orchestrator.process_query(query)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "service": "DataSentience API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)