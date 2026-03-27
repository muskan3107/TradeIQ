"""
agent_core.py — The brain of InvestorCoPilot AI.

InvestorAgent receives a task, builds an execution plan of tool steps,
runs each step while passing a shared context dict forward, logs every
action with a timestamp, handles failures gracefully, and compiles a
structured result dict at the end.
"""

import sys
import os
# Allow imports from the project root regardless of how the module is loaded
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from datetime import datetime, timezone
from typing import Any

# ── Tool imports ──────────────────────────────────────────────────────────────
from tools.document_processor import DocumentProcessor
from tools.metric_extractor import MetricExtractor
from tools.sentiment_analyzer import SentimentAnalyzer
from tools.portfolio_manager import PortfolioManager
from tools.alert_scanner import AlertScanner
from tools.ai_enhancer import AIEnhancer
from backend.confidence_engine import ConfidenceEngine


# ── Supported task types ──────────────────────────────────────────────────────
TASK_ANALYZE_DOCUMENT = "analyze_document"
TASK_ANSWER_QUESTION  = "answer_question"
TASK_CHECK_ALERTS     = "check_alerts"

SUPPORTED_TASKS = {TASK_ANALYZE_DOCUMENT, TASK_ANSWER_QUESTION, TASK_CHECK_ALERTS}


