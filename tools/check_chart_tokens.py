#!/usr/bin/env python3
"""Checks docs/assets/chart-tokens.css against the chart-token spec, and chart pages' wiring.

Usage:
  python3 tools/check_chart_tokens.py tokens
  python3 tools/check_chart_tokens.py page docs/water.html precip runoff wbal elev flow storm shed wuse
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSS = ROOT / "docs/assets/chart-tokens.css"
SPECIES = ROOT / "design-language/tokens/species.json"
CHART = ROOT / "design-language/tokens/chart.json"
RAMPS_JSON = ROOT / "design-language/tokens/ramps.json"

# Chart-specific values allowed to stay raw (plan ruling R4)
ALLOW_RAW = {
    "--spo-hour-grid",
    "--flow-num-fg",  # white numbers on colored markers: contrast color, not a meaning (plan Task 4 Step 3)
    "--runoff-on-bar",  # dark text on hard/permeable bars: contrast color, readable in both modes
    "--shed-on-water",  # dark text on the translucent water fill: contrast color
}
RAW = re.compile(r"#[0-9a-fA-F]{3,8}\b|rgba?\(")
# Words a token-backed value may contain once var() references are removed. Any other word is a
# color function (hsl, oklch, …) or a named color.
VALUE_WORDS = {"color-mix", "in", "srgb", "srgb-linear", "oklab", "transparent", "currentcolor"}
# Page-level variables that belong to page chrome, not charts. --surface-1 and --page stay allowed:
# value halos and separators must match the panel behind them.
PAGE_PAINT = re.compile(r"\b(fill|stroke)[\"']?\s*:\s*[\"']?var\(--(grid|baseline|accent|text-[a-z]+)\)")
SVG_TEXT = re.compile(r"\b(?:svgEl|el)\(\s*[\"']text[\"']\s*,\s*\{([^}]*)\}")

def is_raw(val):
    rest = re.sub(r"var\(--[a-z0-9-]+\)", "", val)
    return bool(RAW.search(rest)) or any(w.lower() not in VALUE_WORDS for w in re.findall(r"[a-zA-Z][a-zA-Z-]*", rest))

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
    fails += check_collection_tokens(css, CHART, "--chart-")
    for cls in ("chart-title", "chart-label", "chart-value", "chart-note"):
        if f".{cls}" not in css: fails.append(f"class .{cls} missing")
    fails += check_species_tokens(css)
    return fails

def check_collection_tokens(css, path, prefix):
    """Each token in a collection file (Ramps steps per mode) must equal its CSS variable,
    <prefix><name with / as ->, in the light block and both dark blocks."""
    ramps, tokens = json.loads(RAMPS_JSON.read_text()), json.loads(Path(path).read_text())["tokens"]
    light, media, forced = (decls(b) for b in blocks(css))
    fails = []
    for token, steps in tokens.items():
        prop = prefix + token.replace("/", "-")
        unknown = [steps.get(m) for m in ("light", "dark") if steps.get(m) not in ramps]
        if unknown: fails.append(f"{prop}: unknown Ramps step {', '.join(map(str, unknown))}"); continue
        want_l, want_d = ramps[steps["light"]], ramps[steps["dark"]]
        if light.get(prop, "").lower() != want_l: fails.append(f"{prop} light {light.get(prop)} ≠ {want_l}")
        if media.get(prop, "").lower() != want_d: fails.append(f"{prop} dark {media.get(prop)} ≠ {want_d}")
        if forced.get(prop, "").lower() != want_d: fails.append(f"{prop} forced dark {forced.get(prop)} ≠ {want_d}")
    return fails

def check_species_tokens(css):
    """--species-* values in all three blocks must equal species.json resolved through ramps.json."""
    return check_collection_tokens(css, SPECIES, "--species-")

def check_page(path, prefixes):
    return check_html((ROOT / path).read_text(), prefixes)

def check_html(html, prefixes):
    fails = []
    if '<link rel="stylesheet" href="assets/chart-tokens.css">' not in html:
        fails.append("chart-tokens.css link missing")
    for prefix in prefixes:
        found = re.findall(rf"(--{prefix}-[a-z0-9-]+):\s*([^;]+);", html)
        if not found: fails.append(f"no --{prefix}-* declarations found")
        for prop, val in found:
            if prop in ALLOW_RAW: continue
            if is_raw(val): fails.append(f"{prop} still raw: {val.strip()}")
    # A rule that sets both `fill` and a text property styles SVG text, prefixed or not.
    for sel, body in re.findall(r"([^{}]+)\{([^{}]*)\}", html):
        if re.search(r"\bfill:", body) and re.search(r"\b(font-size|font-weight|text-anchor)\s*:", body) \
           and "font: var(--chart-font-" not in body:
            fails.append(f"{sel.strip()} is SVG text without a chart font role")
    line = lambda m: html.count("\n", 0, m.start()) + 1
    for m in SVG_TEXT.finditer(html):
        if not re.search(r"\bclass\s*:", m.group(1)):
            fails.append(f"line {line(m)}: SVG text without a class")
    for m in PAGE_PAINT.finditer(html):
        fails.append(f"line {line(m)}: chart {m.group(1)} uses page variable --{m.group(2)}")
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
