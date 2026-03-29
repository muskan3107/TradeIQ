# TradeIQ — AI-Powered Investment Intelligence

> Think Smarter. Trade Clearer. Invest Confidently.

TradeIQ is an agentic AI system designed to help Indian retail investors move beyond guesswork by delivering **structured, explainable, and portfolio-aware financial insights**.

---

## 🚨 The Problem

Despite 14+ crore demat accounts in India, most retail investors:

* Rely on **tips and fragmented information**
* Struggle to interpret **financial reports and filings**
* Use AI tools that act as **black boxes with no explanation**
* Miss opportunities due to **slow or manual analysis**
* Lack access to tools in **vernacular languages**
* Face increasing concerns around **AI cost and energy usage**

---

## 💡 Our Approach

TradeIQ combines **deterministic systems + agentic AI reasoning** to build a reliable and transparent investment assistant:

* Extracts structured financial signals (not just summaries)
* Explains every decision with a **step-by-step reasoning trace**
* Assigns a **confidence score (0–100%)** to reduce blind trust
* Works even without AI (fully deterministic fallback mode)
* Supports **vernacular accessibility (Hindi language support)**
* Minimizes AI usage for **efficiency and sustainability**

---

## 🚀 Key Highlights

* 🧠 **Agent-Based System** — dynamically selects tools based on task
* 📊 **Portfolio-Aware Intelligence** — insights tailored to holdings
* 📉 **Confidence Scoring Engine** — quantifies reliability of outputs
* 🔍 **Reasoning Transparency** — no black-box decisions
* 🌏 **Vernacular Ready** — built for Indian users
* ⚡ **Sustainable Hybrid Design** — reduces unnecessary AI calls

---

## 🧩 System Architecture (High-Level)

```
User Input
   ↓
Frontend (Gradio UI)
   ↓
Agent Core (Decision Engine)
   ↓
Tools Layer
   ├── Document Processor
   ├── Metric Extractor
   ├── Sentiment Analyzer
   ├── Portfolio Manager
   ├── Alert Scanner
   ├── Confidence Engine
   ↓
AI Enhancer (Optional - Ollama)
   ↓
Final Output + Reasoning Trace
```

Fallback:

* If AI is OFF → system runs fully deterministic

---

## 📁 Project Structure

```
TradeIQ/
└── MainApp/
    ├── agent/
    │   ├── agent_core.py
    │   ├── task_planner.py
    │   └── reasoning_logger.py
    │
    ├── tools/
    │   ├── document_processor.py
    │   ├── metric_extractor.py
    │   ├── sentiment_analyzer.py
    │   ├── portfolio_manager.py
    │   ├── alert_scanner.py
    │   ├── ai_enhancer.py
    │   └── market_news.py
    │
    ├── backend/
    │   ├── confidence_engine.py
    │   ├── output_formatter.py
    │   └── validator.py
    │
    ├── frontend/
    │   └── app.py
    │
    ├── data/
    │   ├── portfolio.db
    │   ├── sample_reports/
    │   └── cache/
    │
    ├── config.py
    ├── run.py
    ├── test_system.py
    └── requirements.txt
```

---

## ⚙️ Setup Instructions

```bash
git clone https://github.com/muskan3107/TradeIQ.git
cd TradeIQ/MainApp

python -m venv venv
venv\Scripts\activate        # Windows
# source venv/bin/activate   # Mac/Linux

pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
python run.py
```

Open in browser:

```
http://127.0.0.1:7860
```

---

## 🔧 Runtime Options

```bash
python run.py --port 8080
python run.py --no-ai
python run.py --share
python run.py --debug
```

---

## 🎯 Demo Flow

The app includes a pre-loaded demo report.

Steps:

1. Open "Analyze"
2. Click **"📄 Use Demo TCS Report"**
3. Run analysis
4. Observe:

   * extracted metrics
   * sentiment detection
   * reasoning steps
   * confidence score
   * portfolio impact

---

## 👤 Demo Portfolio

Demo User: **Rahul Sharma**

| Stock    | Shares | Avg Price |
| -------- | ------ | --------- |
| TCS      | 50     | ₹3,850    |
| RELIANCE | 20     | ₹2,870    |
| INFOSYS  | 30     | ₹1,530    |

---

## 🤖 AI Mode

* **ON** → Uses local Ollama (`llama3.2:1b`) for natural language summaries
* **OFF** → Fully deterministic (no AI dependency)

Enable AI:

```bash
ollama pull llama3.2:1b
```

This ensures reliability even in low-connectivity or restricted environments.

---

## 🌏 Vernacular Support

TradeIQ includes basic Hindi UI support for accessibility:

* Analyze → विश्लेषण करें
* Insights → अंतर्दृष्टि
* Portfolio → पोर्टफोलियो
* Confidence → विश्वास स्कोर

---

## 🧪 Testing

```bash
python test_system.py
```

✔ 56 test cases covering:

* document processing
* metric extraction
* sentiment analysis
* portfolio logic
* confidence engine
* AI fallback
* full agent integration

---

## 📈 Potential Impact

TradeIQ reduces manual financial analysis time:

* ⏱ From ~15 minutes → under 2 minutes per report
* 📊 ~2,000+ hours saved daily (at 10,000 users)
* 💰 Faster decision-making improves opportunity capture
* 🧠 Reduces emotional and reactive investing

---

## 🛠 Tech Stack

| Layer          | Technology           |
| -------------- | -------------------- |
| UI             | Gradio 4.x           |
| Backend        | Python 3.10+         |
| PDF Processing | pdfplumber           |
| Database       | SQLite               |
| AI (Optional)  | Ollama (llama3.2:1b) |

---

## 🏁 Final Note

TradeIQ is designed as a **trust-first AI system** — where every insight is explainable, measurable, and actionable.

Unlike black-box AI tools, TradeIQ ensures:

* transparency
* reliability
* user confidence

## Team
* **Muskan Sahay** - [[GitHub Profile Link]](https://github.com/muskan3107)

