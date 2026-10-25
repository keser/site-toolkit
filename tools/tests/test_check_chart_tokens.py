import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from check_chart_tokens import check_html

LINK = '<link rel="stylesheet" href="assets/chart-tokens.css">'


def page(css="", js=""):
    return f"{LINK}<style>{css}</style><script>{js}</script>"


def test_accepts_token_references_and_color_mix():
    css = (".viz-root { --x-a: var(--chart-emphasis); "
           "--x-b: color-mix(in srgb, var(--chart-emphasis) 16%, transparent); }")
    assert check_html(page(css), ["x"]) == []


def test_flags_hsl_value():
    assert check_html(page(".viz-root { --x-a: hsl(20 80% 50%); }"), ["x"]) != []


def test_flags_oklch_value():
    assert check_html(page(".viz-root { --x-a: oklch(0.6 0.2 40); }"), ["x"]) != []


def test_flags_named_color():
    assert check_html(page(".viz-root { --x-a: tomato; }"), ["x"]) != []


def test_flags_named_color_inside_color_mix():
    css = ".viz-root { --x-a: color-mix(in srgb, var(--chart-emphasis) 16%, white); }"
    assert check_html(page(css), ["x"]) != []


def test_flags_unprefixed_svg_text_class_without_font_role():
    css = ".axis-label { fill: var(--chart-neutral-label); font-size: 11px; }"
    assert check_html(page(css), []) != []


def test_accepts_unprefixed_svg_text_class_with_font_role():
    css = ".axis-label { fill: var(--chart-neutral-label); font: var(--chart-font-label); }"
    assert check_html(page(css), []) == []


def test_flags_svg_text_created_without_class():
    js = 'const t = svgEl("text", { x: 1, y: 2, fill: "var(--chart-neutral-label)" });'
    assert check_html(page(js=js), []) != []


def test_accepts_svg_text_created_with_class():
    js = 'const t = svgEl("text", { class: "chart-label", x: 1, y: 2 });'
    assert check_html(page(js=js), []) == []


def test_flags_page_variable_as_chart_paint_in_css():
    assert check_html(page(".x-gl { stroke: var(--grid); }"), []) != []


def test_flags_page_variable_as_chart_paint_in_script():
    js = 'add(el("circle", { cx: 1, cy: 2, r: 9, fill: "var(--accent)" }));'
    assert check_html(page(js=js), []) != []


def test_allows_surface_as_halo_paint():
    js = 'add(el("circle", { cx: 1, cy: 2, r: 9, stroke: "var(--surface-1)" }));'
    assert check_html(page(js=js), []) == []


from check_chart_tokens import check_species_tokens


def test_species_token_drift_is_reported():
    css = (".viz-root { --species-status-native-base: #000000; }\n"
           "@media (prefers-color-scheme: dark) {\n"
           "  :root:where(:not([data-theme=\"light\"])) .viz-root { --species-status-native-base: #000000; }\n}\n"
           ":root[data-theme=\"dark\"] .viz-root { --species-status-native-base: #000000; }")
    fails = check_species_tokens(css)
    assert any("--species-status-native-base" in f for f in fails)


def test_species_unknown_ramp_step_is_reported_not_raised(monkeypatch, tmp_path):
    import check_chart_tokens as cct
    bad = tmp_path / "species.json"
    bad.write_text('{"tokens": {"status/native/base": {"light": "sage/750", "dark": "sage/500"}}}')
    monkeypatch.setattr(cct, "SPECIES", bad)
    fails = check_species_tokens("")
    assert any("sage/750" in f for f in fails)


def test_chart_token_drift_is_reported():
    from check_chart_tokens import check_collection_tokens, CHART
    css = (".viz-root { --chart-season-winter: #000000; }\n"
           "@media (prefers-color-scheme: dark) {\n"
           "  :root:where(:not([data-theme=\"light\"])) .viz-root { --chart-season-winter: #000000; }\n}\n"
           ":root[data-theme=\"dark\"] .viz-root { --chart-season-winter: #000000; }")
    fails = check_collection_tokens(css, CHART, "--chart-")
    assert any("--chart-season-winter light" in f for f in fails)


def test_chart_json_matches_the_published_css():
    from check_chart_tokens import check_collection_tokens, CHART, CSS
    assert check_collection_tokens(CSS.read_text(), CHART, "--chart-") == []
