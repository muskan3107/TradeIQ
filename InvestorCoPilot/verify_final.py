import sys; sys.path.insert(0, '.')
from frontend.app import topbar_html, landing_html, reasoning_html, news_carousel_html, CSS, MARKET_DATA

checks = {
    "design tokens":        "--red:" in CSS and "--red-dark:" in CSS,
    "sticky toolbar":       "position: sticky" in CSS and "height: 64px" in CSS,
    "hero solid red":       "background: var(--red)" in CSS,
    "hero bg blobs":        "bgBlob" in CSS,
    "hero-btn-primary CSS": "hero-btn-primary" in CSS,
    "hackathon tag":        "ET Hackathon 2026" in landing_html("en"),
    "launch live demo btn": "Launch Live Demo" in landing_html("en"),
    "arch walkthrough btn": "Architecture Walkthrough" in landing_html("en"),
    "cta-strip solid":      "cta-strip" in landing_html("en"),
    "problem-card class":   "problem-card" in landing_html("en"),
    "flow-card class":      "flow-card" in landing_html("en"),
    "topbar nav buttons":   "How It Works" in topbar_html("en"),
    "topbar active pill":   "ctrl-chip-green" in topbar_html("en"),
    "portfolio value":      "Demo Portfolio" in topbar_html("en"),
    "ts-chip in CSS":       "ts-chip" in CSS,
    "news timestamps":      "ts-chip" in news_carousel_html("en", [{"title":"Test","source":"ET","link":"#"}]),
    "reason-header":        "reason-header" in reasoning_html("en"),
    "confidence badge":     "Confidence: 82%" in reasoning_html("en"),
    "reason-step border":   "border-left: 4px solid var(--red)" in CSS,
    "card hover -4px":      "translateY(-4px)" in CSS,
    "btn scale 1.02":       "scale(1.02)" in CSS,
    "responsive auto-fit":  "auto-fit" in CSS,
    "NIFTY 22450":          any(m["value"] == 22450 for m in MARKET_DATA),
    "SENSEX 73420":         any(m["value"] == 73420 for m in MARKET_DATA),
    "BANK NIFTY 47210":     any(m["value"] == 47210 for m in MARKET_DATA),
}

passed = sum(v for v in checks.values())
failed = [k for k, v in checks.items() if not v]
print(f"PASSED: {passed}/{len(checks)}")
if failed:
    for f in failed:
        print(f"  FAIL: {f}")
else:
    print("ALL CHECKS PASSED - App is ready for demo!")
