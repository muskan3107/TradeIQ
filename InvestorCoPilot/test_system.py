"""
test_system.py — InvestorCoPilot AI  |  Full system test suite

Run:
    python test_system.py           # all tests
    python test_system.py --verbose # show full output per test
"""

import sys, os, argparse, traceback, textwrap, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# ── Colour helpers (no deps) ──────────────────────────────────────────────────
GREEN  = "\033[92m"
RED    = "\033[91m"
YELLOW = "\033[93m"
CYAN   = "\033[96m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

def _g(s): return f"{GREEN}{s}{RESET}"
def _r(s): return f"{RED}{s}{RESET}"
def _y(s): return f"{YELLOW}{s}{RESET}"
def _c(s): return f"{CYAN}{s}{RESET}"
def _b(s): return f"{BOLD}{s}{RESET}"

# ── Mock / sample data ────────────────────────────────────────────────────────
SAMPLE_TEXT_RICH = """
TCS Q4 FY2024 Results
Revenue: Rs. 62,000 Cr. Net profit: Rs. 12,000 crore.
Operating margin: 25.3%. YoY growth: 4%.
The company reported strong growth and record profit this quarter.
Deal wins accelerated with expansion into new markets.
Revenue increased by 4% year-on-year driven by strong demand.
Management remains optimistic about FY25 outlook.
"""

SAMPLE_TEXT_NEGATIVE = """
INFOSYS Q3 FY2024 Results
Revenue declined to Rs. 38,000 Cr. Net loss reported: Rs. 500 crore.
Margin: 18.2%. YoY growth: -2%.
Weak demand environment. Challenges persist in key verticals.
Risk of further decline. Concerns over client budget cuts.
Headwinds from currency volatility and rising costs.
"""

SAMPLE_TEXT_EMPTY = ""

SAMPLE_TEXT_NO_METRICS = "The board met on Monday to discuss the annual strategy."

MOCK_CONTEXT_FULL = {
    "task_data":  {"stock_name": "TCS", "user_id": "demo_user"},
    "document":   {"text": SAMPLE_TEXT_RICH, "pages_extracted": 18, "success": True},
    "document_processor": {"text": SAMPLE_TEXT_RICH, "pages_extracted": 18, "success": True},
    "metrics":    {"metrics_found": 4, "metrics": {"revenue": 62000.0, "profit": 12000.0, "margin": 25.3, "growth": 4.0}},
    "sentiment":  {"sentiment": "positive", "score": 0.75, "positive_signals": 8, "negative_signals": 2, "total_signals": 10},
    "portfolio":  {"owns_stock": True, "stock": "TCS", "quantity": 50, "avg_price": 3850.0, "current_value": 192500.0},
}

MOCK_CONTEXT_EMPTY = {
    "task_data": {}, "document": {}, "document_processor": {},
    "metrics": {}, "sentiment": {}, "portfolio": {},
}

# ── Test runner ───────────────────────────────────────────────────────────────

class TestRunner:
    def __init__(self, verbose: bool = False):
        self.verbose  = verbose
        self.results  = []   # list of (name, passed, detail, duration_ms)

    def run(self, name: str, fn):
        """Execute fn(), catch any exception, record pass/fail."""
        print(f"  {_c('▶')} {name:<55}", end="", flush=True)
        t0 = time.perf_counter()
        try:
            detail = fn()
            passed = True
            ms = (time.perf_counter() - t0) * 1000
            print(f" {_g('PASS')}  {ms:5.0f}ms")
            if self.verbose and detail:
                for line in str(detail).splitlines()[:12]:
                    print(f"       {line}")
        except AssertionError as exc:
            ms = (time.perf_counter() - t0) * 1000
            passed = False
            detail = f"AssertionError: {exc}"
            print(f" {_r('FAIL')}  {ms:5.0f}ms")
            print(f"       {_r(detail)}")
        except Exception as exc:
            ms = (time.perf_counter() - t0) * 1000
            passed = False
            detail = traceback.format_exc()
            print(f" {_r('FAIL')}  {ms:5.0f}ms")
            print(f"       {_r(str(exc))}")
            if self.verbose:
                print(textwrap.indent(detail, "       "))
        self.results.append((name, passed, detail if not passed else "", ms))

    def section(self, title: str):
        print(f"\n{_b(title)}")
        print("  " + "─" * 60)

    def report(self):
        total  = len(self.results)
        passed = sum(1 for _, p, *_ in self.results if p)
        failed = total - passed
        print(f"\n{'─'*64}")
        print(_b(f"  TEST REPORT   {passed}/{total} passed"))
        print(f"{'─'*64}")
        if failed:
            print(_r(f"  {failed} FAILED:"))
            for name, p, detail, ms in self.results:
                if not p:
                    print(f"    • {name}")
                    if detail:
                        for line in detail.splitlines()[:4]:
                            print(f"        {line}")
        else:
            print(_g("  All tests passed ✅"))
        print(f"{'─'*64}\n")
        return failed == 0


