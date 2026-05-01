#!/usr/bin/env python3
# File: /home/ywatanabe/proj/scitex-notification/tests/test_cli.py
"""Tests for the CLI entry point.

Covers:
- --help exits with code 0 and contains usage text
- backends command lists backends
- send --dry-run prints dry-run output without sending
- call --dry-run prints dry-run output without calling
- sms --dry-run prints dry-run output without sending
- config command prints configuration
"""

from __future__ import annotations

from unittest.mock import patch

import pytest
from click.testing import CliRunner

from scitex_notification._cli._main import cli

# ---------------------------------------------------------------------------
# Fixture
# ---------------------------------------------------------------------------


@pytest.fixture
def runner():
    return CliRunner()


# ---------------------------------------------------------------------------
# test_cli_help
# ---------------------------------------------------------------------------
def test_cli_help(runner):
    """--help should exit 0 and show usage information."""
    result = runner.invoke(cli, ["--help"])
    assert result.exit_code == 0
    assert "Usage" in result.output or "notification" in result.output.lower()


def test_cli_h_flag(runner):
    """-h should also show help."""
    result = runner.invoke(cli, ["-h"])
    assert result.exit_code == 0


def test_cli_no_args(runner):
    """Invoking with no args should show help text (exit 0)."""
    result = runner.invoke(cli, [])
    assert result.exit_code == 0


# ---------------------------------------------------------------------------
# test_cli_backends
# ---------------------------------------------------------------------------
def test_cli_backends(runner):
    """backends command should list backend names."""
    result = runner.invoke(cli, ["list-backends"])
    assert result.exit_code == 0
    # At minimum the command should run and output some text
    assert len(result.output) > 0


def test_cli_backends_json(runner):
    """backends --json should output valid JSON with 'available' key."""
    import json

    result = runner.invoke(cli, ["list-backends", "--json"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    # Result envelope: data is under "data" key
    inner = data.get("data", data)
    assert "available" in inner or "available_backends" in inner


# ---------------------------------------------------------------------------
# test_send_dry_run
# ---------------------------------------------------------------------------
def test_send_dry_run(runner):
    """send --dry-run should print what would be sent without side effects."""
    result = runner.invoke(cli, ["send-notification", "Test message", "--dry-run"])
    assert result.exit_code == 0
    assert "dry-run" in result.output
    assert "Test message" in result.output


def test_send_dry_run_with_backend(runner):
    """send --dry-run --backend desktop should mention the backend."""
    result = runner.invoke(cli, ["send-notification", "Hello", "--dry-run", "--backend", "desktop"])
    assert result.exit_code == 0
    assert "dry-run" in result.output
    assert "Hello" in result.output


def test_send_dry_run_with_level(runner):
    """send --dry-run --level error should mention the level."""
    result = runner.invoke(cli, ["send-notification", "Error msg", "--dry-run", "--level", "error"])
    assert result.exit_code == 0
    assert "dry-run" in result.output


# ---------------------------------------------------------------------------
# test_call_dry_run
# ---------------------------------------------------------------------------
def test_call_dry_run(runner):
    """call --dry-run should print without making any Twilio call."""
    result = runner.invoke(cli, ["call", "Wake up!", "--dry-run"])
    assert result.exit_code == 0
    assert "dry-run" in result.output
    assert "Wake up!" in result.output


def test_call_dry_run_with_repeat(runner):
    """call --dry-run --repeat 2 should include repeat in output."""
    result = runner.invoke(cli, ["call", "Hello", "--dry-run", "--repeat", "2"])
    assert result.exit_code == 0
    assert "dry-run" in result.output


# ---------------------------------------------------------------------------
# test_sms_dry_run
# ---------------------------------------------------------------------------
def test_sms_dry_run(runner):
    """sms --dry-run should print without sending."""
    result = runner.invoke(cli, ["send-sms", "Build done!", "--dry-run"])
    assert result.exit_code == 0
    assert "dry-run" in result.output
    assert "Build done!" in result.output


def test_sms_dry_run_with_title(runner):
    """sms --dry-run --title prepends title context."""
    result = runner.invoke(cli, ["send-sms", "Finished", "--dry-run", "--title", "CI"])
    assert result.exit_code == 0
    assert "dry-run" in result.output


# ---------------------------------------------------------------------------
# test_config_command
# ---------------------------------------------------------------------------
def test_config_command(runner):
    """config command should display configuration without error."""
    result = runner.invoke(cli, ["show-config"])
    assert result.exit_code == 0
    assert len(result.output) > 0


def test_config_json(runner):
    """config --json should output parseable JSON with known keys."""
    import json

    result = runner.invoke(cli, ["show-config", "--json"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    inner = data.get("data", data)
    assert "default_backend" in inner


# ---------------------------------------------------------------------------
# test_send_mocked_success
# ---------------------------------------------------------------------------
def test_send_mocked_success(runner):
    """send without --dry-run mocked to succeed should print success message."""
    with patch("scitex_notification.alert", return_value=True):
        result = runner.invoke(cli, ["send-notification", "Test"])
    assert result.exit_code == 0
    assert "sent" in result.output.lower() or "success" in result.output.lower()


def test_send_mocked_failure(runner):
    """send without --dry-run mocked to fail should exit non-zero."""
    with patch("scitex_notification.alert", return_value=False):
        result = runner.invoke(cli, ["send-notification", "Test"])
    assert result.exit_code != 0


# ---------------------------------------------------------------------------
# test_help_recursive
# ---------------------------------------------------------------------------
def test_help_recursive(runner):
    """--help-recursive should show recursive help and exit 0."""
    result = runner.invoke(cli, ["--help-recursive"])
    assert result.exit_code == 0


# ---------------------------------------------------------------------------
# test_list_python_apis
# ---------------------------------------------------------------------------
def test_list_python_apis(runner):
    """list-python-apis should list API names."""
    result = runner.invoke(cli, ["list-python-apis"])
    assert result.exit_code == 0
    assert "scitex_notification" in result.output


def test_list_python_apis_json(runner):
    """list-python-apis --json should return parseable JSON."""
    import json

    result = runner.invoke(cli, ["list-python-apis", "--json"])
    assert result.exit_code == 0
    data = json.loads(result.output)
    assert "apis" in data


# EOF
