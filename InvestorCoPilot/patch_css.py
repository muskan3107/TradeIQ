"""
Patch app.py in-place:
- Replace CSS block with polished design system
- Fix MARKET_DATA values
- Fix topbar_html
- Fix landing_html hero + CTA
- Fix news_carousel_html (add timestamps)
- Fix reasoning_html (header strip + confidence badge)
- Fix launch_app control-strip layout
"""
import re

with open('frontend/app.py', encoding='utf-8') as f:
    src = f.read()

# ── 1. MARKET DATA ────────────────────────────────────────────────────────────
src = re.sub(
    r'MARKET_DATA\s*=\s*\[.*?\]',
    '''MARKET_DATA = [
    {"index": "NIFTY 50",   "value": 22450, "change": 0.43},
    {"index": "SENSEX",     "value": 73420, "change": 0.38},
    {"index": "BANK NIFTY", "value": 47210, "change": -0.12},
    {"index": "NIFTY IT",   "value": 35640, "change": 1.21},
]''',
    src, flags=re.DOTALL
)
print("MARKET_DATA patched")
with open('frontend/app.py', 'w', encoding='utf-8') as f:
    f.write(src)
print("Saved step 1")