def _assert_keys(d: dict, *keys):
    for k in keys:
        assert k in d, f"Missing key '{k}' in result: {list(d.keys())}"

def _assert_type(val, typ, label="value"):
    assert isinstance(val, typ), f"Expected {typ.__name__} for {label}, got {type(val).__name__}"

# ── DocumentProcessor tests ───────────────────────────────────────────────────

def _doc_tests(r: TestRunner):
    from tools.document_processor import DocumentProcessor
    dp = DocumentProcessor()
    r.section("DocumentProcessor")

    def t_missing_key():
        res = dp.execute({})
        _assert_keys(res, "text", "pages_extracted", "total_pages", "success", "error")
        assert res["success"] is False
        assert "pdf_path" in res["error"].lower() or "no pdf" in res["error"].lower()
        return res["error"]

    def t_empty_path():
        res = dp.execute({"task_data": {"pdf_path": ""}})
        assert res["success"] is False
        return res["error"]

    def t_file_not_found():
        res = dp.execute({"task_data": {"pdf_path": "ghost_report.pdf"}})
        assert res["success"] is False
        assert "not found" in res["error"].lower()
        return res["error"]

    def t_wrong_extension():
        res = dp.execute({"task_data": {"pdf_path": "report.docx"}})
        assert res["success"] is False
        return res["error"]

    def t_result_structure_on_failure():
        res = dp.execute({"task_data": {"pdf_path": "missing.pdf"}})
        _assert_keys(res, "text", "pages_extracted", "total_pages", "success")
        _assert_type(res["text"], str, "text")
        _assert_type(res["pages_extracted"], int, "pages_extracted")
        _assert_type(res["success"], bool, "success")
        return "structure OK"

    r.run("missing task_data key",          t_missing_key)
    r.run("empty pdf_path",                 t_empty_path)
    r.run("file not found",                 t_file_not_found)
    r.run("wrong file extension",           t_wrong_extension)
    r.run("failure result structure valid", t_result_structure_on_failure)


# ── MetricExtractor tests ─────────────────────────────────────────────────────

