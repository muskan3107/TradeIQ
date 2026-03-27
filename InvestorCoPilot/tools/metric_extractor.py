import re


class MetricExtractor:
    """Extracts key financial metrics from text."""

    PATTERNS = {
        "revenue": r"revenue[:\s]+\$?([\d,\.]+)",
        "net_income": r"net income[:\s]+\$?([\d,\.]+)",
        "eps": r"eps[:\s]+\$?([\d,\.]+)",
        "pe_ratio": r"p/?e ratio[:\s]+([\d,\.]+)",
        "debt_to_equity": r"debt.to.equity[:\s]+([\d,\.]+)",
    }

    def extract(self, text: str) -> dict:
        metrics = {}
        lower = text.lower()
        for key, pattern in self.PATTERNS.items():
            match = re.search(pattern, lower)
            if match:
                metrics[key] = match.group(1).replace(",", "")
        return metrics
