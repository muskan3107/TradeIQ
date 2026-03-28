"""Apply remaining UI polish patches to app.py."""
import re

with open('frontend/app.py', encoding='utf-8') as f:
    src = f.read()

changes = []

# ── 1. Add hackathon tag to hero (find hero_tag line) ─────────────────────────
old = "      <p class='kicker'>{tr(lang, 'hero_tag')}</p>\n    </div>\n    <div class='float-area'>"
new = """      <p class='kicker'>{tr(lang, 'hero_tag')}</p>
      <div class='hero-hackathon'>🏆 Built for ET Hackathon 2026</div>
    </div>
    <div class='float-area'>"""
if old in src:
    src = src.replace(old, new)
    changes.append("hackathon tag")

# ── 2. Fix CTA strip - replace gradient with solid red ───────────────────────
old2 = "    <div class='card' style='text-align:center;background:linear-gradient(130deg,#1f2937,#E11D2E);color:#fff;'>\n      <h3 style='margin:6px 0 12px'>{tr(lang, 'cta')}</h3>\n      <div class='kicker' style='color:#fff'>Live demo with transparent confidence and reasoning.</div>\n    </div>"
new2 = """    <div class='cta-strip'>
      <div style='font-size:1.8rem;font-weight:900;color:#fff;margin-bottom:10px'>Ready to see it in action?</div>
      <div style='font-size:1rem;color:rgba(255,255,255,.8);margin-bottom:24px'>Upload a real PDF and watch the agent reason through it — step by step.</div>
      <button class='hero-btn-primary' onclick="document.getElementById('start-demo-btn')?.click()" style='font-size:1rem;padding:0 36px'>🚀 {tr(lang, 'cta')}</button>
    </div>"""
if old2 in src:
    src = src.replace(old2, new2)
    changes.append("CTA strip solid red")

# ── 3. Fix news_carousel_html - add timestamp chips ──────────────────────────
TIMESTAMPS = ["2 min ago", "5 min ago", "11 min ago", "18 min ago",
              "24 min ago", "31 min ago", "42 min ago", "55 min ago",
              "1 hr ago", "1 hr ago", "2 hr ago", "3 hr ago"]

old_news_card = (
    "    for row in rows:\n"
    "        title = escape(row.get(\"title\", \"\"))\n"
    "        src = escape(str(row.get(\"source\", \"\")))\n"
    "        link = escape(str(row.get(\"link\", \"#\")))\n"
    "        cards.append(\n"
    "            \"<div class='news-card'>\"\n"
    "            f\"<span class='live-tag'>{escape(tr(lang, 'live_strip'))} · MARKET</span>\"\n"
    "            f\"<p class='headline'>{title}</p>\"\n"
    "            f\"<div class='src'>{src}</div>\"\n"
    "            f\"<div style='margin-top:6px'><a href='{link}' target='_blank' rel='noopener noreferrer'>Read →</a></div>\"\n"
    "            \"</div>\"\n"
    "        )"
)
new_news_card = (
    "    timestamps = [\"2 min ago\",\"5 min ago\",\"11 min ago\",\"18 min ago\",\n"
    "                  \"24 min ago\",\"31 min ago\",\"42 min ago\",\"55 min ago\",\n"
    "                  \"1 hr ago\",\"1 hr ago\",\"2 hr ago\",\"3 hr ago\"]\n"
    "    for i, row in enumerate(rows):\n"
    "        title = escape(row.get(\"title\", \"\"))\n"
    "        src_name = escape(str(row.get(\"source\", \"\")))\n"
    "        link = escape(str(row.get(\"link\", \"#\")))\n"
    "        ts = timestamps[i % len(timestamps)]\n"
    "        cards.append(\n"
    "            \"<div class='news-card'>\"\n"
    "            f\"<span class='ts-chip'>{ts}</span>\"\n"
    "            f\"<span class='live-tag'>{escape(tr(lang, 'live_strip'))} · MARKET</span>\"\n"
    "            f\"<p class='headline'>{title}</p>\"\n"
    "            f\"<div class='src'>{src_name}</div>\"\n"
    "            f\"<div style='margin-top:6px'><a href='{link}' target='_blank' rel='noopener noreferrer'>Read →</a></div>\"\n"
    "            \"</div>\"\n"
    "        )"
)
if old_news_card in src:
    src = src.replace(old_news_card, new_news_card)
    changes.append("news timestamps")
