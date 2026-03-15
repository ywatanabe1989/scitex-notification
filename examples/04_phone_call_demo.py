#!/usr/bin/env python3
"""Demo: Phone call and SMS alerts via Twilio.

Requires environment variables:
    SCITEX_NOTIFICATION_TWILIO_SID    - Twilio Account SID
    SCITEX_NOTIFICATION_TWILIO_TOKEN  - Twilio Auth Token
    SCITEX_NOTIFICATION_TWILIO_FROM   - Twilio phone number
    SCITEX_NOTIFICATION_TWILIO_TO     - Your phone number

Usage:
    export SCITEX_NOTIFICATION_TWILIO_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    export SCITEX_NOTIFICATION_TWILIO_TOKEN=your_auth_token
    export SCITEX_NOTIFICATION_TWILIO_FROM=+XX-XXX-XXX-XXXX
    export SCITEX_NOTIFICATION_TWILIO_TO=+XX-XXX-XXX-XXXX
    python 04_phone_call_demo.py
"""

import os

import scitex as stx

import scitex_notification as notify


@stx.session
def main(logger=stx.INJECTED):
    """Phone call and SMS demo via Twilio."""
    # Check credentials
    sid = os.environ.get("SCITEX_NOTIFICATION_TWILIO_SID")
    if not sid:
        logger.warning(
            "Twilio not configured. Set SCITEX_NOTIFICATION_TWILIO_* env vars."
        )
        logger.info("See .env.example for the full list.")
        return 0

    # Phone call — wakes you up even in silent mode with repeat
    logger.info("Making phone call...")
    success = notify.call(
        "Training complete. Validation loss 0.042. Model saved.",
        title="ML Pipeline",
        repeat=2,  # Call twice to bypass iOS silent mode
    )
    logger.info(f"  Call: {'sent' if success else 'failed'}")

    # SMS — silent notification with text record
    logger.info("Sending SMS...")
    success = notify.sms(
        "Build #1847 passed. Deploy ready.",
        title="CI/CD",
    )
    logger.info(f"  SMS: {'sent' if success else 'failed'}")

    return 0


if __name__ == "__main__":
    main()
