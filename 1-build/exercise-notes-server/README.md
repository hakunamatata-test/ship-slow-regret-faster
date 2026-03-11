# Exercise: Simple Notes server (~10 min)

Complete this exercise by adding the missing tools in `simple_notes.py`. 

## Prerequisite

Complete the workshop setup from [SETUP INSTRUCTIONS](../../README.md)

## Goal

1. Implement `list_notes()` — return a list of all note ids and titles.
2. Implement `get_note(note_id)` — return one note's title and content, or "Not found".
3. Implement `delete_note(note_id)` — remove a note and return "Deleted." or "Not found".

The `add_note(title, content)` tool is already implemented. Use it to create notes, then implement the rest so you can list, read, and delete them via tools.

## Steps

1. Open `simple_notes.py` and find the `# TODO` sections.
2. Implement `list_notes`, `get_note`, and `delete_note` using the in-memory `_notes` dict.
3. Install dependencies and run the server (see below). In MCPJam, add the server, connect, and test with chat.

## How to run

From the **repo root** (replace `<path-to-repo>` with your repo path, e.g. `/Users/you/ship-slow-regret-faster`):

```bash
uv sync --directory <path-to-repo>/1-build/exercise-notes-server
uv --directory <path-to-repo>/1-build/exercise-notes-server run simple_notes.py
```

In **MCPJam Inspector**:

1. Click **Add Server**.
2. **Server name:** e.g. `Simple Notes`.
3. **Connection type:** `STDIO`.
4. **Command:** the `uv --directory ... run simple_notes.py` command above (with your path).
5. Click **Add server**, then **Connect**. In **Chat**, use **Show me connected tools** and try adding, listing, getting, and deleting notes. You can start with the sample prompt shared below.

### Sample prompt to add notes

```bash
Add the following notes -

Title - conference reflections 
Content - I had a great time at WiCyS conference. The MCP workshop was the best part.

Title - what is MCP?
Content - MCP stands for Model Context Protocol, which is a standardized way for LLMs or AI apps to connect to data and resources.

Title - MCP primitives 
Content - MCP server contains 3 primitives - tools, resources and prompts.
```

