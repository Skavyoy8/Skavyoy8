#!/usr/bin/env python3
"""Génère une carte de stats GitHub façon btop, à partir de l'API GraphQL.

    GITHUB_TOKEN=... python3 scripts/stats.py dist/stats.svg

Lancé chaque jour par .github/workflows/profil.yml.
"""
import json
import os
import sys
import urllib.request
from collections import Counter
from datetime import date, datetime, timezone

from svgkit import BG1, BG2, C, DIM, G, LINE2, MUT, TXT, V, Y, Doc, n, width

LOGIN = os.environ.get("PROFILE_LOGIN", "Skavyoy8")
MOIS = ["janv.", "févr.", "mars", "avr.", "mai", "juin", "juil.", "août", "sept.", "oct.", "nov.", "déc."]
QUERY = """query($login: String!) {
  user(login: $login) {
    createdAt
    repositories(ownerAffiliations: OWNER, isFork: false, privacy: PUBLIC, first: 100) {
      totalCount
      nodes { stargazerCount pushedAt
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) { edges { size node { name color } } } }
    }
    contributionsCollection {
      totalCommitContributions totalPullRequestContributions
      contributionCalendar { totalContributions weeks { contributionDays { contributionCount date } } }
    }
  }
}"""


def fetch():
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode(),
        headers={"Authorization": f"bearer {os.environ['GITHUB_TOKEN']}", "User-Agent": "profile-stats"},
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        data = json.load(r)
    if data.get("errors"):
        sys.exit(f"Erreur GraphQL : {data['errors']}")
    return data["data"]["user"]


def compute(u):
    cal = u["contributionsCollection"]["contributionCalendar"]
    days = [(date.fromisoformat(d["date"]), d["contributionCount"]) for w in cal["weeks"] for d in w["contributionDays"]]
    weeks = [(date.fromisoformat(w["contributionDays"][0]["date"]), sum(d["contributionCount"] for d in w["contributionDays"]))
             for w in cal["weeks"]]
    longest = cur = 0
    for _, c in days:
        cur = cur + 1 if c else 0
        longest = max(longest, cur)
    current = 0
    for _, c in reversed(days[:-1] if days and days[-1][1] == 0 else days):
        if not c:
            break
        current += 1
    langs = Counter()
    colors = {}
    for repo in u["repositories"]["nodes"]:
        for e in repo["languages"]["edges"]:
            langs[e["node"]["name"]] += e["size"]
            colors[e["node"]["name"]] = e["node"]["color"] or MUT
    total = sum(langs.values()) or 1
    top = [(name, size / total, colors[name]) for name, size in langs.most_common(5)]
    pushed = max((r["pushedAt"] for r in u["repositories"]["nodes"] if r["pushedAt"]), default=None)
    created = datetime.fromisoformat(u["createdAt"].replace("Z", "+00:00"))
    return {
        "days": days, "weeks": weeks, "total": cal["totalContributions"],
        "commits": u["contributionsCollection"]["totalCommitContributions"],
        "prs": u["contributionsCollection"]["totalPullRequestContributions"],
        "repos": u["repositories"]["totalCount"],
        "active": sum(1 for _, c in days if c), "longest": longest, "current": current,
        "load": [sum(c for _, c in days[-k:]) for k in (7, 30, 90)],
        "uptime": (datetime.now(timezone.utc) - created).days,
        "pushed": datetime.fromisoformat(pushed.replace("Z", "+00:00")).date() if pushed else None,
        "langs": top,
    }


def box(d, x, y, w, h, num, title, right=""):
    """Boîte arrondie avec titre incrusté dans la bordure, comme btop."""
    out = [f'<rect x="{x + .5}" y="{y + .5}" width="{w - 1}" height="{h - 1}" rx="10" fill="{BG1}" stroke="{LINE2}"/>']
    label = f"┐{num}{title}┌"
    lw = width(label, 13)
    out.append(f'<rect x="{x + 18}" y="{y - 8}" width="{n(lw + 8)}" height="16" fill="{BG1}"/>')
    out.append(d.runs([("┐", LINE2, "r"), (num, Y, "b"), (title, TXT, "b"), ("┌", LINE2, "r")], x + 22, y + 4.5, 13))
    if right:
        rw = width(right, 11)
        out.append(f'<rect x="{n(x + w - 26 - rw)}" y="{y - 8}" width="{n(rw + 8)}" height="16" fill="{BG1}"/>')
        out.append(d.text(right, x + w - 22, y + 4, 11, DIM, "r", "end"))
    return "".join(out)


