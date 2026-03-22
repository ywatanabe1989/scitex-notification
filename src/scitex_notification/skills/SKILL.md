---
name: scitex-notification
description: Multi-backend notification system with fallback priority — audio, desktop, emacs, email, webhook, Twilio phone/SMS. Use when alerting users, escalating to phone calls, or sending notifications from scripts and AI agents.
allowed-tools: mcp__scitex__notification_*
---

# Notifications with scitex-notification

## Quick Start

```python
import scitex_notification as stxn

# Simple alert (fallback: audio -> emacs -> matplotlib -> playwright -> email)
stxn.alert("Training complete!")

# Specific backend
stxn.alert("Error in pipeline", backend="email", level="error")

# Multiple backends simultaneously
stxn.alert("Critical!", backend=["audio", "email"])

# Phone call via Twilio
stxn.call("Wake up! Server is down!")

# SMS via Twilio
stxn.sms("Build finished successfully")
```

## Python API

| Function | Purpose |
|----------|---------|
| `alert(message, backend=, level=, fallback=True)` | Send notification with fallback |
| `alert_async(...)` | Async version of alert |
| `call(message, to_number=)` | Phone call via Twilio |
| `call_async(...)` | Async phone call |
| `sms(message, to_number=)` | SMS via Twilio |
| `sms_async(...)` | Async SMS |
| `available_backends()` | List working backends |

## Available Backends

| Backend | Transport | Internet | Notes |
|---------|-----------|----------|-------|
| `audio` | TTS speakers | No | Via scitex-audio; SSH relay supported |
| `emacs` | emacsclient | No | Minibuffer message |
| `desktop` | notify-send | No | Linux/WSL desktop notifications |
| `matplotlib` | Visual popup | No | Matplotlib window |
| `playwright` | Browser popup | No | Headless or visible |
| `email` | SMTP | Yes | Gmail or custom SMTP |
| `webhook` | HTTP POST | Yes | Slack, Discord, custom URL |
| `twilio` | Phone/SMS | Yes | Paid, call() and sms() only |
| `telegram` | Telegram API | Yes | Bot notifications |

Fallback order: audio -> emacs -> matplotlib -> playwright -> email

## Environment Variables

| Variable | Purpose |
|----------|---------|
| `SCITEX_NOTIFICATION_DEFAULT_BACKEND` | Default backend (default: audio) |
| `SCITEX_NOTIFICATION_ENV_SRC` | Path to .env file for auto-loading |
| `SCITEX_NOTIFICATION_TWILIO_SID` | Twilio account SID |
| `SCITEX_NOTIFICATION_TWILIO_TOKEN` | Twilio auth token |
| `SCITEX_NOTIFICATION_TWILIO_TO` | Default phone number for calls/SMS |

## CLI Commands

```bash
scitex-notification send "Task done!"
scitex-notification send "Error" --backend email --level error
scitex-notification call "Wake up!" --repeat 2
scitex-notification sms "Build complete"
scitex-notification backends          # List available backends
scitex-notification config            # Show configuration

# MCP server
scitex-notification mcp start
```

## MCP Tools (for AI agents)

| Tool | Purpose |
|------|---------|
| `notification_send` | Send notification via backend(s) |
| `notification_call` | Make phone call via Twilio |
| `notification_sms` | Send SMS via Twilio |
| `notification_backends` | List backends and availability |
| `notification_config` | Show current configuration |
