# Automated Regulatory Compliance Mapping System

![Python](https://img.shields.io/badge/Python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-green)
![React](https://img.shields.io/badge/React-Frontend-61DAFB)
![Docker](https://img.shields.io/badge/Docker-Deployment-2496ED)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

# 🚀 Automated Regulatory Compliance Mapping System

An AI-powered cybersecurity governance platform designed to automate compliance mapping between ISO 27001 and NIST Cybersecurity Framework (NIST CSF).

This project combines:

* FastAPI Backend
* React Dashboard
* PostgreSQL Database
* Docker Deployment
* NLP-based Clause Extraction
* Compliance Mapping Engine

---

# 📌 Features

## ✅ Compliance Mapping

* ISO 27001 → NIST CSF mapping
* Confidence score system
* Automated control relationship analysis

## ✅ NLP Clause Extraction

* spaCy-powered clause extraction
* Live text analysis demo
* Regulatory keyword detection

## ✅ Authentication & RBAC

* JWT Authentication
* Role-Based Access Control (RBAC)
* Secure API endpoints

## ✅ React Dashboard

* Interactive frontend dashboard
* Pie & Bar charts
* Real-time compliance overview

## ✅ Docker Deployment

* One-command deployment
* Backend + Frontend + PostgreSQL + Redis

---

# 🛠️ Tech Stack

| Technology   | Purpose                    |
| ------------ | -------------------------- |
| Python 3.12  | Backend                    |
| FastAPI      | API Framework              |
| React + Vite | Frontend                   |
| PostgreSQL   | Database                   |
| SQLAlchemy   | ORM                        |
| Docker       | Deployment                 |
| Redis        | Cache                      |
| spaCy        | NLP Engine                 |
| Axios        | Frontend API Communication |
| Recharts     | Dashboard Charts           |

---

# 📂 Project Structure

```bash
compliance-mapper/
├── README.md
├── docker-compose.yml
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── models/
│   ├── routes/
│   ├── mappings/
│   └── nlp/
└── frontend/
    ├── src/
    └── package.json
```

---

# ⚙️ Installation & Setup

## 1️⃣ Clone Repository

```bash
git clone https://github.com/cyberxpertme/Automated-Regulatory-Compliance-Mapping-System.git
cd Automated-Regulatory-Compliance-Mapping-System
```

---

# 🗄️ Backend Setup

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
python -m spacy download en_core_web_sm
cd backend
uvicorn main:app --reload --port 8001
```

---

# 🎨 Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

---

# 🐳 Docker Deployment

Run the full application:

```bash
docker-compose up --build
```

---

# 🌐 Services

| Service           | URL                                                          |
| ----------------- | ------------------------------------------------------------ |
| React Dashboard   | [http://localhost:5174](http://localhost:5174)               |
| API Documentation | [http://localhost:8001/docs](http://localhost:8001/docs)     |
| Health Check      | [http://localhost:8001/health](http://localhost:8001/health) |

---

# 📊 Project Phases

| Phase   | Description                  | Status |
| ------- | ---------------------------- | ------ |
| Phase 0 | Git + GitHub Setup           | ✅      |
| Phase 1 | FastAPI Backend              | ✅      |
| Phase 2 | PostgreSQL Integration       | ✅      |
| Phase 3 | JWT Authentication + RBAC    | ✅      |
| Phase 4 | NLP Clause Extraction        | ✅      |
| Phase 5 | ISO 27001 → NIST CSF Mapping | ✅      |
| Phase 6 | React Dashboard              | ✅      |
| Phase 7 | Docker Deployment            | ✅      |

---

# 🧠 NLP Engine

The NLP engine uses spaCy to:

* Extract regulatory clauses
* Detect compliance keywords
* Analyze security policies
* Improve automated mapping accuracy

---

# 🔐 Security Features

* JWT Authentication
* RBAC Authorization
* Secure API Structure
* Dockerized Deployment
* Environment Variable Protection

---

# 📈 Future Improvements

* AI-powered compliance recommendations
* SIEM integration
* Real-time monitoring dashboard
* Multi-framework support
* Automated audit reporting

---

# 👨‍💻 Author

Nahid Chowdhury

Cybersecurity Researcher & Developer

---

# 📜 License

This project is licensed under the MIT License.

---

# ⭐ GitHub Repository

[https://github.com/cyberxpertme/Automated-Regulatory-Compliance-Mapping-System](https://github.com/cyberxpertme/Automated-Regulatory-Compliance-Mapping-System)
cat >> README.md << 'EOF'

---

### ✅ Phase 6 — React Frontend Dashboard
**Status:** ✅ Done

**What I did:**
- Created React 18 + Vite frontend
- Built 3-tab dashboard: Dashboard, Mappings, NLP Engine
- Dashboard shows stats cards and charts
- Connected frontend to FastAPI backend
- Fixed CORS issues

---

### ✅ Phase 7 — Docker Full Deployment
**Status:** ✅ Done

**What I did:**
- Created Dockerfile for backend
- Created Dockerfile for frontend
- Updated docker-compose setup
- Full project deployment with one command

**Command to run everything:**

```bash
docker-compose up --build

# 🛡️ Automated Regulatory Compliance Mapping System

> **PMICS Project | CSE-811 | University of Dhaka | Batch 4**

| | |
|---|---|
| 👤 Student 1 | Md Shible Sadiqe — H-411 |
| 👤 Student 2 | Md Nahid Chowdhury — H-392 |
| 🎓 Supervisor | Prof. Abu Ahmed Ferdous |
| 📅 Started | June 2025 |

---

## 🧠 What this project does

Organizations struggle to manually map cybersecurity regulations.
This system automates that using NLP + rule-based engine.

**Example:** ISO 27001 Control A.5.1 → automatically maps to → NIST CSF GV.PO-01

---

## 🏗️ Tech Stack

| Layer | Technology |
|---|---|
| Backend | FastAPI (Python 3.12) |
| Database | PostgreSQL 15 |
| Cache | Redis 7 |
| NLP | spaCy |
| Frontend | React 18 + Vite |
| Auth | JWT + RBAC |
| Deploy | Docker + Nginx |

---

## 📖 Project Diary

> This section is updated after every phase.
> Anyone reading this can follow the exact journey of building this project.

---

### ✅ Phase 0 — Project Setup & Git
**Date:** _(write today's date)_
**Status:** ✅ Done

**What I did:**
- Created project folder structure
- Initialized Git repository
- Connected to GitHub as open source project
- Created this README as project diary

**Commands I ran:**
```bash
mkdir compliance-mapper
cd compliance-mapper
git init
git remote add origin https://github.com/YOUR_USERNAME/compliance-mapper.git
```

**What I learned:**
- How to start a project with Git from scratch
- How README works as living documentation

---

### 🔄 Phase 1 — Backend Foundation
**Status:** 🔄 Not started yet

**Goal:** Get FastAPI running on localhost:8000

**Plan:**
- Setup Python virtual environment
- Install FastAPI and dependencies
- Create first API endpoint
- Test with Swagger UI

---

### ⏳ Phase 2 — Database + Models
**Status:** ⏳ Pending

**Goal:** Connect PostgreSQL, create User and Mapping tables

---

### ⏳ Phase 3 — Authentication (JWT + RBAC)
**Status:** ⏳ Pending

**Goal:** Login system with 3 roles — Admin, Auditor, Viewer

---

### ⏳ Phase 4 — NLP Engine
**Status:** ⏳ Pending

**Goal:** Extract compliance clauses from ISO 27001 text using spaCy

---

### ⏳ Phase 5 — Mapping Engine
**Status:** ⏳ Pending

**Goal:** Auto-map ISO 27001 controls to NIST CSF with confidence score

---

### ⏳ Phase 6 — Frontend Dashboard
**Status:** ⏳ Pending

**Goal:** React dashboard showing compliance charts and mapping table

---

### ⏳ Phase 7 — Docker Deployment
**Status:** ⏳ Pending

**Goal:** Run entire project with one command using Docker Compose

---

## 🗂️ Folder Structure

_(This section will be updated as the project grows)_

---

### ✅ Phase 3 — Authentication (JWT + RBAC)
**Status:** ✅ Done

**What I did:**
- Implemented JWT token based authentication
- Built register, login, and me endpoints
- Created 3 user roles: admin, auditor, viewer
- Passwords hashed with bcrypt
- Protected routes with token verification

**API Endpoints added:**

| Endpoint | What it does |
|----------|-------------|
| POST /auth/register | Create new user with role |
| POST /auth/login | Login, receive JWT token |
| GET /auth/me | Get current logged in user |

**What I learned:**
- How JWT tokens are created and verified
- What bcrypt password hashing does
- What RBAC means

---

### ✅ Phase 4 — NLP Engine
**Status:** ✅ Done

**What I did:**
- Installed spaCy NLP library
- Built clause extractor using keyword matching
- Extracts compliance controls from ISO 27001 text
- Each clause gets a confidence score
- Built demo endpoint with sample ISO 27001 text

**API Endpoints added:**

| Endpoint | What it does |
|----------|-------------|
| POST /nlp/extract | Extract clauses from any text |
| GET /nlp/demo | Run demo on ISO 27001 sample |

**What I learned:**
- How spaCy NLP library works
- What sentence segmentation means
- How confidence scoring works in NLP

---

### ✅ Phase 5 — Mapping Engine
**Status:** ✅ Done

**What I did:**
- Created ISO 27001 to NIST CSF mapping data (10 controls)
- Built mapping API with stats and search endpoints
- Confidence scoring for each mapping (0.0 to 1.0)
- Gap analysis — full vs partial coverage identified
- Database seeding endpoint built
- Tested all endpoints with Swagger UI

**API Endpoints added:**

| Endpoint | What it does |
|----------|-------------|
| GET /mapping/sample | Get all ISO to NIST mappings |
| GET /mapping/stats | Compliance statistics |
| GET /mapping/search/{id} | Search specific control |
| POST /mapping/seed-db | Save mappings to database |
| GET /mapping/from-db | Get mappings from database |

**Sample Result from /mapping/stats:**
- Total Controls: 10
- Full Coverage: 7
- Partial Coverage: 3
- Coverage: 70%
- Avg Confidence: 85.9%

**What I learned:**
- How rule-based mapping engines work
- What confidence scoring means in compliance
- What gap analysis means
- How JSON data becomes API responses

---

### ✅ Phase 6 — React Frontend Dashboard
**Status:** ✅ Done

**What I did:**
- Created React 18 + Vite frontend
- Built 3-tab dashboard: Dashboard, Mappings, NLP Engine
- Dashboard shows 4 stats cards + 2 charts (Pie + Bar)
- Mappings tab shows ISO 27001 to NIST CSF table with confidence badges
- NLP Engine tab runs live clause extraction demo
- Connected frontend to FastAPI backend via axios
- Fixed CORS to allow frontend-backend communication

**Commands I ran:**
````bash
npm create vite@latest frontend -- --template react
npm install axios recharts
npm run dev
\```

**What I learned:**
- How React hooks (useState, useEffect) work
- How axios connects frontend to backend API
- How Recharts builds charts from API data
- What CORS is and why it matters

---

## 🗂️ Final Folder Structure

\```
compliance-mapper/
├── README.md                     ← project diary ✅
├── .gitignore                    ← secrets protected ✅
├── LICENSE                       ← MIT open source ✅
├── docker-compose.yml            ← PostgreSQL + Redis ✅
├── backend/
│   ├── main.py                   ← FastAPI entry point ✅
│   ├── .env                      ← environment variables ✅
│   ├── requirements.txt          ← python dependencies ✅
│   ├── models/
│   │   ├── database.py           ← SQLAlchemy connection ✅
│   │   ├── user.py               ← User model + RBAC ✅
│   │   └── compliance.py         ← Mapping model ✅
│   ├── routes/
│   │   ├── auth.py               ← JWT authentication ✅
│   │   ├── mapping.py            ← Mapping engine API ✅
│   │   └── nlp_routes.py         ← NLP endpoints ✅
│   ├── nlp/
│   │   └── extractor.py          ← spaCy clause extractor ✅
│   └── mappings/
│       └── iso_nist_sample.json  ← ISO 27001 to NIST data ✅
└── frontend/
    ├── src/
    │   ├── App.jsx               ← Main dashboard ✅
    │   └── index.css             ← Global styles ✅
    └── package.json              ← Node dependencies ✅
\```

---

## 🚀 How to Run (Full Setup)

\```bash
git clone https://github.com/cyberxpertme/Automated-Regulatory-Compliance-Mapping-System.git
cd Automated-Regulatory-Compliance-Mapping-System

# Start database
docker-compose up -d

# Start backend
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
python -m spacy download en_core_web_sm
cd backend && uvicorn main:app --reload --port 8001

# Start frontend (new terminal)
cd frontend
npm install
npm run dev
\```

| Service | URL |
|---------|-----|
| Frontend Dashboard | http://localhost:5174 |
| API Documentation | http://localhost:8001/docs |
| Health Check | http://localhost:8001/health |

---

## 📊 Project Summary

| Phase | Feature | Status |
|-------|---------|--------|
| 0 | Git + GitHub Setup | ✅ |
| 1 | FastAPI Backend | ✅ |
| 2 | PostgreSQL Database | ✅ |
| 3 | JWT Authentication + RBAC | ✅ |
| 4 | NLP Clause Extraction | ✅ |
| 5 | ISO 27001 → NIST CSF Mapping | ✅ |
| 6 | React Dashboard | ✅ |
| 7 | Docker Deployment | ⏳ Next |

---

### ✅ Phase 6 — React Frontend Dashboard
**Status:** ✅ Done

**What I did:**
- Created React 18 + Vite frontend
- Built 3-tab dashboard: Dashboard, Mappings, NLP Engine
- Dashboard shows 4 stats cards + 2 charts (Pie + Bar)
- Mappings tab shows ISO 27001 to NIST CSF table with confidence badges
- NLP Engine tab runs live clause extraction demo
- Connected frontend to FastAPI backend via axios
- Fixed CORS to allow frontend-backend communication

**Commands I ran:**
````bash
npm create vite@latest frontend -- --template react
npm install axios recharts
npm run dev
\```

**What I learned:**
- How React hooks (useState, useEffect) work
- How axios connects frontend to backend API
- How Recharts builds charts from API data
- What CORS is and why it matters

---

## 🗂️ Final Folder Structure

\```
compliance-mapper/
├── README.md                     ← project diary ✅
├── .gitignore                    ← secrets protected ✅
├── LICENSE                       ← MIT open source ✅
├── docker-compose.yml            ← PostgreSQL + Redis ✅
├── backend/
│   ├── main.py                   ← FastAPI entry point ✅
│   ├── .env                      ← environment variables ✅
│   ├── requirements.txt          ← python dependencies ✅
│   ├── models/
│   │   ├── database.py           ← SQLAlchemy connection ✅
│   │   ├── user.py               ← User model + RBAC ✅
│   │   └── compliance.py         ← Mapping model ✅
│   ├── routes/
│   │   ├── auth.py               ← JWT authentication ✅
│   │   ├── mapping.py            ← Mapping engine API ✅
│   │   └── nlp_routes.py         ← NLP endpoints ✅
│   ├── nlp/
│   │   └── extractor.py          ← spaCy clause extractor ✅
│   └── mappings/
│       └── iso_nist_sample.json  ← ISO 27001 to NIST data ✅
└── frontend/
    ├── src/
    │   ├── App.jsx               ← Main dashboard ✅
    │   └── index.css             ← Global styles ✅
    └── package.json              ← Node dependencies ✅
\```

---

## 🚀 How to Run (Full Setup)

\```bash
git clone https://github.com/cyberxpertme/Automated-Regulatory-Compliance-Mapping-System.git
cd Automated-Regulatory-Compliance-Mapping-System

# Start database
docker-compose up -d

# Start backend
python3 -m venv venv
source venv/bin/activate
pip install -r backend/requirements.txt
python -m spacy download en_core_web_sm
cd backend && uvicorn main:app --reload --port 8001

# Start frontend (new terminal)
cd frontend
npm install
npm run dev
\```

| Service | URL |
|---------|-----|
| Frontend Dashboard | http://localhost:5174 |
| API Documentation | http://localhost:8001/docs |
| Health Check | http://localhost:8001/health |

---

## 📊 Project Summary

| Phase | Feature | Status |
|-------|---------|--------|
| 0 | Git + GitHub Setup | ✅ |
| 1 | FastAPI Backend | ✅ |
| 2 | PostgreSQL Database | ✅ |
| 3 | JWT Authentication + RBAC | ✅ |
| 4 | NLP Clause Extraction | ✅ |
| 5 | ISO 27001 → NIST CSF Mapping | ✅ |
| 6 | React Dashboard | ✅ |
| 7 | Docker Deployment | ⏳ Next |

---

### ✅ Phase 6 — React Frontend Dashboard
**Status:** ✅ Done

**What I did:**
- Created React 18 + Vite frontend
- Built 3-tab dashboard: Dashboard, Mappings, NLP Engine
- Connected frontend to FastAPI backend
- Added charts and dashboard statistics
- Fixed CORS issues

---

### ✅ Phase 7 — Docker Full Deployment
**Status:** ✅ Done

**What I did:**
- Created Dockerfile for backend
- Created Dockerfile for frontend
- Updated docker-compose setup
- Full deployment ready with one command

**Run project:**

docker-compose up --build

---

## 🎉 Project Complete!

| URL | Service |
|-----|---------|
| http://localhost:5174 | React Dashboard |
| http://localhost:8001/docs | API Swagger UI |
| http://localhost:8001/health | Health Check |

GitHub:
https://github.com/cyberxpertme/Automated-Regulatory-Compliance-Mapping-System

