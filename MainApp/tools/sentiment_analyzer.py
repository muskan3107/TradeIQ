"""
sentiment_analyzer.py — Rule-based financial sentiment detection.

No AI. Pure whole-word keyword matching against curated positive/negative
lexicons tuned for financial report language (earnings calls, annual reports,
investor presentations).

Context input:
    context['document_processor']['text']  — raw text from DocumentProcessor

Return:
    {
        'sentiment':        'positive' | 'negative' | 'neutral',
        'score':            float,   # pos / (pos + neg), range [0, 1]
        'positive_signals': int,
        'negative_signals': int,
        'total_signals':    int,
        'matched_positive': list[str],   # deduplicated words that fired
        'matched_negative': list[str],
        'success':          bool,
        'error':            str          # only on failure
    }
"""

import logging
import re
from typing import Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

# ── Keyword lexicons ──────────────────────────────────────────────────────────
# Words are matched as whole tokens (word boundaries) to avoid false positives
# e.g. "record" should not match inside "recorded" unless it's standalone.

POSITIVE_KEYWORDS: List[str] = [
    # Performance & results
    "growth",
    "grew",
    "increase",
    "increased",
    "improvement",
    "improved",
    "strong",
    "stronger",
    "strength",
    "beat",
    "exceeded",
    "outperformed",
    "outperform",
    "record",
    "expansion",
    "expanded",
    "accelerated",
    "acceleration",
    "momentum",
    "robust",
    # Profitability
    "profit",
    "profitable",
    "profitability",
    "margin",
    "surplus",
    "gain",
    "gains",
    "earnings",
    "dividend",
    "yield",
    # Outlook & confidence
    "optimistic",
    "confident",
    "positive",
    "opportunity",
    "opportunities",
    "promising",
    "upside",
    "recovery",
    "resilient",
    "resilience",
    "stable",
    "stability",
    "upgrade",
    "upgraded",
    "outperformance",
    "breakthrough",
    "milestone",
    "leadership",
    "innovation",
    "efficient",
    "efficiency",
]

NEGATIVE_KEYWORDS: List[str] = [
    # Performance & results
    "decline",
    "declined",
    "decrease",
    "decreased",
    "weak",
    "weaker",
    "weakness",
    "drop",
    "dropped",
    "loss",
    "losses",
    "miss",
    "missed",
    "underperformed",
    "underperform",
    "slowdown",
    "slowed",
    "contraction",
    "contracted",
    "deterioration",
    "deteriorated",
    # Risk & concern
    "concern",
    "concerns",
    "risk",
    "risks",
    "challenge",
    "challenges",
    "headwind",
    "headwinds",
    "pressure",
    "pressures",
    "uncertainty",
    "uncertain",
    "volatile",
    "volatility",
    "disruption",
    "disruptions",
    # Financial stress
    "debt",
    "default",
    "impairment",
    "writeoff",
    "write-off",
    "downgrade",
    "downgraded",
    "deficit",
    "shortfall",
    "penalty",
    "litigation",
    "lawsuit",
    "fraud",
    "investigation",
    "restructuring",
    "layoff",
    "layoffs",
]

# Score thresholds
_THRESHOLD_POSITIVE = 0.6
_THRESHOLD_NEGATIVE = 0.4


class SentimentAnalyzer:
    """
    Counts positive and negative keyword occurrences in financial text
    and derives a sentiment score and label.
    """

    def __init__(self):
        # Pre-compile one regex per keyword for whole-word, case-insensitive matching.
        # Using word boundaries (\b) prevents "loss" matching "glossy", etc.
        self._pos_patterns: List[Tuple[str, re.Pattern]] = [
            (kw, re.compile(rf"\b{re.escape(kw)}\b", re.IGNORECASE))
            for kw in POSITIVE_KEYWORDS
        ]
        self._neg_patterns: List[Tuple[str, re.Pattern]] = [
            (kw, re.compile(rf"\b{re.escape(kw)}\b", re.IGNORECASE))
            for kw in NEGATIVE_KEYWORDS
        ]

    def execute(self, context: Dict) -> Dict:
        """
        Entry point called by the agent.

        Reads text from context['document_processor']['text'].
        Falls back to context['document']['text'] and context['text'].
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
            msg = "Document text is empty — cannot determine sentiment."
            logger.warning(msg)
            return self._failure(msg)

        logger.debug("SentimentAnalyzer: processing %d characters.", len(text))
        return self._analyze(text)

    # ── Core analysis ─────────────────────────────────────────────────────────

    def _analyze(self, text: str) -> Dict:
        pos_hits, pos_matched = self._count_keywords(text, self._pos_patterns)
        neg_hits, neg_matched = self._count_keywords(text, self._neg_patterns)
        total = pos_hits + neg_hits

        # Score: proportion of positive signals; 0.5 when no signals found
        if total == 0:
            score = 0.5
        else:
            score = round(pos_hits / total, 4)

        # Classify
        if score > _THRESHOLD_POSITIVE:
            label = "positive"
        elif score < _THRESHOLD_NEGATIVE:
            label = "negative"
        else:
            label = "neutral"

        logger.debug(
            "SentimentAnalyzer: pos=%d neg=%d score=%.4f label=%s",
            pos_hits, neg_hits, score, label,
        )

        return {
            "sentiment":        label,
            "score":            score,
            "positive_signals": pos_hits,
            "negative_signals": neg_hits,
            "total_signals":    total,
            "matched_positive": pos_matched,
            "matched_negative": neg_matched,
            "success":          True,
        }

    # ── Keyword counting ──────────────────────────────────────────────────────

    @staticmethod
    def _count_keywords(
        text: str,
        patterns: List[Tuple[str, re.Pattern]],
    ) -> Tuple[int, List[str]]:
        """
        Counts total occurrences across all patterns and returns the list of
        keywords that matched at least once (deduplicated, preserving order).

        Returns:
            (total_hit_count, [matched_keywords])
        """
        total_count = 0
        matched: List[str] = []

        for keyword, pattern in patterns:
            hits = len(pattern.findall(text))
            if hits:
                total_count += hits
                matched.append(keyword)

        return total_count, matched

    # ── Context resolution ────────────────────────────────────────────────────

    @staticmethod
    def _resolve_text(context: Dict) -> Optional[str]:
        """
        Tries multiple context key paths to find the document text.

        Priority:
          1. context['document_processor']['text']
          2. context['document']['text']
          3. context['text']
        """
        for path in (
            ("document_processor", "text"),
            ("document", "text"),
            ("text",),
        ):
            try:
                node = context
                for key in path:
                    node = node[key]
                if node and isinstance(node, str):
                    return node
            except (KeyError, TypeError):
                continue
        return None

    # ── Failure helper ────────────────────────────────────────────────────────

    @staticmethod
    def _failure(error: str) -> Dict:
        return {
            "sentiment":        "neutral",
            "score":            0.5,
            "positive_signals": 0,
            "negative_signals": 0,
            "total_signals":    0,
            "matched_positive": [],
            "matched_negative": [],
            "success":          False,
            "error":            error,
        }
