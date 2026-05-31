# 🚕 NYC Taxi Analytics — Live AI Dashboard

> **Live App:** https://app-nyc-taxi.streamlit.app
> ⏳ Note: First load may take 30-60 seconds
> while the AI model initializes. Please be patient!

---

## 🌐 About This Project

This is a fully deployed, cloud-based data engineering
application built on 1 Million real NYC Taxi trips from 2015.

The app combines a live analytics dashboard with an
intelligent AI assistant that can answer questions
about NYC taxi data in plain English!

---

## 📊 Dashboard Page

Real time insights from 993,708 cleaned taxi trips:

- 🚕 **993,708** total trips analyzed
- 💰 **$16,072,117** total revenue
- 💵 **$13.05** average fare per trip
- ⏱️ **15.23 minutes** average trip duration
- 📊 Interactive bar and pie charts
- 💳 Payment type breakdown
- 🕐 Trip patterns by hour of day
- 📋 Complete payment summary table

---

## 🤖 AI Assistant Page

The highlight of this project!
Ask ANY question about NYC taxi data in plain English!

### How it works:
1. You type a question
2. Smart router classifies it as DATA or KNOWLEDGE
3. Routes to correct AI system automatically
4. Returns intelligent answer!

### Two AI Systems:

**Text-to-SQL** (for data questions):
- Converts plain English to SQL automatically
- Runs query against ClickHouse Cloud
- Returns exact numbers and tables

**RAG Assistant** (for knowledge questions):
- Retrieves relevant documents using embeddings
- Uses cosine similarity search
- Groq AI generates contextual answers
- Based on real NYC taxi knowledge base!

### Example Questions:

**Data Questions (Text-to-SQL):**
- "What is the average fare amount?"
- "How many trips were taken in total?"
- "What is total revenue from credit card payments?"
- "What is average trip duration?"

**Knowledge Questions (RAG):**
- "Why do cash riders pay more than credit card riders?"
- "How are NYC taxi fares calculated?"
- "Why are tips higher for credit card payments?"
- "What time of day are taxis busiest?"
- "Which NYC borough generates most revenue?"

### AI Evaluation Results:
🎯 Routing Accuracy:  9/10 = 90%
✅ Answer Accuracy:   9/10 = 90%
🏆 Overall Score:     90.0%
Text-to-SQL: 4/5 correct
RAG:         5/5 correct ← Perfect score!

---

## 🛠️ Tech Stack
Cloud Infrastructure:
──────────────────────
🗄️ ClickHouse Cloud    → Online columnar database
hosting 1M+ taxi trips
Data Pipeline:
───────────────
🔧 dbt                 → SQL transformations
⭐ Star Schema         → fact + dimension tables
✅ 18 data tests       → automated quality checks
AI Layer:
──────────
🤖 Groq API            → LLM (llama-3.3-70b-versatile)
🧠 sentence-transformers → text embeddings (all-MiniLM-L6-v2)
🔍 RAG                 → Retrieval Augmented Generation
💬 Text-to-SQL         → natural language to SQL
🚦 Question Router     → intelligent question classification
Frontend:
──────────
🌐 Streamlit           → web interface
📊 Plotly              → interactive charts
🐍 Python              → backend logic

---

## 📁 Data Architecture
raw.trips (1,000,660 rows)
↓
stg_trips (993,708 cleaned)
↓
┌─────┴──────────┐
↓                ↓
dim_payment    dim_location
↓                ↓
└──────┬──────────┘
↓
fct_trips ← main analytics table

---

## 💡 Key Insights Discovered
💰 Total Revenue:     $16,072,117
🚕 Total Trips:       993,708
💵 Average Fare:      $13.05
⏱️ Average Duration:  15.23 minutes
📍 Average Distance:  3.80 miles
Payment Split:
──────────────
💵 Cash:    62% of trips → $13.51 avg fare
💳 Credit:  38% of trips → $12.28 avg fare
Peak Hours:
────────────
🌆 Busiest: 9 PM  → 61,000 trips
😴 Quietest: 5 AM → 11,000 trips
Tips:
──────
💳 Credit card avg tip = $2.71
(card machine prompts automatically!)
💵 Cash tips not recorded in system

---

## 🔒 Security
✅ All credentials in Streamlit Secrets
✅ No passwords in GitHub
✅ Environment variables throughout
✅ API keys never exposed in code

---

## 📁 Main Project Repository

Full data engineering project with:
- dbt models and tests
- Day by day documentation
- Power BI dashboard screenshots
- Complete commands and insights

👉 **[nyc-taxi-dbt-clickhouse](https://github.com/Syed-H-jafri/nyc-taxi-dbt-clickhouse)**

---

## 👨‍💻 Built By

**Syed H Jafri**
Data Engineer | Python | SQL | AI

🔗 GitHub: [Syed-H-jafri](https://github.com/Syed-H-jafri)

---

*Built with ClickHouse Cloud + dbt + Groq AI +
sentence-transformers + Streamlit*
