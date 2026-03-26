#!/usr/bin/env python3
# Timestamp: "2026-03-16 (ywatanabe)"
# File: /home/ywatanabe/proj/scitex-notification/src/scitex_notification/_cli/_notify_cmds.py

"""CLI subcommands for send / call / sms / backends / config."""

from __future__ import annotations

import sys

import click

from ._helpers import emit_result, fatal

_BACKEND_CHOICES = [
    "audio",
    "emacs",
    "matplotlib",
    "playwright",
    "email",
    "twilio",
    "desktop",
    "webhook",
]

_LEVEL_CHOICES = ["info", "warning", "error", "critical"]


@click.command()
@click.argument("message")
@click.option("--title", "-t", help="Notification title")
@click.option(
    "--backend",
    "-b",
    type=click.Choice(_BACKEND_CHOICES),
    help="Backend to use (auto-selects with fallback if not specified)",
)
@click.option(
    "--level",
    "-l",
    type=click.Choice(_LEVEL_CHOICES),
    default="info",
    help="Alert level (default: info)",
)
@click.option("--no-fallback", is_flag=True, help="Disable backend fallback on error")
@click.option(
    "--dry-run", is_flag=True, help="Print what would be sent without sending"
)
@click.option("--json", "as_json", is_flag=True, help="Output as structured JSON.")
def send(message, title, backend, level, no_fallback, dry_run, as_json):
    """
    Send a notification via configured backends

    \b
    Examples:
      scitex-notification send "Task complete!"
      scitex-notification send "Error" --backend email --level error
      scitex-notification send "Hello" --json
    """
    if dry_run:
        click.echo(
            f"[dry-run] send: message={message!r} title={title!r} "
            f"backend={backend!r} level={level!r} fallback={not no_fallback}"
        )
        return

    if as_json:
        from scitex_dev import wrap_as_cli

        from scitex_notification import alert

        wrap_as_cli(
            alert,
            as_json=True,
            message=message,
            title=title,
            backend=backend,
            level=level,
            fallback=not no_fallback,
        )
        return

    try:
        from scitex_notification import alert

        success = alert(
            message,
            title=title,
            backend=backend,
            level=level,
            fallback=not no_fallback,
        )
        if success:
            click.secho("Notification sent", fg="green")
        else:
            click.secho("Failed to send notification (all backends failed)", fg="red")
            sys.exit(1)
    except Exception as e:
        fatal(str(e))


@click.command()
@click.argument("message")
@click.option("--title", "-t", help="Call title/context")
@click.option(
    "--level",
    "-l",
    type=click.Choice(_LEVEL_CHOICES),
    default="info",
    help="Alert level (default: info)",
)
@click.option("--to", "to_number", help="Destination phone number (overrides default)")
@click.option(
    "--repeat",
    "-r",
    type=int,
    default=1,
    help="Repeat call N times (30s apart). Default: $SCITEX_NOTIFICATION_PHONE_CALL_N_REPEAT (1)",
)
@click.option("--flow-sid", help="Twilio Studio Flow SID (optional)")
@click.option("--dry-run", is_flag=True, help="Print what would happen without calling")
@click.option("--json", "as_json", is_flag=True, help="Output as structured JSON.")
def call(message, title, level, to_number, repeat, flow_sid, dry_run, as_json):
    """
    Make a phone call via Twilio

    \b
    Requires env vars:
      SCITEX_NOTIFY_TWILIO_SID    - Twilio Account SID
      SCITEX_NOTIFY_TWILIO_TOKEN  - Twilio Auth Token
      SCITEX_NOTIFY_TWILIO_FROM   - Twilio phone number
      SCITEX_NOTIFY_TWILIO_TO     - Destination phone number

    \b
    Examples:
      scitex-notification call "Build finished!"
      scitex-notification call "Wake up!" --repeat 2
      scitex-notification call "Alert!" --to +61400000000
    """
    kwargs = {}
    if to_number:
        kwargs["to_number"] = to_number
    if flow_sid:
        kwargs["flow_sid"] = flow_sid
    if repeat > 1:
        kwargs["repeat"] = repeat

    if dry_run:
        click.echo(
            f"[dry-run] call: message={message!r} title={title!r} "
            f"level={level!r} kwargs={kwargs}"
        )
        return

    if as_json:
        from scitex_dev import wrap_as_cli

        from scitex_notification import call as notify_call

        wrap_as_cli(
            notify_call,
            as_json=True,
            message=message,
            title=title,
            level=level,
            **kwargs,
        )
        return

    try:
        from scitex_notification import call as notify_call

        click.echo(f"Calling via Twilio (repeat={repeat})...")
        success = notify_call(message, title=title, level=level, **kwargs)
        if success:
            click.secho("Call initiated successfully", fg="green")
        else:
            click.secho("Failed to make call", fg="red")
            click.echo("Check SCITEX_NOTIFY_TWILIO_* env vars are set correctly.")
            sys.exit(1)
    except Exception as e:
        fatal(str(e))


