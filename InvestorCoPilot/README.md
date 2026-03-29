# TradeIQ — AI-Powered Investment Research Assistant

> Think Smarter. Trade Clearer. Invest Confidently.

Built for the **ET Hackathon 2026** — a production-grade fintech AI assistant that analyzes financial reports, extracts key metrics, scores sentiment, and delivers portfolio-aware insights with full reasoning transparency.

---

## What It Does

- **PDF Analysis** — Upload any annual/quarterly report; extracts revenue, profit, margin, and growth automatically
- **Sentiment Detection** — Rule-based keyword analysis across 100+ financial signals
- **Portfolio Impact** — Cross-references your holdings to surface only what's relevant to you
- **Confidence Scoring** — Deterministic 0–100% score on every insight (no hallucination)
- **Reasoning Trace** — Every step the agent took, shown in plain English
- **AI Summary** — Optional Ollama-powered summary (works without it too)

---

## Project Structure

```
TradeIQ/
├── agent/
│   ├── agent_core.py          # InvestorAgent — orchestrates all tools
│   ├── task_planner.py        # Keyword-based task planner
│   └── reasoning_logger.py    # Step-by-step trace logger
├── tools/
│   ├── document_processor.py  # PDF/HTML text extraction (pdfplumber)
│   ├── metric_extractor.py    # Regex-based financial metric extraction
│   ├── sentiment_analyzer.py  # Lexicon-based sentiment scoring
│   ├── portfolio_manager.py   # SQLite portfolio CRUD + impact analysis
│   ├── alert_scanner.py       # Portfolio alert scanning
│   ├── ai_enhancer.py         # Optional Ollama AI summaries
│   └── market_news.py         # Market news feed
├── backend/
│   ├── confidence_engine.py   # Deterministic confidence scoring
│   ├── output_formatter.py    # Result formatting
│   └── validator.py           # Input validation
├── frontend/
│   └── app.py                 # Gradio UI — full fintech dashboard
├── data/
│   ├── portfolio.db           # SQLite database (auto-created)
│   ├── sample_reports/        # Place PDF reports here
│   └── cache/                 # Temporary cache
├── config.py                  # Paths, model settings, tool config
├── requirements.txt
├── run.py                     # Entry point
└── test_system.py             # Full test suite (56 tests)
```

---

## Setup

```bash
cd InvestorCoPilot
python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux
pip install -r requirements.txt
```

---

## Run

```bash
python run.py
```

Open **http://127.0.0.1:7860** in your browser.

### Options

```bash
python run.py --port 8080      # Custom port
python run.py --no-ai          # Disable Ollama (runs fully offline)
python run.py --share          # Create public Gradio link
python run.py --debug          # Verbose logging
```

---

## Demo

The app ships with a pre-loaded **TCS Q4 FY25** demo report. Click **"📄 Use Demo TCS Report"** in the Analyze tab to see the full pipeline in action without uploading a file.

**Demo portfolio** (Rahul Sharma):
| Stock | Shares | Avg Price |
|-------|--------|-----------|
| TCS | 50 | ₹3,850 |
| RELIANCE | 20 | ₹2,870 |
| INFOSYS | 30 | ₹1,530 |

---

## Run Tests

```bash
python test_system.py
```

56 tests covering all components — document processor, metric extractor, sentiment analyzer, portfolio manager, confidence engine, AI enhancer, and full agent integration.

---

## AI Mode

- **ON** — Uses local [Ollama](https://ollama.com) with `llama3.2:1b` for plain-English summaries
- **OFF** — Fully deterministic mode; all analysis uses regex + rule-based logic only

To enable AI summaries:
```bash
ollama pull llama3.2:1b
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| UI | Gradio 4.x |
| PDF Extraction | pdfplumber |
| Database | SQLite |
| AI (optional) | Ollama / llama3.2:1b |
| Language | Python 3.10+ |
