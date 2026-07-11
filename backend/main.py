from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from models.database import engine, Base
from routes.auth import router as auth_router
from routes.nlp_routes import router as nlp_router
from routes.mapping import router as mapping_router
from routes.reports import router as reports_router
from routes.frameworks import router as frameworks_router
from routes.upload import router as upload_router
from routes.search import router as search_router
import os

load_dotenv()
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Automated Regulatory Compliance Mapping System",
    description="ISO 27001 + PCI-DSS → NIST CSF 2.0 | NLP + TF-IDF | PMICS DU H-411 & H-392",
    version="5.0.0",
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
app.include_router(reports_router)
app.include_router(frameworks_router)
app.include_router(upload_router)
app.include_router(search_router)

@app.get("/")
def root():
    return {
        "project": "Automated Regulatory Compliance Mapping System",
        "team": ["Md Shible Sadiqe — H-411", "Md Nahid Chowdhury — H-392"],
        "university": "University of Dhaka — PMICS Batch 4",
        "status": "Running ✅",
        "version": "5.0.0",
        "features": [
            "ISO 27001:2022 → NIST CSF 2.0 (26 controls)",
            "PCI-DSS v4.0 → NIST CSF 2.0 (21 controls)",
            "Live End-to-End NLP + TF-IDF Demo",
            "Multi-file upload + auto mapping",
            "JWT Auth + RBAC (Admin/Auditor/Viewer)",
            "PDF Report Export",
            "PostgreSQL persistence"
        ],
        "docs": "http://localhost:8001/docs"
    }

@app.get("/health")
def health():
    return {"status": "healthy", "version": "5.0.0"}