def _metric_tests(r: TestRunner):
    from tools.metric_extractor import MetricExtractor
    me = MetricExtractor()
    r.section("MetricExtractor")

    def t_happy_path():
        ctx = {"document_processor": {"text": SAMPLE_TEXT_RICH}}
        res = me.execute(ctx)
        _assert_keys(res, "metrics", "metrics_found", "success")
        assert res["success"] is True
        assert res["metrics_found"] >= 3, f"Expected ≥3 metrics, got {res['metrics_found']}"
        m = res["metrics"]
        assert m.get("revenue") is not None, "revenue not extracted"
        assert m.get("profit")  is not None, "profit not extracted"
        return f"found={res['metrics_found']} metrics={res['metrics']}"

    def t_no_metrics_in_text():
        ctx = {"document_processor": {"text": SAMPLE_TEXT_NO_METRICS}}
        res = me.execute(ctx)
        assert res["success"] is True
        assert res["metrics_found"] == 0
        assert all(v is None for v in res["metrics"].values())
        return "all None as expected"

    def t_empty_text():
        ctx = {"document_processor": {"text": ""}}
        res = me.execute(ctx)
        assert res["success"] is False
        _assert_keys(res, "error")
        return res["error"]

    def t_missing_context_key():
        res = me.execute({})
        assert res["success"] is False
        return res["error"]

    def t_negative_report():
        ctx = {"document_processor": {"text": SAMPLE_TEXT_NEGATIVE}}
        res = me.execute(ctx)
        assert res["success"] is True
        # Margin should always be found; revenue/profit depend on phrasing
        m = res["metrics"]
        assert m.get("margin") is not None, "margin not extracted from negative report"
        return f"revenue={m['revenue']} margin={m['margin']} growth={m['growth']}"

    def t_raw_matches_present():
        ctx = {"document_processor": {"text": SAMPLE_TEXT_RICH}}
        res = me.execute(ctx)
        assert "raw_matches" in res
        _assert_type(res["raw_matches"], dict, "raw_matches")
        return f"raw_matches keys: {list(res['raw_matches'].keys())}"

    def t_values_are_floats():
        ctx = {"document_processor": {"text": SAMPLE_TEXT_RICH}}
        res = me.execute(ctx)
        for k, v in res["metrics"].items():
            if v is not None:
                _assert_type(v, float, k)
        return "all non-None values are float"

    r.run("happy path — rich text",         t_happy_path)
    r.run("no metrics in text",             t_no_metrics_in_text)
    r.run("empty text",                     t_empty_text)
    r.run("missing context key",            t_missing_context_key)
    r.run("negative report text",           t_negative_report)
    r.run("raw_matches present",            t_raw_matches_present)
    r.run("extracted values are floats",    t_values_are_floats)


# ── SentimentAnalyzer tests ───────────────────────────────────────────────────

def _sentiment_tests(r: TestRunner):
    from tools.sentiment_analyzer import SentimentAnalyzer
    sa = SentimentAnalyzer()
    r.section("SentimentAnalyzer")

    def t_positive():
        ctx = {"document_processor": {"text": SAMPLE_TEXT_RICH}}
        res = sa.execute(ctx)
        _assert_keys(res, "sentiment", "score", "positive_signals", "negative_signals", "total_signals", "success")
        assert res["success"] is True
        assert res["sentiment"] == "positive", f"Expected positive, got {res['sentiment']}"
        assert res["score"] > 0.6
        return f"sentiment={res['sentiment']} score={res['score']}"

    def t_negative():
        ctx = {"document_processor": {"text": SAMPLE_TEXT_NEGATIVE}}
        res = sa.execute(ctx)
        assert res["success"] is True
        assert res["sentiment"] == "negative", f"Expected negative, got {res['sentiment']}"
        assert res["score"] < 0.4
        return f"sentiment={res['sentiment']} score={res['score']}"

    def t_neutral_mixed():
        text = "Revenue growth was strong but challenges remain. Some risks and opportunities ahead."
        ctx  = {"document_processor": {"text": text}}
        res  = sa.execute(ctx)
        assert res["success"] is True
        assert res["sentiment"] == "neutral"
        return f"sentiment={res['sentiment']} score={res['score']}"

    def t_no_signals():
        ctx = {"document_processor": {"text": SAMPLE_TEXT_NO_METRICS}}
        res = sa.execute(ctx)
        assert res["success"] is True
        assert res["total_signals"] == 0
        assert res["score"] == 0.5
        return "score=0.5 as expected"

    def t_empty_text():
        ctx = {"document_processor": {"text": ""}}
        res = sa.execute(ctx)
        assert res["success"] is False
        return res["error"]

    def t_matched_lists_present():
        ctx = {"document_processor": {"text": SAMPLE_TEXT_RICH}}
        res = sa.execute(ctx)
        _assert_keys(res, "matched_positive", "matched_negative")
        _assert_type(res["matched_positive"], list, "matched_positive")
        assert len(res["matched_positive"]) > 0
        return f"+ve words: {res['matched_positive'][:5]}"

    def t_score_range():
        for text in [SAMPLE_TEXT_RICH, SAMPLE_TEXT_NEGATIVE, SAMPLE_TEXT_NO_METRICS]:
            ctx = {"document_processor": {"text": text}}
            res = sa.execute(ctx)
            assert 0.0 <= res["score"] <= 1.0, f"Score out of range: {res['score']}"
        return "all scores in [0,1]"

    r.run("positive text",                  t_positive)
    r.run("negative text",                  t_negative)
    r.run("neutral mixed text",             t_neutral_mixed)
    r.run("no signals → score 0.5",         t_no_signals)
    r.run("empty text",                     t_empty_text)
    r.run("matched_positive list present",  t_matched_lists_present)
    r.run("score always in [0, 1]",         t_score_range)

