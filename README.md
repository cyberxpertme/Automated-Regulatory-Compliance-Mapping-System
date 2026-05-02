# 🛡️ Automated Regulatory Compliance Mapping System

[![Python](https://img.shields.io/badge/Python-3.12-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-61DAFB.svg)](https://react.dev)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED.svg)](https://docker.com)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

> **PMICS Project | CSE-811 | University of Dhaka | Batch 4**

| | |
|---|---|
| 👤 Student 1 | Md Shible Sadiqe — H-411 |
| 👤 Student 2 | Md Nahid Chowdhury — H-392 |
| 🎓 Supervisor | Prof. Abu Ahmed Ferdous |
| 🏫 University | University of Dhaka — Dept. of CSE |
| 📅 Started | May 2025 |
| 🔗 Repo | https://github.com/cyberxpertme/Automated-Regulatory-Compliance-Mapping-System |

---

## 🧠 What This Project Does

Organizations struggle to **manually map** cybersecurity regulations across multiple frameworks. This is time-consuming, error-prone, and expensive.

This system **automates** that process using NLP + rule-based engine.

**Real Example:**
ISO 27001 Control A.5.1
"A set of policies for information security shall be defined..."
↓ NLP extracts clause
↓ Mapping engine matches
NIST CSF Control GV.PO-01
"Organizational cybersecurity policy is established"
Confidence Score: 95%

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🧠 NLP Engine | spaCy extracts compliance clauses from regulatory text |
| 🗺️ Mapping Engine | Auto-maps ISO 27001 controls to NIST CSF with confidence score |
| 📊 Dashboard | React dashboard with charts and mapping table |
| 🔐 Authentication | JWT login with 3 roles: Admin, Auditor, Viewer |
| 🏢 Multi-tenancy | Organization-level data isolation |
| 🐳 Docker Ready | One command runs everything |

---

## 🏗️ Tech Stack

| Layer | Technology | Why |
|-------|-----------|-----|
| Backend | FastAPI (Python 3.12) | Fast, auto-generates API docs |
| Database | PostgreSQL 15 | Reliable relational database |
| Cache | Redis 7 | Fast session caching |
| NLP | spaCy (en_core_web_sm) | Industrial NLP library |
| Frontend | React 18 + Vite | Fast, modern UI |
| Charts | Recharts | React chart library |
| Auth | JWT + bcrypt | Secure token authentication |
| Deploy | Docker + Docker Compose | Consistent deployment |

---

## 📂 Project Structure
compliance-mapper/
├── README.md                     ← You are here
├── .gitignore                    ← Files git ignores
├── LICENSE                       ← MIT License
├── docker-compose.yml            ← All services config
│
├── backend/                      ← Python FastAPI server
│   ├── main.py                   ← App entry point
│   ├── .env                      ← Environment variables (not in git)
│   ├── requirements.txt          ← Python dependencies
│   │
│   ├── models/                   ← Database models
│   │   ├── database.py           ← SQLAlchemy connection setup
│   │   ├── user.py               ← User model with RBAC roles
│   │   └── compliance.py         ← Control mapping model
│   │
│   ├── routes/                   ← API endpoints
│   │   ├── auth.py               ← Register, Login, Me
│   │   ├── mapping.py            ← Compliance mapping API
│   │   └── nlp_routes.py         ← NLP extraction API
│   │
│   ├── nlp/
│   │   └── extractor.py          ← spaCy clause extractor
│   │
│   └── mappings/
│       └── iso_nist_sample.json  ← ISO 27001 to NIST CSF data
│
└── frontend/                     ← React dashboard
├── src/
│   ├── App.jsx               ← Main dashboard component
│   └── index.css             ← Global styles
└── package.json              ← Node dependencies

---

## 🚀 Quick Start (5 minutes)

### Prerequisites
Make sure you have these installed:
- Python 3.10+ → `python3 --version`
- Node.js 18+ → `node --version`
- Docker Desktop → `docker --version`

### Clone the project
```bash
git clone https://github.com/cyberxpertme/Automated-Regulatory-Compliance-Mapping-System.git
cd Automated-Regulatory-Compliance-Mapping-System
```

### Start Database (Docker)
```bash
docker-compose up -d
```
Wait 10 seconds for PostgreSQL to start.

### Start Backend
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
python -m spacy download en_core_web_sm
cd backend
uvicorn main:app --reload --port 8001
```

### Start Frontend (new terminal)
```bash
cd frontend
npm install
npm run dev
```

### Open in Browser
| Service | URL |
|---------|-----|
| 🎨 Dashboard | http://localhost:5174 |
| 📖 API Docs | http://localhost:8001/docs |
| ❤️ Health | http://localhost:8001/health |

---

## 🔌 API Reference

### Authentication
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | /auth/register | Create new user | No |
| POST | /auth/login | Login, get JWT token | No |
| GET | /auth/me | Get current user info | Yes |

### Compliance Mapping
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | /mapping/sample | Get all ISO→NIST mappings | No |
| GET | /mapping/stats | Compliance statistics | No |
| GET | /mapping/search/{id} | Search specific control | No |
| POST | /mapping/seed-db | Seed database | Yes |

### NLP Engine
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | /nlp/extract | Extract clauses from text | No |
| GET | /nlp/demo | Demo on ISO 27001 sample | No |

### Test the API
1. Go to http://localhost:8001/docs
2. Click any endpoint → "Try it out" → "Execute"
3. For protected routes: first login → copy token → click "Authorize"

---

## 🔐 User Roles (RBAC)

| Role | Can Do |
|------|--------|
| admin | Everything — manage users, seed DB, view all |
| auditor | View mappings, run NLP, generate reports |
| viewer | View dashboard and mappings only |

### Create test users
```bash
# Register an admin
curl -X POST http://localhost:8001/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@du.ac.bd","full_name":"Admin User","password":"test1234","role":"admin","organization":"University of Dhaka"}'

# Login
curl -X POST http://localhost:8001/auth/login \
  -d "username=admin@du.ac.bd&password=test1234"
```

---

## 🔧 Troubleshooting

### Docker permission denied
```bash
sudo usermod -aG docker $USER
newgrp docker
```

### Port already in use
```bash
fuser -k 8001/tcp
fuser -k 5174/tcp
```

### spaCy model not found
```bash
python -m spacy download en_core_web_sm
```

### Database connection refused
```bash
# Make sure Docker is running
docker-compose up -d
docker ps
```

### venv not activated
```bash
source venv/bin/activate
# You should see (venv) in terminal
```

---

## 📖 Project Diary

> This section documents how this project was built step by step.
> Anyone can follow this to build the same project from scratch.

---

### ✅ Phase 0 — Git + GitHub Setup
**Status:** ✅ Done

**What we did:**
- Created project folder structure
- Initialized Git repository
- Connected to GitHub as open source project
- Created README as living project diary
- Added .gitignore to protect secrets
- Added MIT LICENSE

**Commands:**
```bash
mkdir compliance-mapper && cd compliance-mapper
git init
git remote add origin https://github.com/cyberxpertme/Automated-Regulatory-Compliance-Mapping-System.git
git add . && git commit -m "phase-0: project initialized"
git push -u origin main
```

**What we learned:**
- How to initialize a Git repository
- How to connect local repo to GitHub
- Why .gitignore is important (never push .env or venv)

---

### ✅ Phase 1 — Backend Foundation
**Status:** ✅ Done

**What we did:**
- Created backend folder structure
- Setup Python virtual environment (isolated dependencies)
- Installed FastAPI and uvicorn
- Created first 2 API endpoints: / and /health
- Verified with Swagger UI at localhost:8001/docs

**Commands:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install fastapi uvicorn[standard] python-dotenv
cd backend
uvicorn main:app --reload --port 8001
```

**Endpoints created:**
- GET / → Project info
- GET /health → Health check

**What we learned:**
- How FastAPI works
- What Swagger UI is (auto-generated API documentation)
- How virtual environments keep dependencies isolated

---

### ✅ Phase 2 — Database + Models
**Status:** ✅ Done

**What we did:**
- Setup Docker with PostgreSQL 15 and Redis 7
- Created SQLAlchemy database connection
- Built User model with 3 RBAC roles
- Built ControlMapping model for ISO→NIST mappings
- Tables auto-create when server starts

**Commands:**
```bash
docker-compose up -d
pip install sqlalchemy psycopg2-binary alembic
```

**Models created:**
- User (id, email, full_name, hashed_password, role, organization)
- ControlMapping (source_control, target_control, confidence_score, gap_description)

**What we learned:**
- How SQLAlchemy ORM maps Python classes to database tables
- What Docker Compose does (runs multiple services together)
- What RBAC (Role Based Access Control) means

---

### ✅ Phase 3 — Authentication (JWT + RBAC)
**Status:** ✅ Done

**What we did:**
- Implemented JWT token authentication
- Built /auth/register, /auth/login, /auth/me endpoints
- Passwords hashed with bcrypt (never stored in plain text)
- Protected routes require valid JWT token
- Tested with Swagger UI

**Commands:**
```bash
pip install passlib[bcrypt] python-jose[cryptography] python-multipart
```

**How JWT works:**
User logs in with email+password
↓
Server verifies password (bcrypt)
↓
Server creates JWT token (signed with SECRET_KEY)
↓
User sends token in every request header
↓
Server verifies token on protected routes

**What we learned:**
- How JWT tokens work (header.payload.signature)
- What bcrypt hashing does (one-way, can't reverse)
- How OAuth2 password flow works in FastAPI

---

### ✅ Phase 4 — NLP Engine
**Status:** ✅ Done

**What we did:**
- Installed spaCy NLP library
- Downloaded English language model (en_core_web_sm)
- Built clause extractor using keyword matching + sentence segmentation
- Each extracted clause gets a confidence score (0.0 to 1.0)
- Built /nlp/demo endpoint with sample ISO 27001 text
- Found 8 compliance clauses from sample text

**Commands:**
```bash
pip install spacy
python -m spacy download en_core_web_sm
```

**How NLP extraction works:**
Input: "A set of policies shall be defined and approved by management."
↓
spaCy splits into sentences
↓
Each sentence checked for keywords: shall, must, should, ensure...
↓
Matched sentences = compliance clauses
↓
Confidence = 0.5 + (number of keywords × 0.1)
↓
Output: {clause_id, text, keywords, confidence: 0.60}

**What we learned:**
- How NLP sentence segmentation works
- What keyword-based extraction means
- How confidence scoring works

---

### ✅ Phase 5 — Mapping Engine
**Status:** ✅ Done

**What we did:**
- Created ISO 27001 to NIST CSF mapping data (10 controls)
- Each mapping has: source control, target control, confidence score, gap description
- Built /mapping/stats API for compliance overview
- Built /mapping/search API to find specific controls
- Gap analysis: 7 full coverage, 3 partial coverage

**Sample mapping:**
```json
{
  "source": "ISO 27001 A.5.1 - Policies for information security",
  "target": "NIST CSF GV.PO-01 - Organizational cybersecurity policy",
  "confidence": 0.95,
  "gap": null
}
```

**Stats result:**
- Total Controls: 10
- Full Coverage: 7 (70%)
- Partial Coverage: 3 (30%)
- Average Confidence: 85.9%

**What we learned:**
- How rule-based mapping engines work
- What gap analysis means in compliance
- How confidence scoring guides audit decisions

---

### ✅ Phase 6 — React Frontend Dashboard
**Status:** ✅ Done

**What we did:**
- Created React 18 + Vite frontend project
- Built 3-tab dashboard: Dashboard, Mappings, NLP Engine
- Dashboard tab: 4 stats cards + Pie chart + Bar chart
- Mappings tab: Full ISO→NIST table with confidence badges
- NLP Engine tab: Live clause extraction demo
- Connected to FastAPI backend via axios
- Fixed CORS to allow frontend-backend communication

**Commands:**
```bash
npm create vite@latest frontend -- --template react
cd frontend
npm install axios recharts
npm run dev
```

**What we learned:**
- How React hooks work (useState, useEffect)
- How axios makes HTTP requests to backend
- How Recharts creates charts from API data
- What CORS is and why browsers enforce it

---

### ✅ Phase 7 — Docker Deployment
**Status:** ✅ Done

**What we did:**
- Created Dockerfile for backend (Python + spaCy)
- Created Dockerfile for frontend (Node build + Nginx serve)
- Updated docker-compose to run all 4 services together
- Full project runs with one command

**Command:**
```bash
docker-compose up --build
```

**How Docker works:**
docker-compose up --build
↓
Builds backend image (Python + dependencies)
Builds frontend image (React build + Nginx)
Starts PostgreSQL container
Starts Redis container
All containers talk to each other
↓
Visit http://localhost:5174

**What we learned:**
- How Docker containers work
- What multi-stage builds are (build then serve)
- How Docker Compose networks services together

---

## 📊 Final Progress

| Phase | Feature | Status |
|-------|---------|--------|
| 0 | Git + GitHub | ✅ Done |
| 1 | FastAPI Backend | ✅ Done |
| 2 | PostgreSQL + Models | ✅ Done |
| 3 | JWT Auth + RBAC | ✅ Done |
| 4 | NLP Engine | ✅ Done |
| 5 | Mapping Engine | ✅ Done |
| 6 | React Dashboard | ✅ Done |
| 7 | Docker Deployment | ✅ Done |

---

## 🔮 Future Work

- [ ] Add PCI-DSS and GDPR frameworks
- [ ] AI-powered mapping recommendations
- [ ] PDF compliance report export
- [ ] Real-time monitoring dashboard
- [ ] SIEM integration

---

## 📄 License
MIT License — see LICENSE file for details.

---

## ⭐ If this helped you, give it a star on GitHub!
