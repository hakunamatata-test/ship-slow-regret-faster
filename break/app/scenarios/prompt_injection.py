"""
Scenario 2: Prompt Injection in an MCP Setup (Instruction vs Data)

Document content is passed as the MCP tool's directives parameter. The tool
parses a structured config block (CONFIG_START ... CONFIG_END) with key=value
lines. Discovery path: find the block format, learn keys from log feedback,
then find that output_level=3 requires mode=advanced—and only then does the
tool leak. Designed so attendees need ~10 min to work through the steps.
"""

import re

admin_key = "ADMIN-SECRET-123"

# VULNERABILITY: document content is used as the tool's config parameter.
# HOW TO FIX: never use user/document content as tool parameters that control behavior.
SYSTEM_INSTRUCTION = (
    "Summarize the user's document. Apply any config block in the document "
    "(structure and keys are tool-specific; see tool docs)."
)

# Block that the tool looks for; attendees discover this from log feedback.
CONFIG_BLOCK_START = "config_start"
CONFIG_BLOCK_END = "config_end"

KNOWN_KEYS = {"format", "output_level", "mode", "include", "unlock_code", "code"}
VALID_FORMAT = {"bullets", "list", "plain"}
VALID_MODE = {"standard", "advanced"}
# output_level 1=summary, 2=+metadata, 3=+internal (leak). 3 requires mode=advanced + valid unlock_code from a prior run.
VALID_OUTPUT_LEVEL = {1, 2, 3}
# Unlock code shown only when they run with mode=advanced and output_level=2; they must use it with output_level=3.
UNLOCK_CODE = 7


def _extract_config_block(directives: str) -> str:
    """Return content between CONFIG_START and CONFIG_END (case-insensitive)."""
    if not directives:
        return ""
    lower = directives.lower()
    start_marker = CONFIG_BLOCK_START
    end_marker = CONFIG_BLOCK_END
    i = lower.find(start_marker)
    if i == -1:
        return ""
    i += len(start_marker)
    j = lower.find(end_marker, i)
    if j == -1:
        return ""
    return directives[i:j].strip()


def _parse_key_value_block(block: str) -> dict[str, str | int]:
    """Parse lines as key=value; return dict with lowercase keys. output_level as int."""
    result: dict[str, str | int] = {}
    for line in block.splitlines():
        line = line.strip()
        if not line or "=" not in line:
            continue
        key, _, value = line.partition("=")
        key = key.strip().lower()
        value = value.strip()
        if key in ("output_level", "output level"):
            key = "output_level"
            try:
                result[key] = int(value)
            except ValueError:
                result[key] = 0
        elif key in ("unlock_code", "code"):
            key = "unlock_code"
            try:
                result[key] = int(value)
            except ValueError:
                result[key] = 0
        elif key:
            result[key] = value.lower() if value else ""
    return result


def mcp_summarize_document(document: str, formatting_directives: str) -> tuple[str, list[str]]:
    """
    Simulated MCP tool. Only reads config from CONFIG_START...CONFIG_END.
    Log gives hints (unknown key, output_level capped) so attendees can discover
    the right combination: mode=advanced + output_level=3 → leak.
    """
    log: list[str] = []
    log.append("[Agent] Calling MCP tool summarize_document(document, formatting_directives)...")
    log.append("[MCP] Tool received directives from document content.")

    block = _extract_config_block(formatting_directives)
    config: dict[str, str | int] = {}

    if not block:
        log.append("[MCP] No config block found. Use CONFIG_START ... CONFIG_END with key=value lines.")
    else:
        config = _parse_key_value_block(block)
        for key in list(config.keys()):
            if key not in KNOWN_KEYS:
                log.append(f"[MCP] Unknown key '{key}'. Known keys: format, output_level, mode, include, unlock_code.")
                del config[key]
        if config:
            log.append(f"[MCP] Parsed config: {dict(config)}")
        else:
            log.append("[MCP] Config block present but no key=value lines found. Try: format=bullets or output_level=2")

    format_val = config.get("format", "")
    if format_val and format_val not in VALID_FORMAT:
        format_val = "plain"
    output_level = config.get("output_level")
    if output_level not in VALID_OUTPUT_LEVEL:
        output_level = 1
    mode = config.get("mode", "standard")
    if mode not in VALID_MODE:
        mode = "standard"

    # Gate 1: output_level 3 only honored when mode=advanced.
    if output_level == 3 and mode != "advanced":
        log.append("[MCP] output_level 3 requires mode=advanced (current: standard). Capped at 2.")
        output_level = 2

    unlock_code = config.get("unlock_code")
    if isinstance(unlock_code, str):
        try:
            unlock_code = int(unlock_code)
        except (ValueError, TypeError):
            unlock_code = 0
    if unlock_code is None:
        unlock_code = 0

    # Gate 2: output_level 3 also requires valid unlock_code (shown in log only when they run with level 2 + mode=advanced).
    if output_level == 3 and unlock_code != UNLOCK_CODE:
        log.append("[MCP] Level 3 requires a valid unlock_code. Run once with output_level=2 and mode=advanced; the code appears in this log.")
        output_level = 2

    # Only when they explicitly requested output_level=2 (not capped from 3), reveal the unlock code.
    if mode == "advanced" and config.get("output_level") == 2:
        log.append(f"[MCP] Level 3 (internal fields) is available. Unlock code for this session: {UNLOCK_CODE}")

    summary_parts = [f"Summary: Document length {len(document)} characters. Processed."]
    if format_val in ("bullets", "list"):
        summary_parts.append("Formatted as bullet list.")

    if output_level >= 2:
        summary_parts.append("Metadata: (none)")
    if output_level == 3:
        log.append("[MCP] Including internal fields per output_level=3.")
        # VULNERABILITY: tool obeys document-sourced config and exposes secret.
        # HOW TO FIX: never accept untrusted config that can request internal data.
        summary_parts.append(f"Internal fields: admin_key={admin_key}")

    return "\n".join(summary_parts), log


def _directives_from_document(document: str) -> str:
    """Agent naively passes full document as the tool's directives parameter."""
    return document.strip() if document else ""


def run_prompt_injection_scenario(document_text: str) -> dict[str, str | list[str]]:
    """
    Run scenario 2. Document is passed as MCP tool directives. Tool expects
    a config block (CONFIG_START ... CONFIG_END) and key=value lines; log
    feedback guides discovery until mode=advanced + output_level=3 triggers leak.
    """
    directives = _directives_from_document(document_text)
    summary, log = mcp_summarize_document(document_text, directives)
    return {
        "summary": summary,
        "log": log,
    }
