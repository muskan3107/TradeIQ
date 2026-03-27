"""
metric_extractor.py — Deterministic financial metric extraction via regex.

No AI involved. Patterns cover Indian (₹/crore/lakh) and US ($) formats,
common report phrasing, and abbreviations seen in real filings.

Context input:
    context['document_processor']['text']  — raw text from DocumentProcessor

Return:
    {
        'metrics':       {'revenue': float|None, 'profit': float|None,
                          'margin': float|None,  'growth': float|None},
        'metrics_found': int,
        'raw_matches':   {metric: matched_string},   # for debugging
        'success':       bool,
        'error':         str   # only on failure
    }
"""

import logging
import re
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

# ── Regex pattern bank ────────────────────────────────────────────────────────
# Each entry is (label, compiled_pattern).
# Patterns are tried in order; first match wins for each metric.
# Group 1 must always capture the raw numeric string (may contain commas/dots).

_CURRENCY   = r"(?:₹|rs\.?|inr|usd|\$)\s*"
_NUMBER     = r"([\d,]+(?:\.\d+)?)"          # e.g. 62,000  or  5.2
_UNIT       = r"\s*(?:crore|cr\.?|billion|bn\.?|million|mn\.?|lakh|lac)?"
_UNIT_CAP   = r"\s*(?:crore|cr\.?|billion|bn\.?|million|mn\.?|lakh|lac)"  # unit required
_PCT        = r"([\d,]+(?:\.\d+)?)\s*%"

REVENUE_PATTERNS: List[Tuple[str, re.Pattern]] = [
    ("revenue_labeled",   re.compile(
        r"(?:total\s+)?revenue[s]?\s*[:\-–]?\s*" + _CURRENCY + _NUMBER + _UNIT,
        re.IGNORECASE)),
    ("total_income",      re.compile(
        r"total\s+income\s*[:\-–]?\s*" + _CURRENCY + _NUMBER + _UNIT,
        re.IGNORECASE)),
    ("net_sales",         re.compile(
        r"net\s+sales\s*[:\-–]?\s*" + _CURRENCY + _NUMBER + _UNIT,
        re.IGNORECASE)),
    ("turnover",          re.compile(
        r"(?:gross\s+)?turnover\s*[:\-–]?\s*" + _CURRENCY + _NUMBER + _UNIT,
        re.IGNORECASE)),
    ("revenue_unit_req",  re.compile(
        r"revenue[s]?\s+(?:of\s+)?" + _CURRENCY + _NUMBER + _UNIT_CAP,
        re.IGNORECASE)),
]

PROFIT_PATTERNS: List[Tuple[str, re.Pattern]] = [
    ("pat_labeled",       re.compile(
        r"pat\s*[:\-–]?\s*" + _CURRENCY + _NUMBER + _UNIT,
        re.IGNORECASE)),
    ("net_profit",        re.compile(
        r"net\s+profit\s*[:\-–]?\s*" + _CURRENCY + _NUMBER + _UNIT,
        re.IGNORECASE)),
    ("profit_after_tax",  re.compile(
        r"profit\s+after\s+tax\s*[:\-–]?\s*" + _CURRENCY + _NUMBER + _UNIT,
        re.IGNORECASE)),
    ("profit_before_tax", re.compile(
        r"profit\s+before\s+tax\s*[:\-–]?\s*" + _CURRENCY + _NUMBER + _UNIT,
        re.IGNORECASE)),
    ("net_income",        re.compile(
        r"net\s+income\s*[:\-–]?\s*" + _CURRENCY + _NUMBER + _UNIT,
        re.IGNORECASE)),
    ("ebitda",            re.compile(
        r"ebitda\s*[:\-–]?\s*" + _CURRENCY + _NUMBER + _UNIT,
        re.IGNORECASE)),
]

MARGIN_PATTERNS: List[Tuple[str, re.Pattern]] = [
    ("margin_labeled",    re.compile(
        r"(?:net|operating|ebitda|gross|profit)?\s*margin\s*[:\-–]?\s*" + _PCT,
        re.IGNORECASE)),
    ("margin_pct",        re.compile(
        r"margin\s+(?:of\s+|is\s+|at\s+)?" + _PCT,
        re.IGNORECASE)),
    ("operating_margin",  re.compile(
        r"operating\s+(?:profit\s+)?margin\s*[:\-–]?\s*" + _PCT,
        re.IGNORECASE)),
]

GROWTH_PATTERNS: List[Tuple[str, re.Pattern]] = [
    ("yoy_growth",        re.compile(
        r"y[\-\s]?o[\-\s]?y\s+(?:growth|increase|decline)?\s*[:\-–]?\s*" + _PCT,
        re.IGNORECASE)),
    ("growth_labeled",    re.compile(
        r"(?:revenue|profit|sales|income)?\s*growth\s*[:\-–]?\s*" + _PCT,
        re.IGNORECASE)),
    ("grew_by",           re.compile(
        r"grew\s+(?:by\s+)?" + _PCT,
        re.IGNORECASE)),
    ("increased_by",      re.compile(
        r"(?:increased?|rose|up)\s+(?:by\s+)?" + _PCT,
        re.IGNORECASE)),
    ("declined_by",       re.compile(
        r"(?:declined?|fell|down)\s+(?:by\s+)?" + _PCT,
        re.IGNORECASE)),
]

# Unit multipliers — normalise everything to crore (Indian) or as-is (US)
_UNIT_MULTIPLIERS = {
    "billion": 1_000_000 / 100,   # 1 billion = 10,000 crore (approx, for display)
    "bn":      1_000_000 / 100,
    "million": 1_000,             # 1 million = 10 lakh = 0.1 crore → keep raw
    "mn":      1_000,
    "lakh":    0.01,              # 1 lakh = 0.01 crore
    "lac":     0.01,
    "crore":   1.0,
    "cr":      1.0,
}


