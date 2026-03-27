import sqlite3
from config import DATABASE_PATH


class PortfolioManager:
    """Manages portfolio positions using SQLite."""

    def __init__(self):
        self._init_db()

    def _init_db(self):
        with sqlite3.connect(DATABASE_PATH) as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS positions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    ticker TEXT NOT NULL,
                    shares REAL NOT NULL,
                    avg_cost REAL NOT NULL
                )
            """)

    def add_position(self, ticker: str, shares: float, avg_cost: float):
        with sqlite3.connect(DATABASE_PATH) as conn:
            conn.execute(
                "INSERT INTO positions (ticker, shares, avg_cost) VALUES (?, ?, ?)",
                (ticker.upper(), shares, avg_cost),
            )

    def get_summary(self) -> list:
        with sqlite3.connect(DATABASE_PATH) as conn:
            rows = conn.execute("SELECT ticker, shares, avg_cost FROM positions").fetchall()
        return [{"ticker": r[0], "shares": r[1], "avg_cost": r[2]} for r in rows]
