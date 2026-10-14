import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from build_nav import build, stamp


def _make_docs(tmp_path, nav="<nav>N</nav>", footer="<footer>F</footer>"):
    docs_dir = tmp_path / "docs"
    partials_dir = docs_dir / "_partials"
    partials_dir.mkdir(parents=True)
    (partials_dir / "nav.html").write_text(nav)
    (partials_dir / "footer.html").write_text(footer)
    return docs_dir


def test_stamp_replaces_marker_region():
    html = (
        "<body>\n"
        "<!-- NAV:START -->\n<!-- NAV:END -->\n"
        "<p>content</p>\n"
        "</body>"
    )
    result = stamp(html, "NAV", "<nav>Home</nav>")
    assert "<nav>Home</nav>" in result
    assert "<p>content</p>" in result


def test_stamp_is_idempotent():
    html = "<!-- NAV:START -->\nold\n<!-- NAV:END -->"
    once = stamp(html, "NAV", "<nav>new</nav>")
    twice = stamp(once, "NAV", "<nav>new</nav>")
    assert once == twice
    assert "old" not in once


def test_stamp_leaves_other_markers_alone():
    html = (
        "<!-- NAV:START -->\nnav\n<!-- NAV:END -->\n"
        "<!-- FOOTER:START -->\nfoot\n<!-- FOOTER:END -->"
    )
    result = stamp(html, "NAV", "<nav>new</nav>")
    assert "foot" in result
    assert "<!-- FOOTER:START -->" in result


def test_stamp_returns_unchanged_when_marker_absent():
    html = "<p>no markers here</p>"
    result = stamp(html, "NAV", "<nav>x</nav>")
    assert result == html


def test_build_raises_filenotfounderror_when_partial_missing(tmp_path):
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    # No _partials/ directory created at all, so both partial files are missing.
    (docs_dir / "page.html").write_text(
        "<!-- NAV:START -->\n<!-- NAV:END -->\n"
        "<!-- FOOTER:START -->\n<!-- FOOTER:END -->\n"
    )
    with pytest.raises(FileNotFoundError):
        build(docs_dir)


def test_build_does_not_touch_partials_directory(tmp_path):
    docs_dir = _make_docs(tmp_path, nav="<nav>N</nav>", footer="<footer>F</footer>")
    page = docs_dir / "page.html"
    page.write_text(
        "<!-- NAV:START -->\nold\n<!-- NAV:END -->\n"
        "<!-- FOOTER:START -->\nold\n<!-- FOOTER:END -->\n"
    )
    # The partials themselves also contain marker-looking comments in their own
    # filenames' sibling directory; if build() ever switched from glob to rglob,
    # it would recurse into _partials/ and could rewrite these source files.
    nav_before = (docs_dir / "_partials" / "nav.html").read_text()
    footer_before = (docs_dir / "_partials" / "footer.html").read_text()

    build(docs_dir)

    assert (docs_dir / "_partials" / "nav.html").read_text() == nav_before
    assert (docs_dir / "_partials" / "footer.html").read_text() == footer_before


def test_build_returns_list_of_changed_files(tmp_path):
    docs_dir = _make_docs(tmp_path, nav="<nav>N</nav>", footer="<footer>F</footer>")
    changed_page = docs_dir / "changed.html"
    changed_page.write_text(
        "<!-- NAV:START -->\nold\n<!-- NAV:END -->\n"
        "<!-- FOOTER:START -->\nold\n<!-- FOOTER:END -->\n"
    )
    unchanged_page = docs_dir / "unchanged.html"
    unchanged_page.write_text("<p>no markers here at all</p>")

    changed = build(docs_dir)

    assert changed == [changed_page]
    assert unchanged_page not in changed