# ── PortfolioManager tests ────────────────────────────────────────────────────

def _portfolio_tests(r: TestRunner):
    from tools.portfolio_manager import PortfolioManager
    pm = PortfolioManager()
    r.section("PortfolioManager")

    def t_demo_data_seeded():
        holdings = pm.get_all_holdings("demo_user")
        tickers  = {h["stock"] for h in holdings}
        for expected in ("TCS", "RELIANCE", "INFOSYS"):
            assert expected in tickers, f"{expected} not in demo holdings"
        return f"holdings: {sorted(tickers)}"

    def t_get_holding_tcs():
        h = pm.get_holding("demo_user", "TCS")
        assert h is not None, "TCS holding not found"
        _assert_keys(h, "user_id", "stock", "quantity", "avg_price", "added_date")
        assert h["quantity"] > 0, "TCS quantity should be positive"
        assert h["avg_price"] > 0, "TCS avg_price should be positive"
        return f"qty={h['quantity']} price={h['avg_price']}"

    def t_add_and_retrieve():
        pm.add_holding("test_user", "WIPRO", 10, 450.0)
        h = pm.get_holding("test_user", "WIPRO")
        assert h is not None
        assert h["quantity"] == 10
        assert h["avg_price"] == 450.0
        return "add + retrieve OK"

    def t_update_existing():
        pm.add_holding("test_user", "WIPRO", 25, 460.0)
        h = pm.get_holding("test_user", "WIPRO")
        assert h["quantity"] == 25
        assert h["avg_price"] == 460.0
        return "update (upsert) OK"

    def t_execute_positive_sentiment():
        ctx = {
            "task_data": {"stock_name": "TCS", "user_id": "demo_user"},
            "sentiment": {"sentiment": "positive"},
        }
        res = pm.execute(ctx)
        _assert_keys(res, "owns_stock", "stock", "quantity", "avg_price", "current_value", "impact_message", "success")
        assert res["success"] is True
        assert res["owns_stock"] is True
        assert res["stock"] == "TCS"
        assert "upside" in res["impact_message"].lower()
        return res["impact_message"]

    def t_execute_negative_sentiment():
        ctx = {
            "task_data": {"stock_name": "RELIANCE", "user_id": "demo_user"},
            "sentiment": {"sentiment": "negative"},
        }
        res = pm.execute(ctx)
        assert res["owns_stock"] is True
        assert "risk" in res["impact_message"].lower() or "downside" in res["impact_message"].lower()
        return res["impact_message"]

    def t_execute_neutral_sentiment():
        ctx = {
            "task_data": {"stock_name": "INFOSYS", "user_id": "demo_user"},
            "sentiment": {"sentiment": "neutral"},
        }
        res = pm.execute(ctx)
        assert "monitor" in res["impact_message"].lower()
        return res["impact_message"]

    def t_stock_not_owned():
        ctx = {
            "task_data": {"stock_name": "HDFCBANK", "user_id": "demo_user"},
            "sentiment": {"sentiment": "positive"},
        }
        res = pm.execute(ctx)
        assert res["owns_stock"] is False
        assert res["quantity"] is None
        return res["impact_message"]

    def t_infer_from_filename():
        ctx = {
            "task_data": {"pdf_path": "RELIANCE_Q4_2024.pdf", "user_id": "demo_user"},
            "sentiment": {"sentiment": "positive"},
        }
        res = pm.execute(ctx)
        assert res["stock"] == "RELIANCE"
        return f"inferred stock={res['stock']}"

    def t_no_stock_identifiable():
        res = pm.execute({"task_data": {}, "sentiment": {"sentiment": "positive"}})
        assert res["owns_stock"] is False
        assert res["stock"] == "UNKNOWN"
        return res["impact_message"]

    def t_current_value_calculation():
        h   = pm.get_holding("demo_user", "TCS")
        ctx = {"task_data": {"stock_name": "TCS", "user_id": "demo_user"}, "sentiment": {"sentiment": "neutral"}}
        res = pm.execute(ctx)
        expected = h["quantity"] * h["avg_price"]
        assert abs(res["current_value"] - expected) < 0.01, f"Value mismatch: {res['current_value']} vs {expected}"
        return f"current_value={res['current_value']}"

    r.run("demo data seeded",               t_demo_data_seeded)
    r.run("get_holding TCS",                t_get_holding_tcs)
    r.run("add_holding new user",           t_add_and_retrieve)
    r.run("update existing holding",        t_update_existing)
    r.run("execute — positive sentiment",   t_execute_positive_sentiment)
    r.run("execute — negative sentiment",   t_execute_negative_sentiment)
    r.run("execute — neutral sentiment",    t_execute_neutral_sentiment)
    r.run("stock not in portfolio",         t_stock_not_owned)
    r.run("infer ticker from filename",     t_infer_from_filename)
    r.run("no stock identifiable",          t_no_stock_identifiable)
    r.run("current_value calculation",      t_current_value_calculation)


