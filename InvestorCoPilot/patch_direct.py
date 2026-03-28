"""Direct targeted fixes for remaining failures."""
import re

with open('frontend/app.py', encoding='utf-8') as f:
    src = f.read()

changes = []

# ── Fix 1: topbar_html - find and replace the whole function ─────────────────
# Find the function by its def line and replace up to the next def
topbar_start = src.find('def topbar_html(lang: str) -> str:')
topbar_end   = src.find('\ndef landing_html', topbar_start)
if topbar_start > 0 and topbar_end > 0:
    new_topbar = '''def topbar_html(lang: str) -> str:
    holdings = pm.get_all_holdings("demo_user")
    total = sum(h["quantity"] * h["avg_price"] for h in holdings)
    return f"""
<div class='topbar'>
  <div style='display:flex;align-items:center;gap:20px'>
    <div>
      <div class='brand'>{tr(lang, 'app_name')}</div>
      <div class='demo-meta'>{tr(lang, 'demo_note')}</div>
    </div>
    <div style='display:flex;gap:4px;margin-left:8px'>
      <button class='topbar-nav-btn'
        onclick="document.querySelectorAll('.fade-page')[0]?.scrollIntoView({{behavior:'smooth'}})">
        Home
      </button>
      <button class='topbar-nav-btn'
        onclick="document.getElementById('how-works-section')?.scrollIntoView({{behavior:'smooth'}})">
        How It Works
      </button>
      <button class='topbar-nav-btn'
        onclick="document.getElementById('how-works-section')?.scrollIntoView({{behavior:'smooth'}})">
        Features
      </button>
    </div>
  </div>
  <div class='topbar-right'>
    <div class='demo-meta' style='font-weight:700;color:#0F172A'>
      Demo Portfolio: \u20b9{total:,.0f}
    </div>
    <div class='pill'>{tr(lang, 'demo_user')}</div>
    <div class='ctrl-chip-green'>Active</div>
  </div>
</div>"""
'''
    src = src[:topbar_start] + new_topbar + src[topbar_end:]
    changes.append("topbar_html replaced")

# ── Fix 2: landing_html - replace the return block ───────────────────────────
# Find the return f""" inside landing_html
landing_fn_start = src.find('def landing_html(lang: str) -> str:')
landing_fn_end   = src.find('\ndef reasoning_html', landing_fn_start)
if landing_fn_start > 0 and landing_fn_end > 0:
    landing_fn = src[landing_fn_start:landing_fn_end]
    # Find the return statement
    ret_start = landing_fn.rfind('    return f"""')
    if ret_start > 0:
        new_return = '''    return f"""
<div class='fade-page' id='landing-page'>
  <div class='hero'>
    <div>
      <h1>{tr(lang, 'hero_title')}</h1>
      <p>{tr(lang, 'hero_sub')}</p>
      <p class='kicker'>{tr(lang, 'hero_tag')}</p>
      <div class='hero-hackathon'>&#127942; Built for ET Hackathon 2026</div>
      <div class='hero-btns'>
        <button class='hero-btn-primary'
          onclick="document.getElementById('start-demo-btn')?.click()">
          &#128640; Launch Live Demo
        </button>
        <button class='hero-btn-secondary'
          onclick="document.getElementById('how-works-section')?.scrollIntoView({{behavior:'smooth'}})">
          &#128216; Architecture Walkthrough
        </button>
      </div>
    </div>
    <div class='float-area'>
      {card_1}{card_2}{card_3}
    </div>
  </div>

  <div class='section'>
    <div class='section-title'>{tr(lang, 'problem_solution')}</div>
    <div class='section-sub'>Why InvestorCoPilot AI exists and why it matters.</div>
    <div class='grid-4'>{problem_html}</div>
  </div>

  <div class='section' id='how-works-section'>
    <div class='section-title'>{tr(lang, 'how_it_works')}</div>
    <div class='section-sub'>{tr(lang, 'how_blurb')}</div>
    <div class='flow'>{flow_html}</div>
  </div>

  <div class='section'>
    <div class='cta-strip'>
      <div style='font-size:1.8rem;font-weight:900;color:#fff;margin-bottom:10px'>Ready to see it in action?</div>
      <div style='font-size:1rem;color:rgba(255,255,255,.8);margin-bottom:24px'>Upload a real PDF and watch the agent reason through it step by step.</div>
      <button class='hero-btn-primary' onclick="document.getElementById('start-demo-btn')?.click()" style='font-size:1rem;padding:0 36px'>&#128640; {tr(lang, 'cta')}</button>
    </div>
  </div>
</div>
"""
'''
        new_landing_fn = landing_fn[:ret_start] + new_return
        src = src[:landing_fn_start] + new_landing_fn + src[landing_fn_end:]
        changes.append("landing_html return replaced")

# ── Fix 3: problem_html cards - use problem-card class ───────────────────────
old_prob = "f\"<div class='card'><span class='icon-wrap {klass}'>{icn}</span><h4>{title}</h4><div class='kicker'>{desc}</div></div>\""
new_prob = "f\"<div class='problem-card'><span class='icon-wrap {klass}'>{icn}</span><h4>{title}</h4><div class='body'>{desc}</div></div>\""
if old_prob in src:
    src = src.replace(old_prob, new_prob)
    changes.append("problem-card class")

# ── Fix 4: flow cards - use flow-card class ───────────────────────────────────
old_flow = "f\"<div class='card'><span class='icon-wrap {klass}'>{icn}</span><b>{label}</b></div>\""
new_flow = "f\"<div class='flow-card'><span class='icon-wrap {klass}'>{icn}</span><b>{label}</b></div>\""
if old_flow in src:
    src = src.replace(old_flow, new_flow)
    changes.append("flow-card class")

with open('frontend/app.py', 'w', encoding='utf-8') as f:
    f.write(src)

print(f"Applied {len(changes)} patches:")
for c in changes:
    print(f"  OK: {c}")
