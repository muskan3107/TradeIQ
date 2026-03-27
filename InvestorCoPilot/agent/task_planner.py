class TaskPlanner:
    """Parses a user query and returns an ordered list of tasks to execute."""

    def plan(self, query: str) -> list:
        """
        Simple keyword-based planner. Replace with LLM-based planning as needed.
        Returns a list of task dicts: {name, fn, args, kwargs}
        """
        tasks = []
        q = query.lower()

        if "upload" in q or "report" in q or "pdf" in q:
            from tools.document_processor import DocumentProcessor
            dp = DocumentProcessor()
            tasks.append({"name": "document_processor", "fn": dp.process, "args": [query]})

        if "metric" in q or "revenue" in q or "eps" in q:
            from tools.metric_extractor import MetricExtractor
            me = MetricExtractor()
            tasks.append({"name": "metric_extractor", "fn": me.extract, "args": [query]})

        if "sentiment" in q or "news" in q or "earnings" in q:
            from tools.sentiment_analyzer import SentimentAnalyzer
            sa = SentimentAnalyzer()
            tasks.append({"name": "sentiment_analyzer", "fn": sa.analyze, "args": [query]})

        if "portfolio" in q or "position" in q or "holding" in q:
            from tools.portfolio_manager import PortfolioManager
            pm = PortfolioManager()
            tasks.append({"name": "portfolio_manager", "fn": pm.get_summary, "args": []})

        if "alert" in q or "watch" in q:
            from tools.alert_scanner import AlertScanner
            als = AlertScanner()
            tasks.append({"name": "alert_scanner", "fn": als.scan, "args": []})

        if not tasks:
            from tools.ai_enhancer import AIEnhancer
            ai = AIEnhancer()
            tasks.append({"name": "ai_enhancer", "fn": ai.enhance, "args": [query]})

        return tasks