# ── ConfidenceEngine tests ────────────────────────────────────────────────────

def _confidence_tests(r: TestRunner):
    from backend.confidence_engine import ConfidenceEngine
    ce = ConfidenceEngine()
    r.section("ConfidenceEngine")

    def _ctx(metrics=0, signals=0, owns=False, pages=0):
        return {
            "metrics":   {"metrics_found": metrics},
            "sentiment": {"total_signals": signals},
            "portfolio": {"owns_stock": owns},
            "document":  {"pages_extracted": pages},
        }

    def t_result_structure():
        res = ce.execute(_ctx(3, 10, True, 20))
        _assert_keys(res, "score", "percentage", "label", "factors", "breakdown", "success")
        assert res["success"] is True
        _assert_type(res["score"],      float, "score")
        _assert_type(res["percentage"], int,   "percentage")
        _assert_type(res["factors"],    list,  "factors")
        _assert_type(res["breakdown"],  dict,  "breakdown")
        return "structure OK"

    def t_max_score():
        res = ce.execute(_ctx(4, 15, True, 20))
        assert res["score"] <= 1.0
        assert res["label"] == "Very High"
        return f"score={res['score']} label={res['label']}"

    def t_min_score():
        res = ce.execute(_ctx(0, 0, False, 0))
        assert res["score"] < 0.5
        assert res["label"] == "Low"
        return f"score={res['score']} label={res['label']}"

    def t_label_very_high():
        res = ce.execute(_ctx(4, 12, True, 20))
        assert res["score"] >= 0.80
        assert res["label"] == "Very High"
        return f"score={res['score']}"

    def t_label_moderate():
        res = ce.execute(_ctx(2, 4, False, 6))
        assert res["label"] in ("Moderate", "Low")
        return f"score={res['score']} label={res['label']}"

    def t_factors_have_icons():
        res = ce.execute(_ctx(3, 10, True, 15))
        for f in res["factors"]:
            assert any(icon in f for icon in ("✅", "⚠️", "❌")), f"No icon in factor: {f}"
        return f"{len(res['factors'])} factors with icons"

    def t_breakdown_keys():
        res = ce.execute(_ctx(3, 10, True, 15))
        for k in ("metrics", "signals", "context", "document"):
            assert k in res["breakdown"], f"Missing breakdown key: {k}"
        return f"breakdown={res['breakdown']}"

    def t_score_capped():
        # Even with extreme inputs score must stay ≤ 1.0
        res = ce.execute(_ctx(100, 100, True, 100))
        assert 0.0 <= res["score"] <= 1.0
        return f"score={res['score']} (capped)"

    def t_empty_context():
        res = ce.execute({})
        assert res["success"] is True
        assert res["score"] < 0.5
        return f"score={res['score']}"

    r.run("result structure valid",         t_result_structure)
    r.run("max inputs → Very High",         t_max_score)
    r.run("zero inputs → Low",              t_min_score)
    r.run("label Very High threshold",      t_label_very_high)
    r.run("label Moderate threshold",       t_label_moderate)
    r.run("factors contain icons",          t_factors_have_icons)
    r.run("breakdown has all keys",         t_breakdown_keys)
    r.run("score capped at 1.0",            t_score_capped)
    r.run("empty context handled",          t_empty_context)

