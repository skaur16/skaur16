#!/usr/bin/env python3
"""The animated terminal banners for github.com/skaur16: header (whoami), the project board, and the footer.
Pure SVG with SMIL animation, so GitHub renders it as is. Run: python3 tools/gen.py"""
import os, random

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets")
random.seed(16)

# Sharn's palette: the cassette purple, the amber label, the sunset pink
BG, BAR, LINE, MUTED, TEXT = "#0b0a14", "#141229", "#2a2650", "#6f6c90", "#f1ecdf"
USER, PATH, PINK, LILAC, ORANGE = "#ffc145", "#ff8a3d", "#f4476b", "#b58cff", "#ff8a3d"
MONO = "'JetBrains Mono','SFMono-Regular',Menlo,Consolas,'Liberation Mono',monospace"
PROMPT = [("sharn@skaur", USER), (":", MUTED), ("~", PATH), ("$ ", MUTED)]

_ids = iter("abcdefghijklmnopqrstuvwxyz")

def typed(x, y, parts, size, begin, cps=28, glow=True, suffix=""):
    """text that types itself: a clipPath that widens one character at a time."""
    cid = "clip" + next(_ids) + suffix
    text = "".join(t for t, _ in parts)
    cw = size * 0.6
    n = len(text)
    width = n * cw
    dur = n / cps
    vals = ";".join(f"{2 + i * cw:.1f}" for i in range(n + 1))  # the last step shows the whole line
    keys = ";".join(f"{i / (n + 1):.4f}" for i in range(n + 1))
    spans = "".join(f'<tspan fill="{c}">{t}</tspan>' for t, c in parts)
    g = f' filter="url(#glow)"' if glow else ""
    return (f'<clipPath id="{cid}"><rect x="{x - 2}" y="{y - size * 1.05:.1f}" height="{size * 1.6:.1f}" width="0">'
            f'<animate attributeName="width" begin="{begin:.2f}s" dur="{dur:.3f}s" fill="freeze" calcMode="discrete" values="{vals}" keyTimes="{keys}"/></rect></clipPath>'
            f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="{size}" xml:space="preserve" textLength="{width:.2f}" lengthAdjust="spacing" clip-path="url(#{cid})"{g}>{spans}</text>',
            begin + dur, x + width)

def cursor(x, y, size, begin, travel_n=0, cps=28):
    cw = size * 0.6
    vals = ";".join(f"{x + i * cw:.2f}" for i in range(travel_n + 1))
    keys = ";".join(f"{i / (travel_n + 1):.4f}" for i in range(travel_n + 1))
    move = (f'<animate attributeName="x" begin="{begin:.2f}s" dur="{travel_n / cps:.3f}s" fill="freeze" calcMode="discrete" values="{vals}" keyTimes="{keys}"/>' if travel_n else "")
    return (f'<rect x="{x}" y="{y - size * 0.82:.2f}" width="{cw:.2f}" height="{size * 1.05:.2f}" fill="{USER}" opacity="0" filter="url(#glow)">{move}'
            f'<set attributeName="opacity" to="1" begin="{begin:.2f}s"/><animate attributeName="fill-opacity" values="1;0" dur="1.05s" calcMode="discrete" begin="{begin + travel_n / cps:.2f}s" repeatCount="indefinite"/></rect>')

def frame(w, h, title, body, label):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="{w}" height="{h}" role="img" aria-label="{label}">
  <defs>
    <filter id="glow" x="-20%" y="-50%" width="140%" height="200%"><feGaussianBlur stdDeviation="2.4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="2" fill="#000" opacity=".28"/></pattern>
    <radialGradient id="vig" cx="50%" cy="50%" r="75%"><stop offset="60%" stop-color="#000" stop-opacity="0"/><stop offset="100%" stop-color="#000" stop-opacity=".55"/></radialGradient>
    <linearGradient id="bar" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{USER}" stop-opacity="0"/><stop offset=".5" stop-color="{USER}" stop-opacity=".06"/><stop offset="1" stop-color="{USER}" stop-opacity="0"/></linearGradient>
    <clipPath id="screen"><rect x="2" y="47" width="{w - 4}" height="{h - 49}"/></clipPath>
    <filter id="tintR"><feColorMatrix type="matrix" values="0 0 0 0 1  0 0 0 0 .28  0 0 0 0 .42  0 0 0 1 0"/></filter>
    <filter id="tintC"><feColorMatrix type="matrix" values="0 0 0 0 .55  0 0 0 0 .45  0 0 0 0 1  0 0 0 1 0"/></filter>
  </defs>
  <rect x="1" y="1" width="{w - 2}" height="{h - 2}" rx="12" fill="{BG}" stroke="{LINE}" stroke-width="2"/>
  <path d="M1 13a12 12 0 0 1 12-12h{w - 26}a12 12 0 0 1 12 12v33H1z" fill="{BAR}"/>
  <line x1="1" y1="46" x2="{w - 1}" y2="46" stroke="{LINE}" stroke-width="2"/>
  <circle cx="26" cy="24" r="6.5" fill="#ff5f57"/><circle cx="48" cy="24" r="6.5" fill="#febc2e"/><circle cx="70" cy="24" r="6.5" fill="#28c840"/>
  <text x="{w / 2}" y="29" text-anchor="middle" font-family="{MONO}" font-size="13" fill="{MUTED}">{title}</text>
  <g clip-path="url(#screen)">{body}</g>
  <g clip-path="url(#screen)" pointer-events="none">
    <rect x="0" y="0" width="{w}" height="{h}" fill="url(#scan)"/>
    <rect x="0" y="-120" width="{w}" height="120" fill="url(#bar)"><animate attributeName="y" values="-120;{h}" dur="7s" repeatCount="indefinite"/></rect>
    <rect x="0" y="0" width="{w}" height="{h}" fill="url(#vig)"/>
  </g>
