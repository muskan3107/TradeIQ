import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import gradio as gr
from agent.agent_core import AgentCore
from backend.validator import Validator
from backend.output_formatter import OutputFormatter
from backend.confidence_engine import ConfidenceEngine

agent = AgentCore()
validator = Validator()
formatter = OutputFormatter()
confidence = ConfidenceEngine()


def handle_query(query: str) -> tuple:
    valid, err = validator.validate_query(query)
    if not valid:
        return err, "N/A"

    output = agent.run(query)
    score = confidence.score(output.get("steps", []))
    formatted = formatter.format(output)
    return formatted, f"Confidence: {score * 100:.0f}%"


def launch_app():
    with gr.Blocks(title="InvestorCoPilot") as demo:
        gr.Markdown("# InvestorCoPilot\nAI-powered investment research assistant")

        with gr.Row():
            query_input = gr.Textbox(
                label="Ask a question or paste financial text",
                placeholder="e.g. Analyze sentiment of this earnings call...",
                lines=4,
            )

        with gr.Row():
            submit_btn = gr.Button("Analyze", variant="primary")

        with gr.Row():
            output_box = gr.Textbox(label="Results", lines=20, interactive=False)
            confidence_box = gr.Textbox(label="Confidence", interactive=False)

        submit_btn.click(fn=handle_query, inputs=query_input, outputs=[output_box, confidence_box])

    demo.launch()


if __name__ == "__main__":
    launch_app()
