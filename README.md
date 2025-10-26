# 🧠 Research Genie – AI Service Module
## 📘 Overview

The **AI Service Module** is the intelligence layer of the Research Genie system.
It connects with the Backend and Scraper microservices to generate meaningful insights from research papers using LLMs (Gemini / ChatGPT).

This service refines user queries, receives relevant research papers, analyzes them, and extracts research gaps and summarized insights tailored to the user’s education level.

## ⚙️ Core Responsibilities

- Refine user queries for efficient scraping (optional)
- Communicate with Backend and Scraper microservices
- Process user education details for customized output difficulty
- Use LLM APIs to generate:
  - Research summaries
  - Research gap analyses
  - Simplified explanations (based on user level)
- Return structured output to the Backend for UI display

## 🏗️ Workflow Summary

- Receive query & user profile from the Backend
- (Optional) Refine the user query using NLP-based preprocessing
- Send refined query to Scraper Module
- Receive scraped papers data (metadata, abstracts, etc.)
- Process data through LLM (Gemini/ChatGPT) for:
  - Summarization
  - Gap extraction
  - Difficulty-based explanation
- Return the final structured output to the Backend

## 🧠 Tech Stack

| Category          | Technology                  | Purpose                                  |
| ----------------- | --------------------------- | ---------------------------------------- |
| **Language**      | Python 3.10+                | Core service logic                       |
| **Framework**     | FastAPI / Flask             | RESTful microservice API                 |
| **LLM API**       | Gemini API / OpenAI GPT API | Summarization & research gap generation  |
| **Communication** | REST API / gRPC             | Connects with Backend & Scraper services |
| **Environment**   | Docker / Docker Compose     | Containerized microservice deployment    |
| **Logging**       | Python `logging` / `loguru` | Service logs and debugging               |
| **Testing**       | Pytest                      | Unit and integration testing             |

## 📁 Folder Structure

```
ai_service/
│
├── src/
│   ├── main.py                 # Entry point (FastAPI app)
│   ├── routers/
│   │   ├── ai_routes.py        # Exposes API endpoints
│   │
│   ├── services/
│   │   ├── query_refiner.py    # Optional query cleaner
│   │   ├── llm_processor.py    # Handles LLM calls (Gemini/ChatGPT)
│   │   ├── communication.py    # API requests to backend/scraper
│   │   ├── formatter.py        # Formats final AI output (JSON)
│   │
│   ├── config/
│   │   ├── settings.py         # API keys, environment variables, endpoints
│   │
│   └── utils/
│       ├── prompts.py          # LLM prompt templates
│       ├── logger.py           # Logging configuration
│
├── tests/
│   ├── test_llm_processor.py
│   ├── test_query_refiner.py
│
├── requirements.txt
├── .gitignore
├── .env.example
└── README.md
```

## 🧩 API Endpoints (Example)

| Endpoint          | Method | Description                                          |
| ----------------- | ------ | ---------------------------------------------------- |
| `/refine_query`   | POST   | Refine user query before scraping                    |
| `/analyze_papers` | POST   | Process papers + user data to generate research gaps |
| `/health`         | GET    | Check service health                                 |


## 🚀 Setup & Run

1. Clone the Repository
```
git clone https://github.com/ResearchGenie/ai_service.git
cd ai_service
```

2. Create Virtual Environment
```
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

3. Install Dependencies
```
pip install -r requirements.txt
```

4. Run Service
```
uvicorn src.main:app --reload
```
