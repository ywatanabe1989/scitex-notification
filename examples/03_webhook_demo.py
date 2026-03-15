#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Timestamp: "2026-03-16 (ywatanabe)"
# File: ./examples/03_webhook_demo.py

"""Demo: Send alerts to Slack or Discord via webhook.

Set SCITEX_NOTIFICATION_WEBHOOK_URL to your webhook URL first:
    Slack:   https://hooks.slack.com/services/...
    Discord: https://discord.com/api/webhooks/...
"""

import os

import scitex as stx

import scitex_notification as notify


@stx.session
def main(logger=stx.session.INJECTED):
    """Send a webhook notification if SCITEX_NOTIFICATION_WEBHOOK_URL is set."""

    webhook_url = os.environ.get("SCITEX_NOTIFICATION_WEBHOOK_URL")
    if not webhook_url:
        logger.warning(
            "SCITEX_NOTIFICATION_WEBHOOK_URL not set — skipping webhook send."
        )
        logger.info("  Slack:   https://hooks.slack.com/services/...")
        logger.info("  Discord: https://discord.com/api/webhooks/...")
        return 0

    success = notify.alert("Build complete!", backend="webhook", fallback=False)
    logger.info(f"Webhook sent: {success}")

    return 0


if __name__ == "__main__":
    main()

# EOF
