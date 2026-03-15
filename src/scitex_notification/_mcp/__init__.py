#!/usr/bin/env python3
# Timestamp: "2026-03-16 (ywatanabe)"
# File: /home/ywatanabe/proj/scitex-notification/src/scitex_notification/_mcp/__init__.py

"""MCP handlers and schemas for scitex_notification server."""

from .handlers import (
    available_backends_handler,
    get_config_handler,
    list_backends_handler,
    notify_handler,
)
from .tool_schemas import get_tool_schemas

__all__ = [
    "get_tool_schemas",
    "notify_handler",
    "list_backends_handler",
    "available_backends_handler",
    "get_config_handler",
]

# EOF