class InvestorAgent:
    """
    Orchestrates tool execution for investment research tasks.

    Usage:
        agent = InvestorAgent()
        result = agent.receive_task("analyze_document", {"source": "report.pdf"})
    """

    def __init__(self):
        # Instantiate all tools once; they are reused across calls.
        self.document_processor = DocumentProcessor()
        self.metric_extractor   = MetricExtractor()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.portfolio_manager  = PortfolioManager()
        self.alert_scanner      = AlertScanner()
        self.ai_enhancer        = AIEnhancer()
        self.confidence_engine  = ConfidenceEngine()

        # Reasoning trace is reset on every receive_task call.
        self._trace: list[str] = []

    # ── Public entry point ────────────────────────────────────────────────────

    def receive_task(self, task_type: str, task_data: dict) -> dict:
        """
        Main entry point.

        Args:
            task_type: One of 'analyze_document', 'answer_question', 'check_alerts'.
            task_data: Arbitrary dict passed to the first tool and carried through
                       the context.  For 'analyze_document' it must contain 'source'.

        Returns:
            Structured result dict (see module docstring for schema).
        """
        self._trace = []
        started_at = datetime.now(timezone.utc).isoformat()

        self._log_step("receive_task", f"task_type='{task_type}' | data_keys={list(task_data.keys())}")

        # ── Validate task type ────────────────────────────────────────────────
        if task_type not in SUPPORTED_TASKS:
            self._log_step("validation_error", f"Unknown task type: '{task_type}'")
            return self._error_result(started_at, task_type, f"Unsupported task type: '{task_type}'")

        # ── Build plan ────────────────────────────────────────────────────────
        plan = self._create_plan(task_type, task_data)
        self._log_step("plan_created", f"{len(plan)} steps: {[s['name'] for s in plan]}")

        # ── Execute plan ──────────────────────────────────────────────────────
        context = self._execute_plan(plan, task_data)

        # ── Compile and return ────────────────────────────────────────────────
        result = self._compile_result(context, started_at, task_type)
        self._log_step("task_complete", f"success={result['success']} | confidence={result['confidence']}")
        return result

    # ── Plan builder ──────────────────────────────────────────────────────────

    def _create_plan(self, task_type: str, task_data: dict) -> list[dict]:
        """
        Returns an ordered list of step descriptors.

        Each step is:
            {
                'name': str,          # human-readable label
                'fn':   callable,     # tool method to call
                'input_key': str,     # key in context to pass as primary input
                                      # (None → pass full context dict)
                'output_key': str,    # key under which to store the result
            }
        """
        if task_type == TASK_ANALYZE_DOCUMENT:
            return [
                {
                    "name": "document_processor",
                    "fn": self.document_processor.process,
                    # The raw source (file path or text) lives in task_data['source']
                    "input_key": "source",
                    "output_key": "document",
                },
                {
                    "name": "metric_extractor",
                    "fn": self._extract_metrics_from_context,
                    # Reads context['document']['text'] internally
                    "input_key": None,
                    "output_key": "metrics",
                },
                {
                    "name": "sentiment_analyzer",
                    "fn": self._analyze_sentiment_from_context,
                    "input_key": None,
                    "output_key": "sentiment",
                },
                {
                    "name": "portfolio_manager",
                    "fn": lambda _ctx: self.portfolio_manager.get_summary(),
                    "input_key": None,
                    "output_key": "portfolio",
                },
                {
                    "name": "confidence_engine",
                    "fn": self._score_confidence_from_context,
                    "input_key": None,
                    "output_key": "confidence",
                },
                {
                    # Optional — runs only when document text is available
                    "name": "ai_enhancer",
                    "fn": self._enhance_from_context,
                    "input_key": None,
                    "output_key": "ai_summary",
                    "optional": True,
                },
            ]

        if task_type == TASK_ANSWER_QUESTION:
            return [
                {
                    "name": "question_classifier",
                    "fn": self._classify_question,
                    "input_key": "question",
                    "output_key": "question_class",
                },
                {
                    "name": "portfolio_manager",
                    "fn": lambda _ctx: self.portfolio_manager.get_summary(),
                    "input_key": None,
                    "output_key": "portfolio",
                },
                {
                    "name": "alert_scanner",
                    "fn": lambda _ctx: self.alert_scanner.scan(),
                    "input_key": None,
                    "output_key": "alerts",
                },
                {
                    "name": "confidence_engine",
                    "fn": self._score_confidence_from_context,
                    "input_key": None,
                    "output_key": "confidence",
                },
            ]

        if task_type == TASK_CHECK_ALERTS:
            return [
                {
                    "name": "alert_scanner",
                    "fn": lambda _ctx: self.alert_scanner.scan(),
                    "input_key": None,
                    "output_key": "alerts",
                },
                {
                    "name": "portfolio_manager",
                    "fn": lambda _ctx: self.portfolio_manager.get_summary(),
                    "input_key": None,
                    "output_key": "portfolio",
                },
                {
                    "name": "confidence_engine",
                    "fn": self._score_confidence_from_context,
                    "input_key": None,
                    "output_key": "confidence",
                },
            ]

        return []  # unreachable after validation, but safe fallback

    # ── Plan executor ─────────────────────────────────────────────────────────

    def _execute_plan(self, plan: list[dict], task_data: dict) -> dict:
        """
        Runs each step in order, accumulating results in a shared context dict.

        - Each tool receives the full context so it can read prior outputs.
        - On failure the step is skipped and execution continues.
        - The original task_data is merged into context at the start.
        """
        # Seed context with the raw task inputs so tools can read them directly.
        context: dict[str, Any] = dict(task_data)
        context["_steps_succeeded"] = []
        context["_steps_failed"]    = []

        for step in plan:
            name       = step["name"]
            fn         = step["fn"]
            input_key  = step.get("input_key")
            output_key = step["output_key"]
            optional   = step.get("optional", False)

            self._log_step(f"start:{name}", f"optional={optional}")

            try:
                # Determine what to pass to the tool function.
                if input_key is not None:
                    # Pass the specific value from context (falls back to None).
                    arg = context.get(input_key)
                    result = fn(arg)
                else:
                    # Pass the whole context so the tool can pick what it needs.
                    result = fn(context)

                context[output_key] = result
                context["_steps_succeeded"].append(name)
                self._log_step(f"done:{name}", f"output_key='{output_key}' | result_type={type(result).__name__}")

            except Exception as exc:  # noqa: BLE001
                # Log the failure but keep going — resilience over perfection.
                error_msg = f"{type(exc).__name__}: {exc}"
                context[output_key] = None
                context["_steps_failed"].append({"step": name, "error": error_msg})
                self._log_step(
                    f"error:{name}",
                    f"{'(optional) ' if optional else ''}FAILED — {error_msg}",
                )

        return context

    # ── Result compiler ───────────────────────────────────────────────────────

    def _compile_result(self, context: dict, timestamp: str, task_type: str) -> dict:
        """
        Assembles the final structured result from the execution context.
        """
        failed_steps = context.get("_steps_failed", [])
        succeeded    = context.get("_steps_succeeded", [])

        # Determine overall success: at least one non-optional step succeeded
        # and the critical outputs are not all None.
        critical_outputs = ["metrics", "sentiment", "portfolio", "alerts", "question_class"]
        any_critical = any(context.get(k) is not None for k in critical_outputs)
        success = len(succeeded) > 0 and (any_critical or task_type == TASK_CHECK_ALERTS)

        # Portfolio impact: simple summary of current positions vs. sentiment
        portfolio_impact = self._derive_portfolio_impact(context)

        # Confidence value — already computed by confidence_engine step (float 0-1)
        raw_confidence = context.get("confidence", 0.0)
        confidence_payload = {
            "score": raw_confidence,
            "level": self._confidence_label(raw_confidence),
            "steps_succeeded": len(succeeded),
            "steps_failed": len(failed_steps),
        }

        result: dict[str, Any] = {
            "timestamp":        timestamp,
            "task_type":        task_type,
            "success":          success,
            "metrics":          context.get("metrics") or {},
            "sentiment":        context.get("sentiment") or {},
            "portfolio_impact": portfolio_impact,
            "confidence":       confidence_payload,
            "reasoning_trace":  list(self._trace),
            "agent_used":       True,
        }

        # Optional fields — only include when data is present
        if context.get("alerts") is not None:
            result["alerts"] = context["alerts"]

        if context.get("question_class") is not None:
            result["question_class"] = context["question_class"]

        if context.get("ai_summary") is not None:
            result["summary"] = context["ai_summary"].get("summary", "")

        if failed_steps:
            result["warnings"] = [f"{s['step']}: {s['error']}" for s in failed_steps]

        return result

    # ── Logging ───────────────────────────────────────────────────────────────

    def _log_step(self, action: str, details: str = "") -> None:
        """
        Appends a timestamped entry to the reasoning trace.

        Format: [HH:MM:SS.mmm UTC] ACTION | details
        """
        ts    = datetime.now(timezone.utc).strftime("%H:%M:%S.%f")[:-3]
        entry = f"[{ts} UTC] {action.upper():<30} | {details}"
        self._trace.append(entry)

    # ── Internal tool adapters ────────────────────────────────────────────────
    # These bridge the gap between the generic context dict and each tool's
    # specific method signature.

    def _extract_metrics_from_context(self, context: dict) -> dict:
        """Pulls text from the document_processor output and runs MetricExtractor."""
        doc  = context.get("document") or {}
        text = doc.get("text", "") if isinstance(doc, dict) else str(doc)
        if not text:
            raise ValueError("No document text available for metric extraction.")
        return self.metric_extractor.extract(text)

    def _analyze_sentiment_from_context(self, context: dict) -> dict:
        """Pulls text from the document_processor output and runs SentimentAnalyzer."""
        doc  = context.get("document") or {}
        text = doc.get("text", "") if isinstance(doc, dict) else str(doc)
        if not text:
            raise ValueError("No document text available for sentiment analysis.")
        return self.sentiment_analyzer.analyze(text)

    def _score_confidence_from_context(self, context: dict) -> float:
        """
        Builds a results list from all non-private context keys and scores them.
        """
        results = [
            {"result": v}
            for k, v in context.items()
            if not k.startswith("_") and v is not None
        ]
        return self.confidence_engine.score(results)

    def _enhance_from_context(self, context: dict) -> dict:
        """Generates an AI summary from available document text."""
        doc  = context.get("document") or {}
        text = doc.get("text", "") if isinstance(doc, dict) else ""

        # Build a richer prompt by appending extracted metrics and sentiment
        metrics   = context.get("metrics") or {}
        sentiment = context.get("sentiment") or {}

        prompt_parts = []
        if text:
            prompt_parts.append(f"Document excerpt: {text[:500]}")
        if metrics:
            prompt_parts.append(f"Metrics: {metrics}")
        if sentiment:
            prompt_parts.append(f"Sentiment: {sentiment}")

        if not prompt_parts:
            raise ValueError("No content available for AI enhancement.")

        return self.ai_enhancer.enhance("\n".join(prompt_parts))

    def _classify_question(self, question: str) -> dict:
        """
        Lightweight keyword-based question classifier.
        Returns a category and the original question for downstream tools.
        """
        if not question:
            raise ValueError("Question text is empty.")

        q = question.lower()

        if any(w in q for w in ("portfolio", "holding", "position", "stock")):
            category = "portfolio_query"
        elif any(w in q for w in ("alert", "watch", "notify", "threshold")):
            category = "alert_query"
        elif any(w in q for w in ("sentiment", "news", "feeling", "outlook")):
            category = "sentiment_query"
        elif any(w in q for w in ("metric", "revenue", "eps", "profit", "ratio")):
            category = "metric_query"
        else:
            category = "general_query"

        return {"category": category, "question": question}

    # ── Helpers ───────────────────────────────────────────────────────────────

    def _derive_portfolio_impact(self, context: dict) -> dict:
        """
        Cross-references sentiment with portfolio positions to flag potential impact.
        """
        portfolio = context.get("portfolio") or []
        sentiment = context.get("sentiment") or {}
        label     = sentiment.get("label", "neutral")
        score     = sentiment.get("score", 0.0)

        if not portfolio:
            return {"positions_affected": 0, "sentiment_signal": label, "note": "No positions on record."}

        return {
            "positions_affected": len(portfolio),
            "sentiment_signal":   label,
            "sentiment_score":    score,
            "note": (
                f"Sentiment is {label} (score {score}). "
                f"Review {len(portfolio)} position(s) for potential impact."
            ),
        }

    @staticmethod
    def _confidence_label(score: float) -> str:
        if score >= 0.8:
            return "high"
        if score >= 0.5:
            return "medium"
        return "low"

    @staticmethod
    def _error_result(timestamp: str, task_type: str, message: str) -> dict:
        return {
            "timestamp":        timestamp,
            "task_type":        task_type,
            "success":          False,
            "metrics":          {},
            "sentiment":        {},
            "portfolio_impact": {},
            "confidence":       {"score": 0.0, "level": "low"},
            "warnings":         [message],
            "reasoning_trace":  [],
            "agent_used":       True,
        }
