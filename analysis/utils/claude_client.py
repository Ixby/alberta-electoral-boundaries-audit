"""
claude_client.py — Claude CLI wrapper for all sentiment analysis scripts.

Provides resolve_claude() and call_claude() so every script uses a single,
tested implementation instead of inline subprocess boilerplate.

Dependencies:
  Forward:  (consumed by sentiment scripts)
  Backward: (stdlib only — no project imports)
"""
from __future__ import annotations

import json
import logging
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

logger = logging.getLogger(__name__)


def resolve_claude() -> str:
    """Return the full path to the claude CLI executable.

    On Windows the npm-installed claude.cmd wrapper is preferred because
    a bare 'claude' is not on the subprocess PATH even when available in
    interactive shells.
    """
    if sys.platform == "win32":
        npm_bin = Path(os.environ.get("APPDATA", "")) / "npm" / "claude.cmd"
        if npm_bin.exists():
            return str(npm_bin)
    return shutil.which("claude") or shutil.which("claude.cmd") or "claude"


# Resolved once at import time; scripts import this constant directly.
CLAUDE_CMD: str = resolve_claude()


def call_claude(
    text:          str,
    system_prompt: str,
    json_schema:   str,
    *,
    model:   str = "sonnet",
    timeout: int = 180,
) -> dict:
    """Invoke the Claude CLI and return the parsed structured-output dict.

    Returns {} on any failure (timeout, non-zero exit, JSON parse error).
    Callers should treat {} as an error and log/skip accordingly.

    Args:
        text:          The submission or Hansard turn text (sent via stdin).
        system_prompt: The task instruction passed as the positional prompt arg.
        json_schema:   JSON string of the schema for --json-schema validation.
        model:         Claude model alias (default "sonnet").
        timeout:       Subprocess timeout in seconds (default 180).
    """
    cmd = [
        CLAUDE_CMD, "--print",
        "--model",         model,
        "--output-format", "json",
        "--json-schema",   json_schema,
        "--no-session-persistence",
        system_prompt,
    ]
    try:
        result = subprocess.run(
            cmd,
            input=text,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=timeout,
        )
        if result.returncode != 0:
            logger.warning("Claude CLI error (rc=%d): %s",
                           result.returncode, result.stderr[:200])
            return {}

        outer = json.loads(result.stdout)

        # --json-schema puts validated output in "structured_output"
        structured = outer.get("structured_output")
        if isinstance(structured, dict):
            return structured

        # Fallback: "result" field may contain a raw JSON string
        inner = outer.get("result", "")
        if isinstance(inner, str):
            # Strip markdown code fence if present
            m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", inner, re.DOTALL)
            if m:
                inner = m.group(1)
            inner = inner.strip()
            if inner.startswith("{"):
                try:
                    return json.loads(inner)
                except json.JSONDecodeError:
                    pass

        logger.warning("Claude CLI: could not parse structured output")
        return {}

    except subprocess.TimeoutExpired:
        logger.warning("Claude CLI: timeout after %ds", timeout)
        return {}
    except json.JSONDecodeError as e:
        logger.warning("Claude CLI: JSON decode error: %s", e)
        return {}
    except Exception as e:
        logger.warning("Claude CLI: unexpected error: %s", e)
        return {}