</svg>
'''

# a 5x7 block alphabet for the big name
GLYPHS = {
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "N": ["10001", "11001", "10101", "10011", "10001", "10001", "10001"],
}

def blockname(word, cell=15, gap=1):
    """rows of blocks that switch on one row at a time, with a chromatic glitch now and then."""
    rows = []
    cols_total = len(word) * 6
    for r in range(7):
        d = []
        for gi, ch in enumerate(word):
            for c, bit in enumerate(GLYPHS[ch][r]):
                if bit == "1":
                    x = (gi * 6 + c) * cell
                    d.append(f"M{x} {r * cell}h{cell + 0.4}v{cell + 0.4}h-{cell + 0.4}z")
        rows.append(" ".join(d))
    W, H = cols_total * cell, 7 * cell
    paths = "".join(f'<path d="{d}" fill="url(#ink)" opacity="0"><set attributeName="opacity" to="1" begin="{2.9 + i * 0.08:.2f}s"/></path>' for i, d in enumerate(rows))
    return W, H, f'''<defs>
    <linearGradient id="ink" x1="0" y1="0" x2="{W}" y2="{H}" gradientUnits="userSpaceOnUse"><stop offset="0" stop-color="{USER}"/><stop offset=".55" stop-color="{ORANGE}"/><stop offset="1" stop-color="{PINK}"/></linearGradient>
    <clipPath id="slice1"><rect x="-20" y="{H * 0.2:.1f}" width="{W + 40}" height="{H * 0.12:.1f}"/></clipPath>
    <clipPath id="slice2"><rect x="-20" y="{H * 0.6:.1f}" width="{W + 40}" height="{H * 0.09:.1f}"/></clipPath>
    <g id="name">{paths}</g>
  </defs>
  <g transform="translate(40 118)">
    <g opacity="0"><set attributeName="opacity" to="1" begin="2.9s"/>
      <use href="#name" opacity=".38" filter="url(#tintR)"><animateTransform attributeName="transform" type="translate" values="-1.5 0;-1.5 0;-9 1;5 -1;-1.5 0;-6 0;-1.5 0;-1.5 0" keyTimes="0;.62;.625;.63;.635;.64;.645;1" dur="6s" begin="2.9s" repeatCount="indefinite"/></use>
      <use href="#name" opacity=".38" filter="url(#tintC)"><animateTransform attributeName="transform" type="translate" values="1.5 0;1.5 0;8 -1;-6 1;1.5 0;7 0;1.5 0;1.5 0" keyTimes="0;.62;.625;.63;.635;.64;.645;1" dur="6s" begin="2.9s" repeatCount="indefinite"/></use>
      <use href="#name" filter="url(#glow)"/>
    </g>
    <g opacity="0"><animate attributeName="opacity" values="0;0;1;0;1;0;0;0" keyTimes="0;.62;.625;.63;.635;.64;.645;1" calcMode="discrete" dur="6s" begin="2.9s" repeatCount="indefinite"/>
      <rect x="-20" y="{H * 0.2:.1f}" width="{W + 40}" height="{H * 0.12:.1f}" fill="{BG}"/>
      <use href="#name" clip-path="url(#slice1)" transform="translate(18 0)"/>
      <use href="#name" clip-path="url(#slice2)" transform="translate(-14 0)"/>
    </g>
  </g>'''

def header():
    body = ""
    first, end, _ = typed(40, 88, PROMPT + [("whoami", TEXT)], 17, 0.4)
    body += first
    W, H, name = blockname("SHARN")
    body += name
    lines = [("Sharandeep Kaur", TEXT), ("mobile developer · Kotlin & Compose", MUTED), ("Swift on the side, C# at school", MUTED), ("Waterloo, Ontario", MUTED), ("open to co-op · skaur.dev", USER)]
    at, y = 3.5, 144
    for i, (txt, col) in enumerate(lines):
        s, at, _ = typed(560, y, [("› ", USER), (txt, col)], 15, at, cps=30, glow=(i == 0), suffix=str(i))
        body += s
        at += 0.1
        y += 28
    s, at2, xend = typed(40, 300, PROMPT, 17, at + 0.3, glow=True, suffix="p")
    body += s + cursor(xend, 300, 17, at2)
    return frame(960, 340, "sharn@skaur — zsh — 120×28", body, "Terminal: whoami — SHARN. Sharandeep Kaur, mobile developer")

def board():
    rows = [("reviewspot", "Kotlin · a reviews app, Compose all the way", USER, "live", 3.2),
            ("travelbuddy", "Swift · trips, their details and expenses", PINK, "shipped", 3.9),
            ("eat-n-split", "React · who owes whom, settled", LILAC, "building", 4.6),
            ("skaur.dev", "the cassette portfolio: pencil, tape, deck", ORANGE, "live", 5.3)]
    body, at, _ = typed(32, 82, PROMPT + [("./projects --status", TEXT)], 14, 0.3, cps=20)
    body += f'<text x="32" y="118" font-family="{MONO}" font-size="14" fill="{MUTED}" xml:space="preserve" textLength="714" lengthAdjust="spacing" opacity="0">PID   PROJECT      WHAT                                             LOAD        STATE<set attributeName="opacity" to="1" begin="{at + 0.2:.2f}s"/></text>'
    y = 152
    for i, (name, what, col, state, dur) in enumerate(rows):
        b = at + 0.45 + i * 0.28
        load = ";".join(f"{random.uniform(24, 76):.1f}" for _ in range(7))
        load += ";" + load.split(";")[0]
        label = f"{i + 1:04d}  "
        body += (f'<g opacity="0"><animate attributeName="opacity" values="0;1" dur=".25s" begin="{b:.2f}s" fill="freeze"/>'
                 f'<text x="32" y="{y}" font-family="{MONO}" font-size="14" xml:space="preserve" textLength="571.2" lengthAdjust="spacing"><tspan fill="{MUTED}">{label}</tspan><tspan fill="{col}" font-weight="700">{name:<13}</tspan><tspan fill="{TEXT}">{what:<48}</tspan></text>'
                 f'<rect x="603" y="{y - 11}" width="80" height="11" rx="2" fill="#1a1733"/><rect x="603" y="{y - 11}" width="40" height="11" rx="2" fill="{col}" opacity=".85"><animate attributeName="width" values="{load}" dur="{dur}s" repeatCount="indefinite"/></rect>'
                 f'<circle cx="708" cy="{y - 5}" r="4.5" fill="{col}" filter="url(#glow)"><animate attributeName="opacity" values="1;.25;1" dur="{1.4 + i * 0.25:.2f}s" repeatCount="indefinite"/></circle>'
                 f'<text x="719" y="{y}" font-family="{MONO}" font-size="14" fill="{col}">{state}</text></g>')
        y += 34
    s, at2, xend = typed(32, 286, PROMPT, 14, at + 0.45 + len(rows) * 0.28 + 0.3, suffix="q")
    body += s + cursor(xend, 286, 14, at2)
    return frame(960, 300, "~/projects — status", body, "Projects: ReviewSpot, TravelBuddy, eat-n-split, skaur.dev")

def footer():
    s1, at, xend = typed(32, 84, PROMPT + [("exit", TEXT)], 15, 0.5, cps=10)
    s2, at2, xend2 = typed(250, 84, [("// logout · thanks for stopping by — let's build something", MUTED)], 15, at + 0.4, cps=50, glow=False, suffix="f")
    return frame(960, 112, "zsh", s1 + s2 + cursor(250, 84, 15, at + 0.4, travel_n=58, cps=50), "exit — thanks for stopping by")

if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    for name, fn in (("header.svg", header), ("now.svg", board), ("footer.svg", footer)):
        with open(os.path.join(OUT, name), "w") as f:
            f.write(fn())
        print(name, os.path.getsize(os.path.join(OUT, name)), "bytes")
