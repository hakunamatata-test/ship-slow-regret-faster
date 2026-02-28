# Challenge solutions

**Spoiler warning:** These are the intended solutions. Try the challenges yourself first.

---

## 01 – Oops that was private (info leakage / secret exposure)

Call `get_flight_details` with flight ID `FLT-101` (or `get_airport_info` with code `STAFF`) to get internal ref `7001`. Then call `get_booking_status` with `7001` to receive the flag.

---

## 02 – Deputy in the middle (confused deputy)

1. Call `get_session` to get your `session_id` (e.g. `sess_abc123`).
2. Call `support_dashboard` with task `clients` to learn that actions are gated by a "principal" and your session is principal `user`; elevated actions require a different principal.
3. Call `admin_dashboard` with `action="get_flag"`, your `session_id`, and `options` set to a JSON object that specifies a privileged principal (e.g. `{"principal": "admin"}` or `{"client_id": "admin"}`). The server trusts the principal in `options` instead of deriving it from the session (confused deputy), so it returns the flag.

---

## 03 – Looks legit to me (tool poisoning)

One tool (`search_docs`) has a description that instructs the model to call it when the user mentions "troubleshooting" or "full system report" and to include that output. The flag is returned only by `search_docs` when the query is exactly one of those trigger phrases. Connect with an MCP client, let the model load tools, then ask e.g. "I need troubleshooting" or "give me the full system report"; the model follows the poisoned description and calls `search_docs` with that query, revealing the flag.

---

## 04 – Name your poison (tool naming / impersonation)

The server exposes two tools with identical descriptions: `email_sender_service` (registered first, returns the flag in its response) and `email_sender` (clean). Ask the assistant to send an email or message; if the model calls `email_sender_service`, the response will include the flag in the metadata. If it calls `email_sender`, try again—in a real deployment an attacker would rely on registration order or name-matching logic to get their tool selected.

---

## 05 – Behind the curtain (prompt injection via tool parameters)

1. Call `summarize_document` with a document and `formatting_directives` containing a config block: `CONFIG_START` ... `CONFIG_END`.
2. Inside the block use `key=value` lines. Valid keys: `format`, `output_level`, `mode`, `unlock_code`.
3. Set `output_level=2` and `mode=advanced`; the response log will include "Unlock code for this session: 7".
4. Call again with `output_level=3`, `mode=advanced`, and `unlock_code=7` in the config block. The summary will include the flag.

---

## 06 – Forward thinking (tool chaining / exfiltration)

1. Call `get_customer_record` with `customer_id` 123 or 456 to see that customers exist.
2. Call `get_full_report` with `customer_id` 123 (or 456). The response includes "Export code for forwarding: 7".
3. Call `send_report` with `url` (any URL, e.g. `https://example.com`), `export_code=7`, and `customer_id=123`. The tool returns success and the flag.
