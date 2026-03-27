"""
portfolio_manager.py — SQLite-backed portfolio manager with sentiment impact analysis.

Stores user holdings, seeds demo data on first run, and calculates potential
upside/risk based on the sentiment signal produced by SentimentAnalyzer.

Context input (from agent):
    context['task_data']['stock_name']      — explicit stock ticker (optional)
    context['task_data']['pdf_path']        — PDF filename used to infer ticker
    context['task_data']['user_id']         — defaults to 'demo_user'
    context['sentiment']['sentiment']       — 'positive' | 'negative' | 'neutral'

Return:
    {
        'owns_stock':     bool,
        'stock':          str,
        'quantity':       int   | None,
        'avg_price':      float | None,
        'current_value':  float | None,
        'impact_message': str,
        'success':        bool,
        'error':          str   # only on failure
    }
"""

import logging
import os
import re
import sqlite3
from datetime import date
from typing import Dict, List, Optional

from config import DATABASE_PATH

logger = logging.getLogger(__name__)

# ── Constants ─────────────────────────────────────────────────────────────────

DEFAULT_USER   = "demo_user"
IMPACT_UP      = 0.05   # +5 % upside on positive sentiment
IMPACT_DOWN    = 0.05   # -5 % risk   on negative sentiment

# Known tickers for fuzzy filename matching
KNOWN_TICKERS = {
    "TCS", "RELIANCE", "INFOSYS", "HDFCBANK", "WIPRO",
    "ICICIBANK", "AXISBANK", "SBIN", "BAJFINANCE", "HINDUNILVR",
}

# Demo seed data — loaded once when the table is first created
DEMO_HOLDINGS = [
    ("demo_user", "TCS",      50, 3850.00),
    ("demo_user", "RELIANCE", 20, 2870.00),
    ("demo_user", "INFOSYS",  30, 1530.00),
]


