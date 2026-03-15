#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Timestamp: "2026-03-16 (ywatanabe)"
# File: ./examples/02_level_alerts.py

"""Demo: Alert levels — info, warning, error, critical."""

import scitex as stx

import scitex_notification as notify


@stx.session
def main(logger=stx.session.INJECTED):
    """Send alerts at each urgency level using the default fallback chain."""

    for level in ["info", "warning", "error", "critical"]:
        success = notify.alert(f"This is a {level} alert", level=level)
        logger.info(f"  {level}: {'sent' if success else 'failed'}")

    return 0


if __name__ == "__main__":
    main()

# EOF
