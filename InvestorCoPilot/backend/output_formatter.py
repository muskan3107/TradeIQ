import json


class OutputFormatter:
    """Formats agent results for display in the UI."""

    def format(self, agent_output: dict) -> str:
        lines = [f"Query: {agent_output.get('query', '')}", ""]
        for step in agent_output.get("steps", []):
            lines.append(f"[{step['task']}]")
            lines.append(json.dumps(step["result"], indent=2, default=str))
            lines.append("")
        lines.append("--- Reasoning Log ---")
        lines.extend(agent_output.get("reasoning", []))
        return "\n".join(lines)
