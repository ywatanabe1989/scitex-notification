#!/usr/bin/env python3
# File: /home/ywatanabe/proj/scitex-notification/tests/test_env_loader.py
"""Tests for the environment variable loader.

Covers:
- parse_src_file() with a temp file
- _parse_value() quote handling
- load_env_from_path() with nonexistent path
- load_scitex_notification_env() when env var is set / not set
"""

from __future__ import annotations

import os
import textwrap


# ---------------------------------------------------------------------------
# test_parse_src_file_basic
# ---------------------------------------------------------------------------
def test_parse_src_file_basic(tmp_path):
    """parse_src_file() extracts plain KEY=VALUE pairs."""
    from scitex_notification._env_loader import parse_src_file

    src = tmp_path / "test.src"
    src.write_text(
        textwrap.dedent("""\
            FOO=bar
            BAZ=qux
        """)
    )

    result = parse_src_file(src)
    assert result == {"FOO": "bar", "BAZ": "qux"}


# ---------------------------------------------------------------------------
# test_parse_src_file_export_prefix
# ---------------------------------------------------------------------------
def test_parse_src_file_export_prefix(tmp_path):
    """parse_src_file() strips 'export ' prefix."""
    from scitex_notification._env_loader import parse_src_file

    src = tmp_path / "test.src"
    src.write_text("export MY_VAR=hello\n")

    result = parse_src_file(src)
    assert result["MY_VAR"] == "hello"


# ---------------------------------------------------------------------------
# test_parse_src_file_comments_and_blank_lines
# ---------------------------------------------------------------------------
def test_parse_src_file_comments_and_blank_lines(tmp_path):
    """parse_src_file() ignores comment lines and blank lines."""
    from scitex_notification._env_loader import parse_src_file

    src = tmp_path / "test.src"
    src.write_text(
        textwrap.dedent("""\
            # This is a comment

            KEY=value
            # Another comment
        """)
    )

    result = parse_src_file(src)
    assert result == {"KEY": "value"}


# ---------------------------------------------------------------------------
# test_parse_value_double_quotes
# ---------------------------------------------------------------------------
def test_parse_value_double_quotes():
    """_parse_value() removes surrounding double quotes."""
    from scitex_notification._env_loader import _parse_value

    assert _parse_value('"hello world"') == "hello world"


def test_parse_value_single_quotes():
    """_parse_value() removes surrounding single quotes."""
    from scitex_notification._env_loader import _parse_value

    assert _parse_value("'hello world'") == "hello world"


def test_parse_value_no_quotes():
    """_parse_value() leaves plain values unchanged."""
    from scitex_notification._env_loader import _parse_value

    assert _parse_value("plain_value") == "plain_value"


def test_parse_value_empty_string():
    """_parse_value() handles empty string."""
    from scitex_notification._env_loader import _parse_value

    assert _parse_value("") == ""


def test_parse_value_variable_expansion(monkeypatch):
    """_parse_value() expands $VAR references from os.environ."""
    from scitex_notification._env_loader import _parse_value

    monkeypatch.setenv("_TEST_EXPAND", "world")
    result = _parse_value("hello_$_TEST_EXPAND")
    # The variable name _TEST_EXPAND should be expanded
    assert "world" in result or result == "hello_world"


# ---------------------------------------------------------------------------
# test_load_env_from_nonexistent_path
# ---------------------------------------------------------------------------
def test_load_env_from_nonexistent_path():
    """load_env_from_path() returns empty dict for a nonexistent path."""
    from scitex_notification._env_loader import load_env_from_path

    result = load_env_from_path("/nonexistent/path/that/does/not/exist.src")
    assert result == {}


# ---------------------------------------------------------------------------
# test_load_env_from_file_path
# ---------------------------------------------------------------------------
def test_load_env_from_file_path(tmp_path):
    """load_env_from_path() loads variables from a single .src file."""
    from scitex_notification._env_loader import load_env_from_path

    src = tmp_path / "config.src"
    src.write_text("LOADED_KEY=loaded_value\n")

    result = load_env_from_path(str(src))
    assert result["LOADED_KEY"] == "loaded_value"


# ---------------------------------------------------------------------------
# test_load_env_from_directory
# ---------------------------------------------------------------------------
def test_load_env_from_directory(tmp_path):
    """load_env_from_path() loads *.src files from a directory."""
    from scitex_notification._env_loader import load_env_from_path

    (tmp_path / "a.src").write_text("VAR_A=alpha\n")
    (tmp_path / "b.src").write_text("VAR_B=beta\n")
    (tmp_path / "notasrc.txt").write_text("IGNORED=yes\n")

    result = load_env_from_path(str(tmp_path))
    assert result["VAR_A"] == "alpha"
    assert result["VAR_B"] == "beta"
    assert "IGNORED" not in result


# ---------------------------------------------------------------------------
# test_load_scitex_notification_env_no_var_set
# ---------------------------------------------------------------------------
def test_load_scitex_notification_env_no_var_set(monkeypatch):
    """load_scitex_notification_env() returns 0 when env var is not set."""
    from scitex_notification._env_loader import load_scitex_notification_env

    monkeypatch.delenv("SCITEX_NOTIFICATION_ENV_SRC", raising=False)
    count = load_scitex_notification_env()
    assert count == 0


# ---------------------------------------------------------------------------
# test_load_scitex_notification_env_with_file
# ---------------------------------------------------------------------------
def test_load_scitex_notification_env_with_file(tmp_path, monkeypatch):
    """load_scitex_notification_env() loads vars and returns count."""
    from scitex_notification._env_loader import load_scitex_notification_env

    src = tmp_path / "notify.src"
    src.write_text(
        textwrap.dedent("""\
            SCITEX_TEST_LOADED_A=value_a
            SCITEX_TEST_LOADED_B=value_b
        """)
    )
    monkeypatch.setenv("SCITEX_NOTIFICATION_ENV_SRC", str(src))

    count = load_scitex_notification_env()
    assert count == 2
    assert os.environ.get("SCITEX_TEST_LOADED_A") == "value_a"
    assert os.environ.get("SCITEX_TEST_LOADED_B") == "value_b"

    # Clean up
    monkeypatch.delenv("SCITEX_TEST_LOADED_A", raising=False)
    monkeypatch.delenv("SCITEX_TEST_LOADED_B", raising=False)


# ---------------------------------------------------------------------------
# test_parse_src_file_nonexistent_returns_empty
# ---------------------------------------------------------------------------
def test_parse_src_file_nonexistent_returns_empty(tmp_path):
    """parse_src_file() returns empty dict for a nonexistent file."""
    from scitex_notification._env_loader import parse_src_file

    result = parse_src_file(tmp_path / "nonexistent.src")
    assert result == {}


# EOF
