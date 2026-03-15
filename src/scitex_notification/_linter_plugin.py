#!/usr/bin/env python3
# Timestamp: "2026-03-16 (ywatanabe)"
# File: /home/ywatanabe/proj/scitex-notification/src/scitex_notification/_linter_plugin.py

"""Linter plugin entry point for scitex-notification.

Implements the scitex_linter.plugins entry point interface.
"""


def get_plugin() -> dict:
    """Return linter plugin definition for scitex-notification.

    Returns
    -------
    dict
        Plugin definition with rules, call_rules, axes_hints, and checkers.
    """
    return {
        "rules": [],
        "call_rules": {},
        "axes_hints": {},
        "checkers": [],
    }


# EOF
