"""
run.py — TradeIQ  |  Main entry point

Usage:
    python run.py              # normal launch
    python run.py --no-ai      # skip Ollama check, AI summaries disabled
    python run.py --port 8080  # custom port
    python run.py --share      # create public Gradio share link
    python run.py --debug      # verbose logging
"""

import argparse
import logging
import os
import signal
import sys

# ── Make project root importable from any working directory ──────────────────
ROOT = os.path.dirname(os.path.abspath(__file__))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from config import CACHE_DIR, DATA_DIR, DATABASE_PATH, REPORTS_DIR

# ── Logging setup (done before any project imports so all modules inherit) ───
def _setup_logging(debug: bool) -> None:
    level  = logging.DEBUG if debug else logging.INFO
    fmt    = "%(asctime)s  %(levelname)-8s  %(name)s — %(message)s"
    datefmt = "%H:%M:%S"
    logging.basicConfig(level=level, format=fmt, datefmt=datefmt)
    # Silence noisy third-party loggers unless in debug mode
    if not debug:
        for noisy in ("httpx", "httpcore", "gradio", "urllib3", "PIL"):
            logging.getLogger(noisy).setLevel(logging.WARNING)

logger = logging.getLogger("run")

# ── Demo portfolio seed data ──────────────────────────────────────────────────
DEMO_HOLDINGS = [
    ("demo_user", "TCS",      50, 3850.00),
    ("demo_user", "RELIANCE", 20, 2870.00),
    ("demo_user", "INFOSYS",  30, 1530.00),
]


# ── Initialisation helpers ────────────────────────────────────────────────────

def _ensure_directories() -> None:
    """Create data/, cache/, and sample_reports/ if they don't exist."""
    for path in (DATA_DIR, CACHE_DIR, REPORTS_DIR):
        os.makedirs(path, exist_ok=True)
    logger.debug("Directories ready: %s", DATA_DIR)


def _seed_demo_portfolio() -> None:
    """
    Ensures demo_user has the three seed holdings.
    Uses add_holding (INSERT OR REPLACE) so re-runs are idempotent.
    """
    from tools.portfolio_manager import PortfolioManager
    pm = PortfolioManager()
    for user_id, stock, qty, price in DEMO_HOLDINGS:
        existing = pm.get_holding(user_id, stock)
        if not existing:
            pm.add_holding(user_id, stock, qty, price)
            logger.info("  Seeded  %-10s %d shares @ ₹%.2f", stock, qty, price)
        else:
            logger.debug("  Exists  %-10s — skipping seed", stock)


def _write_sample_pdf_readme() -> None:
    """Drop a README in sample_reports/ so the folder isn't empty."""
    readme = os.path.join(REPORTS_DIR, "README.txt")
    if not os.path.exists(readme):
        with open(readme, "w") as f:
            f.write(
                "Place PDF annual/quarterly reports here.\n"
                "Naming convention: <TICKER>_Q<N>_<YEAR>.pdf\n"
                "Example: TCS_Q4_2024.pdf\n"
            )
        logger.debug("Created sample_reports/README.txt")


def _check_dependencies() -> dict:
    """
    Soft-checks optional and required dependencies.
    Returns a status dict printed at startup.
    """
    status = {}

    # Required
    for pkg in ("gradio", "pdfplumber", "bs4"):
        try:
            __import__(pkg)
            status[pkg] = "✅"
        except ImportError:
            status[pkg] = "❌ MISSING"

    # Optional — Ollama
    try:
        import subprocess
        r = subprocess.run(["ollama", "list"], capture_output=True, timeout=3)
        status["ollama"] = "✅" if r.returncode == 0 else "⚠️  not running"
    except Exception:
        status["ollama"] = "⚠️  not installed (AI summaries disabled)"

    return status


