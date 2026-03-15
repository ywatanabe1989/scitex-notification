#!/usr/bin/env python3
# Timestamp: "2026-03-16 (ywatanabe)"
# File: /home/ywatanabe/proj/scitex-notification/src/scitex_notification/_cli/_helpers.py

"""Shared CLI helper utilities."""

from __future__ import annotations

import json
import sys

import click


def print_help_recursive(ctx, cmd, indent: int = 0) -> None:
    """Recursively print help for a command and all subcommands."""
    prefix = "  " * indent
    click.echo(f"{prefix}{cmd.name}: {cmd.get_short_help_str()}")
    if hasattr(cmd, "commands"):
        for name, subcmd in sorted(cmd.commands.items()):
            sub_ctx = click.Context(subcmd, parent=ctx, info_name=name)
            print_help_recursive(sub_ctx, subcmd, indent + 1)


def group_to_json(ctx, cmd) -> None:
    """Output group info as JSON."""
    data = {
        "name": cmd.name,
        "help": cmd.help,
        "subcommands": {},
    }
    if hasattr(cmd, "commands"):
        for name, subcmd in cmd.commands.items():
            data["subcommands"][name] = subcmd.get_short_help_str()
    click.echo(json.dumps(data, indent=2))


def emit_result(data: dict, success: bool = True) -> None:
    """Emit a JSON result, using scitex_dev.Result if available."""
    try:
        from scitex_dev import Result

        click.echo(Result(success=success, data=data).to_json())
    except ImportError:
        click.echo(json.dumps({"success": success, "data": data}, indent=2))


def fatal(msg: str) -> None:
    """Print error and exit."""
    click.secho(f"Error: {msg}", fg="red", err=True)
    sys.exit(1)


# EOF
