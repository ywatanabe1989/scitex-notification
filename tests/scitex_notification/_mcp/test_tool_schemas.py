#!/usr/bin/env python3
"""Smoke tests for scitex_notification._mcp.tool_schemas."""

import pytest

from scitex_notification._mcp import tool_schemas


def _get_schemas():
    schemas = tool_schemas.get_tool_schemas()
    out = []
    for s in schemas:
        if hasattr(s, "model_dump"):
            out.append(s.model_dump())
        elif isinstance(s, dict):
            out.append(s)
        else:
            out.append(
                {
                    "name": getattr(s, "name", None),
                    "description": getattr(s, "description", None),
                }
            )
    return out


class TestToolSchemas:
    def test_returns_nonempty_list(self):
        schemas = _get_schemas()
        assert isinstance(schemas, list)
        assert len(schemas) > 0

    def test_every_tool_has_name_and_description(self):
        for s in _get_schemas():
            assert s["name"] and isinstance(s["name"], str)
            assert s["description"] and isinstance(s["description"], str)

    def test_names_are_unique(self):
        names = [s["name"] for s in _get_schemas()]
        assert len(names) == len(set(names))


if __name__ == "__main__":
    import os

    pytest.main([os.path.abspath(__file__), "-v"])

# EOF