@click.command()
@click.argument("message")
@click.option("--title", "-t", help="SMS title/subject (prepended to message)")
@click.option("--to", "to_number", help="Destination phone number (overrides default)")
@click.option("--dry-run", is_flag=True, help="Print what would happen without sending")
@click.option("--json", "as_json", is_flag=True, help="Output as structured JSON.")
def sms(message, title, to_number, dry_run, as_json):
    """
    Send an SMS via Twilio

    \b
    Requires env vars:
      SCITEX_NOTIFY_TWILIO_SID    - Twilio Account SID
      SCITEX_NOTIFY_TWILIO_TOKEN  - Twilio Auth Token
      SCITEX_NOTIFY_TWILIO_FROM   - Twilio phone number
      SCITEX_NOTIFY_TWILIO_TO     - Destination phone number

    \b
    Examples:
      scitex-notification sms "Build finished!"
      scitex-notification sms "Alert!" --to +61400000000
    """
    kwargs = {}
    if to_number:
        kwargs["to_number"] = to_number

    if dry_run:
        click.echo(
            f"[dry-run] sms: message={message!r} title={title!r} kwargs={kwargs}"
        )
        return

    if as_json:
        from scitex_dev import wrap_as_cli

        from scitex_notification import sms as notify_sms

        wrap_as_cli(notify_sms, as_json=True, message=message, title=title, **kwargs)
        return

    try:
        from scitex_notification import sms as notify_sms

        click.echo("Sending SMS via Twilio...")
        success = notify_sms(message, title=title, **kwargs)
        if success:
            click.secho("SMS sent successfully", fg="green")
        else:
            click.secho("Failed to send SMS", fg="red")
            click.echo("Check SCITEX_NOTIFY_TWILIO_* env vars are set correctly.")
            sys.exit(1)
    except Exception as e:
        fatal(str(e))


@click.command(name="backends")
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def list_backends(as_json):
    """
    List notification backends and their availability

    \b
    Example:
      scitex-notification backends
      scitex-notification backends --json
    """
    try:
        from scitex_notification import DEFAULT_FALLBACK_ORDER, available_backends
        from scitex_notification._backends import BACKENDS

        available = available_backends()

        if as_json:
            emit_result(
                {
                    "available": available,
                    "all_backends": list(BACKENDS.keys()),
                    "fallback_order": DEFAULT_FALLBACK_ORDER,
                }
            )
            return

        click.secho("Notification Backends", fg="cyan", bold=True)
        click.echo("=" * 40)
        click.echo("\nFallback order:")
        for i, b in enumerate(DEFAULT_FALLBACK_ORDER, 1):
            status = (
                click.style("available", fg="green")
                if b in available
                else click.style("not available", fg="red")
            )
            click.echo(f"  {i}. {b}: {status}")

        non_fallback = [b for b in BACKENDS if b not in DEFAULT_FALLBACK_ORDER]
        if non_fallback:
            click.echo("\nExplicit-only backends:")
            for b in non_fallback:
                status = (
                    click.style("available", fg="green")
                    if b in available
                    else click.style("not available", fg="red")
                )
                click.echo(f"  - {b}: {status}")
    except Exception as e:
        fatal(str(e))


@click.command()
@click.option("--json", "as_json", is_flag=True, help="Output as JSON")
def config(as_json):
    """
    Show current notification configuration

    \b
    Example:
      scitex-notification config
      scitex-notification config --json
    """
    try:
        from scitex_notification._backends._config import get_config

        cfg = get_config()

        if as_json:
            emit_result(
                {
                    "default_backend": cfg.default_backend,
                    "backend_priority": cfg.backend_priority,
                    "available_priority": cfg.get_available_backend_priority(),
                    "first_available": cfg.get_first_available_backend(),
                }
            )
            return

        click.secho("Notification Configuration", fg="cyan", bold=True)
        click.echo("=" * 40)
        click.echo(f"\nDefault backend: {cfg.default_backend}")
        click.echo(f"Priority order:  {', '.join(cfg.backend_priority)}")
        click.echo(f"First available: {cfg.get_first_available_backend()}")

        avail = cfg.get_available_backend_priority()
        if avail:
            click.echo("\nAvailable (in priority order):")
            for b in avail:
                click.echo(f"  - {b}")
    except Exception as e:
        fatal(str(e))


# EOF
