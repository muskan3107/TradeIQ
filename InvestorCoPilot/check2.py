import sys; sys.path.insert(0, '.')
from frontend.app import topbar_html, landing_html, CSS

nav  = topbar_html('en')
land = landing_html('en')

checks = {
    "topbar red border":    "border-bottom: 3px solid #E11D2E" in CSS,
    "hero solid red":       "background: #E11D2E" in CSS,
    "no pink gradient":     "linear-gradient(145deg, #fff7f7" not in CSS,
    "no body gradient":     "linear-gradient(180deg, #fff1f2" not in CSS,
    "topbar nav buttons":   "How It Works" in nav,
    "topbar active pill":   "Active" in nav,
    "hero scroll JS":       "scrollIntoView" in land,
    "landing id":           "landing-page" in land,
    "CTA solid red":        "#E11D2E" in land,
    "hero white h1":        "color: #fff" in CSS,
}
failed = [k for k,v in checks.items() if not v]
if failed:
    for f in failed: print("FAIL:", f)
else:
    print(f"ALL {len(checks)} CHECKS PASSED  |  CSS: {len(CSS)} chars")
