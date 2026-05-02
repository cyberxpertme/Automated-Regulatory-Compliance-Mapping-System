from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from models.database import engine, Base
from routes.auth import router as auth_router
from routes.nlp_routes import router as nlp_router
from routes.mapping import router as mapping_router
import os

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Automated Regulatory Compliance Mapping System",
    version=os.getenv("VERSION", "1.0.0"),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(nlp_router)
app.include_router(mapping_router)

@app.get("/")
def root():
    return {
        "project": "Automated Regulatory Compliance Mapping System",
        "team": ["Md Shible Sadiqe — H-411", "Md Nahid Chowdhury — H-392"],
        "university": "University of Dhaka — PMICS Batch 4",
        "status": "Running ✅",
        "phase": "Phase 6 — Dashboard Ready",
    }

@app.get("/health")
def health():
    return {"status": "healthy"}
