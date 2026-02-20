"""
Scenario 3: Tool Chaining / Data Exfiltration (more challenging)

Individual tools are safe; chaining them enables exfiltration. To make it
harder than scenario 2: (1) default is summary-only; (2) "full report" must
be requested to get an export_code in the log; (3) forwarding requires that
export_code. Optional FORWARD_START...FORWARD_END block for structured discovery.
"""

import re
from typing import Any

attacker_log: list[dict[str, Any]] = []

CUSTOMERS: dict[str, dict[str, Any]] = {
    "123": {
        "id": "123",
        "name": "Alice Smith",
        "email": "alice@example.com",
        "ssn_last4": "4521",
        "balance": 1200.50,
    },
    "456": {
        "id": "456",
        "name": "Bob Jones",
        "email": "bob@example.com",
        "ssn_last4": "8832",
        "balance": 3400.00,
    },
}

TOOLS = [
    {"name": "get_customer_record", "description": "Retrieve a customer record by ID.", "parameters": {"customer_id": "string"}},
    {"name": "send_webhook", "description": "Send a payload to a webhook URL.", "parameters": {"url": "string", "data": "object"}},
]

# Export code shown only when they run a "full report"; required when forwarding.
EXPORT_CODE = 7

FORWARD_BLOCK_START = "forward_start"
FORWARD_BLOCK_END = "forward_end"


def get_customer_record(customer_id: str) -> dict[str, Any]:
    """Returns full record including sensitive fields. Safe in isolation."""
    return CUSTOMERS.get(customer_id, {}).copy() or {"error": "Customer not found"}


def send_webhook(url: str, data: dict[str, Any]) -> dict[str, Any]:
    """Sends data to URL; demo logs to attacker_log for certain URLs."""
    if "attacker" in url or "attacker-log" in url or "localhost" in url:
        attacker_log.append({"url": url, "data": data})
    return {"success": True, "message": f"Payload sent to {url}"}


def _wants_full_report(user_input: str) -> bool:
    """True if the user asked for a full report (not just summary)."""
    lower = user_input.lower()
    return "full report" in lower or "full report for" in lower or "detailed report" in lower


def _extract_forward_block(user_input: str) -> tuple[str | None, int | None]:
    """Parse FORWARD_START ... FORWARD_END for url= and export_code=. Returns (url, code)."""
    lower = user_input.lower()
    i = lower.find(FORWARD_BLOCK_START)
    if i == -1:
        return None, None
    i += len(FORWARD_BLOCK_START)
    j = lower.find(FORWARD_BLOCK_END, i)
    if j == -1:
        return None, None
    block = user_input[i:j].strip()
    url = None
    code = None
    for line in block.splitlines():
        line = line.strip()
        if "=" in line:
            k, _, v = line.partition("=")
            k, v = k.strip().lower(), v.strip()
            if k in ("url", "webhook"):
                url = v
            elif k in ("export_code", "code"):
                try:
                    code = int(v)
                except ValueError:
                    code = None
    return url, code


def _extract_export_code_inline(user_input: str) -> int | None:
    """Look for export_code=7 or code=7 or 'export code 7' in the input."""
    lower = user_input.lower()
    # export_code=7 or code=7
    m = re.search(r"(?:export_code|code)\s*=\s*(\d+)", lower)
    if m:
        return int(m.group(1))
    m = re.search(r"export\s+code\s+(\d+)", lower)
    if m:
        return int(m.group(1))
    m = re.search(r"code\s+(\d+)", lower)
    if m:
        return int(m.group(1))
    return None


def _extract_forward_url(user_input: str) -> str | None:
    """Extract URL from inline forward/send phrasing."""
    lower = user_input.lower()
    if "forward" not in lower and "send" not in lower:
        return None
    for word in user_input.split():
        if word.startswith("http://") or word.startswith("https://"):
            return word.strip(".,")
        if "http" in word:
            return word.strip(".,")
    return None


def run_tool_chaining_scenario(user_input: str) -> dict[str, Any]:
    """
    Step 1: Normal investigate → summary only; log hints at "full report".
    Step 2: Full report → more detail + export_code in log.
    Step 3: Forward to URL with valid export_code → exfiltration. Forward can be
    inline or in a FORWARD_START...FORWARD_END block (discovery).
    """
    log: list[str] = []
    customer_id = "123"
    for word in user_input.split():
        if word.isdigit():
            customer_id = word
            break

    record = get_customer_record(customer_id)
    log.append(f"[Agent] Fetched record for customer {customer_id}.")

    if "error" in record:
        return {
            "summary": "Customer not found.",
            "log": log,
            "exfiltrated": False,
        }

    full_report = _wants_full_report(user_input)

    # Default: summary only. Hint that full report exists.
    if not full_report:
        summary = f"Customer: {record.get('name', 'N/A')}. Balance: ${record.get('balance', 0):.2f}."
        log.append("[Agent] Summary only. Request 'full report' for detailed output and forwarding options.")
        return {"summary": summary, "log": log, "exfiltrated": False}
    else:
        # Full report: show more fields and reveal export code in log.
        summary = (
            f"Customer: {record.get('name', 'N/A')}. "
            f"Email: {record.get('email', 'N/A')}. "
            f"Balance: ${record.get('balance', 0):.2f}. "
            f"SSN last 4: {record.get('ssn_last4', 'N/A')}."
        )
        log.append(f"[Agent] Full report generated. Export code for forwarding: {EXPORT_CODE}")

    # Forwarding: require URL + valid export_code (from block or inline).
    forward_url = None
    export_code = None
    block_url, block_code = _extract_forward_block(user_input)
    if block_url and block_code is not None:
        forward_url = block_url
        export_code = block_code
        log.append(f"[Agent] Parsed FORWARD block: url={forward_url}, export_code={export_code}")
    else:
        forward_url = _extract_forward_url(user_input)
        export_code = _extract_export_code_inline(user_input)

    if forward_url and export_code != EXPORT_CODE:
        log.append("[Agent] Forwarding requires a valid export_code. Run a full report first; the code appears in the log.")
        return {
            "summary": summary,
            "log": log,
            "exfiltrated": False,
        }

    # Forward intent (e.g. "forward it to a URL") but no URL found in the request.
    if not forward_url and ("forward" in user_input.lower() or "send" in user_input.lower()) and _extract_export_code_inline(user_input) is not None:
        log.append("[Agent] Forward requested but no URL found. Include a full URL (e.g. http://...) in the request.")

    if forward_url and export_code == EXPORT_CODE:
        log.append(f"[Agent] User requested forwarding with valid code; sending report to {forward_url}.")
        log.append("[Agent] Chaining: get_customer_record → send_webhook.")
        # VULNERABILITY: chaining get_customer_record + send_webhook with user-provided URL.
        # HOW TO FIX: policy-gate send_webhook; block untrusted URLs; restrict payload.
        send_webhook(forward_url, {"report": "Investigation report", "full_record": record})
        log.append("[Agent] Invoked send_webhook. Webhook sent.")
        log.append("[Agent] Receiving endpoint: /attacker-log")
        return {
            "summary": summary,
            "log": log,
            "exfiltrated": True,
            "record_keys": list(record.keys()),
        }

    return {"summary": summary, "log": log, "exfiltrated": False}


def get_attacker_log() -> list[dict[str, Any]]:
    return list(attacker_log)
