class ConfidenceEngine:
    """Scores agent output confidence based on data completeness."""

    def score(self, results: list) -> float:
        if not results:
            return 0.0
        filled = sum(1 for r in results if r.get("result"))
        return round(filled / len(results), 2)
