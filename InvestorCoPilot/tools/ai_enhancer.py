"""
ai_enhancer.py — Optional local AI enhancement via Ollama.

Completely optional — the rest of the pipeline works fine without it.
If Ollama is not installed or the model isn't downloaded, execute() returns
success=False with a clear reason and the agent continues normally.

Context keys read:
    context['metrics']['metrics']          dict of extracted financials
    context['sentiment']['sentiment']      label + score
    context['portfolio']['stock']          ticker
    context['portfolio']['impact_message'] impact summary
    context['document']['pages_extracted'] int
"""

import logging
import subprocess
from typing import Dict, Optional

logger = logging.getLogger(__name__)

TIMEOUT_SECONDS = 15


class AIEnhancer:
    """
    Generates a plain-English investment summary using a local Ollama model.
    Degrades gracefully when Ollama is unavailable.
    """

    def __init__(self, model: str = "llama3.2:1b"):
        self.model     = model
        self.available = self._check_availability()
        if self.available:
            logger.debug("AIEnhancer: Ollama is available (model=%s).", self.model)
        else:
            logger.debug("AIEnhancer: Ollama not available — AI summaries disabled.")

    # ── Availability check ────────────────────────────────────────────────────

    def _check_availability(self) -> bool:
        """
        Returns True only if:
          - `ollama` binary is on PATH  (returncode == 0 from `ollama list`)
          - No exception is raised (FileNotFoundError, PermissionError, etc.)
        """
        try:
            result = subprocess.run(
                ["ollama", "list"],
                capture_output=True,
                timeout=5,
            )
            available = result.returncode == 0
            if not available:
                logger.debug(
                    "AIEnhancer: `ollama list` returned code %d — stderr: %s",
                    result.returncode,
                    result.stderr.decode(errors="replace").strip(),
                )
            return available
        except FileNotFoundError:
            logger.debug("AIEnhancer: `ollama` binary not found on PATH.")
        except subprocess.TimeoutExpired:
            logger.debug("AIEnhancer: `ollama list` timed out.")
        except Exception as exc:  # noqa: BLE001
            logger.debug("AIEnhancer: availability check failed — %s", exc)
        return False

    # ── Agent entry point ─────────────────────────────────────────────────────

    def execute(self, context: Dict) -> Dict:
        """
        Generates an AI summary if Ollama is available, otherwise returns a
        graceful failure so the agent can continue without it.
        """
        if not self.available:
            return self._failure(
                "Ollama is not installed or not running. "
                "Install from https://ollama.com and run `ollama pull llama3.2:1b` "
                "to enable AI summaries."
            )

        prompt = self._build_prompt(context)
        if not prompt.strip():
            return self._failure("Could not build a prompt — no analysis data in context.")

        return self._run_model(prompt)

    # ── Prompt builder ────────────────────────────────────────────────────────

    def _build_prompt(self, context: Dict) -> str:
        """
        Assembles a concise, data-rich prompt from prior tool outputs.
        Requests a 2-3 sentence plain-English summary with no jargon.
        """
        parts: list[str] = []

        # Metrics
        metrics = self._safe_get(context, "metrics", "metrics") or {}
        if metrics:
            metric_lines = [
                f"{k.replace('_', ' ').title()}: {v}"
                for k, v in metrics.items()
                if v is not None
            ]
            if metric_lines:
                parts.append("Financial metrics: " + ", ".join(metric_lines))

        # Sentiment
        sentiment_label = self._safe_get(context, "sentiment", "sentiment") or "neutral"
        sentiment_score = self._safe_get(context, "sentiment", "score")
        pos_signals     = self._safe_get(context, "sentiment", "positive_signals") or 0
        neg_signals     = self._safe_get(context, "sentiment", "negative_signals") or 0
        parts.append(
            f"Sentiment: {sentiment_label}"
            + (f" (score {sentiment_score:.2f})" if sentiment_score is not None else "")
            + f" — {pos_signals} positive signals, {neg_signals} negative signals."
        )

        # Portfolio
        stock          = self._safe_get(context, "portfolio", "stock")
        owns_stock     = self._safe_get(context, "portfolio", "owns_stock")
        impact_message = self._safe_get(context, "portfolio", "impact_message")
        if stock:
            ownership = "is in your portfolio" if owns_stock else "is NOT in your portfolio"
            parts.append(f"Stock {stock} {ownership}.")
        if impact_message:
            parts.append(f"Portfolio impact: {impact_message}")

        # Document completeness
        pages = self._safe_get(context, "document", "pages_extracted")
        if pages is not None:
            parts.append(f"Analysis based on {pages} pages of the report.")

        data_block = "\n".join(parts) if parts else "No detailed data available."

        prompt = (
            "You are a financial assistant helping retail investors understand reports.\n"
            "Based on the following analysis data, write a 2-3 sentence summary.\n"
            "Use simple language — no jargon, no bullet points, no markdown.\n\n"
            f"{data_block}\n\n"
            "Summary:"
        )

        logger.debug("AIEnhancer prompt (%d chars):\n%s", len(prompt), prompt)
        return prompt

    # ── Model runner ──────────────────────────────────────────────────────────

    def _run_model(self, prompt: str) -> Dict:
        """Calls `ollama run <model> <prompt>` and returns the result dict."""
        try:
            result = subprocess.run(
                ["ollama", "run", self.model, prompt],
                capture_output=True,
                text=True,
                timeout=TIMEOUT_SECONDS,
            )

            if result.returncode != 0:
                stderr = result.stderr.strip()
                # Detect common "model not found" error
                if "not found" in stderr.lower() or "pull" in stderr.lower():
                    return self._failure(
                        f"Model '{self.model}' is not downloaded. "
                        f"Run `ollama pull {self.model}` to install it."
                    )
                return self._failure(
                    f"Ollama returned exit code {result.returncode}. "
                    f"stderr: {stderr[:200]}"
                )

            text = result.stdout.strip()
            if not text:
                return self._failure("Ollama returned an empty response.")

            logger.debug("AIEnhancer: generated %d chars.", len(text))
            return {
                "text":    text,
                "success": True,
                "reason":  None,
                "model":   self.model,
            }

        except subprocess.TimeoutExpired:
            return self._failure(
                f"Ollama timed out after {TIMEOUT_SECONDS}s. "
                "The model may be loading — try again in a moment."
            )
        except FileNotFoundError:
            # Ollama was available at init but disappeared (e.g. service stopped)
            self.available = False
            return self._failure("Ollama binary not found. It may have been uninstalled.")
        except Exception as exc:  # noqa: BLE001
            return self._failure(f"Unexpected error: {type(exc).__name__}: {exc}")

    # ── Helpers ───────────────────────────────────────────────────────────────

    @staticmethod
    def _safe_get(context: Dict, tool_key: str, field: str) -> Optional[object]:
        """Safely reads context[tool_key][field], returns None on any miss."""
        try:
            val = context[tool_key][field]
            return val
        except (KeyError, TypeError):
            return None

    @staticmethod
    def _failure(reason: str) -> Dict:
        return {
            "text":    None,
            "success": False,
            "reason":  reason,
            "model":   None,
        }
