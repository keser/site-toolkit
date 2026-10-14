import subprocess
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from port_report import main, port

PORT_REPORT_SCRIPT = Path(__file__).resolve().parent.parent / "port_report.py"

FRAGMENT = (
    '<meta charset="utf-8">\n'
    '<title>Example Report</title>\n'
    '<style>.viz-root { color: red; }</style>\n'
    '<div class="viz-root">\n'
    '  <p>hello</p>\n'
    '</div>\n'
)


def test_port_splits_head_and_body():
    result = port(FRAGMENT)
    assert "<title>Example Report</title>" in result
    assert result.index("<head>") < result.index("<title>Example Report</title>") < result.index("</head>")
    assert result.index("</head>") < result.index('<div class="viz-root">')


def test_port_inserts_empty_markers():
    result = port(FRAGMENT)
    assert "<!-- NAV:START -->\n<!-- NAV:END -->" in result
    assert "<!-- FOOTER:START -->\n<!-- FOOTER:END -->" in result


def test_port_preserves_body_content():
    result = port(FRAGMENT)
    assert "<p>hello</p>" in result


def test_port_raises_on_missing_viz_root():
    with pytest.raises(ValueError):
        port("<p>no viz-root div here</p>")


def test_main_writes_expected_file(tmp_path, monkeypatch):
    source_path = tmp_path / "source.html"
    source_path.write_text(FRAGMENT)
    dest_path = tmp_path / "nested" / "dest.html"

    monkeypatch.setattr(sys, "argv", ["port_report.py", str(source_path), str(dest_path)])
    main()

    assert dest_path.exists()
    assert dest_path.read_text() == port(FRAGMENT)


def test_main_creates_missing_dest_parent_dirs(tmp_path, monkeypatch):
    source_path = tmp_path / "source.html"
    source_path.write_text(FRAGMENT)
    dest_path = tmp_path / "does" / "not" / "exist" / "dest.html"

    monkeypatch.setattr(sys, "argv", ["port_report.py", str(source_path), str(dest_path)])
    main()

    assert dest_path.exists()


def test_main_exits_with_usage_on_wrong_arg_count(monkeypatch, capsys):
    monkeypatch.setattr(sys, "argv", ["port_report.py", "only-one-arg"])
    with pytest.raises(SystemExit) as exc_info:
        main()

    assert exc_info.value.code == 2
    assert "usage:" in capsys.readouterr().err


def test_main_raises_on_missing_source_file(tmp_path, monkeypatch):
    missing_source = tmp_path / "does-not-exist.html"
    dest_path = tmp_path / "dest.html"

    monkeypatch.setattr(sys, "argv", ["port_report.py", str(missing_source), str(dest_path)])
    with pytest.raises(FileNotFoundError):
        main()


def test_cli_entry_point_writes_file_via_subprocess(tmp_path):
    source_path = tmp_path / "source.html"
    source_path.write_text(FRAGMENT)
    dest_path = tmp_path / "dest.html"

    result = subprocess.run(
        [sys.executable, str(PORT_REPORT_SCRIPT), str(source_path), str(dest_path)],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0
    assert dest_path.exists()
    assert dest_path.read_text() == port(FRAGMENT)
    assert f"wrote {dest_path}" in result.stdout