class MetricExtractor:
    """
    Extracts revenue, profit, margin, and growth from financial report text
    using deterministic regex patterns only.
    """

    def execute(self, context: Dict) -> Dict:
        """
        Entry point called by the agent.

        Reads text from context['document_processor']['text'].
        Falls back to context['document']['text'] for backward compatibility.
        """
        text = self._resolve_text(context)

        if text is None:
            msg = (
                "No text found in context. "
                "Expected context['document_processor']['text'] to be a non-empty string."
            )
            logger.warning(msg)
            return self._failure(msg)

        if not text.strip():
            msg = "Document text is empty — nothing to extract."
            logger.warning(msg)
            return self._failure(msg)

        logger.debug("MetricExtractor: processing %d characters of text.", len(text))
        return self._extract(text)

    # ── Core extraction ───────────────────────────────────────────────────────

    def _extract(self, text: str) -> Dict:
        raw_matches: Dict[str, str] = {}

        revenue = self._first_match(text, REVENUE_PATTERNS, "revenue", raw_matches)
        profit  = self._first_match(text, PROFIT_PATTERNS,  "profit",  raw_matches)
        margin  = self._first_pct_match(text, MARGIN_PATTERNS, "margin", raw_matches)
        growth  = self._first_pct_match(text, GROWTH_PATTERNS, "growth", raw_matches)

        metrics = {
            "revenue": revenue,
            "profit":  profit,
            "margin":  margin,
            "growth":  growth,
        }
        found = sum(1 for v in metrics.values() if v is not None)

        logger.debug(
            "MetricExtractor: found %d/%d metrics. raw_matches=%s",
            found, len(metrics), raw_matches,
        )

        return {
            "metrics":       metrics,
            "metrics_found": found,
            "raw_matches":   raw_matches,   # useful for debugging / UI display
            "success":       True,
        }

    # ── Pattern matching helpers ──────────────────────────────────────────────

    def _first_match(
        self,
        text: str,
        patterns: List[Tuple[str, re.Pattern]],
        label: str,
        raw_matches: Dict,
    ) -> Optional[float]:
        """
        Tries each pattern in order.  Returns the first successfully parsed
        float value, or None if nothing matched.

        Captures the raw matched substring in raw_matches[label] for debugging.
        """
        for name, pattern in patterns:
            match = pattern.search(text)
            if match:
                raw_num = match.group(1)
                value   = self._parse_number(raw_num)
                if value is None:
                    logger.debug("Pattern '%s' matched '%s' but parse failed.", name, raw_num)
                    continue

                # Detect unit in the surrounding match text and apply multiplier
                surrounding = match.group(0).lower()
                value = self._apply_unit(value, surrounding)

                raw_matches[label] = match.group(0).strip()
                logger.debug(
                    "Metric '%s' matched by pattern '%s': raw='%s' -> %.4f",
                    label, name, raw_num, value,
                )
                return value

        logger.debug("Metric '%s': no pattern matched.", label)
        return None

    def _first_pct_match(
        self,
        text: str,
        patterns: List[Tuple[str, re.Pattern]],
        label: str,
        raw_matches: Dict,
    ) -> Optional[float]:
        """
        Same as _first_match but for percentage values (no unit multiplier).
        """
        for name, pattern in patterns:
            match = pattern.search(text)
            if match:
                raw_num = match.group(1)
                value   = self._parse_number(raw_num)
                if value is None:
                    continue
                raw_matches[label] = match.group(0).strip()
                logger.debug(
                    "Metric '%s' matched by pattern '%s': raw='%s' -> %.4f%%",
                    label, name, raw_num, value,
                )
                return value

        logger.debug("Metric '%s': no pattern matched.", label)
        return None

    # ── Value cleaning ────────────────────────────────────────────────────────

    @staticmethod
    def _parse_number(raw: str) -> Optional[float]:
        """Strips commas and converts to float.  Returns None on failure."""
        try:
            return float(raw.replace(",", "").strip())
        except (ValueError, AttributeError):
            return None

    @staticmethod
    def _apply_unit(value: float, text: str) -> float:
        """
        Scales the value based on the unit word found in the matched text.
        Crore is the base unit; billion/million/lakh are converted.
        """
        for unit, multiplier in _UNIT_MULTIPLIERS.items():
            if unit in text:
                return round(value * multiplier, 4)
        # No recognised unit — return as-is (could be a plain number in the text)
        return value

    # ── Context resolution ────────────────────────────────────────────────────

    @staticmethod
    def _resolve_text(context: Dict) -> Optional[str]:
        """
        Tries multiple context key paths to find the document text.

        Priority:
          1. context['document_processor']['text']   (canonical agent path)
          2. context['document']['text']             (backward compat)
          3. context['text']                         (direct pass-through)
        """
        try:
            text = context["document_processor"]["text"]
            if text and isinstance(text, str):
                return text
        except (KeyError, TypeError):
            pass

        try:
            text = context["document"]["text"]
            if text and isinstance(text, str):
                return text
        except (KeyError, TypeError):
            pass

        try:
            text = context["text"]
            if text and isinstance(text, str):
                return text
        except (KeyError, TypeError):
            pass

        return None

    # ── Failure helper ────────────────────────────────────────────────────────

    @staticmethod
    def _failure(error: str) -> Dict:
        return {
            "metrics":       {"revenue": None, "profit": None, "margin": None, "growth": None},
            "metrics_found": 0,
            "raw_matches":   {},
            "success":       False,
            "error":         error,
        }
