"""Boîte à outils SVG partagée par build_assets.py et stats.py.

Le texte est dessiné avec les contours de JetBrains Mono (glyphs.json) :
le rendu est identique sur tous les navigateurs, sans dépendre des polices installées.
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
_GL = json.loads((HERE / "glyphs.json").read_text(encoding="utf-8"))
ICONS = json.loads((HERE / "icons.json").read_text(encoding="utf-8"))
UPM, ADV = _GL["upm"], _GL["adv"]

# Palette commune
BG0, BG1, BG2 = "#05080d", "#0a0f16", "#101823"
LINE, LINE2 = "#1c2735", "#2a384b"
TXT, MUT, DIM = "#e6edf3", "#8b98a9", "#566476"
G, C, V, Y, R, B = "#3dff9a", "#2de2e6", "#9d7bff", "#ffcc66", "#ff5c7a", "#4da3ff"

REDUCED = "@media (prefers-reduced-motion:reduce){*{animation:none!important}.rm-hide{display:none}}"


def n(x):
    """Nombre compact pour les attributs SVG."""
    s = f"{x:.2f}".rstrip("0").rstrip(".")
    return "0" if s in ("-0", "") else s


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")


def cw(size):
    """Largeur d'un caractère (police à chasse fixe)."""
    return size * ADV / UPM


def width(s, size):
    return len(s) * cw(size)


class Doc:
    def __init__(self, w, h, title, desc=""):
        self.w, self.h, self.title, self.desc = w, h, title, desc
        self.glyphs = {}
        self.defs, self.css, self.body = [], [], []

    def add(self, *parts):
        self.body.extend(parts)

    def _gid(self, wt, ch):
        gid = f"{wt}{ord(ch):x}"
        if gid not in self.glyphs:
            d = _GL[wt].get(ch)
            if d is None:
                raise KeyError(f"glyphe absent de glyphs.json : {ch!r}")
            self.glyphs[gid] = d
        return gid

    def text(self, s, x, y, size, fill=TXT, wt="r", anchor="start", cls=None, opacity=None):
        """Texte en <use> de glyphes ; (x, y) = début de la ligne de base."""
        if anchor == "middle":
            x -= width(s, size) / 2
        elif anchor == "end":
            x -= width(s, size)
        k = size / UPM
        uses = "".join(
            f'<use href="#{self._gid(wt, ch)}" x="{i * ADV}"/>' for i, ch in enumerate(s) if ch != " "
        )
        a = f' class="{cls}"' if cls else ""
        o = f' opacity="{opacity}"' if opacity is not None else ""
        return f'<g{a}{o} fill="{fill}" transform="translate({n(x)} {n(y)}) scale({k:g} {-k:g})">{uses}</g>'

    def runs(self, parts, x, y, size, anchor="start", cls=None):
        """Plusieurs morceaux colorés sur une même ligne : [(texte, couleur, graisse), ...]."""
        total = sum(width(p[0], size) for p in parts)
        if anchor == "middle":
            x -= total / 2
        elif anchor == "end":
            x -= total
        out = []
        for p in parts:
            t, fill, wt = p if len(p) == 3 else (p[0], p[1], "r")
            if t.strip():
                out.append(self.text(t, x, y, size, fill, wt))
            x += width(t, size)
        a = f' class="{cls}"' if cls else ""
        return f"<g{a}>{''.join(out)}</g>"

    def path_text(self, s, x, y, size, wt="x"):
        """Texte converti en un seul tracé (utile pour un dégradé qui traverse tout le mot)."""
        k = size / UPM
        out = []
        for i, ch in enumerate(s):
            if ch == " ":
                continue
            ox = i * ADV
            for tok in re.finditer(r"([MLQCZ])([^MLQCZ]*)", _GL[wt][ch]):
                cmd, nums = tok.group(1), [int(v) for v in tok.group(2).split()]
                pts = " ".join(
                    f"{n(x + (nums[j] + ox) * k)} {n(y - nums[j + 1] * k)}" for j in range(0, len(nums), 2)
                )
                out.append(cmd + pts)
        return "".join(out)

    def icon(self, slug, cx, cy, size, fill):
        """Icône simple-icons (viewBox 24) centrée en (cx, cy)."""
        k = size / 24
        return (
            f'<path fill="{fill}" transform="translate({n(cx - size / 2)} {n(cy - size / 2)}) scale({k:g})" '
            f'd="{ICONS[slug]}"/>'
        )

    def render(self):
        glyphs = "".join(f'<path id="{gid}" d="{d}"/>' for gid, d in self.glyphs.items())
        css = "".join(self.css) + REDUCED
        return (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
            f'viewBox="0 0 {self.w} {self.h}" role="img" aria-labelledby="t d">'
            f'<title id="t">{esc(self.title)}</title><desc id="d">{esc(self.desc)}</desc>'
            f"<style>{css}</style><defs>{glyphs}{''.join(self.defs)}</defs>"
            f"{''.join(self.body)}</svg>\n"
        )

    def save(self, path):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        Path(path).write_text(self.render(), encoding="utf-8")
        print(f"{path} ({Path(path).stat().st_size // 1024} Ko)")


def keyframes_show(name, start, cycle, end=None):
    """Élément invisible jusqu'à `start` secondes (puis jusqu'à `end`), sur un cycle de `cycle` secondes."""
    a = start / cycle * 100
    if end is None:
        return f"@keyframes {name}{{0%,{a:.2f}%{{opacity:0}}{a + 0.01:.2f}%,100%{{opacity:1}}}}"
    b = end / cycle * 100
    return f"@keyframes {name}{{0%,{a:.2f}%{{opacity:0}}{a + 0.01:.2f}%,{b:.2f}%{{opacity:1}}{b + 0.01:.2f}%,100%{{opacity:0}}}}"


def chip(doc, x, y, label, color, size=12.5, dot=True, h=26):
    """Pastille arrondie ; renvoie (svg, largeur)."""
    pad = 12
    tw = width(label, size)
    w = tw + pad * 2 + (14 if dot else 0)
    parts = [
        f'<rect x="{n(x)}" y="{n(y)}" width="{n(w)}" height="{h}" rx="{h / 2}" fill="{color}" fill-opacity=".08" '
        f'stroke="{color}" stroke-opacity=".45"/>'
    ]
    tx = x + pad
    if dot:
        parts.append(f'<circle cx="{n(tx + 3)}" cy="{n(y + h / 2)}" r="3" fill="{color}"/>')
        tx += 14
    parts.append(doc.text(label, tx, y + h / 2 + size * 0.36, size, color, "b"))
    return "".join(parts), w
