from config import TOOL_CONFIG

POSITIVE_WORDS = {"growth", "profit", "beat", "strong", "record", "increase", "positive", "outperform"}
NEGATIVE_WORDS = {"loss", "decline", "miss", "weak", "cut", "decrease", "negative", "underperform"}


class SentimentAnalyzer:
    """Simple lexicon-based sentiment analyzer for financial text."""

    def __init__(self):
        cfg = TOOL_CONFIG["sentiment_analyzer"]
        self.pos_threshold = cfg["threshold_positive"]
        self.neg_threshold = cfg["threshold_negative"]

    def analyze(self, text: str) -> dict:
        words = text.lower().split()
        total = len(words) or 1
        pos = sum(1 for w in words if w in POSITIVE_WORDS)
        neg = sum(1 for w in words if w in NEGATIVE_WORDS)
        score = (pos - neg) / total

        if score >= self.pos_threshold:
            label = "positive"
        elif score <= -self.neg_threshold:
            label = "negative"
        else:
            label = "neutral"

        return {"score": round(score, 4), "label": label, "positive_hits": pos, "negative_hits": neg}
