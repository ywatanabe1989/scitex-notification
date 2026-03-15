#!/usr/bin/env python3
# File: /home/ywatanabe/proj/scitex-notification/tests/test_backends.py
"""Tests for the backend registry and backend types.

Covers:
- BACKENDS dict has expected keys
- get_backend() returns a BaseNotifyBackend instance
- get_backend() raises ValueError for unknown name
- All backends have is_available()
- All backends have send()
- NotifyResult dataclass fields
- NotifyLevel enum values
"""

from __future__ import annotations

import pytest


# ---------------------------------------------------------------------------
# test_backends_dict_has_expected_keys
# ---------------------------------------------------------------------------
def test_backends_dict_has_expected_keys():
    from scitex_notification._backends import BACKENDS

    expected_keys = {
        "audio",
        "email",
        "desktop",
        "emacs",
        "webhook",
        "matplotlib",
        "playwright",
        "twilio",
    }
    assert set(BACKENDS.keys()) == expected_keys


# ---------------------------------------------------------------------------
# test_get_backend_returns_instance
# ---------------------------------------------------------------------------
def test_get_backend_returns_instance():
    from scitex_notification._backends import get_backend
    from scitex_notification._backends._types import BaseNotifyBackend

    backend = get_backend("desktop")
    assert isinstance(backend, BaseNotifyBackend)


# ---------------------------------------------------------------------------
# test_get_backend_unknown_raises
# ---------------------------------------------------------------------------
def test_get_backend_unknown_raises():
    from scitex_notification._backends import get_backend

    with pytest.raises(ValueError, match="Unknown backend"):
        get_backend("nonexistent_backend_xyz")


# ---------------------------------------------------------------------------
# test_all_backends_have_is_available
# ---------------------------------------------------------------------------
def test_all_backends_have_is_available():
    from scitex_notification._backends import BACKENDS

    for name, cls in BACKENDS.items():
        instance = cls()
        assert hasattr(instance, "is_available"), (
            f"Backend '{name}' is missing is_available()"
        )
        assert callable(instance.is_available), (
            f"Backend '{name}'.is_available is not callable"
        )
        # Call it — should return bool without raising
        result = instance.is_available()
        assert isinstance(result, bool), (
            f"Backend '{name}'.is_available() should return bool, got {type(result)}"
        )


# ---------------------------------------------------------------------------
# test_all_backends_have_send_method
# ---------------------------------------------------------------------------
def test_all_backends_have_send_method():
    import inspect

    from scitex_notification._backends import BACKENDS

    for name, cls in BACKENDS.items():
        instance = cls()
        assert hasattr(instance, "send"), f"Backend '{name}' is missing send()"
        assert callable(instance.send), f"Backend '{name}'.send is not callable"
        # send() must be a coroutine function (async def)
        assert inspect.iscoroutinefunction(instance.send), (
            f"Backend '{name}'.send() must be async"
        )


# ---------------------------------------------------------------------------
# test_notify_result_dataclass
# ---------------------------------------------------------------------------
def test_notify_result_dataclass():
    from scitex_notification._backends._types import NotifyResult

    result = NotifyResult(
        success=True,
        backend="desktop",
        message="hello",
        timestamp="2026-01-01T00:00:00",
    )
    assert result.success is True
    assert result.backend == "desktop"
    assert result.message == "hello"
    assert result.timestamp == "2026-01-01T00:00:00"
    assert result.error is None
    assert result.details is None


def test_notify_result_with_error():
    from scitex_notification._backends._types import NotifyResult

    result = NotifyResult(
        success=False,
        backend="email",
        message="failed",
        timestamp="2026-01-01T00:00:00",
        error="SMTP error",
        details={"code": 500},
    )
    assert result.success is False
    assert result.error == "SMTP error"
    assert result.details == {"code": 500}


# ---------------------------------------------------------------------------
# test_notify_level_enum
# ---------------------------------------------------------------------------
def test_notify_level_enum_values():
    from scitex_notification._backends._types import NotifyLevel

    assert NotifyLevel.INFO.value == "info"
    assert NotifyLevel.WARNING.value == "warning"
    assert NotifyLevel.ERROR.value == "error"
    assert NotifyLevel.CRITICAL.value == "critical"


def test_notify_level_enum_from_string():
    from scitex_notification._backends._types import NotifyLevel

    assert NotifyLevel("info") is NotifyLevel.INFO
    assert NotifyLevel("warning") is NotifyLevel.WARNING
    assert NotifyLevel("error") is NotifyLevel.ERROR
    assert NotifyLevel("critical") is NotifyLevel.CRITICAL


def test_notify_level_enum_invalid_raises():
    from scitex_notification._backends._types import NotifyLevel

    with pytest.raises(ValueError):
        NotifyLevel("not_a_level")


# ---------------------------------------------------------------------------
# test_backend_name_attribute
# ---------------------------------------------------------------------------
def test_all_backends_have_name_attribute():
    from scitex_notification._backends import BACKENDS

    for registry_key, cls in BACKENDS.items():
        instance = cls()
        assert hasattr(instance, "name"), (
            f"Backend '{registry_key}' class is missing 'name' attribute"
        )
        assert isinstance(instance.name, str), (
            f"Backend '{registry_key}'.name must be a string"
        )


# EOF
