#!/usr/bin/env python3
"""Extrait les contours de JetBrains Mono vers glyphs.json (à relancer seulement pour ajouter des caractères).

    pip install fonttools
    python3 scripts/extract_glyphs.py /chemin/vers/JetBrainsMono-{Regular,Bold,ExtraBold}.ttf

JetBrains Mono est sous licence SIL Open Font License 1.1 (https://github.com/JetBrains/JetBrainsMono).
"""
import json
import sys
from pathlib import Path

from fontTools.pens.basePen import BasePen
from fontTools.ttLib import TTFont

CHARS = (
    "".join(chr(c) for c in range(32, 127))
    + "àâäçéèêëîïôöùûüÿœæÀÂÄÇÉÈÊËÎÏÔÖÙÛÜŒÆ"
    + "·—–’‘“”«»…″′°×÷±≈≤≥→←↑↓↗↘⇄▸▶◂●○◆◇■□▪▫█▌▐▀▄░▒▓"
    + "┌┐└┘─│├┤┬┴┼╭╮╯╰━┃┏┓┗┛╌╎¹²³⁴⁵⁶€✓✗"
)


class CmdPen(BasePen):
    def __init__(self, glyphset):
        super().__init__(glyphset)
        self.out = []

    def _moveTo(self, p):
        self.out.append(f"M{round(p[0])} {round(p[1])}")

    def _lineTo(self, p):
        self.out.append(f"L{round(p[0])} {round(p[1])}")

    def _qCurveToOne(self, p1, p2):
        self.out.append(f"Q{round(p1[0])} {round(p1[1])} {round(p2[0])} {round(p2[1])}")

    def _curveToOne(self, p1, p2, p3):
        self.out.append("C" + " ".join(f"{round(x)} {round(y)}" for x, y in (p1, p2, p3)))

    def _closePath(self):
        self.out.append("Z")


def extract(path):
    font = TTFont(path)
    cmap, gs = font.getBestCmap(), font.getGlyphSet()
    out = {}
    for ch in CHARS:
        name = cmap.get(ord(ch))
        if name is None:
            print(f"absent : {ch!r} dans {Path(path).name}", file=sys.stderr)
            continue
        pen = CmdPen(gs)
        gs[name].draw(pen)
        out[ch] = "".join(pen.out)
    return font, out


def main():
    paths = sys.argv[1:]
    if len(paths) != 3:
        sys.exit("usage : extract_glyphs.py Regular.ttf Bold.ttf ExtraBold.ttf")
    data = {}
    for key, path in zip("rbx", paths):
        font, data[key] = extract(path)
    data["upm"] = font["head"].unitsPerEm
    data["adv"] = font["hmtx"]["space"][0]
    dest = Path(__file__).resolve().parent / "glyphs.json"
    dest.write_text(json.dumps(data, ensure_ascii=False, separators=(",", ":")), encoding="utf-8")
    print(f"{dest} : {dest.stat().st_size // 1024} Ko")


if __name__ == "__main__":
    main()
