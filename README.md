
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
