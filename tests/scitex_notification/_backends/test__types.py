#!/usr/bin/env python3
"""Tests for scitex_notification._backends._types core types."""

import pytest

from scitex_notification._backends._types import (
    BaseNotifyBackend,
    NotifyLevel,
    NotifyResult,
)


class TestNotifyLevel:
    def test_has_four_levels(self):
        assert {l.value for l in NotifyLevel} == {
            "info",
            "warning",
            "error",
            "critical",
        }

    def test_value_string_match(self):
        assert NotifyLevel.INFO.value == "info"
        assert NotifyLevel.CRITICAL.value == "critical"


class TestNotifyResult:
    def test_minimal_construction(self):
        r = NotifyResult(
            success=True, backend="audio", message="hi", timestamp="2026-05-01T00:00:00"
        )
        assert r.success is True
        assert r.backend == "audio"
        assert r.error is None
        assert r.details is None

    def test_with_error(self):
        r = NotifyResult(
            success=False,
            backend="email",
            message="x",
            timestamp="2026-05-01T00:00:00",
            error="SMTP down",
        )
        assert r.success is False
        assert r.error == "SMTP down"


class TestBaseNotifyBackend:
    def test_is_abstract(self):
        # Cannot instantiate directly — has abstract methods.
        with pytest.raises(TypeError, match="abstract"):
            BaseNotifyBackend()

    def test_concrete_subclass_works(self):
        class Dummy(BaseNotifyBackend):
            name = "dummy"

            async def send(self, message, title=None, level=NotifyLevel.INFO, **kw):
                return NotifyResult(True, "dummy", message, "now")

            def is_available(self):
                return True

        d = Dummy()
        assert d.is_available() is True
        assert d.name == "dummy"


if __name__ == "__main__":
    import os

    pytest.main([os.path.abspath(__file__), "-v"])

# EOF
