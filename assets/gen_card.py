"""Generate the profile card and contact buttons (dark + light) as SVG.

Run: python3 assets/gen_card.py
Edit LINES below, re-run, commit the two SVGs.
"""
from pathlib import Path
from xml.sax.saxutils import escape

PROMPT = "nikita@begenfys:~$"
COMMAND = "whoami --verbose"
LINES = [
    ("Role", "Product Engineer · backend-heavy"),
    ("Experience", "4+ years, commercial"),
    ("Builds", "payments & billing · support ops · internal platforms"),
    ("Languages", "Python · TypeScript · Go"),
    ("Data", "PostgreSQL · MySQL · ClickHouse · Redis · RabbitMQ"),
    ("Infra", "Docker Swarm · Kubernetes · CI/CD · Prometheus · Loki"),
    ("AI", "LLM integrations · agents · MCP · RAG (in progress)"),
    ("Status", "open to product teams · remote or relocation"),
]

THEMES = {
    "dark": dict(bg="#0d1117", bar="#161b22", border="#30363d", text="#c9d1d9",
                 muted="#8b949e", key="#79c0ff", accent="#7ee787", dots=("#ff5f56", "#ffbd2e", "#27c93f")),
    "light": dict(bg="#ffffff", bar="#f6f8fa", border="#d0d7de", text="#1f2328",
                  muted="#656d76", key="#0550ae", accent="#1a7f37", dots=("#ff5f56", "#ffbd2e", "#27c93f")),
}

W, PAD, LH, KEY_W = 820, 28, 26, 13  # KEY_W: key column width in chars
FONT = "ui-monospace, SFMono-Regular, 'SF Mono', Menlo, Consolas, 'Liberation Mono', monospace"


def render(t: dict) -> str:
    top = 44
    y0 = top + 36
    h = y0 + LH * (len(LINES) + 2) + 10
    rows = []
    # prompt line
    rows.append(
        f'<text x="{PAD}" y="{y0}" class="l" style="animation-delay:.1s">'
        f'<tspan fill="{t["accent"]}">{PROMPT}</tspan> <tspan fill="{t["text"]}">{COMMAND}</tspan></text>'
    )
    for i, (k, v) in enumerate(LINES, start=1):
        dots = "." * (KEY_W - len(k))
        rows.append(
            f'<text x="{PAD}" y="{y0 + LH * i}" class="l" style="animation-delay:{0.35 + i * 0.12:.2f}s">'
            f'<tspan fill="{t["key"]}">{escape(k)}</tspan><tspan fill="{t["muted"]}"> {dots} </tspan>'
            f'<tspan fill="{t["text"]}">{escape(v)}</tspan></text>'
        )
    last = y0 + LH * (len(LINES) + 1)
    delay = 0.35 + (len(LINES) + 1) * 0.12
    rows.append(
        f'<text x="{PAD}" y="{last}" class="l" style="animation-delay:{delay:.2f}s">'
        f'<tspan fill="{t["accent"]}">{PROMPT}</tspan><tspan class="cur" fill="{t["text"]}"> ▋</tspan></text>'
    )
    d1, d2, d3 = t["dots"]
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{h}" viewBox="0 0 {W} {h}" role="img" aria-label="Nikita Perminov — Product Engineer">
  <title>Nikita Perminov — Product Engineer</title>
  <style>
    text {{ font-family: {FONT}; font-size: 15px; white-space: pre; }}
    .l {{ animation: in .45s ease-out both; }}
    .cur {{ animation: blink 1.1s steps(1) infinite; }}
    @keyframes in {{ from {{ opacity: 0; transform: translateX(-6px); }} to {{ opacity: 1; transform: none; }} }}
    @keyframes blink {{ 50% {{ opacity: 0; }} }}
    @media (prefers-reduced-motion: reduce) {{ .l {{ animation: none; }} .cur {{ animation: none; }} }}
  </style>
  <rect x=".5" y=".5" width="{W - 1}" height="{h - 1}" rx="10" fill="{t["bg"]}" stroke="{t["border"]}"/>
  <path d="M.5 {top}V10.5a10 10 0 0 1 10-10h{W - 21}a10 10 0 0 1 10 10V{top}z" fill="{t["bar"]}"/>
  <line x1=".5" y1="{top}" x2="{W - .5}" y2="{top}" stroke="{t["border"]}"/>
  <circle cx="22" cy="22" r="6" fill="{d1}"/><circle cx="42" cy="22" r="6" fill="{d2}"/><circle cx="62" cy="22" r="6" fill="{d3}"/>
  <text x="{W / 2}" y="27" text-anchor="middle" fill="{t["muted"]}" style="font-size:13px">begenFys — zsh</text>
  {chr(10).join("  " + r for r in rows).strip()}
</svg>
'''


if __name__ == "__main__":
    out = Path(__file__).parent
    for name, theme in THEMES.items():
        (out / f"card-{name}.svg").write_text(render(theme), encoding="utf-8")
        print("wrote", out / f"card-{name}.svg")


# ---------------------------------------------------------------------------
# Contact buttons: Telegram is primary (filled), email is secondary (outline).
# ---------------------------------------------------------------------------
SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif"
PLANE = ("M21.2 3.2 2.9 10.3c-1.2.5-1.2 1.2-.2 1.5l4.7 1.5 1.8 5.5c.2.6.1.9.8.9.5 0 .7-.2 1-.5l2.3-2.2 "
         "4.7 3.5c.9.5 1.5.2 1.7-.8l3.1-14.6c.3-1.3-.5-1.9-1.6-1.4zM8.5 13.4l9.3-5.9c.4-.3.9-.1.5.2l-7.6 "
         "6.9-.3 3.2-1.9-4.4z")
BUTTONS = {
    "telegram": dict(label="Telegram", sub="@begenFys", w=212, icon="plane"),
    "email": dict(label="Email", sub="", w=112, icon="mail"),
}
TG_BLUE = "#229ED9"


def render_button(kind: str, theme_name: str) -> str:
    b, t = BUTTONS[kind], THEMES[theme_name]
    w, h = b["w"], 40
    primary = kind == "telegram"
    fill = TG_BLUE if primary else t["bar"]
    stroke = TG_BLUE if primary else t["border"]
    fg = "#ffffff" if primary else t["text"]
    sub_fg = "rgba(255,255,255,.78)" if primary else t["muted"]
    if b["icon"] == "plane":
        icon = f'<g transform="translate(14 8) scale(1)"><path d="{PLANE}" fill="{fg}"/></g>'
    else:
        icon = (f'<g transform="translate(14 10)" fill="none" stroke="{fg}" stroke-width="1.8" '
                f'stroke-linejoin="round"><rect x="1" y="2" width="20" height="16" rx="3"/>'
                f'<path d="M2 4l9 7 9-7"/></g>')
    sub = (f'<tspan fill="{sub_fg}" font-weight="400" dx="8">{escape(b["sub"])}</tspan>' if b["sub"] else "")
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{escape(b["label"])}">
  <rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="{h / 2 - .5}" fill="{fill}" stroke="{stroke}"/>
  {icon}
  <text x="46" y="25.5" fill="{fg}" font-family="{SANS}" font-size="15" font-weight="600">{escape(b["label"])}{sub}</text>
</svg>
'''


if __name__ == "__main__":
    out = Path(__file__).parent
    for kind in BUTTONS:
        for name in THEMES:
            f = out / f"btn-{kind}-{name}.svg"
            f.write_text(render_button(kind, name), encoding="utf-8")
            print("wrote", f)