def _print_banner(port: int, share: bool, dep_status: dict, no_ai: bool) -> None:
    line = "─" * 54
    print(f"\n{line}")
    print("  TradeIQ  |  Fintech Research Assistant")
    print(line)
    print(f"  URL      : http://127.0.0.1:{port}")
    if share:
        print("  Share    : public link will appear below ↓")
    print(f"  Database : {DATABASE_PATH}")
    print(f"  AI mode  : {'disabled (--no-ai)' if no_ai else 'auto (Ollama)'}")
    print(f"\n  Dependencies:")
    for pkg, st in dep_status.items():
        print(f"    {pkg:<12} {st}")
    print(f"\n  Demo portfolio (demo_user):")
    for _, stock, qty, price in DEMO_HOLDINGS:
        print(f"    {stock:<10} {qty:>3} shares @ ₹{price:,.2f}")
    print(f"{line}\n")


# ── Graceful shutdown ─────────────────────────────────────────────────────────

def _register_shutdown() -> None:
    def _handler(sig, frame):
        print("\n\nShutting down TradeIQ... bye 👋")
        sys.exit(0)
    signal.signal(signal.SIGINT,  _handler)
    signal.signal(signal.SIGTERM, _handler)


# ── CLI argument parsing ──────────────────────────────────────────────────────

def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="TradeIQ — Fintech Research Assistant",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("--port",   type=int, default=7860,
                        help="Port to run Gradio on (default: 7860)")
    parser.add_argument("--share",  action="store_true",
                        help="Create a public Gradio share link")
    parser.add_argument("--no-ai",  action="store_true",
                        help="Disable Ollama AI summaries")
    parser.add_argument("--debug",  action="store_true",
                        help="Enable verbose debug logging")
    return parser.parse_args()


# ── Main ──────────────────────────────────────────────────────────────────────

def main() -> None:
    args = _parse_args()
    _setup_logging(args.debug)
    _register_shutdown()

    logger.info("Starting TradeIQ...")

    # 1. Filesystem
    _ensure_directories()
    _write_sample_pdf_readme()

    # 2. Database + demo data
    logger.info("Initialising database and seeding demo portfolio...")
    _seed_demo_portfolio()

    # 3. Dependency check
    dep_status = _check_dependencies()

    # 4. Optionally disable AI enhancer before the agent is imported
    if args.no_ai:
        os.environ["INVESTORCOPILOT_NO_AI"] = "1"
        logger.info("AI summaries disabled via --no-ai flag.")

    # 5. Import and verify core components (fail fast with a clear message)
    logger.info("Loading agent and tools...")
    try:
        from agent.agent_core import InvestorAgent          # noqa: F401
        from tools.document_processor import DocumentProcessor  # noqa: F401
        from tools.metric_extractor    import MetricExtractor   # noqa: F401
        from tools.sentiment_analyzer  import SentimentAnalyzer # noqa: F401
        from tools.portfolio_manager   import PortfolioManager  # noqa: F401
        from tools.alert_scanner       import AlertScanner      # noqa: F401
        from tools.ai_enhancer         import AIEnhancer        # noqa: F401
        from backend.confidence_engine import ConfidenceEngine  # noqa: F401
        logger.info("All components loaded successfully.")
    except ImportError as exc:
        logger.error("Failed to load a required component: %s", exc)
        print(f"\n❌  Import error: {exc}")
        print("    Run:  pip install -r requirements.txt\n")
        sys.exit(1)

    # 6. Print startup banner
    _print_banner(args.port, args.share, dep_status, args.no_ai)

    # 7. Launch Gradio
    logger.info("Launching Gradio on port %d (share=%s)...", args.port, args.share)
    try:
        from frontend.app import launch_app
        launch_app(port=args.port, share=args.share)
    except OSError as exc:
        if "address already in use" in str(exc).lower():
            print(f"\n❌  Port {args.port} is already in use.")
            print(f"    Try:  python run.py --port {args.port + 1}\n")
        else:
            print(f"\n❌  Failed to start server: {exc}\n")
        sys.exit(1)


if __name__ == "__main__":
    main()
