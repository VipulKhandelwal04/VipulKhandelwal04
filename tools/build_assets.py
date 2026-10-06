"""Builds the profile README's SVG assets (dark panels, like GitHub's own UI).

Run from the repo root: python3 tools/build_assets.py
Dark only on purpose: GitHub's renderer breaks <picture> inside links (the image
gets re-linked to its own file), and dark panels read well on both GitHub themes.
One accent (the portfolio red), one radius (8px), system fonts only, because
GitHub serves README SVGs as images and they cannot load web fonts.
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
OUT.mkdir(exist_ok=True)

THEMES = {
    "dark": dict(bg0="#0d1117", bg1="#151b23", line="#30363d", text="#e6edf3",
                 muted="#9198a1", accent="#FF4655", node="#161b22", soft="#3d1d22"),
}
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, monospace"
R = 8


def frame(w, h, t, body, rid="bg"):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">
  <defs>
    <linearGradient id="{rid}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="{t['bg0']}"/><stop offset="1" stop-color="{t['bg1']}"/>
    </linearGradient>
  </defs>
  <rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="{R}" fill="url(#{rid})" stroke="{t['line']}"/>
{body}
</svg>
"""


def header(t):
    # Product loop on the right: problem -> build -> eval gate -> ship, a branch
    # down to "cut", and a dashed measure loop from ship back to problem.
    def node(x, y, label, w=74, hot=False):
        stroke = t["accent"] if hot else t["line"]
        return (f'  <rect x="{x-w/2}" y="{y-14}" width="{w}" height="28" rx="6" fill="{t["node"]}" stroke="{stroke}" stroke-width="1.2"/>\n'
                f'  <text x="{x}" y="{y+4.5}" text-anchor="middle" font-family="{MONO}" font-size="12" fill="{t["text"] if not hot else t["accent"]}">{label}</text>\n')

    px, bx, ex, sx, y = 548, 646, 746, 840, 104
    cut_y = 176
    body = f"""
  <text x="40" y="92" font-family="{SANS}" font-size="38" font-weight="650" letter-spacing="-0.5" fill="{t['text']}">Vipul Khandelwal</text>
  <text x="41" y="124" font-family="{SANS}" font-size="14" font-weight="600" letter-spacing="2.6" fill="{t['accent']}">AI PRODUCT MANAGER WHO BUILDS</text>
  <text x="41" y="160" font-family="{SANS}" font-size="14" fill="{t['muted']}">Four years in product analytics. Three products live.</text>

  <path id="main" d="M {px+37} {y} L {sx-37} {y}" fill="none" stroke="{t['line']}" stroke-width="1.4"/>
  <path id="cut" d="M {px+37} {y} L {ex-18} {y} L {ex} {y+18} L {ex} {cut_y-14}" fill="none"/>
  <path d="M {ex} {y+18} L {ex} {cut_y-14}" fill="none" stroke="{t['line']}" stroke-width="1.4" stroke-dasharray="3 4"/>
  <path id="loop" d="M {sx} {y-14} C {sx} 34, {px} 34, {px} {y-14}" fill="none" stroke="{t['line']}" stroke-width="1.4" stroke-dasharray="3 4"/>
  <text x="{(px+sx)/2}" y="40" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{t['muted']}">measure</text>

  <circle r="4.5" fill="{t['accent']}" opacity="0">
    <animateMotion dur="7s" repeatCount="indefinite" keyPoints="0;1" keyTimes="0;1" calcMode="linear"><mpath href="#main"/></animateMotion>
    <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.06;0.9;1" dur="7s" repeatCount="indefinite"/>
  </circle>
  <circle r="4" fill="{t['muted']}" opacity="0">
    <animateMotion dur="7s" begin="3.5s" repeatCount="indefinite"><mpath href="#cut"/></animateMotion>
    <animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;0.01;0.06;0.85;1" dur="7s" begin="3.5s" repeatCount="indefinite"/>
  </circle>
{node(px, y, 'problem', 76)}{node(bx, y, 'build', 62)}  <rect x="{ex-17}" y="{y-17}" width="34" height="34" rx="6" transform="rotate(45 {ex} {y})" fill="{t['node']}" stroke="{t['accent']}" stroke-width="1.2"/>
  <text x="{ex}" y="{y+4}" text-anchor="middle" font-family="{MONO}" font-size="11" fill="{t['accent']}">eval</text>
{node(sx, y, 'ship', 60, hot=True)}{node(ex, cut_y, 'cut', 52)}
"""
    return frame(880, 212, t, body)


