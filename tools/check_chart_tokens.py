#!/usr/bin/env python3
"""Checks docs/assets/chart-tokens.css against the chart-token spec, and chart pages' wiring.

Usage:
  python3 tools/check_chart_tokens.py tokens
  python3 tools/check_chart_tokens.py page docs/water.html precip runoff wbal elev flow storm shed wuse
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSS = ROOT / "docs/assets/chart-tokens.css"

# (light, dark), copied from site-plan/specs/2026-10-14-chart-tokens-design.md via the Ramps table
TOKENS = {
    "season-winter": ("#476de7", "#638bff"), "season-spring": ("#698436", "#849f55"),
    "season-summer": ("#e748c1", "#e748c1"), "season-fall": ("#b09100", "#cbad42"),
    "water-rain": ("#638bff", "#8cacff"), "water-flow": ("#3353c1", "#638bff"),
    "water-body": ("#b4caff", "#233c94"), "land-permeable": ("#698436", "#849f55"),
    "land-ground": ("#7a7975", "#959490"), "emphasis": ("#d75509", "#f66d1e"),
    "emphasis-fill": ("#fdd9c4", "#4e1f03"), "alert": ("#ad1e26", "#ff8780"),
    "neutral-grid": ("#e0dfdd", "#474644"), "neutral-axis": ("#b1afac", "#605f5b"),
    "neutral-reference": ("#605f5b", "#b1afac"), "neutral-label": ("#2e2e2c", "#e0dfdd"),
    "neutral-label-muted": ("#605f5b", "#959490"), "neutral-surface": ("#f0f0ee", "#2e2e2c"),
    "categorical-1": ("#476de7", "#638bff"), "categorical-2": ("#516920", "#849f55"),
    "categorical-3": ("#e748c1", "#ca18a6"), "categorical-4": ("#907600", "#b09100"),
    "categorical-5": ("#008c81", "#2ea89c"), "categorical-6": ("#a877e5", "#8e5aca"),
    "categorical-7": ("#ef5c58", "#d2383b"),
}
# Chart-specific values allowed to stay raw (plan ruling R4)
ALLOW_RAW = {
    "--spo-hour-grid",
    "--flow-num-fg",  # white numbers on colored markers: contrast color, not a meaning (plan Task 4 Step 3)
    "--runoff-on-bar",  # dark text on hard/permeable bars: contrast color, readable in both modes
    "--shed-on-water",  # dark text on the translucent water fill: contrast color
}
RAW = re.compile(r"#[0-9a-fA-F]{3,8}\b|rgba?\(")

def blocks(css):
    light = re.search(r"^\.viz-root \{([^}]*)\}", css, re.M)
    media = re.search(r'@media \(prefers-color-scheme: dark\) \{\s*:root:where\(:not\(\[data-theme="light"\]\)\) \.viz-root \{([^}]*)\}', css)
    forced = re.search(r':root\[data-theme="dark"\] \.viz-root \{([^}]*)\}', css)
    return [m.group(1) if m else None for m in (light, media, forced)]

def decls(block):
    return dict(re.findall(r"(--[a-z0-9-]+):\s*([^;]+);", block or ""))

def check_tokens():
    fails = []
    if not CSS.exists():
        return [f"missing {CSS.relative_to(ROOT)}"]
    css = CSS.read_text()
    if "fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700" not in css:
        fails.append("JetBrains Mono import missing")
    light, media, forced = (decls(b) for b in blocks(css))
    if media != forced:
        fails.append("the two dark blocks differ")
    for name, (l, d) in TOKENS.items():
        prop = f"--chart-{name}"
        if light.get(prop, "").lower() != l: fails.append(f"{prop} light {light.get(prop)} ≠ {l}")
        if media.get(prop, "").lower() != d: fails.append(f"{prop} dark {media.get(prop)} ≠ {d}")
    for cls in ("chart-title", "chart-label", "chart-value", "chart-note"):
        if f".{cls}" not in css: fails.append(f"class .{cls} missing")
    return fails

def check_page(path, prefixes):
    fails = []
    html = (ROOT / path).read_text()
    if '<link rel="stylesheet" href="assets/chart-tokens.css">' not in html:
        fails.append("chart-tokens.css link missing")
    for prefix in prefixes:
        found = re.findall(rf"(--{prefix}-[a-z0-9-]+):\s*([^;]+);", html)
        if not found: fails.append(f"no --{prefix}-* declarations found")
        for prop, val in found:
            if prop in ALLOW_RAW: continue
            if RAW.search(val): fails.append(f"{prop} still raw: {val.strip()}")
    for cls in re.findall(r"\.([a-z0-9]+-[a-z0-9-]+) \{[^}]*font-size", html):
        if any(cls.startswith(p + "-") for p in prefixes) and re.search(rf"\.{cls} \{{[^}}]*fill:", html) \
           and not re.search(rf"\.{cls} \{{[^}}]*font: var\(--chart-font-", html):
            fails.append(f".{cls} is SVG text without a chart font role")
    # A `fill` presentation attribute loses to a CSS class rule that sets `fill`, so the color
    # never renders. Colored text on a classed element must pass `style:"fill:…"` instead.
    for cls, attr in re.findall(r'class:\s*"([a-z0-9-]+)"[^{}]*?[,{]\s*fill:\s*"([^"]+)"', html):
        if re.search(rf"\.{cls} \{{[^}}]*\bfill:", html):
            fails.append(f'.{cls} text sets fill:"{attr}" as an attribute; the class fill overrides it')
    return fails

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "tokens"
    fails = check_tokens() if mode == "tokens" else check_page(sys.argv[2], sys.argv[3:])
    for f in fails: print("FAIL", f)
    print("OK" if not fails else f"{len(fails)} failure(s)")
    sys.exit(1 if fails else 0)
