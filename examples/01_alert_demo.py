#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Timestamp: "2026-03-16 (ywatanabe)"
# File: ./examples/01_alert_demo.py

"""Demo: Send alerts through available backends.

Fallback priority (when no backend specified):
    audio -> emacs -> matplotlib -> playwright -> email
"""

import scitex as stx

import scitex_notification as notify


@stx.session
def main(logger=stx.session.INJECTED):
    """Send alerts using the default fallback chain and a specific backend."""

    # List available backends
    logger.info(f"Available backends: {notify.available_backends()}")

    # Simple alert — uses fallback chain: audio -> emacs -> matplotlib -> ...
    success = notify.alert("Hello from scitex-notification!", title="Demo")
    logger.info(f"Alert sent: {success}")

    # Specific backend, no fallback
    success = notify.alert("Desktop notification", backend="desktop", fallback=False)
    logger.info(f"Desktop alert: {success}")

    return 0


if __name__ == "__main__":
    main()

# EOF
