#!/usr/bin/env python3
"""Checks a token palette for color-vision-deficiency separation and edge contrast.

Usage:
  python3 tools/palette_check.py design-language/tokens/ramps.json design-language/tokens/species.json
"""
import itertools, json, sys

# Machado, Oliveira & Fernandes (2009), severity 1.0, applied to linear RGB
MACHADO = {
    "protan": ((0.152286, 1.052583, -0.204868), (0.114503, 0.786281, 0.099216), (-0.003882, -0.048116, 1.051998)),
    "deutan": ((0.367322, 0.860646, -0.227968), (0.280085, 0.672501, 0.047413), (-0.011820, 0.042940, 0.968881)),
    "tritan": ((1.255528, -0.076749, -0.178779), (-0.078411, 0.930809, 0.147602), (0.004733, 0.691367, 0.303900)),
}
KINDS = ("normal", "deutan", "protan", "tritan")

def hex_to_rgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))

def _lin(c): return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
def _gam(c):
    c = min(max(c, 0.0), 1.0)
    return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055

def simulate(rgb, kind):
    if kind == "normal": return rgb
    lin = [_lin(c) for c in rgb]
    return tuple(_gam(sum(m * v for m, v in zip(row, lin))) for row in MACHADO[kind])

def _lab(rgb):
    r, g, b = (_lin(c) for c in rgb)
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    y = 0.2126 * r + 0.7152 * g + 0.0722 * b
    z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883
    f = lambda t: t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116
    fx, fy, fz = f(x), f(y), f(z)
    return 116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)

def delta_e(a, b, kind="normal"):
    la, lb = _lab(simulate(hex_to_rgb(a), kind)), _lab(simulate(hex_to_rgb(b), kind))
    return sum((p - q) ** 2 for p, q in zip(la, lb)) ** 0.5

def contrast(a, b):
    lum = lambda h: sum(w * _lin(c) for w, c in zip((0.2126, 0.7152, 0.0722), hex_to_rgb(h)))
    hi, lo = sorted((lum(a), lum(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)

def check(ramps, palette):
    fails, c = [], palette["checks"]
    for mode in ("light", "dark"):
        hexes = {}
        for name, steps in palette["tokens"].items():
            step = steps.get(mode)
            if step is None: fails.append(f"{mode} {name}: no {mode} value")
            elif step not in ramps: fails.append(f"{mode} {name}: unknown Ramps step {step}")
            else: hexes[name] = ramps[step]
        named = {n for g in c["distinct"] + c["adjacent"] for n in g} | set(c["edges"])
        if mode == "light":
            fails += [f"checks name unknown token {n}" for n in sorted(named - set(palette["tokens"]))]
        pairs = [p for g in c["distinct"] for p in itertools.combinations(g, 2)]
        pairs += [p for g in c["adjacent"] for p in zip(g, g[1:])]
        for a, b in pairs:
            if a not in hexes or b not in hexes: continue  # already reported above
            for kind in KINDS:
                d = delta_e(hexes[a], hexes[b], kind)
                if d < c["floor_de"]: fails.append(f"{mode} {a} vs {b}: ΔE {d:.1f} under {kind}")
        for e in c["edges"]:
            if e not in hexes: continue
            for s in c["surfaces"].get(mode, []):
                r = contrast(hexes[e], s)
                if r < c["contrast_min"]: fails.append(f"{mode} {e} on {s}: contrast {r:.2f}")
    return fails

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__.strip(), file=sys.stderr)
        sys.exit(2)
    ramps, palette = (json.load(open(p)) for p in sys.argv[1:3])
    fails = check(ramps, palette)
    for f in fails: print("FAIL", f)
    print("OK" if not fails else f"{len(fails)} failure(s)")
    sys.exit(1 if fails else 0)