def now(t):
    lines = [
        "decide what you will measure before you decide what you will build",
        "an AI feature is ready when it passes the evals, not when the demo works",
        "start rule-based. earn the complex model with usage data",
    ]
    n, dur = len(lines), 15
    parts = []
    for i, line in enumerate(lines):
        a, b = i / n, (i + 1) / n
        vals = "0;0;1;1;0;0" if i else "1;1;0;0"
        times = (f"0;{a:.3f};{a+0.005:.3f};{b-0.02:.3f};{b-0.015:.3f};1" if i
                 else f"0;{b-0.02:.3f};{b-0.015:.3f};1")
        parts.append(f'''  <text x="44" y="30" font-family="{MONO}" font-size="13.5" fill="{t['text']}" opacity="{1 if i == 0 else 0}">{escape(line)}
    <animate attributeName="opacity" values="{vals}" keyTimes="{times}" dur="{dur}s" repeatCount="indefinite"/>
  </text>''')
    body = f"""  <text x="22" y="30" font-family="{MONO}" font-size="14" fill="{t['accent']}">&gt;</text>
{chr(10).join(parts)}
  <rect x="846" y="16" width="8" height="17" rx="1" fill="{t['accent']}">
    <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.51;1" dur="1.1s" repeatCount="indefinite"/>
  </rect>
"""
    return frame(880, 48, t, body, rid="bgn")


def wrap(text, limit):
    out, cur = [], ""
    for word in text.split():
        if len(cur) + len(word) + (1 if cur else 0) > limit:
            out.append(cur)
            cur = word
        else:
            cur = f"{cur} {word}" if cur else word
    return out + ([cur] if cur else [])


def card(t, title, status, desc, link):
    lines = wrap(desc, 50)
    desc_svg = "\n".join(
        f'  <text x="26" y="{86 + i*21}" font-family="{SANS}" font-size="14" fill="{t["muted"]}">{escape(l)}</text>'
        for i, l in enumerate(lines))
    live = status == "Live"
    cw = 14 + len(status) * 7.4
    chip = (f'  <rect x="{406-cw}" y="26" width="{cw}" height="22" rx="11" fill="{t["soft"] if live else "none"}" stroke="{t["accent"] if live else t["line"]}"/>\n'
            f'  <text x="{406-cw/2}" y="41" text-anchor="middle" font-family="{SANS}" font-size="11.5" font-weight="600" fill="{t["accent"] if live else t["muted"]}">{status}</text>')
    body = f"""  <text x="26" y="48" font-family="{SANS}" font-size="21" font-weight="650" fill="{t['text']}">{escape(title)}</text>
{chip}
{desc_svg}
  <text x="26" y="172" font-family="{MONO}" font-size="12.5" fill="{t['accent']}">{escape(link)} &#x2197;</text>
"""
    return frame(432, 196, t, body, rid="bgc")


def button(t, label, w):
    body = f'  <text x="{w/2}" y="27" text-anchor="middle" font-family="{SANS}" font-size="14" font-weight="600" fill="{t["text"]}">{escape(label)} <tspan fill="{t["accent"]}">&#x2197;</tspan></text>\n'
    return frame(w, 42, t, body, rid="bgb")


CARDS = {
    "card-pouncity": ("Pouncity", "Live",
                      "AI pet-care companion for dog and cat owners. One living profile per pet, with personalised diet, health and grooming guidance.",
                      "pouncity.vercel.app"),
    "card-abhyudaya": ("Abhyudaya.ai", "Live",
                       "AI learning platform for people who use AI every day but can't yet build with it. Short lessons, quick checks and honest progress.",
                       "abhyudaya-ai.vercel.app"),
    "card-fastlane": ("FastLane", "Live",
                      "Vendor onboarding portal that shows every vendor where they stand, who owns the next step and what is still needed.",
                      "fastlane-xi.vercel.app"),
    "card-epfo": ("EPFO Portal Revamp", "Concept",
                  "Concept redesign of India's EPFO member portal, focused on grievances you can follow to closure. Not affiliated with EPFO.",
                  "epfo-revamped-concept.vercel.app"),
}
BUTTONS = {"btn-portfolio": ("Portfolio", 132), "btn-linkedin": ("LinkedIn", 124), "btn-email": ("Email", 104)}

for name, t in THEMES.items():
    (OUT / "header.svg").write_text(header(t))
    (OUT / "now.svg").write_text(now(t))
    for key, args in CARDS.items():
        (OUT / f"{key}.svg").write_text(card(t, *args))
    for key, (label, w) in BUTTONS.items():
        (OUT / f"{key}.svg").write_text(button(t, label, w))

print("wrote", len(list(OUT.glob("*.svg"))), "files to", OUT)
