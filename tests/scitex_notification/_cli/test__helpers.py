#!/usr/bin/env python3
"""Tests for scitex_notification._cli._helpers."""

import json

import click
import pytest

from scitex_notification._cli._helpers import (
    emit_result,
    group_to_json,
    print_help_recursive,
)


@click.group()
def root():
    """Root group."""


@root.command()
def hello():
    """Say hello."""


class TestPrintHelpRecursive:
    def test_emits_command_names(self, capsys):
        ctx = click.Context(root)
        print_help_recursive(ctx, root)
        out = capsys.readouterr().out
        assert "root" in out
        assert "hello" in out


class TestGroupToJson:
    def test_emits_valid_json_with_subcommands(self, capsys):
        ctx = click.Context(root)
        group_to_json(ctx, root)
        out = capsys.readouterr().out
        d = json.loads(out)
        assert d["name"] == "root"
        assert "hello" in d["subcommands"]


class TestEmitResult:
    def test_writes_dict_payload(self, capsys):
        emit_result({"x": 1}, success=True)
        out = capsys.readouterr().out
        # Output may be wrapped in scitex_dev Result envelope OR plain JSON
        # — verify the payload key landed somewhere.
        assert '"x"' in out or "'x'" in out


if __name__ == "__main__":
    import os

    pytest.main([os.path.abspath(__file__), "-v"])

# EOF
