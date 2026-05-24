---
title: Multi Agent Research Assistant
emoji: 🔬
colorFrom: blue
colorTo: purple
sdk: docker
app_file: app.py
pinned: false
---


# 🔬 Multi-Agent AI Research Assistant

An intelligent AI-powered research assistant that automatically searches the web, evaluates information quality, and writes professional research reports — completely FREE and fast!

![Python](https://img.shields.io/badge/Python-3.11-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-UI-red)
![Groq](https://img.shields.io/badge/Groq-Llama70B-purple)
![Tavily](https://img.shields.io/badge/Tavily-Search-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 🎯 What Does This Project Do?

You type any research question → 4 AI Agents work together automatically → You get a full professional research report in 30-60 seconds!

**Example Questions:**
- *"What are the latest developments in AI agents 2025?"*
- *"How does quantum computing work?"*
- *"What is the future of renewable energy?"*

---

## 🏗️ System Architecture

User Types Question
↓
🧠 Manager Agent (Orchestrator)
↓
⚡ Quick Answer Tool (fast first search)
↓
🔍 Research Agent → Search + Scrape Web
↓
⚖️ Judge Agent → Score Quality (0.0 to 1.0)
↓
Score >= 0.85? ──YES──→ ✍️ Writer Agent → Final Report
↓
NO
↓
🔍 Research Agent → Search Again (better query)
↓
⚖️ Judge Agent → Score Again
↓
Still Low? → 🌐 Deep Scrape Top 5 Websites
↓
✍️ Writer Agent → Final Report
↓
📥 PDF Download Ready!


---

## 🤖 The 4 AI Agents — Detailed Explanation

---

### 🧠 Agent 1 — Manager Agent
**File:** `agents.py` → `manager_agent()`

**Job:** The boss of the system. Controls all other agents and decides what happens next.

**How it works step by step:**
1. Receives the user's research question
2. Calls Quick Answer Tool for a fast first result
3. Sends question to Research Agent to search the web
4. Sends collected evidence to Judge Agent for quality check
5. If Judge says NEEDS_MORE → sends Research Agent to search again with improved query
6. If still not enough → triggers deep scraping of top 5 websites
7. Once Judge approves → sends everything to Writer Agent
8. Returns final report + activity logs to the UI

**Why it matters:** Without the Manager Agent, the other agents wouldn't know when to run or what to do next. It's the brain that coordinates the entire workflow.

---

### 🔍 Agent 2 — Research Agent
**File:** `agents.py` → `research_agent()`

**Job:** Find the best information from the internet about the research question.

**How it works step by step:**
1. Receives the research question from Manager Agent
2. Calls `search_and_scrape()` tool from `tools.py`
3. Searches top 3 most relevant websites using Tavily API
4. Scrapes and reads full content of each website
5. Formats all collected content with source titles and URLs
6. Returns structured evidence to Manager Agent

**What it collects from each source:**
- Source title
- Source URL
- Summary content from Tavily
- Full scraped text (first 1000 characters)

**Why it matters:** This agent brings real, live, up-to-date information from the internet — not old training data.

---

### ⚖️ Agent 3 — Judge Agent
**File:** `agents.py` → `judge_agent()` + `parse_judge_result()`

**Job:** Evaluate the quality of collected evidence and decide if it's good enough to write a report.

**How it works step by step:**
1. Receives the research question + all collected evidence
2. Sends both to Groq Llama 70B with a strict evaluation prompt
3. AI evaluates the evidence and responds in structured format
4. `parse_judge_result()` extracts the score, decision, and missing info
5. Returns score, decision (GOOD/NEEDS_MORE), and what's missing

**Judge Output Format:**

SCORE: 0.9
DECISION: GOOD
REASON: Evidence covers the topic comprehensively with recent sources
MISSING: NONE

**Scoring Rules:**
| Score | Decision | Action |
|---|---|---|
| 0.85 — 1.0 | GOOD | Proceed to Writer Agent |
| 0.0 — 0.84 | NEEDS_MORE | Research Agent searches again |

**Why it matters:** Without the Judge Agent, the Writer might create a report based on incomplete or irrelevant information. The Judge ensures report quality is always high.

---

### ✍️ Agent 4 — Writer Agent
**File:** `agents.py` → `writer_agent()`

**Job:** Write a professional, detailed research report based on all verified evidence.

**How it works step by step:**
1. Receives the research question + all approved evidence
2. Sends to Groq Llama 70B with a professional report writing prompt
3. AI writes a structured 6-section report
4. Returns the complete report text to Manager Agent

**Report Structure:**

📋 Executive Summary   — Short overview of findings
🔑 Key Findings        — Most important points discovered
📖 Context             — Background information
🔬 Detailed Analysis   — Deep explanation of the topic
💡 Implications        — Why this matters, future impact
📚 Sources             — List of all websites used

**Why it matters:** The Writer Agent transforms raw scraped data into a clean, professional, human-readable report that anyone can understand.

---

## 🛠️ Tools — Detailed Explanation

**File:** `tools.py`

The tools are helper functions used by the agents to interact with the internet.

---

### ⚡ Tool 1 — quick_answer()
**Job:** Get a fast, basic answer before doing deep research.

**How it works:**
- Sends query to Tavily with `search_depth="basic"`
- Gets top 3 results quickly
- Returns combined content as a quick first answer
- Used by Manager Agent at the very beginning

---

### 🔍 Tool 2 — search_web()
**Job:** Search the internet and return a list of relevant URLs and content.

**How it works:**
- Sends query to Tavily Search API
- Gets top 5 results with titles, URLs, and content snippets
- Returns structured list of results
- Used for deep scraping phase when Judge needs more info

---

### 🔍+📄 Tool 3 — search_and_scrape()
**Job:** Search the internet AND read the full content of each website.

**How it works:**
- Sends query to Tavily with `search_depth="advanced"`
- For each result, calls `scrape_url()` to read full page content
- Returns combined search + scraped data
- This is the main tool used by Research Agent

---

### 📄 Tool 4 — scrape_url()
**Job:** Go to a specific website and read all its text content.

**How it works:**
- Opens the given URL using Python `requests`
- Uses `BeautifulSoup` to parse the HTML
- Removes unwanted tags (scripts, ads, navigation, footer)
- Returns clean readable text (first 3000 characters)
- Used for deep scraping in the final fallback phase

---

## 📄 Helper Functions

**File:** `agents.py`

### call_llm()
**Job:** Send a prompt to Groq API and get AI response.
- Takes a prompt + optional system message
- Calls Groq Llama 70B model
- Returns the AI's text response
- Used by Judge Agent and Writer Agent

### parse_judge_result()
**Job:** Extract structured data from Judge Agent's text response.
- Reads the judge's text line by line
- Extracts SCORE, DECISION, and MISSING fields
- Returns them as Python variables
- Handles errors if format is unexpected

---

## 📁 Project Structure

multi-agent-ai-research-assistant/
│
├── app.py                 ← Main Streamlit UI + CSS styling
├── agents.py              ← All 4 AI Agents + helper functions
├── tools.py               ← Search + Scrape tools (Tavily + BS4)
├── scraper.py             ← Standalone website scraper
├── report_generator.py    ← PDF report generator (ReportLab)
├── requirements.txt       ← All Python dependencies
├── .env                   ← API Keys (NOT pushed to GitHub)
├── .gitignore             ← Files ignored by Git
└── README.md              ← This file

---

## ✨ Full Feature List

| Feature | Description |
|---|---|
| 🤖 4 AI Agents | Manager, Researcher, Judge, Writer |
| ⚡ Quick Answer | Fast first result before deep research |
| 🌐 Live Web Search | Real-time internet search via Tavily |
| 📄 Web Scraping | Reads full content of websites |
| ⚖️ Quality Scoring | Judge scores evidence 0.0 → 1.0 |
| 🔄 Auto Retry | Searches again if quality is low |
| 🌐 Deep Scraping | Reads top 5 sites if needed |
| ✍️ AI Report Writing | Professional 6-section report |
| 📊 Activity Log | See every agent action in real time |
| 📥 PDF Export | Download report as PDF |
| 🎨 Beautiful UI | Sky blue + purple + pink gradient |
| 💰 100% Free | No paid APIs, no GPU needed |

---

## 🛠️ Tech Stack

| Technology | Purpose | Cost |
|---|---|---|
| Groq Llama 70B | AI model for thinking + writing | FREE |
| Tavily Search API | Web search + content retrieval | FREE |
| BeautifulSoup4 | HTML parsing + web scraping | FREE |
| Streamlit | Web application UI | FREE |
| ReportLab | PDF generation | FREE |
| Python 3.11 | Core programming language | FREE |
| python-dotenv | Environment variable management | FREE |

---

## 🚀 Run Locally — Step by Step

### Step 1 — Clone the repository
```bash
git clone https://github.com/Sailaja-Kalle/multi-agent-ai-research-assistant.git
cd multi-agent-ai-research-assistant
```

### Step 2 — Create virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3 — Install all dependencies
```bash
pip install -r requirements.txt
```

### Step 4 — Get FREE API Keys

**Tavily API Key (Web Search):**
1. Go to https://tavily.com
2. Sign up for free account
3. Copy your API key from dashboard

**Groq API Key (AI Model):**
1. Go to https://console.groq.com
2. Sign up for free account
3. Create new API key
4. Copy your API key

### Step 5 — Create .env file
Create a file named `.env` in the project folder:

TAVILY_API_KEY=your_tavily_api_key_here
GROQ_API_KEY=your_groq_api_key_here

### Step 6 — Run the application
```bash
streamlit run app.py
```

Open browser at: **http://localhost:8501**

---

## 🔑 Environment Variables

| Variable | Description | Where to Get |
|---|---|---|
| TAVILY_API_KEY | Tavily web search API key | https://tavily.com |
| GROQ_API_KEY | Groq LLM API key | https://console.groq.com |

---

## 💡 How To Use

1. Open the app at http://localhost:8501
2. Type your research question in the search box
3. Click **🔍 Research Now** button
4. Watch the **Agent Activity Log** to see agents working
5. Read the generated **Research Report**
6. Click **📥 Download PDF Report** to save as PDF

---

## 🚀 Live Demo

## 🚀 Live Demo

| Platform | Link |
|---|---|
| 🤗 Hugging Face | [Open App](https://huggingface.co/spaces/Sailaja0031/multi-agent-research-assistant) |
| 🎈 Streamlit Cloud | [Open App](https://multi-agent-ai-research.streamlit.app) |
| 🚀 Render | [Open App](https://multi-agent-ai-research-assistant-qsx9.onrender.com) |

> No installation needed — just open and use for free!
> No installation needed — just open and use for free!

## 👩‍💻 Built By

**Sailaja Kalle** — AI Engineer

Passionate about building real-world AI solutions using Agentic AI, LLMs, RAG pipelines, and NLP. Focused on healthcare AI and solving problems for underserved communities.

🔗 GitHub: https://github.com/Sailaja-Kalle

---



