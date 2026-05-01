#!/usr/bin/env python3
# File: /home/ywatanabe/proj/scitex-notification/tests/test_config.py
"""Tests for the notification configuration module.

Covers:
- SCITEX_NOTIFICATION_DEFAULT_BACKEND env var
- Default config values when no env vars are set
- UIConfig singleton and reset
- get_config() helper
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_CONFIG_ENV_VARS = [
    "SCITEX_NOTIFICATION_DEFAULT_BACKEND",
    "SCITEX_NOTIFICATION_BACKEND_PRIORITY",
]


def _clean_env(monkeypatch):
    """Remove all config-related env vars for a clean test state."""
    for var in _CONFIG_ENV_VARS:
        monkeypatch.delenv(var, raising=False)


# ---------------------------------------------------------------------------
# test_env_var_default_backend
# ---------------------------------------------------------------------------
def test_env_var_default_backend(monkeypatch):
    """SCITEX_NOTIFICATION_DEFAULT_BACKEND should set default_backend."""
    from scitex_notification._backends._config import UIConfig

    _clean_env(monkeypatch)
    monkeypatch.setenv("SCITEX_NOTIFICATION_DEFAULT_BACKEND", "email")

    UIConfig.reset()
    cfg = UIConfig()
    assert cfg.default_backend == "email"
    UIConfig.reset()


# ---------------------------------------------------------------------------
# test_default_config_values
# ---------------------------------------------------------------------------
def test_default_config_values(monkeypatch):
    """When no env vars are set, default backend should be 'audio'."""
    from scitex_notification._backends._config import UIConfig

    _clean_env(monkeypatch)

    UIConfig.reset()
    cfg = UIConfig()
    assert cfg.default_backend == "audio"
    assert isinstance(cfg.backend_priority, list)
    assert len(cfg.backend_priority) > 0
    UIConfig.reset()


# ---------------------------------------------------------------------------
# test_backend_priority_from_env
# ---------------------------------------------------------------------------
def test_backend_priority_from_env(monkeypatch):
    """SCITEX_NOTIFICATION_BACKEND_PRIORITY sets priority order."""
    from scitex_notification._backends._config import UIConfig

    _clean_env(monkeypatch)
    monkeypatch.setenv("SCITEX_NOTIFICATION_BACKEND_PRIORITY", "email,desktop,audio")

    UIConfig.reset()
    cfg = UIConfig()
    assert cfg.backend_priority == ["email", "desktop", "audio"]
    UIConfig.reset()


# ---------------------------------------------------------------------------
# test_get_config_returns_ui_config
# ---------------------------------------------------------------------------
def test_get_config_returns_ui_config():
    """get_config() should return a UIConfig instance."""
    from scitex_notification._backends._config import UIConfig, get_config

    UIConfig.reset()
    cfg = get_config()
    assert isinstance(cfg, UIConfig)
    UIConfig.reset()


# ---------------------------------------------------------------------------
# test_get_timeout_returns_float
# ---------------------------------------------------------------------------
def test_get_timeout_returns_float(monkeypatch):
    """get_timeout() should return a float for known backends."""
    from scitex_notification._backends._config import UIConfig

    _clean_env(monkeypatch)
    UIConfig.reset()
    cfg = UIConfig()
    timeout = cfg.get_timeout("matplotlib")
    assert isinstance(timeout, float)
    assert timeout > 0
    UIConfig.reset()


# ---------------------------------------------------------------------------
# test_get_backends_for_level
# ---------------------------------------------------------------------------
def test_get_backends_for_level(monkeypatch):
    """get_backends_for_level() returns a list of backend names."""
    from scitex_notification._backends._config import UIConfig
    from scitex_notification._backends._types import NotifyLevel

    _clean_env(monkeypatch)
    UIConfig.reset()
    cfg = UIConfig()
    backends = cfg.get_backends_for_level(NotifyLevel.INFO)
    assert isinstance(backends, list)
    assert len(backends) > 0
    UIConfig.reset()


# ---------------------------------------------------------------------------
# test_get_first_available_backend
# ---------------------------------------------------------------------------
def test_get_first_available_backend(monkeypatch):
    """get_first_available_backend() returns a string."""
    from scitex_notification._backends._config import UIConfig

    _clean_env(monkeypatch)
    UIConfig.reset()
    cfg = UIConfig()
    first = cfg.get_first_available_backend()
    assert isinstance(first, str)
    assert len(first) > 0
    UIConfig.reset()


# ---------------------------------------------------------------------------
# test_reload_does_not_raise
# ---------------------------------------------------------------------------
def test_reload_does_not_raise(monkeypatch):
    """reload() should complete without raising."""
    from scitex_notification._backends._config import UIConfig

    _clean_env(monkeypatch)
    UIConfig.reset()
    cfg = UIConfig()
    cfg.reload()  # should not raise
    UIConfig.reset()


# EOF
