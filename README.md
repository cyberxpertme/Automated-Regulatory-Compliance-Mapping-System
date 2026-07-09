# 🛡️ Automated Regulatory Compliance Mapping System

[![Python](https://img.shields.io/badge/Python-3.13-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg)](https://react.dev)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **PMICS Project | CSE-811 | University of Dhaka | Batch 4**

| | |
|---|---|
| 👤 Student 1 | Md Shible Sadiqe — H-411 |
| 👤 Student 2 | Md Nahid Chowdhury — H-392 |
| 🎓 Supervisor | Prof. Abu Ahmed Ferdaus, Associate Professor, Dept. of CSE, University of Dhaka |
| 📅 Started | May 2025 |
| 🔗 GitHub | https://github.com/cyberxpertme/Automated-Regulatory-Compliance-Mapping-System |

---

## 🧠 What This Project Does

Organizations operating in regulated sectors must comply with multiple cybersecurity frameworks simultaneously — ISO 27001, NIST CSF, and PCI-DSS. Manually cross-mapping controls across these frameworks is time-consuming, error-prone, and must be repeated every time a framework is updated.

This system **automates** that process using NLP (Natural Language Processing) and TF-IDF based semantic similarity.

**Example:**
---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 🧠 NLP Clause Extraction | spaCy sentence segmentation + keyword detection extracts compliance clauses |
| 🗺️ TF-IDF Mapping Engine | Cosine similarity maps each clause to nearest NIST CSF 2.0 control |
| 📊 Live Dashboard | React dashboard with real-time charts, coverage stats, confidence scores |
| 📤 Multi-File Upload | Upload 2+ PDF/TXT documents, get combined auto-mapped compliance analysis |
| 📄 PDF Report Export | Professional compliance report generated on demand via ReportLab |
| 🔐 JWT Authentication | Login/Register with bcrypt password hashing |
| 👥 RBAC | 3 roles: Admin, Auditor, Viewer |
| 🏢 Multi-Framework | ISO 27001:2022 + PCI-DSS v4.0 → NIST CSF 2.0 |
| 🗄️ DB Persistence | All upload history saved permanently in PostgreSQL |
| 🐳 Docker Ready | One-command deployment via Docker Compose |

---

## 🏗️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI (Python 3.13) |
| NLP | spaCy (en_core_web_sm) |
| Mapping | scikit-learn (TF-IDF + cosine similarity) |
| Database | PostgreSQL 15 |
| Cache | Redis 7 |
| ORM | SQLAlchemy 2.x |
| Auth | JWT (python-jose) + bcrypt (passlib) |
| Frontend | React 18 + Vite |
| Charts | Recharts |
| PDF | ReportLab + pdfplumber |
| DevOps | Docker + Docker Compose |

---

## 📂 Project Structure
---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+
- Docker Desktop

### 1. Clone
```bash
git clone https://github.com/cyberxpertme/Automated-Regulatory-Compliance-Mapping-System.git
cd Automated-Regulatory-Compliance-Mapping-System
```

### 2. Start Database
```bash
docker-compose up -d
docker ps
```

### 3. Start Backend
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
python -m spacy download en_core_web_sm
cd backend
uvicorn main:app --reload --port 8001
```

### 4. Start Frontend
```bash
cd frontend
npm install
npm run dev
```

### 5. Open in Browser
| Service | URL |
|---------|-----|
| 🎨 Dashboard | http://localhost:5173 |
| 📖 API Docs | http://localhost:8001/docs |
| ❤️ Health | http://localhost:8001/health |

### 6. Create Admin Account
```bash
curl -X POST http://localhost:8001/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@du.ac.bd","full_name":"Admin","password":"test1234","role":"admin","organization":"University of Dhaka"}'
```

---

## 🔌 API Reference

### Authentication
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | /auth/register | No | Create new user |
| POST | /auth/login | No | Login, get JWT token |
| GET | /auth/me | Yes | Get current user |

### Compliance Mapping
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | /mapping/sample | No | All ISO 27001 mappings |
| GET | /mapping/stats | No | Coverage + confidence stats |
| GET | /mapping/search/{id} | No | Search specific control |

### Multi-Framework
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | /frameworks/list | No | List supported frameworks |
| GET | /frameworks/{id}/mappings | No | Mappings for framework |
| GET | /frameworks/{id}/stats | No | Stats for framework |
| GET | /frameworks/combined/stats | No | Combined stats all frameworks |

### NLP Engine
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | /nlp/extract | No | Extract clauses from text |
| GET | /nlp/demo | No | Demo on ISO 27001 sample |

### Upload & Auto-Map
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| POST | /upload/analyze-multi | No | Upload 2+ files, auto-map |
| GET | /upload/live-stats | No | Latest upload batch stats |
| GET | /upload/history | No | All past upload batches |
| GET | /upload/download-report | No | PDF report from last upload |

### Reports
| Method | Endpoint | Auth | Description |
|--------|----------|------|-------------|
| GET | /reports/download | No | Full framework PDF report |
| GET | /reports/preview | No | Report summary |

---

## 📊 Current System Statistics

| Metric | Value |
|--------|-------|
| ISO 27001:2022 Controls | 26 |
| PCI-DSS v4.0 Controls | 21 |
| Total Controls Mapped | 47 |
| Target Framework Controls | 106 (NIST CSF 2.0) |
| ISO 27001 Avg Confidence | 92.3% |
| PCI-DSS Avg Confidence | 93.1% |
| Full Coverage | 91.5% |

---

## 👥 User Roles (RBAC)

| Role | Permissions |
|------|-------------|
| Admin | Full access — manage users, seed DB, all operations |
| Auditor | Upload documents, run NLP, generate reports |
| Viewer | Read-only — view dashboard and mappings |

---

## 🔧 Troubleshooting

| Problem | Fix |
|---------|-----|
| `No module named 'fastapi'` | `source venv/bin/activate` |
| `Address already in use` | `fuser -k 8001/tcp` |
| `Connection refused (5432)` | `docker-compose up -d` |
| `bcrypt error` | `pip install "bcrypt==4.0.1"` |
| Scanned PDF not working | Use text-based PDF or .txt file |

---

## 📖 Project Development Diary

> This section documents how this project was built step by step.

---

### ✅ Phase 0 — Git + GitHub Setup
**Status:** ✅ Done

- Created project folder and Git repository
- Connected to GitHub as open source project
- Created README as living project diary
- Added .gitignore and MIT LICENSE

---

### ✅ Phase 1 — Backend Foundation
**Status:** ✅ Done

- Setup Python virtual environment
- Installed FastAPI and uvicorn
- Created root and health endpoints
- Verified with Swagger UI at /docs

---

### ✅ Phase 2 — Database + Models
**Status:** ✅ Done

- Setup Docker with PostgreSQL 15 and Redis 7
- Created SQLAlchemy database connection
- Built User model with RBAC roles (Admin/Auditor/Viewer)
- Built ControlMapping model for ISO→NIST mappings
- Tables auto-create on server startup

---

### ✅ Phase 3 — Authentication (JWT + RBAC)
**Status:** ✅ Done

- Implemented JWT token authentication
- Built /auth/register, /auth/login, /auth/me endpoints
- Passwords hashed with bcrypt (pinned to 4.0.1 for passlib compatibility)
- Protected routes with token verification

---

### ✅ Phase 4 — NLP Clause Extraction
**Status:** ✅ Done

- Installed spaCy with en_core_web_sm English model
- Built clause extractor: sentence segmentation + 20-keyword vocabulary
- Each clause assigned a confidence score
- Built /nlp/extract and /nlp/demo endpoints

---

### ✅ Phase 5 — Mapping Engine
**Status:** ✅ Done

- Created ISO 27001 to NIST CSF mapping data (10 initial controls)
- Built mapping API with stats, search, and seed-db endpoints
- Confidence scoring and gap analysis implemented

---

### ✅ Phase 6 — React Frontend Dashboard
**Status:** ✅ Done

- Created React 18 + Vite frontend
- Built 3-tab dashboard: Dashboard, Mappings, NLP Engine
- Connected to FastAPI backend via axios
- Fixed CORS for frontend-backend communication

---

### ✅ Phase 7 — Docker Deployment
**Status:** ✅ Done

- Created Dockerfile for backend and frontend
- docker-compose runs all services together
- Entire project deployable with one command

---

### ✅ Phase 8 — Real ISO 27001 Data
**Status:** ✅ Done

- Imported real ISO 27001:2022 controls (26 controls)
- Imported NIST CSF 2.0 controls (106 subcategories)
- Average confidence: 92.3%
- Category breakdown: Organizational, People, Physical, Technological

---

### ✅ Phase 9 — TF-IDF NLP Engine
**Status:** ✅ Done

- Implemented TF-IDF vectorization with scikit-learn
- Added cosine similarity scoring against NIST CSF reference texts
- Combined TF-IDF score with keyword-density boost
- More accurate semantic matching than simple keyword detection

---

### ✅ Phase 10 — PDF Report Export
**Status:** ✅ Done

- Built professional PDF report generator using ReportLab
- Executive summary, mapping table, gap analysis in report
- Added Download PDF Report button on dashboard

---

### ✅ Phase 11 — Multi-Framework Support (PCI-DSS)
**Status:** ✅ Done

- Added PCI-DSS v4.0 controls (21 controls) mapped to NIST CSF
- Built /frameworks API with per-framework and combined stats
- Framework selector UI on dashboard
- Total: 47 controls across ISO 27001 + PCI-DSS

---

### ✅ Phase 12-13 — Multi-File Upload + Live Dashboard
**Status:** ✅ Done

- POST /upload/analyze-multi accepts 2+ files at once
- Combined NLP+TF-IDF mapping across all uploaded files
- Live stats banner updates dashboard in real-time
- Combined PDF report downloadable after upload
- Upload & Auto-Map tab added to frontend

---

### ✅ Phase 14 — Login UI + Database Persistence
**Status:** ✅ Done

- Built Login/Register UI connected to JWT backend
- Guest mode for quick demo access
- Created UploadHistory and UploadClause database tables
- All upload analysis saved permanently in PostgreSQL
- Upload history survives server restart

---

## 🔮 Future Work

- [ ] BERT/DistilBERT semantic embeddings for higher accuracy
- [ ] SHAP explainability for mapping decisions
- [ ] GDPR and ISO 22301 framework support
- [ ] OCR for scanned/image-based PDF documents
- [ ] Upload history UI page in dashboard
- [ ] RBAC enforcement on frontend (role-based button visibility)

---

## 📄 License
MIT License — see LICENSE file for details.

---

## ⭐ If this helped you, give it a star on GitHub!