def render(s):
    W, H = 1000, 336
    d = Doc(W, H, f"Stats GitHub de {LOGIN}",
            f"{s['total']} contributions sur 12 mois, {s['commits']} commits, {s['repos']} dépôts publics, "
            f"{s['active']} jours actifs. Langages : " + ", ".join(f"{l} {p:.0%}" for l, p, _ in s["langs"]) + ".")
    gx, gy, gw, gh = 26, 36, 680, 112
    weeks = s["weeks"][-53:]
    colw = gw / len(weeks)
    rows = 18
    rh = gh / rows
    d.defs.append(f'<pattern id="cell" x="{gx}" y="{gy}" width="{n(colw)}" height="{n(rh)}" patternUnits="userSpaceOnUse">'
                  f'<rect width="{n(colw - 2.4)}" height="{n(rh - 1.8)}" rx="1" fill="{BG2}"/></pattern>')
    d.css.append(".col{transform-box:fill-box;transform-origin:50% 100%;animation:rise .9s cubic-bezier(.2,.8,.2,1) both}"
                 "@keyframes rise{from{transform:scaleY(0)}}"
                 ".sweep{animation:sweep 6s linear infinite}@keyframes sweep{from{transform:translateX(0)}to{transform:translateX(680px)}}")
    b = [box(d, 0, 10, W, 176, "¹", "activité", "12 derniers mois")]
    b.append(f'<rect x="{gx}" y="{gy}" width="{n(gw)}" height="{n(gh)}" fill="url(#cell)"/>')
    top = max((c for _, c in weeks), default=0) or 1
    palette = [G] * 6 + [C] * 6 + [V] * 6
    for i, (start, count) in enumerate(weeks):
        if not count:
            continue
        k = max(1, round(count / top * rows))
        cells = "".join(f'<rect x="{n(gx + i * colw)}" y="{n(gy + gh - (j + 1) * rh)}" width="{n(colw - 2.4)}" '
                        f'height="{n(rh - 1.8)}" rx="1" fill="{palette[j]}"/>' for j in range(k))
        b.append(f'<g class="col" style="animation-delay:{i * 12}ms">{cells}</g>')
    b.append(f'<rect class="sweep rm-hide" x="{gx}" y="{gy}" width="2" height="{gh}" fill="{C}" fill-opacity=".35"/>')
    seen = set()
    for i, (start, _) in enumerate(weeks):
        if start.month not in seen and start.day <= 7 and i < len(weeks) - 2:
            seen.add(start.month)
            b.append(d.text(MOIS[start.month - 1], gx + i * colw, gy + gh + 18, 10.5, DIM))
    # colonne de droite de la boîte activité
    rx = 740
    b.append(f'<path d="M{rx - 16} 34V168" stroke="{LINE2}" stroke-dasharray="2 4"/>')
    b.append(d.text(str(s["total"]), rx, 82, 44, G, "x"))
    b.append(d.text("contributions", rx + width(str(s["total"]), 44) + 10, 82, 13, MUT))
    b.append(d.text("load average", rx, 114, 11, DIM))
    la = s["load"]
    b.append(d.runs([(str(la[0]), C, "b"), (" · ", DIM, "r"), (str(la[1]), C, "b"), (" · ", DIM, "r"), (str(la[2]), C, "b"),
                     ("  7j/30j/90j", DIM, "r")], rx, 134, 13))
    b.append(d.runs([("série ", DIM, "r"), (f"{s['current']} j", Y, "b"), (" · record ", DIM, "r"), (f"{s['longest']} j", Y, "b")],
                    rx, 160, 13))

    # langages
    b.append(box(d, 0, 202, 490, 120, "²", "langages"))
    blocks = 22
    for k, (name, pct, col) in enumerate(s["langs"][:4]):
        y = 236 + k * 22
        b.append(d.text(name[:12], 22, y, 12.5, TXT))
        filled = max(1, round(pct * blocks))
        for j in range(blocks):
            b.append(f'<rect x="{134 + j * 12.5}" y="{y - 10}" width="9.5" height="11" rx="1.5" fill="{col if j < filled else BG2}"/>')
        b.append(d.text(f"{pct:.0%}".replace("%", " %"), 470, y, 12.5, MUT, "r", "end"))

    # système
    b.append(box(d, 510, 202, 490, 120, "³", "système"))
    pushed = s["pushed"].strftime("%d/%m/%Y") if s["pushed"] else "—"
    rows_ = [("uptime", f"{s['uptime']} jours", "dépôts", f"{s['repos']} publics"),
             ("commits", f"{s['commits']} (12 mois)", "pull req.", str(s["prs"])),
             ("jours actifs", str(s["active"]), "dernier push", pushed)]
    for k, (k1, v1, k2, v2) in enumerate(rows_):
        y = 240 + k * 26
        b.append(d.text(k1, 532, y, 12, DIM))
        b.append(d.text(v1, 636, y, 12.5, TXT, "b"))
        b.append(d.text(k2, 772, y, 12, DIM))
        b.append(d.text(v2, 876, y, 12.5, TXT, "b"))
    today = date.today().strftime("%d/%m/%Y")
    b.append(d.text(f"maj {today} · GitHub Actions", W - 4, H - 2, 10, DIM, "r", "end"))
    d.add(*b)
    return d


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "dist/stats.svg"
    render(compute(fetch())).save(out)


if __name__ == "__main__":
    main()