# ── AIEnhancer tests ──────────────────────────────────────────────────────────

def _ai_tests(r: TestRunner):
    from tools.ai_enhancer import AIEnhancer
    ai = AIEnhancer()
    r.section("AIEnhancer")

    def t_result_structure_unavailable():
        # Ollama almost certainly not running in CI — test graceful failure
        if ai.available:
            return "Ollama available — skipping unavailable test"
        res = ai.execute(MOCK_CONTEXT_FULL)
        _assert_keys(res, "text", "success", "reason", "model")
        assert res["success"] is False
        assert res["text"] is None
        assert isinstance(res["reason"], str) and len(res["reason"]) > 0
        return res["reason"]

    def t_prompt_builds_correctly():
        prompt = ai._build_prompt(MOCK_CONTEXT_FULL)
        assert len(prompt) > 50, "Prompt too short"
        assert "TCS" in prompt or "revenue" in prompt.lower()
        assert "Summary:" in prompt
        return f"prompt length={len(prompt)} chars"

    def t_prompt_empty_context():
        prompt = ai._build_prompt(MOCK_CONTEXT_EMPTY)
        assert "Summary:" in prompt
        return f"prompt length={len(prompt)} chars"

    def t_failure_result_shape():
        res = ai._failure("test reason")
        _assert_keys(res, "text", "success", "reason", "model")
        assert res["success"] is False
        assert res["text"] is None
        assert res["reason"] == "test reason"
        return "failure shape OK"

    def t_availability_check_returns_bool():
        result = ai._check_availability()
        _assert_type(result, bool, "availability")
        return f"available={result}"

    r.run("graceful failure when unavailable", t_result_structure_unavailable)
    r.run("prompt builds from context",        t_prompt_builds_correctly)
    r.run("prompt handles empty context",      t_prompt_empty_context)
    r.run("_failure() shape correct",          t_failure_result_shape)
    r.run("_check_availability returns bool",  t_availability_check_returns_bool)


# ── AgentCore integration tests ───────────────────────────────────────────────