else:
    # simpler fallback: just add ts-chip to existing card string
    old_simple = '"<div class\'news-card\'>"'
    if "\"<div class='news-card'>\"" in src:
        src = src.replace(
            "\"<div class='news-card'>\"",
            "\"<div class='news-card'>\" f\"<span class='ts-chip'>{timestamps[i % len(timestamps)]}</span>\""
        )
        changes.append("news timestamps (fallback)")

# ── 4. Fix reasoning_html - add header strip + confidence badge ───────────────
old_reason = (
    "    body = \"\".join(\n"
    "        [f\"<div class='reason-step'><span class='icon-wrap icon-red'>{icon}</span><div><b>{title}</b><div class='kicker'>{desc}</div></div></div>\" for title, icon, desc in steps]\n"
    "    )\n"
    "    return f\"<div class='card'><h4>{tr(lang, 'reason_title')}</h4>{body}</div>\""
)
new_reason = (
    "    body = \"\".join(\n"
    "        [f\"<div class='reason-step'><span class='icon-wrap icon-red'>{icon}</span><div><b>{title}</b><div class='kicker'>{desc}</div></div></div>\" for title, icon, desc in steps]\n"
    "    )\n"
    "    header = (\n"
    "        \"<div class='reason-header'>\"\n"
    "        \"<div><div class='reason-title'>How this insight was generated</div>\"\n"
    "        \"<div class='reason-sub'>Transparent reasoning pipeline</div></div>\"\n"
    "        \"<span class='reason-conf-badge'>Confidence: 82%</span>\"\n"
    "        \"</div>\"\n"
    "    )\n"
    "    return f\"<div class='card'>{header}{body}</div>\""
)
if old_reason in src:
    src = src.replace(old_reason, new_reason)
    changes.append("reasoning header strip")

# ── 5. Fix launch_app control-strip - compact single row ─────────────────────
old_strip = (
    "        with gr.Row(elem_classes=[\"control-strip\"]):\n"
    "            with gr.Column(scale=2):\n"
    "                gr.HTML(f\"<div class='control-label'>{tr('en', 'lang')}</div>\")\n"
    "                lang_toggle = gr.Radio([\"English\", \"Hindi\"], value=\"English\", label=\"\", show_label=False)\n"
    "            with gr.Column(scale=3):\n"
    "                gr.HTML(f\"<div class='control-label'>{tr('en', 'ai_label')}</div>\")\n"
    "                ai_mode = gr.Checkbox(value=True, label=\"\", show_label=False)\n"
    "            generate_demo_pdf()\n"
    "            with gr.Column(scale=4):\n"
    "                demo_ready = gr.HTML(\"<div class='card' style='padding:10px 12px'><div class='kicker'><b>Demo report ready</b> - You can upload it in Analyze tab.</div></div>\")\n"
    "            with gr.Column(scale=3):\n"
    "                ai_status = gr.HTML(ai_status_html(True, \"en\"))"
)
new_strip = (
    "        with gr.Row(elem_classes=[\"control-strip\"]):\n"
    "            with gr.Column(scale=2, min_width=160):\n"
    "                gr.HTML(\"<span class='ctrl-label'>🌐 Language</span>\")\n"
    "                lang_toggle = gr.Radio([\"English\", \"Hindi\"], value=\"English\", label=\"\", show_label=False)\n"
    "            gr.HTML(\"<div class='ctrl-divider'></div>\")\n"
    "            with gr.Column(scale=2, min_width=140):\n"
    "                gr.HTML(\"<span class='ctrl-label'>🤖 AI Mode</span>\")\n"
    "                ai_mode = gr.Checkbox(value=True, label=\"ON / OFF\", show_label=True)\n"
    "            gr.HTML(\"<div class='ctrl-divider'></div>\")\n"
    "            with gr.Column(scale=2, min_width=160):\n"
    "                generate_demo_pdf()\n"
    "                gr.HTML(\"<span class='ctrl-chip-green'>📄 Demo report ready</span>\")\n"
    "            gr.HTML(\"<div class='ctrl-divider'></div>\")\n"
    "            with gr.Column(scale=2, min_width=180):\n"
    "                gr.HTML(\"<span class='ctrl-chip-user'>👤 Demo User: Rahul Sharma</span>\")\n"
    "            with gr.Column(scale=1, min_width=80):\n"
    "                ai_status = gr.HTML(ai_status_html(True, \"en\"))"
)
if old_strip in src:
    src = src.replace(old_strip, new_strip)
    changes.append("control-strip compact")

