#!/usr/bin/env python3
"""Génère les SVG animés du profil dans assets/.

Pour changer un texte (rang TryHackMe, projets, parcours…), modifie-le ici puis lance :
    python3 scripts/build_assets.py
"""
import math
from pathlib import Path

from svgkit import (B, BG0, BG1, BG2, C, DIM, G, LINE, LINE2, MUT, R, TXT, V, Y, Doc, chip, cw,
                    keyframes_show, n, width)

OUT = Path(__file__).resolve().parent.parent / "assets"


def frame(d, w, h, rx=18):
    return f'<rect x=".5" y=".5" width="{w - 1}" height="{h - 1}" rx="{rx}" fill="{BG1}" stroke="{LINE}"/>'


# ─────────────────────────────────────────────────────────────── bannière
def header():
    W, H = 1200, 320
    d = Doc(W, H, "Skavyoy8 — Luke",
            "Bannière animée : Skavyoy8, Luke, Terminale Bac Pro CIEL, France. "
            "Cybersécurité, réseaux, Linux et homelab, avec la topologie du homelab à droite.")
    d.defs.append(f"""
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#060a10"/><stop offset="1" stop-color="#0b1422"/></linearGradient>
<radialGradient id="gG"><stop offset="0" stop-color="{G}" stop-opacity=".16"/><stop offset="1" stop-color="{G}" stop-opacity="0"/></radialGradient>
<radialGradient id="gV"><stop offset="0" stop-color="{V}" stop-opacity=".22"/><stop offset="1" stop-color="{V}" stop-opacity="0"/></radialGradient>
<radialGradient id="gC"><stop offset="0" stop-color="{C}" stop-opacity=".12"/><stop offset="1" stop-color="{C}" stop-opacity="0"/></radialGradient>
<linearGradient id="tg" gradientUnits="userSpaceOnUse" x1="56" y1="0" x2="356" y2="0" spreadMethod="reflect">
  <stop offset="0" stop-color="{C}"/><stop offset="1" stop-color="{G}"/>
  <animateTransform attributeName="gradientTransform" type="translate" from="0 0" to="600 0" dur="7s" repeatCount="indefinite"/>
</linearGradient>
<linearGradient id="fade" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity=".25"/><stop offset=".55" stop-color="#fff" stop-opacity=".7"/><stop offset="1" stop-color="#fff"/></linearGradient>
<mask id="gm"><rect width="{W}" height="{H}" fill="url(#fade)"/></mask>
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#15273a" stroke-width="1"/></pattern>
<pattern id="sl" width="4" height="3" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#fff" fill-opacity=".028"/></pattern>
<linearGradient id="sb" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{C}" stop-opacity="0"/><stop offset=".8" stop-color="{C}" stop-opacity=".045"/><stop offset="1" stop-color="{C}" stop-opacity="0"/></linearGradient>
<clipPath id="card"><rect width="{W}" height="{H}" rx="20"/></clipPath>
<clipPath id="bands"><rect y="112" width="{W}" height="14"/><rect y="140" width="{W}" height="9"/><rect y="163" width="{W}" height="20"/></clipPath>
""")
    d.css.append("""
.grid{animation:grid 6s linear infinite}@keyframes grid{to{transform:translate(40px,40px)}}
.scan{animation:scan 7s linear infinite}@keyframes scan{from{transform:translateY(0)}to{transform:translateY(480px)}}
.glow{animation:glow 9s ease-in-out infinite alternate}@keyframes glow{from{opacity:.55}to{opacity:1}}
.blink{animation:blink 1.1s steps(1) infinite}@keyframes blink{50%{opacity:0}}
.gl1{animation:gl1 5s steps(1) infinite}.gl2{animation:gl2 5s steps(1) infinite}.ttl{animation:ttl 5s steps(1) infinite}
@keyframes gl1{0%,86%,93%,100%{opacity:0;transform:none}87%{opacity:.85;transform:translate(-7px,0)}89%{opacity:.7;transform:translate(5px,0)}91%{opacity:.8;transform:translate(-3px,0)}}
@keyframes gl2{0%,86%,93%,100%{opacity:0;transform:none}88%{opacity:.85;transform:translate(6px,0)}90%{opacity:.6;transform:translate(-5px,0)}92%{opacity:.7;transform:translate(3px,0)}}
@keyframes ttl{0%,86%,93%,100%{transform:none}88%{transform:translate(2px,0)}90%{transform:translate(-2px,0)}}
""")
    b = [f'<g clip-path="url(#card)">', f'<rect width="{W}" height="{H}" fill="url(#bg)"/>',
         f'<g mask="url(#gm)" opacity=".7"><rect class="grid" x="-40" y="-40" width="{W + 80}" height="{H + 80}" fill="url(#grid)"/></g>',
         f'<g class="glow"><circle cx="170" cy="330" r="330" fill="url(#gG)"/><circle cx="1060" cy="30" r="320" fill="url(#gV)"/>'
         f'<circle cx="860" cy="170" r="220" fill="url(#gC)"/></g>']

    # topologie du homelab
    nodes = {
        "inet": (1132, 50, "internet", DIM), "box": (1060, 104, "box", MUT), "sw": (980, 160, "switch", C),
        "ms": (866, 160, "ms-01", G), "pi": (768, 82, "pi-hole", C), "kuma": (726, 166, "kuma", C),
        "jf": (782, 252, "jellyfin", C), "opn": (970, 250, "opnsense", V), "ad": (1068, 272, "AD", V),
        "meta": (1122, 206, "metasploitable", V),
    }
    edges = [("inet", "box", DIM, "4 4", 1.2), ("box", "sw", LINE2, None, 1.4), ("sw", "ms", C, None, 2.6),
             ("ms", "pi", LINE2, None, 1.4), ("ms", "kuma", LINE2, None, 1.4), ("ms", "jf", LINE2, None, 1.4),
             ("ms", "opn", V, "5 4", 1.3), ("opn", "ad", V, "5 4", 1.3), ("opn", "meta", V, "5 4", 1.3)]
    b.append(f'<rect x="934" y="190" width="250" height="110" rx="14" fill="{V}" fill-opacity=".04" stroke="{V}" '
             f'stroke-opacity=".35" stroke-dasharray="3 5"/>')
    b.append(d.text("vlan lab · isolé", 1176, 182, 10.5, V, "b", "end", opacity=".8"))
    for i, (a, z, col, dash, sw) in enumerate(edges):
        (x1, y1, *_), (x2, y2, *_) = nodes[a], nodes[z]
        da = f' stroke-dasharray="{dash}"' if dash else ""
        b.append(f'<path id="e{i}" d="M{x1} {y1}L{x2} {y2}" stroke="{col}" stroke-width="{sw}" stroke-opacity=".7"{da} fill="none"/>')
    b.append(d.text("10G", 923, 150, 10.5, C, "b", "middle"))
    packets = [(2, C, 1.4, 0, False), (2, C, 1.4, .7, True), (1, MUT, 2.2, .3, False), (3, G, 2.4, .2, False),
               (4, G, 2.0, 1.1, True), (5, G, 2.6, .6, False), (6, V, 2.2, .4, False), (7, V, 2.0, 1.4, False),
               (8, V, 2.4, .9, True), (0, DIM, 3.0, 0, True)]
    for e, col, dur, beg, rev in packets:
        kp = ' keyPoints="1;0" keyTimes="0;1" calcMode="linear"' if rev else ""
        b.append(f'<circle r="2.6" fill="{col}"><animateMotion dur="{dur}s" begin="{beg}s" repeatCount="indefinite"{kp}>'
                 f'<mpath href="#e{e}"/></animateMotion></circle>')
    for key, (x, y, label, col) in nodes.items():
        if key == "ms":
            b.append(f'<circle cx="{x}" cy="{y}" r="20" fill="none" stroke="{G}" stroke-width="1.5">'
                     f'<animate attributeName="r" values="20;44" dur="2.6s" repeatCount="indefinite"/>'
                     f'<animate attributeName="stroke-opacity" values=".7;0" dur="2.6s" repeatCount="indefinite"/></circle>')
            b.append(f'<rect x="{x - 17}" y="{y - 17}" width="34" height="34" rx="8" fill="{BG2}" stroke="{G}" stroke-width="1.8"/>')
            for k in range(3):
                b.append(f'<rect x="{x - 9}" y="{y - 9 + k * 7}" width="18" height="4" rx="1.5" fill="{G}" fill-opacity="{.9 - k * .25}"/>')
            lw = width("ms-01 · proxmox", 11.5) + 12
            b.append(f'<rect x="{n(x - lw / 2)}" y="{y + 24}" width="{n(lw)}" height="17" rx="5" fill="#08101a" fill-opacity=".9"/>')
            b.append(d.text("ms-01 · proxmox", x, y + 36, 11.5, G, "b", "middle"))
        else:
            b.append(f'<circle cx="{x}" cy="{y}" r="7" fill="{BG1}" stroke="{col}" stroke-width="1.6"/><circle cx="{x}" cy="{y}" r="2.6" fill="{col}"/>')
            lw = width(label, 10.5) + 10
            b.append(f'<rect x="{n(x - lw / 2)}" y="{y + 13}" width="{n(lw)}" height="14" rx="4" fill="#08101a" fill-opacity=".85"/>')
            b.append(d.text(label, x, y + 23, 10.5, MUT if col != V else V, "r", "middle"))

    # texte de gauche
    b.append(d.runs([("┌──(", C, "r"), ("skavyoy", G, "b"), ("@", MUT, "r"), ("homelab", G, "b"), (")-[", C, "r"),
                     ("~", TXT, "b"), ("]", C, "r")], 60, 70, 15))
    b.append(d.runs([("└─", C, "r"), ("$ ", V, "b"), ("cat bonjour.txt", TXT, "r")], 60, 94, 15))
    b.append(f'<rect class="blink" x="{60 + 20 * cw(15) + 2}" y="81" width="{cw(15)}" height="17" fill="{G}"/>')
    title = d.path_text("Skavyoy8", 56, 196, 100, "x")
    b.append(f'<g clip-path="url(#bands)"><path class="gl1" d="{title}" fill="{R}" opacity="0"/>'
             f'<path class="gl2" d="{title}" fill="{C}" opacity="0"/></g>')
    b.append(f'<path class="ttl" d="{title}" fill="url(#tg)"/>')
    b.append(d.runs([("Luke", TXT, "b"), (" · ", DIM, "r"), ("Terminale Bac Pro CIEL", MUT, "r"), (" · ", DIM, "r"),
                     ("France", MUT, "r")], 60, 238, 19))
    x = 60
    for label, col in (("cybersécurité", G), ("réseaux", C), ("linux", V), ("homelab", Y)):
        svg, w = chip(d, x, 260, label, col, 12.5, True, 28)
        b.append(svg)
        x += w + 10

    b.append(f'<rect class="scan" y="-160" width="{W}" height="160" fill="url(#sb)"/>')
    b.append(f'<rect width="{W}" height="{H}" fill="url(#sl)"/>')
    b.append("</g>")
    b.append(f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="20" fill="none" stroke="#1d2b3d"/>')
    for cx, cy, sx, sy in ((16, 16, 1, 1), (W - 16, 16, -1, 1), (16, H - 16, 1, -1), (W - 16, H - 16, -1, -1)):
        b.append(f'<path d="M{cx} {cy + 20 * sy}V{cy}H{cx + 20 * sx}" fill="none" stroke="{C}" stroke-opacity=".55" stroke-width="2"/>')
    d.add(*b)
    d.save(OUT / "header.svg")


# ─────────────────────────────────────────────────────────────── terminal
LOCK = [
    "......########......",
    ".....##########.....",
    "....####....####....",
    "....###......###....",
    "....##........##....",
    "....##........##....",
    "....##........##....",
    "....##........##....",
    "....##........##....",
    "..################..",
    ".##################.",
    ".##################.",
    ".##################.",
    ".########..########.",
    ".#######....#######.",
    ".#######....#######.",
    ".########..########.",
    ".########..########.",
    ".########..########.",
    ".##################.",
    ".##################.",
    "..################..",
]

FETCH = [
    [("luke", G, "b"), ("@", MUT, "r"), ("skavyoy8", C, "b")],
    [("─" * 13, DIM, "r")],
    [("OS          ", C, "b"), ("Linux (Debian) · Windows", TXT, "r")],
    [("Formation   ", C, "b"), ("Terminale Bac Pro CIEL", TXT, "r")],
    [("Spécialité  ", C, "b"), ("Cyber · Info & réseaux · Électronique", TXT, "r")],
    [("Objectif    ", C, "b"), ("BTS SIO option SISR · alternance · 2027", TXT, "r")],
    [("Pratique    ", C, "b"), ("TryHackMe · 0x3 [Pathfinder] · top 35 %", TXT, "r")],
    [("Homelab     ", C, "b"), ("MS-01 · Proxmox · lien 10G · rack 10″", TXT, "r")],
    [("Outils      ", C, "b"), ("nmap · Wireshark · VirtualBox", TXT, "r")],
    [("Devise      ", C, "b"), ("j'apprends en pratiquant", Y, "r")],
]

NMAP = [
    ("22/tcp", "linux", "daily driver · VMs VirtualBox"),
    ("53/udp", "réseaux", "OSI · IPv4 · ARP · DHCP · DNS"),
    ("443/tcp", "cybersécurité", "nmap · Wireshark · CTF"),
    ("8006/tcp", "proxmox", "homelab · en préparation"),
]


def terminal():
    W, S, LH = 880, 15, 22
    CW = cw(S)
    X0, TOP = 30, 40
    T = 24.0  # durée d'un cycle d'animation
    lines = 2 + 12 + 2 + 5 + 2
    H = TOP + 26 + lines * LH + 14
    d = Doc(W, H, "whoami — Skavyoy8",
            "Terminal animé : fastfetch (Linux Debian et Windows, Terminale Bac Pro CIEL, objectif BTS SIO SISR "
            "en alternance en 2027, TryHackMe 0x3 Pathfinder top 35 %, homelab MS-01 Proxmox) "
            "puis un nmap humoristique de ses compétences.")
    d.defs.append(f"""
<linearGradient id="lk" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="{len(LOCK) * LH / 2}" spreadMethod="reflect">
  <stop offset="0" stop-color="{C}"/><stop offset="1" stop-color="{G}"/>
  <animateTransform attributeName="gradientTransform" type="translate" values="0 0;0 {len(LOCK) * LH};0 0" dur="8s" repeatCount="indefinite"/>
</linearGradient>""")
    d.css.append(f".all{{animation:all {T}s linear infinite}}@keyframes all{{0%,96%{{opacity:1}}99%,100%{{opacity:0}}}}"
                 ".blink{animation:blink 1.1s steps(1) infinite}@keyframes blink{50%{opacity:0}}")
    anim_i = [0]

    def appear(t):
        i = anim_i[0] = anim_i[0] + 1
        d.css.append(keyframes_show(f"a{i}", t, T) + f".a{i}{{animation:a{i} {T}s linear infinite}}")
        return f"a{i}"

    def typed(x, y, cmd, t0, t1, t_show):
        """Masque qui glisse caractère par caractère pour simuler la frappe."""
        i = anim_i[0] = anim_i[0] + 1
        steps, w = len(cmd), len(cmd) * CW
        p0, p1, ps, pe = (t0 / T * 100, t1 / T * 100, t_show / T * 100, (t1 + .3) / T * 100)
        d.css.append(
            f"@keyframes m{i}{{0%,{p0:.2f}%{{transform:translateX(0);animation-timing-function:steps({steps},end)}}"
            f"{p1:.2f}%,100%{{transform:translateX({n(w)}px)}}}}.m{i}{{animation:m{i} {T}s linear infinite}}"
            f"@keyframes c{i}{{0%,{ps:.2f}%{{opacity:0}}{ps + .01:.2f}%,{pe:.2f}%{{opacity:1}}{pe + .01:.2f}%,100%{{opacity:0}}}}"
            f".c{i}{{animation:c{i} {T}s linear infinite}}")
        return (f'<g class="m{i} rm-hide"><rect x="{n(x)}" y="{y - S}" width="{n(w + CW)}" height="{LH}" fill="{BG1}"/>'
                f'<rect class="c{i}" x="{n(x)}" y="{y - 13}" width="{n(CW)}" height="17" fill="{G}"/></g>')

    def prompt(y, t):
        return d.runs([("┌──(", C, "r"), ("skavyoy", G, "b"), ("@", MUT, "r"), ("homelab", G, "b"), (")-[", C, "r"),
                       ("~", TXT, "b"), ("]", C, "r")], X0, y, S, cls=appear(t))

    def command(y, cmd, t, t0):
        t1 = t0 + .09 * len(cmd)
        body = d.runs([("└─", C, "r"), ("$ ", V, "b"), (cmd, TXT, "r")], X0, y, S)
        return f'<g class="{appear(t)}">{body}{typed(X0 + 4 * CW, y, cmd, t0, t1, t)}</g>', t1

    b = [frame(d, W, H, 14),
         f'<path d="M14 .5H{W - 14}A13.5 13.5 0 0 1 {W - .5} 14V{TOP}H.5V14A13.5 13.5 0 0 1 14 .5Z" fill="{BG2}"/>',
         f'<path d="M.5 {TOP}H{W - .5}" stroke="{LINE}"/>']
    for k, col in enumerate((R, Y, G)):
        b.append(f'<circle cx="{22 + k * 20}" cy="{TOP / 2}" r="6" fill="{col}" fill-opacity=".9"/>')
    b.append(d.text("skavyoy@homelab: ~", W / 2, TOP / 2 + 4.5, 12.5, MUT, "r", "middle"))

    body = []
    y = TOP + 30
    body.append(prompt(y, .3))
    y += LH
    g, t_end = command(y, "fastfetch", .3, .9)
    body.append(g)
    y += LH

    # logo cadenas en pixels + infos
    t = t_end + .5
    px = [f'<rect x="{n(X0 + c * CW)}" y="{n(y - 16 + r * LH / 2)}" width="{n(CW - 1.2)}" height="{n(LH / 2 - 1.2)}" rx="1.2"/>'
          for r, row in enumerate(LOCK) for c, ch in enumerate(row) if ch == "#"]
    body.append(f'<g class="{appear(t)}" fill="url(#lk)">{"".join(px)}</g>')
    ix = X0 + 20 * CW + 34
    for k, parts in enumerate(FETCH):
        body.append(d.runs(parts, ix, y + k * LH, S, cls=appear(t + .06 * k)))
    yk = y + (len(FETCH) + .5) * LH
    sw = [f'<rect x="{n(ix + k * 26)}" y="{n(yk - 12)}" width="22" height="14" rx="2" fill="{col}"/>'
          for k, col in enumerate((R, Y, G, C, B, V, MUT, TXT))]
    body.append(f'<g class="{appear(t + .7)}">{"".join(sw)}</g>')
    y += 12 * LH

    t = t + 1.4
    body.append(prompt(y, t))
    y += LH
    g, t_end = command(y, "nmap -sV skavyoy8", t, t + .5)
    body.append(g)
    y += LH
    t = t_end + .6
    body.append(d.runs([("PORT      STATE  SERVICE        VERSION", MUT, "b")], X0, y, S, cls=appear(t)))
    for k, (port, svc, ver) in enumerate(NMAP):
        y += LH
        body.append(d.runs([(port.ljust(10), Y, "r"), ("open   ", G, "b"), (svc.ljust(15), C, "r"), (ver, TXT, "r")],
                           X0, y, S, cls=appear(t + .15 * (k + 1))))
    y += LH
    t += 1.3
    body.append(prompt(y, t))
    y += LH
    cur = f'<rect class="blink" x="{n(X0 + 4 * CW)}" y="{y - 13}" width="{n(CW)}" height="17" fill="{G}"/>'
    body.append(f'<g class="{appear(t)}">{d.runs([("└─", C, "r"), ("$ ", V, "b")], X0, y, S)}{cur}</g>')
    b.append(f'<g class="all">{"".join(body)}</g>')
    d.add(*b)
    d.save(OUT / "terminal.svg")


# ─────────────────────────────────────────────────────────────── compétences
def nmap_icon(cx, cy, s, col):
    r = s / 2
    return (f'<g fill="none" stroke="{col}" stroke-width="1.6"><circle cx="{cx}" cy="{cy}" r="{r}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r * .55}" stroke-opacity=".6"/><path d="M{cx - r} {cy}H{cx + r}M{cx} {cy - r}V{cy + r}" stroke-opacity=".35"/></g>'
            f'<path d="M{cx} {cy}L{cx} {cy - r}A{r} {r} 0 0 1 {n(cx + r * .87)} {n(cy - r * .5)}Z" fill="{col}" fill-opacity=".35">'
            f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="3s" repeatCount="indefinite"/></path>'
            f'<circle cx="{n(cx + r * .45)}" cy="{n(cy + r * .2)}" r="2" fill="{col}"><animate attributeName="opacity" values="0;1;0" dur="3s" repeatCount="indefinite"/></circle>')


def windows_icon(cx, cy, s, col):
    h, g = s / 2 - 1, 2
    return "".join(f'<rect x="{n(cx - s / 2 + i * (h + g))}" y="{n(cy - s / 2 + j * (h + g))}" width="{n(h)}" height="{n(h)}" fill="{col}"/>'
                   for i in (0, 1) for j in (0, 1))


SKILLS = [
    ("Cybersécurité", "// je m'entraîne en pratiquant", G, [
        ("wireshark", "Wireshark", "#3b9ad9"), ("@nmap", "nmap", G), ("tryhackme", "TryHackMe", "#ff4b5c")],
     ["repérer les services ouverts", "observer le trafic réseau", "résoudre des CTF"]),
    ("Réseaux", "// comment ça communique", C, [
        ("#OSI", "7 couches", C), ("#IPv4", "adressage", C), ("#ARP", "résolution", C), ("#DHCP", "auto-config", C),
        ("#DNS", "noms", C), ("#VLAN", "segmenter", C), ("#LAN", "réseau local", C)], []),
    ("Systèmes", "// tout tester sans rien casser", V, [
        ("linux", "Linux", "#fcc624"), ("debian", "Debian", "#e0355a"), ("@windows", "Windows", "#3aa0ff"),
        ("proxmox", "Proxmox", "#e57000"), ("virtualbox", "VirtualBox", "#5b8def"), ("docker", "Docker", "#2496ed"),
        ("pihole", "Pi-hole", "#f0505a")], []),
    ("Web & code", "// mes sites et mes fiches", Y, [
        ("html5", "HTML", "#e34f26"), ("css", "CSS", "#4f8cff"), ("javascript", "JavaScript", "#f7df1e"),
        ("typescript", "TypeScript", "#4c8fe0"), ("nextdotjs", "Next.js", TXT), ("tailwindcss", "Tailwind", "#06b6d4"),
        ("git", "Git", "#f05032"), ("github", "GitHub", TXT)], []),
]


def skills():
    W, RH, GAP = 1000, 108, 12
    H = len(SKILLS) * (RH + GAP) - GAP
    d = Doc(W, H, "Compétences",
            "Cybersécurité : Wireshark, nmap, TryHackMe. Réseaux : OSI, IPv4, ARP, DHCP, DNS, VLAN, LAN. "
            "Systèmes : Linux, Debian, Windows, Proxmox, VirtualBox, Docker, Pi-hole. "
            "Web : HTML, CSS, JavaScript, TypeScript, Next.js, Tailwind, Git, GitHub.")
    d.defs.append('<linearGradient id="sh" x1="0" x2="1"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
                  '<stop offset=".5" stop-color="#fff" stop-opacity=".07"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>')
    d.css.append(".pulse{animation:pulse 3s ease-in-out infinite alternate}@keyframes pulse{from{opacity:.45}to{opacity:1}}")
    b = []
    for r, (title, sub, acc, tiles, notes) in enumerate(SKILLS):
        y = r * (RH + GAP)
        d.defs.append(f'<clipPath id="row{r}"><rect y="{y}" width="{W}" height="{RH}" rx="16"/></clipPath>')
        d.css.append(f".sh{r}{{animation:sh 7s {r * 1.2}s ease-in-out infinite}}")
        b.append(f'<rect x=".5" y="{y + .5}" width="{W - 1}" height="{RH - 1}" rx="16" fill="{BG1}" stroke="{LINE}"/>')
        b.append(f'<rect class="pulse" x="0" y="{y + 22}" width="4" height="{RH - 44}" rx="2" fill="{acc}"/>')
        b.append(d.text(f"0{r + 1}", 26, y + 34, 12, acc, "b"))
        b.append(d.text(title, 26, y + 60, 19, TXT, "b"))
        b.append(d.text(sub, 26, y + 84, 11.5, DIM))
        b.append(f'<path d="M262 {y + 20}V{y + RH - 20}" stroke="{LINE2}" stroke-dasharray="2 4"/>')
        for k, (slug, label, col) in enumerate(tiles):
            tx, ty = 288 + k * 86, y + 14
            cx, cy = tx + 29, ty + 29
            b.append(f'<rect x="{tx}" y="{ty}" width="58" height="58" rx="13" fill="{BG2}" stroke="{LINE2}"/>')
            if slug.startswith("#"):
                word = slug[1:]
                b.append(d.text(word, cx, cy + 5, 15 if len(word) <= 3 else 13, col, "x", "middle"))
            elif slug == "@nmap":
                b.append(nmap_icon(cx, cy, 30, col))
            elif slug == "@windows":
                b.append(windows_icon(cx, cy, 26, col))
            else:
                b.append(d.icon(slug, cx, cy, 30, col))
            b.append(d.text(label, cx, y + 95, 11, MUT, "r", "middle"))
        for k, note in enumerate(notes):
            nx = 288 + len(tiles) * 86 + 14
            b.append(d.runs([("→ ", acc, "b"), (note, MUT, "r")], nx, y + 37 + k * 23, 13))
        b.append(f'<g clip-path="url(#row{r})"><rect class="sh{r}" x="-300" y="{y}" width="260" height="{RH}" fill="url(#sh)"/></g>')
    d.css.append(f"@keyframes sh{{0%{{transform:translateX(0)}}45%,100%{{transform:translateX({W + 340}px)}}}}")
    d.add(*b)
    d.save(OUT / "skills.svg")


# ─────────────────────────────────────────────────────────────── homelab
def homelab():
    W, H = 1000, 660
    d = Doc(W, H, "Homelab — rack 10 pouces",
            "Rack 10 pouces 8U en préparation : écran tactile, patch panel Cat6, switch MokerLink 8×2.5G, "
            "Minisforum MS-01 sous Proxmox (i5-12600H, 32 Go, NVMe 1 To, 2×SFP+ 10G), réserve NAS. "
            "Services prévus : Pi-hole, Homepage, Uptime Kuma, Jellyfin, Immich, Samba, dashboard Pronote, labs cyber isolés.")
    d.defs.append(f"""
<linearGradient id="bar" x1="0" y1="1" x2="0" y2="0"><stop offset="0" stop-color="{G}"/><stop offset="1" stop-color="{C}"/></linearGradient>
<pattern id="vent" width="10" height="8" patternUnits="userSpaceOnUse"><circle cx="5" cy="4" r="2.2" fill="#05080d"/></pattern>
<pattern id="grill" width="5" height="5" patternUnits="userSpaceOnUse"><rect width="3" height="5" fill="#0b1119"/></pattern>""")
    d.css.append("""
.eq{transform-box:fill-box;transform-origin:50% 100%;animation:eq 1.6s ease-in-out infinite alternate}
@keyframes eq{0%{transform:scaleY(.25)}100%{transform:scaleY(1)}}
.led{animation:led 1s steps(1) infinite}@keyframes led{50%{opacity:.15}}
.pwr{animation:pwr 2.4s ease-in-out infinite alternate}@keyframes pwr{from{opacity:.35}to{opacity:1}}
.seg{transform-box:fill-box;transform-origin:0 50%;animation:seg 1.6s cubic-bezier(.2,.8,.2,1) both}
@keyframes seg{from{transform:scaleX(0)}to{transform:scaleX(1)}}
""")
    b = [frame(d, W, H)]
    b.append(d.runs([("~/", DIM, "r"), ("homelab", C, "b")], 30, 48, 17))
    b.append(d.text("rack 10″ · 8U · un vrai serveur à la maison pour pratiquer", 30, 72, 12.5, MUT))
    svg, w = chip(d, 0, 0, "phase 1 · en préparation", Y, 12, True, 28)
    b.append(f'<g transform="translate({n(W - 30 - w)} 30)">{svg}</g>')

    # rack
    RX, RW, U, RT = 70, 290, 46, 150
    IX, IW = RX + 16, RW - 32
    units = [("Écran tactile 7,84″", 2, 2, "screen"), ("Patch panel Cat6", .5, 1, "patch"),
             ("Switch MokerLink", 1, 1, "switch"), ("Minisforum MS-01", 2, 1, "ms01"),
             ("Réserve · futur NAS", 1, 1, "reserve"), ("Cache ventilé", 1, 2, "vent"), ("Cache plein", .5, 2, "blank")]
    RB = RT + 8 * U
    b.append(f'<rect x="{RX - 6}" y="{RT - 12}" width="{RW + 12}" height="12" rx="3" fill="#1a2433" stroke="{LINE2}"/>')
    b.append(f'<rect x="{RX - 6}" y="{RB}" width="{RW + 12}" height="12" rx="3" fill="#1a2433" stroke="{LINE2}"/>')
    for fx in (RX + 4, RX + RW - 26):
        b.append(f'<rect x="{fx}" y="{RB + 12}" width="22" height="8" rx="2" fill="#141c28"/>')
    for rx_ in (RX, RX + RW - 16):
        b.append(f'<rect x="{rx_}" y="{RT}" width="16" height="{8 * U}" fill="#151e2b" stroke="{LINE2}"/>')
        for k in range(24):
            b.append(f'<rect x="{rx_ + 5.5}" y="{n(RT + k * U / 3 + 5.5)}" width="5" height="5" rx="1" fill="#070b10"/>')
    # routeur posé dessus (phase 2)
    b.append(f'<rect x="150" y="{RT - 44}" width="130" height="30" rx="6" fill="#0e141d" stroke="{Y}" stroke-opacity=".55" stroke-dasharray="4 3"/>')
    b.append(d.text("GL.iNet", 166, RT - 24, 11, MUT, "b"))
    b.append(f'<circle class="led" cx="262" cy="{RT - 29}" r="2.2" fill="{Y}" style="animation-duration:2.2s"/>')
    labels = [("Routeur GL.iNet", "dessus · phase 2", 2, RT - 29)]
    y = RT
    for name, u, phase, kind in units:
        h = u * U
        x0, y0, w0, h0 = IX + 2, y + 1.5, IW - 4, h - 3
        if kind == "reserve":
            b.append(f'<rect x="{x0}" y="{y0}" width="{w0}" height="{h0}" rx="3" fill="none" stroke="{DIM}" stroke-dasharray="4 4"/>')
            b.append(d.text("réserve · futur NAS", IX + IW / 2, y + h / 2 + 4, 10.5, DIM, "r", "middle"))
        else:
            dash = ' stroke-dasharray="4 3"' if phase == 2 else ""
            stroke = Y if phase == 2 else LINE2
            so = ' stroke-opacity=".55"' if phase == 2 else ""
            fill = "#0f1520" if phase == 2 else "#151d29"
            b.append(f'<rect x="{x0}" y="{y0}" width="{w0}" height="{h0}" rx="3" fill="{fill}" stroke="{stroke}"{so}{dash}/>')
        if kind == "screen":
            sx, sy, sw_, sh_ = IX + 16, y + 9, IW - 32, h - 18
            b.append(f'<rect x="{sx}" y="{sy}" width="{sw_}" height="{sh_}" rx="4" fill="#03060a" stroke="#1e2a3a"/>')
            b.append(d.text("btop · cpu", sx + 8, sy + 14, 9, C, "b"))
            b.append(d.text("● proxmox en ligne", sx + sw_ - 8, sy + 14, 9, G, "r", "end"))
            for k in range(17):
                bh = sh_ - 30
                dur = 0.9 + (k * 37 % 11) / 10
                b.append(f'<rect class="eq" x="{sx + 10 + k * 12.4}" y="{sy + 22}" width="8" height="{bh}" rx="1.5" fill="url(#bar)" '
                         f'style="animation-duration:{dur:.1f}s;animation-delay:-{k * .23:.2f}s"/>')
        elif kind == "patch":
            for k in range(12):
                px = IX + 18 + k * 19
                b.append(f'<rect x="{px}" y="{y + 7}" width="13" height="9" rx="1.5" fill="#05080d" stroke="#2a3748"/>')
                if k < 5:
                    b.append(f'<rect x="{px + 2}" y="{y + 5}" width="9" height="3" rx="1" fill="{(C, V, G, Y, B)[k]}"/>')
        elif kind == "switch":
            b.append(d.text("MokerLink", IX + 12, y + 20, 9.5, MUT, "b"))
            b.append(d.text("8×2.5G", IX + 12, y + 33, 8.5, DIM))
            for k in range(8):
                px = IX + 76 + k * 17
                b.append(f'<rect x="{px}" y="{y + 21}" width="14" height="12" rx="1.5" fill="#05080d" stroke="#2a3748"/>')
                col = G if k % 3 else Y
                b.append(f'<circle class="led" cx="{px + 7}" cy="{y + 14}" r="1.8" fill="{col}" '
                         f'style="animation-duration:{.35 + (k * 53 % 9) / 10:.2f}s;animation-delay:-{k * .17:.2f}s"/>')
            for k in range(2):
                px = IX + 218 + k * 18
                b.append(f'<rect x="{px}" y="{y + 22}" width="15" height="9" rx="1" fill="#05080d" stroke="{C}" stroke-opacity=".6"/>')
            b.append(f'<circle class="led" cx="{IX + 225}" cy="{y + 14}" r="1.8" fill="{C}" style="animation-duration:.5s"/>')
        elif kind == "ms01":
            b.append(f'<rect x="{IX + 4}" y="{y + h - 9}" width="{IW - 8}" height="5" rx="1.5" fill="#202b3b"/>')
            mx, my, mw, mh = IX + 22, y + 9, IW - 44, h - 19
            b.append(f'<rect x="{mx}" y="{my}" width="{mw}" height="{mh}" rx="7" fill="#1b2433" stroke="#33445a"/>')
            b.append(f'<rect x="{mx + 10}" y="{my + 10}" width="{mw * .48}" height="{mh - 20}" rx="3" fill="url(#grill)" stroke="#2a3748"/>')
            b.append(d.text("MS-01", mx + mw * .48 + 24, my + 26, 13, TXT, "x"))
            b.append(d.text("proxmox · 10G", mx + mw * .48 + 24, my + 42, 9.5, C, "r"))
            for k in range(3):
                b.append(f'<rect x="{mx + mw * .48 + 24 + k * 14}" y="{my + 52}" width="10" height="5" rx="1" fill="#05080d" stroke="#2a3748"/>')
            b.append(f'<circle cx="{mx + mw - 18}" cy="{my + 20}" r="7" fill="none" stroke="#3a4a60" stroke-width="1.5"/>')
            b.append(f'<circle class="pwr" cx="{mx + mw - 18}" cy="{my + 20}" r="3.2" fill="{G}"/>')
        elif kind == "vent":
            b.append(f'<rect x="{IX + 14}" y="{y + 9}" width="{IW - 28}" height="{h - 18}" fill="url(#vent)" opacity=".9"/>')
        labels.append((name, f"{n(u)}U · phase {phase}", phase, y + h / 2))
        y += h
    for name, sub, phase, ly in labels:
        col = Y if phase == 2 else G
        lx0 = 288 if ly < RT else RX + RW + 8
        b.append(f'<path d="M{lx0} {n(ly)}H392" stroke="{LINE2}" stroke-dasharray="2 3"/>'
                 f'<circle cx="392" cy="{n(ly)}" r="2.5" fill="{col}"/>')
        b.append(d.text(name, 402, ly - 2, 12.5, TXT, "b"))
        b.append(d.text(sub, 402, ly + 13, 10.5, col))

    # colonne de droite : MS-01, mémoire, services
    X, CWD = 592, 380
    b.append(f'<rect x="{X}" y="96" width="{CWD}" height="186" rx="12" fill="{BG2}" stroke="{LINE}"/>')
    b.append(d.text("Minisforum MS-01", X + 20, 126, 15, TXT, "b"))
    b.append(d.text("le cœur du lab", X + CWD - 20, 126, 11.5, DIM, "r", "end"))
    specs = [("CPU", "Intel i5-12600H"), ("RAM", "32 Go"), ("SSD", "NVMe 1 To · 3 emplacements"),
             ("Réseau", "2× SFP+ 10G · 2× 2.5G"), ("Conso", "25–35 W au repos"), ("OS", "Proxmox VE")]
    for k, (key, val) in enumerate(specs):
        yy = 156 + k * 21
        b.append(d.text(key, X + 20, yy, 12.5, C, "b"))
        b.append(d.text(val, X + 100, yy, 12.5, TXT))
    b.append(d.runs([("mémoire vive", TXT, "b"), (" · 32 Go", DIM, "r")], X, 312, 13))
    segs = [(12, C, "services ~12 Go"), (15, V, "labs ~15 Go"), (5, LINE2, "libre")]
    sx = X
    for k, (go, col, _) in enumerate(segs):
        sw_ = CWD * go / 32
        b.append(f'<rect class="seg" x="{n(sx)}" y="324" width="{n(sw_ - 3)}" height="12" rx="4" fill="{col}" style="animation-delay:{.3 + k * .35:.2f}s"/>')
        sx += sw_
    lx = X
    for go, col, label in segs:
        b.append(f'<circle cx="{lx + 4}" cy="{354}" r="4" fill="{col}"/>')
        b.append(d.text(label, lx + 14, 358, 11, MUT))
        lx += width(label, 11) + 34
    b.append(d.text("services prévus", X, 396, 13, TXT, "b"))
    svcs = [("Pi-hole", "bloque les pubs pour toute la maison", C), ("Homepage + Kuma", "accueil et alertes", C),
            ("Jellyfin & Immich", "vidéos et photos perso", C), ("Samba", "mini NAS pour partager", C),
            ("Dashboard Pronote", "hébergé sur le lab", C), ("Labs cyber", "Metasploitable · AD · OPNsense", V)]
    for k, (name, desc, col) in enumerate(svcs):
        yy = 422 + k * 21
        b.append(d.runs([("▸ ", col, "b"), (name, TXT, "b"), ("  " + desc, MUT, "r")], X, yy, 12))

    # chemin réseau
    SY = 560
    b.append(f'<rect x="30" y="{SY}" width="{W - 60}" height="66" rx="12" fill="{BG2}" stroke="{LINE}"/>')
    boxes = [(52, "Box internet", "aucun port ouvert", MUT), (405, "Switch MokerLink", "8 × 2.5G · VLAN", C),
             (758, "MS-01 · Proxmox", "services + labs", G)]
    for bx, name, sub, col in boxes:
        b.append(f'<rect x="{bx}" y="{SY + 11}" width="190" height="44" rx="9" fill="{BG1}" stroke="{col}" stroke-opacity=".6"/>')
        b.append(d.text(name, bx + 95, SY + 30, 12, TXT, "b", "middle"))
        b.append(d.text(sub, bx + 95, SY + 46, 10.5, DIM, "r", "middle"))
    links = [(242, 405, "1 câble", MUT, 1.4), (595, 758, "SFP+ 10G", C, 2.6)]
    for k, (x1, x2, label, col, sw_) in enumerate(links):
        b.append(f'<path id="l{k}" d="M{x1} {SY + 33}H{x2}" stroke="{col}" stroke-width="{sw_}" stroke-opacity=".75"/>')
        b.append(d.text(label, (x1 + x2) / 2, SY + 25, 10.5, col, "b", "middle"))
        for j, (dur, beg, rev) in enumerate(((1.6, 0, False), (1.6, .8, True))):
            kp = ' keyPoints="1;0" keyTimes="0;1" calcMode="linear"' if rev else ""
            b.append(f'<circle r="3" fill="{col if k else G}"><animateMotion dur="{dur}s" begin="{beg}s" repeatCount="indefinite"{kp}>'
                     f'<mpath href="#l{k}"/></animateMotion></circle>')
    b.append(d.text("accessible uniquement depuis la maison · plus tard : un routeur GL.iNet isolera le lab",
                    W / 2, 648, 11, DIM, "r", "middle"))
    d.add(*b)
    d.save(OUT / "homelab.svg")


# ─────────────────────────────────────────────────────────────── projets
PROJECTS = [
    ("portfolio", "Portfolio", "Skavyoy8/Skavyoy8.github.io", C,
     ["Mon site : homelab interactif, compétences,", "projets et parcours. Sans tracker ni cookie."],
     ["Next.js", "TypeScript", "Tailwind"]),
    ("interview", "Interview Lab", "Skavyoy8/interview-lab", V,
     ["Entraînement à l'oral d'entretien en anglais :", "reconnaissance vocale, examen blanc, fiches."],
     ["HTML", "JavaScript", "anglais"]),
    ("log", "Logarithmes", "Skavyoy8/maths-log-base-q", Y,
     ["Exercices : logarithme décimal et logarithme", "de base q. Maths bac pro · BTS CIEL."],
     ["HTML", "maths", "exercices"]),
    ("battery", "Piles & accus", "Skavyoy8/sciences-piles-accus", G,
     ["Fiche de révision et QCM : oxydoréduction,", "piles et accumulateurs. Terminale bac pro."],
     ["HTML", "sciences", "QCM"]),
]


def card_icon(kind, x, y, col):
    cx, cy = x + 26, y + 26
    if kind == "portfolio":
        return (f'<path d="M{cx - 6} {cy - 9}L{cx - 14} {cy}L{cx - 6} {cy + 9}M{cx + 6} {cy - 9}L{cx + 14} {cy}L{cx + 6} {cy + 9}" '
                f'fill="none" stroke="{col}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>'
                f'<rect class="blink" x="{cx - 2}" y="{cy - 8}" width="4" height="16" rx="1" fill="{col}"/>')
    if kind == "interview":
        return "".join(f'<rect class="eq" x="{cx - 14 + k * 6}" y="{cy - 11}" width="4" height="22" rx="2" fill="{col}" '
                       f'style="animation-duration:{.5 + (k * 7 % 5) / 10:.1f}s;animation-delay:-{k * .13:.2f}s"/>' for k in range(5))
    if kind == "log":
        return (f'<path d="M{cx - 15} {cy + 13}H{cx + 15}M{cx - 13} {cy + 15}V{cy - 15}" stroke="{DIM}" stroke-width="1.5"/>'
                f'<path class="draw" pathLength="100" d="M{cx - 11} {cy + 14}C{cx - 10} {cy - 2} {cx - 4} {cy - 8} {cx + 14} {cy - 11}" '
                f'fill="none" stroke="{col}" stroke-width="2.6" stroke-linecap="round"/>')
    # batterie qui se charge
    return (f'<rect x="{cx - 9}" y="{cy - 13}" width="18" height="27" rx="3" fill="none" stroke="{col}" stroke-width="2"/>'
            f'<rect x="{cx - 4}" y="{cy - 16}" width="8" height="3" rx="1" fill="{col}"/>'
            f'<rect class="charge" x="{cx - 6}" y="{cy - 10}" width="12" height="21" rx="1.5" fill="{col}" fill-opacity=".85"/>')


def cards():
    W, H = 490, 196
    for kind, title, slug, acc, desc, tags in PROJECTS:
        d = Doc(W, H, title, f"{title} ({slug}) : {' '.join(desc)} Tags : {', '.join(tags)}.")
        d.defs.append(f'<radialGradient id="gl" cx="1" cy="0" r="1"><stop offset="0" stop-color="{acc}" stop-opacity=".16"/>'
                      f'<stop offset="1" stop-color="{acc}" stop-opacity="0"/></radialGradient>'
                      f'<linearGradient id="tb" x1="0" x2="1"><stop offset="0" stop-color="{acc}" stop-opacity="0"/>'
                      f'<stop offset=".5" stop-color="{acc}"/><stop offset="1" stop-color="{acc}" stop-opacity="0"/></linearGradient>'
                      f'<clipPath id="cc"><rect width="{W}" height="{H}" rx="16"/></clipPath>')
        d.css.append(".blink{animation:blink 1.1s steps(1) infinite}@keyframes blink{50%{opacity:0}}"
                     ".eq{transform-box:fill-box;transform-origin:50% 50%;animation:eq 1s ease-in-out infinite alternate}"
                     "@keyframes eq{from{transform:scaleY(.25)}to{transform:scaleY(1)}}"
                     ".draw{stroke-dasharray:100;animation:draw 3.2s ease-in-out infinite}"
                     "@keyframes draw{0%{stroke-dashoffset:100}55%,85%{stroke-dashoffset:0}100%{stroke-dashoffset:-100}}"
                     ".charge{transform-box:fill-box;transform-origin:50% 100%;animation:charge 2.6s ease-in-out infinite}"
                     "@keyframes charge{0%{transform:scaleY(.1)}80%,100%{transform:scaleY(1)}}"
                     ".tb{animation:tb 4s ease-in-out infinite}@keyframes tb{0%{transform:translateX(-360px)}100%{transform:translateX(490px)}}")
        b = [f'<g clip-path="url(#cc)"><rect width="{W}" height="{H}" fill="{BG1}"/><rect width="{W}" height="{H}" fill="url(#gl)"/>'
             f'<rect class="tb" y="0" width="360" height="2" fill="url(#tb)"/></g>',
             f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="16" fill="none" stroke="{LINE}"/>',
             f'<rect x="24" y="24" width="52" height="52" rx="13" fill="{BG2}" stroke="{acc}" stroke-opacity=".45"/>',
             card_icon(kind, 24, 24, acc),
             d.text(title, 92, 48, 19, TXT, "x"),
             d.text(slug, 92, 69, 11.5, DIM)]
        svg, w = chip(d, 0, 0, "en ligne", G, 11, True, 24)
        b.append(f'<g transform="translate({n(W - 24 - w)} 26)">{svg}</g>')
        for k, line in enumerate(desc):
            b.append(d.text(line, 24, 112 + k * 21, 13, MUT))
        x = 24
        for t in tags:
            tw = width(t, 11) + 20
            b.append(f'<rect x="{n(x)}" y="152" width="{n(tw)}" height="22" rx="6" fill="{acc}" fill-opacity=".08" stroke="{acc}" stroke-opacity=".3"/>')
            b.append(d.text(t, x + 10, 167, 11, acc, "b"))
            x += tw + 8
        b.append(d.runs([("↗ ", acc, "b"), ("ouvrir", TXT, "b")], W - 24, 167, 12, "end"))
        d.add(*b)
        d.save(OUT / f"card-{kind}.svg")


# ─────────────────────────────────────────────────────────────── parcours
STEPS = [
    ("2026", "Je me lance", "GitHub · portfolio · TryHackMe", "done"),
    ("2026 – 2027", "Terminale Bac Pro CIEL", "Cyber · Réseaux · Électronique", "now"),
    ("juin 2027", "Bac Pro CIEL", "le diplôme en poche", "next"),
    ("sept. 2027", "BTS SIO option SISR", "en alternance · je cherche !", "goal"),
]


def timeline():
    W, H = 1000, 220
    d = Doc(W, H, "Parcours",
            "Parcours : 2026, premiers projets (GitHub, portfolio, TryHackMe) ; 2026–2027, Terminale Bac Pro CIEL (en cours) ; "
            "juin 2027, Bac Pro CIEL ; septembre 2027, BTS SIO option SISR en alternance (recherche en cours).")
    d.defs.append(f'<linearGradient id="done" gradientUnits="userSpaceOnUse" x1="140" x2="380"><stop offset="0" stop-color="{C}"/><stop offset="1" stop-color="{G}"/></linearGradient>')
    d.css.append(".flow{animation:flow 1.2s linear infinite}@keyframes flow{to{stroke-dashoffset:-16}}"
                 ".here{animation:here 1.6s ease-in-out infinite alternate}@keyframes here{from{transform:translateY(0)}to{transform:translateY(-5px)}}")
    xs = [140, 380, 620, 860]
    TY = 104
    b = [frame(d, W, H)]
    b.append(f'<path d="M{xs[0]} {TY}H{xs[1]}" stroke="url(#done)" stroke-width="4" stroke-linecap="round"/>')
    b.append(f'<path id="fut" d="M{xs[1]} {TY}H{xs[3]}" stroke="{LINE2}" stroke-width="3"/>')
    b.append(f'<path class="flow" d="M{xs[1]} {TY}H{xs[3]}" stroke="{C}" stroke-opacity=".55" stroke-width="3" stroke-dasharray="4 12"/>')
    for k in range(3):
        b.append(f'<circle r="3.5" fill="{G}"><animateMotion dur="4.5s" begin="{k * 1.5}s" repeatCount="indefinite"><mpath href="#fut"/></animateMotion>'
                 f'<animate attributeName="opacity" values="0;1;1;0" dur="4.5s" begin="{k * 1.5}s" repeatCount="indefinite"/></circle>')
    for x, (date, title, sub, state) in zip(xs, STEPS):
        col = {"done": C, "now": G, "next": MUT, "goal": Y}[state]
        if state == "now":
            b.append(f'<circle cx="{x}" cy="{TY}" r="12" fill="none" stroke="{G}" stroke-width="2">'
                     f'<animate attributeName="r" values="12;30" dur="2s" repeatCount="indefinite"/>'
                     f'<animate attributeName="stroke-opacity" values=".8;0" dur="2s" repeatCount="indefinite"/></circle>')
            svg, w = chip(d, 0, 0, "tu es ici", G, 11, False, 22)
            b.append(f'<g class="here"><g transform="translate({n(x - w / 2)} 30)">{svg}</g></g>')
        b.append(f'<circle cx="{x}" cy="{TY}" r="11" fill="{BG1}" stroke="{col}" stroke-width="2.5"/>')
        if state == "done":
            b.append(f'<path d="M{x - 5} {TY}l3.5 3.5 6.5-7" fill="none" stroke="{C}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>')
        else:
            b.append(f'<circle cx="{x}" cy="{TY}" r="4.5" fill="{col}"/>')
        b.append(d.text(date, x, 72, 12, col, "b", "middle"))
        b.append(d.text(title, x, 146, 14.5, TXT, "x", "middle"))
        b.append(d.text(sub, x, 168, 11.5, Y if state == "goal" else MUT, "r", "middle"))
    d.add(*b)
    d.save(OUT / "timeline.svg")


# ─────────────────────────────────────────────────────────────── pied de page
def footer():
    W, H = 1200, 170
    d = Doc(W, H, "Merci de ta visite", "Pied de page : un signal d'oscilloscope passe de l'analogique au numérique. Merci de ta visite !")
    d.defs.append(f'<linearGradient id="tr" x1="0" x2="1"><stop offset="0" stop-color="{C}"/><stop offset=".5" stop-color="{G}"/>'
                  f'<stop offset="1" stop-color="{V}"/></linearGradient>'
                  f'<pattern id="osc" width="40" height="20" patternUnits="userSpaceOnUse"><path d="M40 0H0V20" fill="none" stroke="#132131"/></pattern>'
                  f'<clipPath id="fc"><rect width="{W}" height="{H}" rx="18"/></clipPath>')
    d.css.append(".flow{animation:flow 2s linear infinite}@keyframes flow{to{stroke-dashoffset:-60}}"
                 ".blink{animation:blink 1.1s steps(1) infinite}@keyframes blink{50%{opacity:0}}")
    pts, mid, amp = [], 58, 22
    for x in range(40, 600, 4):
        pts.append(f"{x} {n(mid - amp * math.sin((x - 40) / 560 * 2 * math.pi * 3.5))}")
    sq = ""
    x, hi = 600, True
    while x < 1160:
        y = mid - amp if hi else mid + amp
        sq += f"V{y}H{min(x + 40, 1160)}"
        x += 40
        hi = not hi
    path = "M" + "L".join(pts) + f"L600 {mid}" + sq
    b = [f'<g clip-path="url(#fc)"><rect width="{W}" height="{H}" fill="{BG1}"/><rect y="10" width="{W}" height="100" fill="url(#osc)" opacity=".8"/></g>',
         f'<rect x=".5" y=".5" width="{W - 1}" height="{H - 1}" rx="18" fill="none" stroke="{LINE}"/>',
         f'<path id="tr" d="{path}" fill="none" stroke="url(#tr)" stroke-width="7" stroke-opacity=".12" stroke-linejoin="round"/>',
         f'<path d="{path}" fill="none" stroke="url(#tr)" stroke-width="2.2" stroke-linejoin="round"/>',
         f'<path class="flow" d="{path}" fill="none" stroke="#fff" stroke-opacity=".5" stroke-width="2.2" stroke-dasharray="6 54"/>',
         f'<circle r="4.5" fill="#fff"><animateMotion dur="6s" repeatCount="indefinite"><mpath href="#tr"/></animateMotion></circle>',
         d.text("analogique", 40, 102, 10.5, DIM),
         d.text("numérique", 1160, 102, 10.5, DIM, "r", "end"),
         d.text("Merci de ta visite !", W / 2, 130, 20, TXT, "x", "middle"),
         d.runs([("skavyoy@homelab", G, "b"), (":~$ ", MUT, "r"), ("exit", TXT, "r")], W / 2 - 6, 154, 13, "middle"),
         f'<rect class="blink" x="{n(W / 2 - 6 + width("skavyoy@homelab:~$ exit", 13) / 2 + 4)}" y="143" width="8" height="14" fill="{G}"/>']
    d.add(*b)
    d.save(OUT / "footer.svg")


if __name__ == "__main__":
    header()
    terminal()
    skills()
    homelab()
    cards()
    timeline()
    footer()