def _agent_tests(r: TestRunner):
    from agent.agent_core import InvestorAgent
    agent = InvestorAgent()
    r.section("AgentCore — Integration")

    REQUIRED_KEYS = {"timestamp", "task_type", "success", "metrics",
                     "sentiment", "portfolio_impact", "confidence",
                     "reasoning_trace", "agent_used"}

    def t_analyze_document_raw_text():
        res = agent.receive_task("analyze_document", {
            "source":     SAMPLE_TEXT_RICH,
            "stock_name": "TCS",
            "user_id":    "demo_user",
        })
        for k in REQUIRED_KEYS:
            assert k in res, f"Missing key '{k}'"
        assert res["agent_used"] is True
        assert res["task_type"] == "analyze_document"
        return f"success={res['success']} keys={list(res.keys())}"

    def t_answer_question():
        res = agent.receive_task("answer_question", {
            "question": "What are my TCS holdings?",
            "user_id":  "demo_user",
        })
        for k in REQUIRED_KEYS:
            assert k in res, f"Missing key '{k}'"
        assert res["task_type"] == "answer_question"
        return f"success={res['success']}"

    def t_check_alerts():
        res = agent.receive_task("check_alerts", {"user_id": "demo_user"})
        for k in REQUIRED_KEYS:
            assert k in res, f"Missing key '{k}'"
        assert res["task_type"] == "check_alerts"
        return f"success={res['success']}"

    def t_invalid_task_type():
        res = agent.receive_task("fly_to_moon", {})
        assert res["success"] is False
        assert "agent_used" in res
        assert len(res.get("warnings", [])) > 0
        return f"warnings={res['warnings']}"

    def t_reasoning_trace_populated():
        res = agent.receive_task("check_alerts", {"user_id": "demo_user"})
        trace = res.get("reasoning_trace", [])
        assert len(trace) >= 4, f"Expected ≥4 trace entries, got {len(trace)}"
        return f"{len(trace)} trace entries"

    def t_trace_entry_format():
        res   = agent.receive_task("check_alerts", {"user_id": "demo_user"})
        trace = res.get("reasoning_trace", [])
        for entry in trace:
            _assert_type(entry, str, "trace entry")
            assert "[" in entry and "UTC]" in entry, f"Bad trace format: {entry}"
        return f"all {len(trace)} entries have timestamp"

    def t_confidence_is_dict():
        res  = agent.receive_task("check_alerts", {"user_id": "demo_user"})
        conf = res.get("confidence")
        assert isinstance(conf, dict), f"confidence should be dict, got {type(conf)}"
        assert "score" in conf or "percentage" in conf
        return f"confidence={conf}"

    def t_tool_failure_continues():
        # Pass a bad PDF path — document_processor fails but agent should continue
        res = agent.receive_task("analyze_document", {
            "pdf_path":   "nonexistent_file.pdf",
            "stock_name": "TCS",
            "user_id":    "demo_user",
        })
        # Agent should not raise — it should return a result dict
        assert isinstance(res, dict)
        assert "reasoning_trace" in res
        return f"returned dict with {len(res['reasoning_trace'])} trace entries"

    def t_empty_task_data():
        res = agent.receive_task("check_alerts", {})
        assert isinstance(res, dict)
        assert "agent_used" in res
        return f"success={res['success']}"

    def t_metrics_structure():
        res = agent.receive_task("analyze_document", {
            "source":  SAMPLE_TEXT_RICH,
            "user_id": "demo_user",
        })
        # metrics may be nested under 'metrics' key from MetricExtractor
        m = res.get("metrics") or {}
        _assert_type(m, dict, "metrics")
        return f"metrics keys={list(m.keys())}"

    def t_sentiment_structure():
        res = agent.receive_task("analyze_document", {
            "source":  SAMPLE_TEXT_RICH,
            "user_id": "demo_user",
        })
        s = res.get("sentiment") or {}
        _assert_type(s, dict, "sentiment")
        return f"sentiment={s}"

    def t_portfolio_impact_structure():
        res = agent.receive_task("analyze_document", {
            "source":     SAMPLE_TEXT_RICH,
            "stock_name": "TCS",
            "user_id":    "demo_user",
        })
        pi = res.get("portfolio_impact") or {}
        _assert_type(pi, dict, "portfolio_impact")
        return f"portfolio_impact keys={list(pi.keys())}"

    r.run("analyze_document — raw text",    t_analyze_document_raw_text)
    r.run("answer_question",                t_answer_question)
    r.run("check_alerts",                   t_check_alerts)
    r.run("invalid task type → failure",    t_invalid_task_type)
    r.run("reasoning_trace populated",      t_reasoning_trace_populated)
    r.run("trace entries have timestamp",   t_trace_entry_format)
    r.run("confidence is dict",             t_confidence_is_dict)
    r.run("tool failure → agent continues", t_tool_failure_continues)
    r.run("empty task_data handled",        t_empty_task_data)
    r.run("metrics structure valid",        t_metrics_structure)
    r.run("sentiment structure valid",      t_sentiment_structure)
    r.run("portfolio_impact structure",     t_portfolio_impact_structure)


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="InvestorCoPilot system tests")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show test output")
    args = parser.parse_args()

    print(f"\n{_b('InvestorCoPilot AI — System Test Suite')}")
    print(f"{'═'*64}")

    runner = TestRunner(verbose=args.verbose)

    _doc_tests(runner)
    _metric_tests(runner)
    _sentiment_tests(runner)
    _portfolio_tests(runner)
    _confidence_tests(runner)
    _ai_tests(runner)
    _agent_tests(runner)

    ok = runner.report()
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
