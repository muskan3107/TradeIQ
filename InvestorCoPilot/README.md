# InvestorCoPilot

An AI-powered investment research assistant built for hackathon. It processes financial documents, extracts key metrics, analyzes sentiment, and manages portfolio data — all through a conversational agent interface.

## Features

- PDF/HTML financial report ingestion
- Automated metric extraction (revenue, EPS, P/E, etc.)
- Sentiment analysis on earnings calls and news
- Portfolio tracking with SQLite
- Real-time alert scanning
- AI-enhanced summaries and reasoning logs

## Project Structure

```
InvestorCoPilot/
├── agent/          # Core agent logic and task planning
├── tools/          # Individual tool modules
├── backend/        # Confidence engine, formatter, validator
├── frontend/       # Gradio UI
├── data/           # Database, reports, cache
├── config.py       # Central configuration
├── run.py          # Entry point
└── requirements.txt
```

## Setup

1. Clone the repo and navigate into the project:
   ```bash
   cd InvestorCoPilot
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## How to Run

```bash
python run.py
```

This starts the Gradio web UI. Open the URL shown in the terminal (usually `http://127.0.0.1:7860`) in your browser.
