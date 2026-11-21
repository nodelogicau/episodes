#!/usr/bin/env python3
"""Redraw the proof figure in docs/index.html from the episodes binary's own
output on docs/example.

    python3 docs/timeline-figure.py

Runs `episodes list --json`, `episodes thread --json` and `episodes show
--json` against the example workspace and rewrites the SVG between the
TIMELINE-FIGURE markers in index.html. Nothing outside the markers is
touched. With the same binary the result is byte-identical; with a newer one
the version written into the figure changes, which is the signal to re-read
the caption.

One lane per standpoint, one column per day from the Monday of the first
episode's week to the last day anything was observed. A container is drawn
around its children; a reference episode is a trace (dashed); an act is
drawn in the accent; a link is an arrow; a source that has gone is a badge
on the trace's lane on the day it was observed. Ids are never drawn.
"""

import datetime as dt
import json
import os
import re
import subprocess
import sys
from html import escape
from zoneinfo import ZoneInfo

HERE = os.path.dirname(os.path.abspath(__file__))
WORKSPACE = os.path.join(HERE, "example")
PAGE = os.path.join(HERE, "index.html")
BEGIN = "<!-- TIMELINE-FIGURE:BEGIN -->"
END = "<!-- TIMELINE-FIGURE:END -->"

LABEL_W = 96      # lane-label column
EMPTY_DAY_W = 44  # a day with nothing in it
SLOT_W = 180      # one group (an episode, a container, a badge)
DAY_PAD = 10
TOP = 48          # below the day headers
LANE_H = 80
BOX_W = 150
BOX_H = 62
CHARS = 20        # characters per line at the small size in a box


def run(*args):
    out = subprocess.run(
        ["episodes", "--workspace", WORKSPACE, *args, "--json"],
        check=True, capture_output=True, text=True,
    ).stdout
    return json.loads(out)


def parse_occurred(value):
    """An RFC 9557 value: RFC 3339 with an optional [zone] suffix."""
    m = re.match(r"^([^\[]+)(?:\[([^\]]+)\])?$", value)
    stamp, zone = m.group(1), m.group(2)
    t = dt.datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    return t.astimezone(ZoneInfo(zone)) if zone else t


def lane_name(standpoint):
    seg = standpoint.rstrip("/").rsplit("/", 1)[-1]
    return seg.capitalize() if "/people/" in standpoint else seg


def wrap(text, width=CHARS, lines=2):
    words, out, cur = text.split(), [], ""
    for w in words:
        if len(cur) + len(w) + (1 if cur else 0) <= width:
            cur = f"{cur} {w}" if cur else w
        else:
            out.append(cur)
            cur = w
    if cur:
        out.append(cur)
    if len(out) > lines:
        out = out[:lines]
        out[-1] = out[-1][: width - 1].rstrip() + "…"
    return out


def hhmm(t):
    return t.strftime("%H:%M")


