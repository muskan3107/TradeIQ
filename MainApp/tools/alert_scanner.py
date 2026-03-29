from tools.portfolio_manager import PortfolioManager


class AlertScanner:
    """Scans portfolio positions and generates simple threshold alerts."""

    def __init__(self, price_drop_threshold: float = 0.05):
        self.threshold = price_drop_threshold
        self.pm = PortfolioManager()

    def scan(self) -> list:
        positions = self.pm.get_summary()
        alerts = []
        for pos in positions:
            # Placeholder: in production, fetch live price and compare
            alerts.append({
                "ticker": pos["ticker"],
                "message": f"Monitoring {pos['ticker']} — no live feed connected yet.",
            })
        return alerts
