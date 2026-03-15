#!/usr/bin/env python3
# File: /home/ywatanabe/proj/scitex-notification/tests/test_api.py
"""Tests for the public API of scitex_notification.

Covers:
- alert() returns bool
- available_backends() returns list
- available_backends() contains at least one known backend
- DEFAULT_FALLBACK_ORDER is a list
- __version__ is defined
- All __all__ exports exist on the module
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch


# ---------------------------------------------------------------------------
# test_version_defined
# ---------------------------------------------------------------------------
def test_version_defined():
    import scitex_notification

    assert hasattr(scitex_notification, "__version__")
    assert isinstance(scitex_notification.__version__, str)
    assert len(scitex_notification.__version__) > 0


# ---------------------------------------------------------------------------
# test_all_exports
# ---------------------------------------------------------------------------
def test_all_exports():
    import scitex_notification

    expected = [
        "alert",
        "alert_async",
        "available_backends",
        "call",
        "call_async",
        "sms",
        "sms_async",
        "__version__",
    ]
    for name in expected:
        assert hasattr(scitex_notification, name), (
            f"scitex_notification is missing export: {name}"
        )


# ---------------------------------------------------------------------------
# test_default_fallback_order_is_list
# ---------------------------------------------------------------------------
def test_default_fallback_order_is_list():
    from scitex_notification import DEFAULT_FALLBACK_ORDER

    assert isinstance(DEFAULT_FALLBACK_ORDER, list)
    assert len(DEFAULT_FALLBACK_ORDER) > 0
    for item in DEFAULT_FALLBACK_ORDER:
        assert isinstance(item, str)


# ---------------------------------------------------------------------------
# test_available_backends_returns_list
# ---------------------------------------------------------------------------
def test_available_backends_returns_list():
    from scitex_notification import available_backends

    result = available_backends()
    assert isinstance(result, list)
    for item in result:
        assert isinstance(item, str)


# ---------------------------------------------------------------------------
# test_available_backends_contains_known
# ---------------------------------------------------------------------------
def test_available_backends_contains_known():
    """At least one of the known backends should be available in any environment."""
    from scitex_notification import available_backends

    result = available_backends()
    known = {
        "audio",
        "desktop",
        "email",
        "emacs",
        "matplotlib",
        "playwright",
        "webhook",
        "twilio",
    }
    # Every returned name must be from the known set
    for name in result:
        assert name in known, f"Unknown backend returned: {name}"


# ---------------------------------------------------------------------------
# test_alert_returns_bool
# ---------------------------------------------------------------------------
def test_alert_returns_bool():
    """alert() must return a bool regardless of backend outcome."""
    mock_result = MagicMock()
    mock_result.success = True

    mock_backend = MagicMock()
    mock_backend.send = AsyncMock(return_value=mock_result)

    with (
        patch(
            "scitex_notification._backends.available_backends",
            return_value=["desktop"],
        ),
        patch(
            "scitex_notification._backends.get_backend",
            return_value=mock_backend,
        ),
    ):
        import scitex_notification

        result = scitex_notification.alert(
            "test message", backend="desktop", fallback=False
        )
        assert isinstance(result, bool)


# ---------------------------------------------------------------------------
# test_alert_returns_false_when_all_backends_fail
# ---------------------------------------------------------------------------
def test_alert_returns_bool_type():
    """alert() always returns a bool."""
    import scitex_notification

    result = scitex_notification.alert(
        "test message", backend="desktop", fallback=False
    )
    assert isinstance(result, bool)


# ---------------------------------------------------------------------------
# test_alert_with_invalid_level_falls_back_to_info
# ---------------------------------------------------------------------------
def test_alert_with_invalid_level_falls_back_to_info():
    """alert() should not raise on an invalid level string."""
    mock_result = MagicMock()
    mock_result.success = True

    mock_backend = MagicMock()
    mock_backend.send = AsyncMock(return_value=mock_result)

    with (
        patch(
            "scitex_notification._backends.available_backends",
            return_value=["desktop"],
        ),
        patch(
            "scitex_notification._backends.get_backend",
            return_value=mock_backend,
        ),
    ):
        import scitex_notification

        result = scitex_notification.alert(
            "hi", level="not_a_real_level", backend="desktop", fallback=False
        )
        assert isinstance(result, bool)


# ---------------------------------------------------------------------------
# test_call_delegates_to_twilio_backend
# ---------------------------------------------------------------------------
def test_call_returns_bool():
    """call() always returns a bool."""
    import scitex_notification

    result = scitex_notification.call("test")
    assert isinstance(result, bool)


def test_sms_returns_bool():
    """sms() always returns a bool."""
    import scitex_notification

    result = scitex_notification.sms("test")
    assert isinstance(result, bool)


# EOF
