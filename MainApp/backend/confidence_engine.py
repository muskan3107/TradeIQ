"""
confidence_engine.py — Deterministic confidence scoring for InvestorCoPilot.

100% formula-based. No AI. Reads four signals from the agent context and
produces a weighted score, human-readable label, per-factor breakdown, and
an explanation list for display in the UI.

Context keys read:
    context['metrics']['metrics_found']          int
    context['sentiment']['total_signals']        int
    context['portfolio']['owns_stock']           bool
    context['document']['pages_extracted']       int

All keys are optional — missing data simply scores the minimum for that factor.
"""

import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)

# ── Scoring constants ─────────────────────────────────────────────────────────

BASE_SCORE = 0.30   # floor before any factors are added

# Factor weights (max contribution of each factor)
W_METRICS   = 0.25
W_SIGNALS   = 0.20
W_CONTEXT   = 0.15
W_DOCUMENT  = 0.10

# Thresholds
METRICS_HIGH,  METRICS_MID  = 3, 2
SIGNALS_HIGH,  SIGNALS_MID  = 10, 5
PAGES_HIGH,    PAGES_MID    = 15, 5

# Label bands
LABEL_VERY_HIGH = 0.80
LABEL_HIGH      = 0.65
LABEL_MODERATE  = 0.50


class ConfidenceEngine:
    """
    Scores analysis confidence based on four deterministic factors:
      1. Number of financial metrics extracted
      2. Number of sentiment signals detected
      3. Whether the user owns the analysed stock
      4. Document completeness (pages extracted)
    """

    def execute(self, context: Dict) -> Dict:
        """
        Entry point called by the agent.

        Args:
            context: Shared agent context dict containing outputs from
                     document_processor, metric_extractor, sentiment_analyzer,
                     and portfolio_manager.

        Returns:
            Structured confidence result (see module docstring).
        """
        try:
            # ── Read signals from context ─────────────────────────────────────
            metrics_found   = self._read_int(context, "metrics",   "metrics_found")
            total_signals   = self._read_int(context, "sentiment", "total_signals")
            owns_stock      = self._read_bool(context, "portfolio", "owns_stock")
            pages_extracted = self._read_int(context, "document",  "pages_extracted")

            logger.debug(
                "ConfidenceEngine inputs: metrics=%d signals=%d owns=%s pages=%d",
                metrics_found, total_signals, owns_stock, pages_extracted,
            )

            # ── Score each factor ─────────────────────────────────────────────
            score_metrics,  label_metrics  = self._score_metrics(metrics_found)
            score_signals,  label_signals  = self._score_signals(total_signals)
            score_context,  label_context  = self._score_context(owns_stock)
            score_document, label_document = self._score_document(pages_extracted)

            # ── Aggregate ─────────────────────────────────────────────────────
            raw_score = BASE_SCORE + score_metrics + score_signals + score_context + score_document
            score     = round(min(max(raw_score, 0.0), 1.0), 4)
            pct       = int(score * 100)
            label     = self._label(score)

            breakdown = {
                "base":     BASE_SCORE,
                "metrics":  score_metrics,
                "signals":  score_signals,
                "context":  score_context,
                "document": score_document,
            }

            factors = [label_metrics, label_signals, label_context, label_document]

            logger.debug(
                "ConfidenceEngine: score=%.4f (%d%%) label=%s breakdown=%s",
                score, pct, label, breakdown,
            )

            return {
                "score":      score,
                "percentage": pct,
                "label":      label,
                "factors":    factors,
                "breakdown":  breakdown,
                "success":    True,
            }

        except Exception as exc:  # noqa: BLE001
            msg = f"{type(exc).__name__}: {exc}"
            logger.error("ConfidenceEngine.execute failed: %s", msg)
            return self._failure(msg)

    # ── Factor scorers ────────────────────────────────────────────────────────

    @staticmethod
    def _score_metrics(count: int):
        """Factor 1 — financial metrics extracted (max 0.25)."""
        if count >= METRICS_HIGH:
            return W_METRICS, f"✅ {count} metrics found (+{W_METRICS})"
        if count >= METRICS_MID:
            return 0.15, f"⚠️  {count} metrics found (+0.15)"
        return 0.05, f"❌ {count} metrics found (+0.05)"

    @staticmethod
    def _score_signals(count: int):
        """Factor 2 — sentiment keyword signals (max 0.20)."""
        if count >= SIGNALS_HIGH:
            return W_SIGNALS, f"✅ {count} sentiment signals (+{W_SIGNALS})"
        if count >= SIGNALS_MID:
            return 0.12, f"⚠️  {count} sentiment signals (+0.12)"
        return 0.05, f"❌ {count} sentiment signals (+0.05)"

    @staticmethod
    def _score_context(owns: bool):
        """Factor 3 — portfolio context (max 0.15)."""
        if owns:
            return W_CONTEXT, f"✅ Stock found in portfolio (+{W_CONTEXT})"
        return 0.05, "❌ Stock not in portfolio (+0.05)"

    @staticmethod
    def _score_document(pages: int):
        """Factor 4 — document completeness (max 0.10)."""
        if pages >= PAGES_HIGH:
            return W_DOCUMENT, f"✅ {pages} pages extracted (+{W_DOCUMENT})"
        if pages >= PAGES_MID:
            return 0.06, f"⚠️  {pages} pages extracted (+0.06)"
        return 0.02, f"❌ {pages} pages extracted (+0.02)"

    # ── Label mapping ─────────────────────────────────────────────────────────

    @staticmethod
    def _label(score: float) -> str:
        if score >= LABEL_VERY_HIGH:
            return "Very High"
        if score >= LABEL_HIGH:
            return "High"
        if score >= LABEL_MODERATE:
            return "Moderate"
        return "Low"

    # ── Safe context readers ──────────────────────────────────────────────────

    @staticmethod
    def _read_int(context: Dict, tool_key: str, field: str, default: int = 0) -> int:
        """Safely reads an integer from context[tool_key][field]."""
        try:
            val = context[tool_key][field]
            return int(val) if val is not None else default
        except (KeyError, TypeError, ValueError):
            return default

    @staticmethod
    def _read_bool(context: Dict, tool_key: str, field: str, default: bool = False) -> bool:
        """Safely reads a boolean from context[tool_key][field]."""
        try:
            val = context[tool_key][field]
            return bool(val) if val is not None else default
        except (KeyError, TypeError):
            return default

    # ── Failure helper ────────────────────────────────────────────────────────

    @staticmethod
    def _failure(error: str) -> Dict:
        return {
            "score":      0.0,
            "percentage": 0,
            "label":      "Low",
            "factors":    [],
            "breakdown":  {},
            "success":    False,
            "error":      error,
        }
