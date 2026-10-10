# AI Resume Screening & Ranking Intelligence

[![GitHub License](https://img.shields.io/badge/License-MIT-blue.svg?style=for-the-badge)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![PyTorch](https://img.shields.io/badge/PyTorch-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org/)
[![SentenceTransformers](https://img.shields.io/badge/Sentence--Transformers-BGE-orange?style=for-the-badge)](https://sbert.net/)

<p align="center">
  <b>An enterprise-grade, high-performance semantic resume screening and candidate ranking web application powered by FastAPI and state-of-the-art transformer vector embeddings.</b>
</p>

---

## Overview

**ProITbridge AI Resume Screening** is an intelligent recruitment tool designed to automate and optimize candidate evaluation. Instead of relying on manual keyword searches or simple text matching, this system uses a **hybrid scoring architecture** combining domain-specific skill synonym mapping with dense vector semantic embeddings.

The system evaluates candidate resumes against predefined or custom Job Descriptions (JDs), computes an accurate fit score, and ranks candidates instantly in a clean, Astra-inspired enterprise web dashboard.

---

## Key Features

*  **Lightning-Fast Inference:** Optimized PyTorch inference pipeline running batched vector evaluations in under 2 seconds.
*  **Hybrid Scoring Model:** Combines 40% hard skill and synonym-mapped keyword overlap with 60% deep semantic context.
*  **Dynamic Role Switcher:** Instantly toggle between pre-configured job descriptions (*Senior Data Engineer*, *Data Analyst – BI*) or input custom JDs.
*  **Multi-File Upload:** Supports batch uploading of 5+ candidate documents simultaneously (`.pdf`, `.docx`, `.txt`).
*  **Persistent AJAX Frontend:** Async file dropzone with visual attachment confirmations and explicit clear/run controls.
*  **Professional Light Enterprise UI:** Modern, clean, and accessible light theme layout built with custom CSS variables and responsive tables.

---

## How It Works

```text
               INPUT
                 │
                 ▼
       ┌───────────────────┐
       │ Job Description & │
       │ Candidate Resumes │
       └─────────┬─────────┘
                 │
         ┌───────┴───────┐
         ▼               ▼
┌─────────────────┐ ┌──────────────────────┐
│  Skill & Entity │ │ Dense Vector Encoder │
│   Extraction    │ │  (Sentence Transformers)│
└────────┬────────┘ └──────────┬───────────┘
         │                   │
         ▼                   ▼
 Hard Skill Overlap    Semantic Similarity
         │                   │
         └─────────┬─────────┘
                   │
                   ▼
       ┌───────────────────────┐
       │   Hybrid Composite    │
       │    Fit Score (0-98%)  │
       └──────────┬────────────┘
                  │
                  ▼
       ┌───────────────────────┐
       │  Ranked Candidates    │
       │  Dashboard Display    │
       └───────────────────────┘

```

---

## Technology Stack

| Component | Technology / Library | Purpose |
| --- | --- | --- |
| **Backend API** | FastAPI, Uvicorn | High-performance asynchronous web framework |
| **Deep Learning** | PyTorch, Sentence-Transformers | Vector embedding generation and tensor operations |
| **Model** | `BAAI/bge-large-en-v1.5` / `all-MiniLM-L6-v2` | Dense semantic representation |
| **Document Parsing** | PyMuPDF (`fitz`), `python-docx` | Text extraction from PDF and Word documents |
| **Data Processing** | Pandas, NumPy | Score sorting, ranking, and matrix similarity computation |
| **Frontend** | HTML5, CSS3, Modern JavaScript | Interactive UI, drag-and-drop zone, and AJAX workflows |

---

## Project Structure

```text
resume-screening-app/
│
├── app.py                 # FastAPI application & route handlers
├── requirements.txt       # Project dependencies
│
├── backend/
│   ├── __init__.py
│   ├── extraction.py      # PDF and Word document text parsers
│   ├── preprocessing.py   # Text cleaning and skill synonym mapping
│   ├── embedding.py       # Cached singleton model loader & vectorizer
│   └── evaluate.py        # Hybrid skill + semantic scoring logic
│
├── templates/
│   └── index.html         # Astra-inspired light-themed web interface
│
└── static/
    ├── style.css          # Custom enterprise styling & components
    └── script.js          # File dropzone, AJAX submission, & role switcher

```

---

## Installation & Setup

### 1. Clone the Repository

```bash
git clone [https://github.com/Abdulla-B-Official/AI-Resume-Screening-System.git](https://github.com/Abdulla-B-Official/AI-Resume-Screening-System.git)
cd AI-Resume-Screening-System/resume-screening-app

```

### 2. Create a Virtual Environment

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

```

### 3. Install Dependencies

```bash
pip install -r requirements.txt

```

### 4. Run the Application

```bash
python app.py

```

Open your browser and navigate to: **`http://127.0.0.1:8000`**

---

## Evaluation & Scoring Logic

The scoring engine bypasses artificial ceilings by blending two complementary metrics:

1. **Skill Overlap Score (40%):** Extracts keywords from the job description and candidate resume, mapping variants through a domain-specific synonym dictionary (e.g., `pbi` $\rightarrow$ `power bi`, `py` $\rightarrow$ `python`).
2. **Semantic Similarity (60%):** Splits texts into manageable chunks, encodes them into dense vectors using transformer models, and computes matrix cosine similarities.

---

## Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://www.google.com/search?q=https://github.com/Abdulla-B-Official/AI-Resume-Screening-System/issues).

---

### Screen Smarter. Hire Faster. Automate Recruitment.

⭐ If you found this project useful, consider giving the repository a star!