class PortfolioManager:
    """
    Manages user stock holdings in SQLite and evaluates portfolio impact
    based on document sentiment.
    """

    def __init__(self, db_path: str = DATABASE_PATH):
        self.db_path = db_path
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        self._init_db()

    # ── Agent entry point ─────────────────────────────────────────────────────

    def execute(self, context: Dict) -> Dict:
        """
        Called by the agent.  Extracts stock name, looks up the holding,
        and calculates sentiment-driven impact.
        """
        try:
            user_id = self._resolve_user(context)
            stock   = self._extract_stock_name(context)

            if not stock:
                return self._result(
                    owns_stock=False,
                    stock="UNKNOWN",
                    impact_message=(
                        "Could not identify a stock ticker from the document. "
                        "Provide task_data['stock_name'] or name the PDF after the ticker "
                        "(e.g. TCS_Q4.pdf)."
                    ),
                )

            holding = self.get_holding(user_id, stock)

            if not holding:
                return self._result(
                    owns_stock=False,
                    stock=stock,
                    impact_message=f"{stock} is not in your portfolio.",
                )

            # ── Sentiment-driven impact ───────────────────────────────────────
            sentiment_label = self._resolve_sentiment(context)
            quantity        = holding["quantity"]
            avg_price       = holding["avg_price"]
            current_value   = round(quantity * avg_price, 2)

            if sentiment_label == "positive":
                upside_value   = round(current_value * IMPACT_UP, 2)
                impact_message = (
                    f"Positive outlook for {stock}. "
                    f"Potential upside of ~{IMPACT_UP*100:.0f}% "
                    f"(≈ ₹{upside_value:,.2f} on your {quantity} shares)."
                )
            elif sentiment_label == "negative":
                risk_value     = round(current_value * IMPACT_DOWN, 2)
                impact_message = (
                    f"Negative signals detected for {stock}. "
                    f"Potential downside risk of ~{IMPACT_DOWN*100:.0f}% "
                    f"(≈ ₹{risk_value:,.2f} on your {quantity} shares). "
                    "Consider reviewing your position."
                )
            else:
                impact_message = (
                    f"Neutral sentiment for {stock}. Monitor closely — "
                    "no strong directional signal from the document."
                )

            logger.debug(
                "PortfolioManager: user=%s stock=%s sentiment=%s value=%.2f",
                user_id, stock, sentiment_label, current_value,
            )

            return self._result(
                owns_stock=True,
                stock=stock,
                quantity=quantity,
                avg_price=avg_price,
                current_value=current_value,
                impact_message=impact_message,
            )

        except Exception as exc:  # noqa: BLE001
            msg = f"{type(exc).__name__}: {exc}"
            logger.error("PortfolioManager.execute failed: %s", msg)
            return self._result(
                owns_stock=False,
                stock="UNKNOWN",
                impact_message="Portfolio lookup failed.",
                success=False,
                error=msg,
            )

    # ── CRUD operations ───────────────────────────────────────────────────────

    def add_holding(
        self,
        user_id: str,
        stock: str,
        quantity: int,
        avg_price: float,
    ) -> None:
        """
        Inserts or replaces a holding for the given user and stock.
        If the stock already exists for that user, the row is updated.
        """
        stock = stock.upper().strip()
        today = date.today().isoformat()
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO holdings (user_id, stock, quantity, avg_price, added_date)
                VALUES (?, ?, ?, ?, ?)
                ON CONFLICT(user_id, stock)
                DO UPDATE SET quantity=excluded.quantity,
                              avg_price=excluded.avg_price,
                              added_date=excluded.added_date
                """,
                (user_id, stock, quantity, avg_price, today),
            )
        logger.debug("add_holding: user=%s stock=%s qty=%d price=%.2f", user_id, stock, quantity, avg_price)

    def get_holding(self, user_id: str, stock: str) -> Optional[Dict]:
        """
        Returns a single holding dict or None if not found.

        Dict keys: user_id, stock, quantity, avg_price, added_date
        """
        stock = stock.upper().strip()
        with self._connect() as conn:
            row = conn.execute(
                "SELECT user_id, stock, quantity, avg_price, added_date "
                "FROM holdings WHERE user_id=? AND stock=?",
                (user_id, stock),
            ).fetchone()
        if row:
            return {"user_id": row[0], "stock": row[1], "quantity": row[2],
                    "avg_price": row[3], "added_date": row[4]}
        return None

    def get_all_holdings(self, user_id: str) -> List[Dict]:
        """Returns all holdings for a user, ordered by stock ticker."""
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT user_id, stock, quantity, avg_price, added_date "
                "FROM holdings WHERE user_id=? ORDER BY stock",
                (user_id,),
            ).fetchall()
        return [
            {"user_id": r[0], "stock": r[1], "quantity": r[2],
             "avg_price": r[3], "added_date": r[4]}
            for r in rows
        ]

    # ── Stock name extraction ─────────────────────────────────────────────────

    def _extract_stock_name(self, context: Dict) -> Optional[str]:
        """
        Resolves a stock ticker from the context using three strategies:

        1. Explicit task_data['stock_name']
        2. PDF filename  (e.g. TCS_Q4_2024.pdf  →  TCS)
        3. Scan document text for known ticker mentions
        """
        # Strategy 1 — explicit override
        try:
            name = context["task_data"]["stock_name"]
            if name and isinstance(name, str) and name.strip():
                return name.strip().upper()
        except (KeyError, TypeError):
            pass

        # Strategy 2 — infer from PDF filename
        try:
            pdf_path = context["task_data"]["pdf_path"]
            if pdf_path:
                basename = os.path.splitext(os.path.basename(pdf_path))[0]
                # First segment before underscore/hyphen/space is usually the ticker
                first_token = re.split(r"[_\-\s]", basename)[0].upper()
                if first_token in KNOWN_TICKERS:
                    logger.debug("_extract_stock_name: inferred '%s' from filename.", first_token)
                    return first_token
                # Fallback: check if any known ticker appears anywhere in the basename
                for ticker in KNOWN_TICKERS:
                    if ticker in basename.upper():
                        logger.debug("_extract_stock_name: found '%s' in filename.", ticker)
                        return ticker
        except (KeyError, TypeError):
            pass

        # Strategy 3 — scan document text for known tickers
        try:
            text = (
                context.get("document_processor", {}).get("text")
                or context.get("document", {}).get("text")
                or ""
            )
            if text:
                upper_text = text.upper()
                for ticker in KNOWN_TICKERS:
                    # Match whole word only
                    if re.search(rf"\b{ticker}\b", upper_text):
                        logger.debug("_extract_stock_name: found '%s' in document text.", ticker)
                        return ticker
        except (AttributeError, TypeError):
            pass

        return None

    # ── Internal helpers ──────────────────────────────────────────────────────

    def _init_db(self) -> None:
        """Creates the holdings table and seeds demo data if it doesn't exist."""
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS holdings (
                    user_id    TEXT NOT NULL,
                    stock      TEXT NOT NULL,
                    quantity   INTEGER NOT NULL,
                    avg_price  REAL NOT NULL,
                    added_date TEXT NOT NULL,
                    PRIMARY KEY (user_id, stock)
                )
                """
            )
            # Seed demo data only when the table is empty
            count = conn.execute("SELECT COUNT(*) FROM holdings").fetchone()[0]
            if count == 0:
                today = date.today().isoformat()
                conn.executemany(
                    "INSERT OR IGNORE INTO holdings (user_id, stock, quantity, avg_price, added_date) "
                    "VALUES (?, ?, ?, ?, ?)",
                    [(u, s, q, p, today) for u, s, q, p in DEMO_HOLDINGS],
                )
                logger.debug("PortfolioManager: seeded %d demo holdings.", len(DEMO_HOLDINGS))

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA journal_mode=WAL")   # safe for concurrent reads
        return conn

    @staticmethod
    def _resolve_user(context: Dict) -> str:
        try:
            uid = context["task_data"]["user_id"]
            if uid and isinstance(uid, str):
                return uid.strip()
        except (KeyError, TypeError):
            pass
        return DEFAULT_USER

    @staticmethod
    def _resolve_sentiment(context: Dict) -> str:
        """Reads sentiment label from context['sentiment']['sentiment']."""
        try:
            label = context["sentiment"]["sentiment"]
            if label in ("positive", "negative", "neutral"):
                return label
        except (KeyError, TypeError):
            pass
        return "neutral"

    @staticmethod
    def _result(
        owns_stock: bool,
        stock: str,
        quantity: Optional[int] = None,
        avg_price: Optional[float] = None,
        current_value: Optional[float] = None,
        impact_message: str = "",
        success: bool = True,
        error: Optional[str] = None,
    ) -> Dict:
        out = {
            "owns_stock":     owns_stock,
            "stock":          stock,
            "quantity":       quantity,
            "avg_price":      avg_price,
            "current_value":  current_value,
            "impact_message": impact_message,
            "success":        success,
        }
        if error:
            out["error"] = error
        return out
