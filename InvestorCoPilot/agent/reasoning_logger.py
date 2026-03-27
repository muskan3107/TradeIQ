from datetime import datetime


class ReasoningLogger:
    """Tracks agent reasoning steps for transparency and debugging."""

    def __init__(self):
        self._log = []

    def log(self, message: str):
        entry = f"[{datetime.now().strftime('%H:%M:%S')}] {message}"
        self._log.append(entry)

    def get_log(self) -> list:
        return list(self._log)

    def clear(self):
        self._log.clear()
