class Validator:
    """Validates inputs before passing them to the agent."""

    MAX_QUERY_LENGTH = 2000

    def validate_query(self, query: str) -> tuple:
        """Returns (is_valid: bool, error_message: str)."""
        if not query or not query.strip():
            return False, "Query cannot be empty."
        if len(query) > self.MAX_QUERY_LENGTH:
            return False, f"Query exceeds {self.MAX_QUERY_LENGTH} characters."
        return True, ""