def main():
    version = run("version")["version"]
    listed = run("list")["episodes"]
    full = {e["id"]: run("show", e["id"])["episode"] for e in listed}

    # Groups: a container with its children, or a standalone episode.
    children = {}
    for e in listed:
        if e.get("container"):
            children.setdefault(e["container"], []).append(e)
    for cid in children:
        children[cid] = run("thread", cid)["children"]

    zone = None
    for e in listed:
        z = re.search(r"\[([^\]]+)\]", e["occurred"]["start"])
        if z:
            zone = ZoneInfo(z.group(1))
            break

    groups = []  # (start, day, kind, payload)
    for e in listed:
        if e.get("container"):
            continue
        start = parse_occurred(e["occurred"]["start"])
        if e["id"] in children:
            groups.append((start, start.date(), "container", e))
        else:
            groups.append((start, start.date(), "episode", e))
        status = full[e["id"]].get("source_status")
        if status and status.get("state") == "gone":
            seen = dt.datetime.fromisoformat(
                status["verified"].replace("Z", "+00:00")).astimezone(zone)
            groups.append((seen, seen.date(), "gone", e))
    groups.sort(key=lambda g: (g[0], g[2]))

    # Lanes, in order of first appearance.
    lanes = []
    for _, _, kind, e in groups:
        members = children.get(e["id"], []) if kind == "container" else [e]
        for m in members:
            if m["standpoint"] not in lanes:
                lanes.append(m["standpoint"])
    lane_y = {s: TOP + i * LANE_H for i, s in enumerate(lanes)}

    # Columns: Monday of the first week to the last day with a group.
    first = groups[0][1] - dt.timedelta(days=groups[0][1].weekday())
    last = max(g[1] for g in groups)
    days = [first + dt.timedelta(days=i) for i in range((last - first).days + 1)]
    per_day = {d: [g for g in groups if g[1] == d] for d in days}
    day_x, x = {}, LABEL_W
    for d in days:
        n = len(per_day[d])
        w = EMPTY_DAY_W if n == 0 else DAY_PAD * 2 + SLOT_W * n
        day_x[d] = (x, w)
        x += w
    width = x + 6
    lanes_bottom = TOP + LANE_H * len(lanes)
    height = lanes_bottom + 108

    svg = []
    add = svg.append
    add(f'<svg class="min720" viewBox="0 0 {width} {height}" role="img" '
        f'aria-labelledby="proof-title proof-desc">')
    add('  <title id="proof-title">A week of episodes, as the binary lists them</title>')
    add('  <desc id="proof-desc">One lane for each standpoint and one column for '
        'each day. A dashed box is a trace of something that lives elsewhere; a solid '
        'box holds content that has no other home; an accented box is an act the '
        'person attested; a conversation is drawn around its turns. An arrow is a link '
        'from one episode to another. A red badge marks a source that has gone, on the '
        'day it was observed; the trace remains.</desc>')
    add('  <defs>')
    add('    <marker id="ahp" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" '
        'markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" '
        'class="head"/></marker>')
    add('  </defs>')
    add(f'  <text x="8" y="24" class="lbl">'
        f'{escape(days[0].strftime("%B %Y"))}</text>')
    for d in days:
        dx, dw = day_x[d]
        label = d.strftime("%a") if dw == EMPTY_DAY_W else d.strftime("%a %-d")
        add(f'  <text x="{dx + dw / 2:.0f}" y="24" text-anchor="middle" class="lbl" '
            f'font-weight="600">{label}</text>')
        add(f'  <line x1="{dx}" y1="34" x2="{dx}" y2="{lanes_bottom}" class="grid"/>')
    add(f'  <line x1="{width - 6}" y1="34" x2="{width - 6}" y2="{lanes_bottom}" class="grid"/>')
    for s in lanes:
        y = lane_y[s]
        add(f'  <line x1="0" y1="{y}" x2="{width - 6}" y2="{y}" class="grid"/>')
        add(f'  <text x="8" y="{y + LANE_H / 2 + 5:.0f}" class="small" font-weight="600">'
            f'{escape(lane_name(s))}<title>{escape(s)}</title></text>')
    add(f'  <line x1="0" y1="{lanes_bottom}" x2="{width - 6}" y2="{lanes_bottom}" class="grid"/>')

    boxes = {}  # id -> (x, y) of the box's top-left

    def box(e, x, y, cls, first_line):
        start = parse_occurred(e["occurred"]["start"])
        lines = wrap(e["label"]) if e.get("label") else wrap(
            "“" + e.get("text", "") + "”")
        tip = [f'{e["kind"]}', f'standpoint {e["standpoint"]}',
               f'occurred {e["occurred"]["start"]}'
               + (f' to {e["occurred"]["end"]}' if e["occurred"].get("end") else "")
               + f' ({e["occurred"]["basis"]})',
               f'content: {e["mode"]}']
        if e.get("label"):
            tip.append(f'label: {e["label"]}')
        if e.get("text"):
            tip.append(f'text: {e["text"]}')
        if e.get("ordinal"):
            tip.append(f'ordinal {e["ordinal"]}')
        add(f'  <g><title>{escape(" · ".join(tip))}</title>')
        add(f'    <rect x="{x}" y="{y}" width="{BOX_W}" height="{BOX_H}" rx="8" class="{cls}"/>')
        add(f'    <text x="{x + 10}" y="{y + 19}" class="small" font-weight="600">'
            f'{escape(first_line(start))}</text>')
        for i, line in enumerate(lines):
            add(f'    <text x="{x + 10}" y="{y + 37 + i * 16}" class="small lbl">'
                f'{escape(line)}</text>')
        add('  </g>')
        boxes[e["id"]] = (x, y)

    for d in days:
        dx, _ = day_x[d]
        for i, (start, _, kind, e) in enumerate(per_day[d]):
            gx = dx + DAY_PAD + i * SLOT_W
            if kind == "episode":
                y = lane_y[e["standpoint"]] + (LANE_H - BOX_H) / 2
                if e["mode"] == "ref":
                    box(e, gx, y, "trace", lambda t, e=e: f'{hhmm(t)} · {e["kind"]}')
                elif e["mode"] == "attested":
                    end = parse_occurred(e["occurred"]["end"]) if e["occurred"].get("end") else None
                    box(e, gx, y, "box-accent",
                        lambda t, end=end: f'{hhmm(t)}' + (f'–{hhmm(end)}' if end else '')
                        + ' · an act')
                else:
                    box(e, gx, y, "box", lambda t, e=e: f'{hhmm(t)} · {e["kind"]}')
            elif kind == "container":
                kids = children[e["id"]]
                ys = [lane_y[k["standpoint"]] for k in kids]
                top, bottom = min(ys) + 4, max(ys) + LANE_H - 4
                add(f'  <g><title>{escape(e["kind"])} · standpoint {escape(e["standpoint"])} · '
                    f'occurred {escape(e["occurred"]["start"])} · {len(kids)} turns, in order</title>')
                add(f'    <rect x="{gx - 6}" y="{top}" width="{BOX_W + 12}" '
                    f'height="{bottom - top}" rx="12" class="container"/>')
                add(f'    <text x="{gx + BOX_W + 2}" y="{top - 6}" text-anchor="end" '
                    f'class="lbl small">{escape(e["kind"])} · {len(kids)} turns</text>')
                add('  </g>')
                for k in kids:
                    k = dict(k, label=None)
                    y = lane_y[k["standpoint"]] + 6
                    box(k, gx, y, "box",
                        lambda t, k=k: f'{hhmm(t)} · turn {k["ordinal"]}')
            elif kind == "gone":
                y = lane_y[e["standpoint"]] + (LANE_H - 44) / 2
                tx, ty = boxes[e["id"]]
                add(f'  <path d="M{tx + BOX_W},{ty + BOX_H / 2:.0f} L{gx},{y + 22:.0f}" '
                    f'class="edge edge-dash"/>')
                add(f'  <g><title>source_status: gone · verified {escape(start.isoformat())}'
                    f' · the episode keeps its place</title>')
                add(f'    <rect x="{gx}" y="{y}" width="{BOX_W}" height="44" rx="8" class="box-stale"/>')
                add(f'    <text x="{gx + 10}" y="{y + 18}" class="stale-t small">'
                    f'{hhmm(start)} · source gone</text>')
                add(f'    <text x="{gx + 10}" y="{y + 35}" class="small lbl">the trace remains</text>')
                add('  </g>')

    # Links between episodes, drawn last so they sit on top.
    for eid, ep in full.items():
        for link in ep.get("links") or []:
            target = link.get("href")
            if eid in boxes and target in boxes:
                (ax, ay), (bx, by) = boxes[eid], boxes[target]
                y1, y2 = ay + BOX_H / 2, by + BOX_H / 2
                add(f'  <path d="M{ax + BOX_W},{y1:.0f} L{bx - 4},{y2:.0f}" class="edge" '
                    f'marker-end="url(#ahp)"/>')
                add(f'  <text x="{(ax + BOX_W + bx) / 2:.0f}" y="{min(y1, y2) - 6:.0f}" '
                    f'text-anchor="middle" class="lbl small">{escape(link["rel"])}</text>')

    ly = lanes_bottom + 28
    add(f'  <rect x="{LABEL_W}" y="{ly - 11}" width="22" height="14" rx="3" class="trace"/>')
    add(f'  <text x="{LABEL_W + 30}" y="{ly}" class="small">a trace: the content lives elsewhere</text>')
    add(f'  <rect x="{LABEL_W + 330}" y="{ly - 11}" width="22" height="14" rx="3" class="box"/>')
    add(f'  <text x="{LABEL_W + 360}" y="{ly}" class="small">inline: this is its only home</text>')
    ly += 26
    add(f'  <rect x="{LABEL_W}" y="{ly - 11}" width="22" height="14" rx="3" class="box-accent"/>')
    add(f'  <text x="{LABEL_W + 30}" y="{ly}" class="small">an act the person attested</text>')
    add(f'  <rect x="{LABEL_W + 330}" y="{ly - 11}" width="22" height="14" rx="3" class="container"/>')
    add(f'  <text x="{LABEL_W + 360}" y="{ly}" class="small">a container, its turns in order</text>')
    add(f'  <text x="{width - 6}" y="{height - 8}" text-anchor="end" class="small lbl">'
        f'{len(listed)} episodes · drawn by episodes {escape(version)}</text>')
    add('</svg>')

    page = open(PAGE, encoding="utf-8").read()
    i, j = page.find(BEGIN), page.find(END)
    if i < 0 or j < i:
        sys.exit(f"{PAGE}: TIMELINE-FIGURE markers not found")
    new = page[: i + len(BEGIN)] + "\n" + "\n".join(svg) + "\n" + page[j:]
    if new != page:
        with open(PAGE, "w", encoding="utf-8") as f:
            f.write(new)
    print(f"timeline figure: {len(listed)} episodes, {len(lanes)} lanes, "
          f"{len(days)} days, episodes {version}")


if __name__ == "__main__":
    main()