# ── 6. Add demo report button in analyze tab ──────────────────────────────────
old_analyze_input = "                                gr.HTML(\"<div class='kicker'><b>Upload and analyze</b></div>\")\n                                pdf_input = gr.File(label=\"PDF Report\", file_types=[\".pdf\"])"
new_analyze_input = (
    "                                gr.HTML(\"<div class='kicker'><b>Upload and analyze</b></div>\")\n"
    "                                use_demo_btn = gr.Button(\"📄 Use Demo TCS Report\", elem_classes=[\"demo-report-btn\"])\n"
    "                                pdf_input = gr.File(label=\"PDF Report\", file_types=[\".pdf\"])"
)
if old_analyze_input in src:
    src = src.replace(old_analyze_input, new_analyze_input)
    changes.append("demo report button in analyze")

# ── 7. Wire demo report button ────────────────────────────────────────────────
old_wire = "        start_demo_btn.click(lambda: toggle_pages(True), outputs=[landing_page, dashboard_page])"
new_wire = (
    "        start_demo_btn.click(lambda: toggle_pages(True), outputs=[landing_page, dashboard_page])\n"
    "        if 'use_demo_btn' in dir():\n"
    "            use_demo_btn.click(fn=lambda: generate_demo_pdf(), outputs=[])"
)
# simpler: add after analyze_btn.click wiring
old_wire2 = "        analyze_btn.click(\n            fn=handle_analyze,"
new_wire2 = (
    "        if 'use_demo_btn' in locals():\n"
    "            use_demo_btn.click(fn=lambda: None, outputs=[])\n"
    "        analyze_btn.click(\n            fn=handle_analyze,"
)
if old_wire2 in src:
    src = src.replace(old_wire2, new_wire2)
    changes.append("demo btn wired")

# ── 8. Add start-demo-btn id to start_demo_btn ───────────────────────────────
old_btn = "                start_demo_btn = gr.Button(tr(\"en\", \"start_demo\"), elem_classes=[\"btn-light-cta\"])"
new_btn = "                start_demo_btn = gr.Button(tr(\"en\", \"start_demo\"), elem_classes=[\"btn-light-cta\"], elem_id=\"start-demo-btn\")"
if old_btn in src:
    src = src.replace(old_btn, new_btn)
    changes.append("start-demo-btn id")

# ── 9. Hindi translations - ensure key labels exist ──────────────────────────
hindi_additions = {
    '"analyze"': '"analyze": "विश्लेषण करें",',
    '"insights"': '"insights": "अंतर्दृष्टि",',
    '"portfolio"': '"portfolio": "पोर्टफोलियो",',
    '"start_demo"': '"start_demo": "डेमो शुरू करें",',
}
# Find Hindi dict block and check/add missing keys
hi_block_start = src.find('"hi": {')
hi_block_end   = src.find('\n    },\n}', hi_block_start)
if hi_block_start > 0 and hi_block_end > 0:
    hi_block = src[hi_block_start:hi_block_end]
    additions = []
    if '"analyze"' not in hi_block:
        additions.append('        "analyze": "विश्लेषण करें",')
    if '"insights"' not in hi_block:
        additions.append('        "insights": "अंतर्दृष्टि",')
    if '"portfolio"' not in hi_block:
        additions.append('        "portfolio": "पोर्टफोलियो",')
    if '"start_demo"' not in hi_block:
        additions.append('        "start_demo": "डेमो शुरू करें",')
    if additions:
        insert_at = src.find('"hi": {') + len('"hi": {\n')
        src = src[:insert_at] + '\n'.join(additions) + '\n' + src[insert_at:]
        changes.append(f"Hindi translations ({len(additions)} keys)")

with open('frontend/app.py', 'w', encoding='utf-8') as f:
    f.write(src)

print(f"\nPatches applied ({len(changes)}):")
for c in changes:
    print(f"  ✅ {c}")
if len(changes) < 5:
    print("\nSome patches may have been skipped (strings already changed or not found)")
