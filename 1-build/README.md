# BUILD the MCP

Welcome to Phase 1 of the workshop! In this phase you will **build** MCP (Model Context Protocol) servers and run them through [**MCPJam Inspector**](https://github.com/MCPJam/inspector). You'll see a demo of a full-featured server, do a short hands-on exercise during the session, and have a take-home project to extend the demo server.

---

## Prerequisites

Complete the workshop setup from the [main repo README](../../README.md) (clone repo, install uv, Node.js/npx, run MCPJam Inspector, join Slack).

---

## Build repo structure

The `1-build/` folder contains two MCP server projects:

| Project | What it is | When you use it |
|--------|------------|------------------|
| **[local_discovery/](./local_discovery/README.md)** | Full MCP server for discovering local restaurants, events, and venues. Uses Google Places API and Ticketmaster Discovery API. Exposes tools, resources, and prompts. | **Demo during the workshop**; then **take-home exercise** to extend it with more tools (see [Local Discovery README](./local_discovery/README.md)). |
| **[exercise-notes-server/](./exercise-notes-server/README.md)** | Minimal Notes server scaffold. You add the missing tools (`list_notes`, `get_note`, `delete_note`) and wire the `note://{id}` resource. No API keys required. | **Hands-on during the workshop** (~10 min). |

- **During the workshop:** The facilitator will demo **Local Discovery**. You will then complete the **Simple Notes** exercise in `exercise-notes-server/` by implementing the TODO tools and resource.
- **Take-home:** Extend **Local Discovery** by adding more tools, resources, or prompts using ideas in [TOOL_IDEAS.md](./local_discovery/TOOL_IDEAS.md) (see [Local Discovery README](./local_discovery/README.md)).

---

## 1. Run MCPJam Inspector

1. Start MCPJam Inspector:

   ```bash
   npx @mcpjam/inspector@latest
   ```

2. MCPJam Inspector will open in your browser.
3. Sign in to use freely available models.

---

## 2. Workshop exercise: Simple Notes server

During the session, complete the **Simple Notes** exercise (~10 min). No API keys required.

- **Instructions:** [exercise-notes-server/README.md](./exercise-notes-server/README.md)
- **Run in MCPJam:** Add a server with **Connection type** `STDIO` and **Command** (replace `<path>` with your repo path):

  ```bash
  uv --directory <path>/1-build/exercise-notes-server run simple_notes.py
  ```

Install dependencies first: `uv sync --directory <path>/1-build/exercise-notes-server`.

---

## 3. Take home exercise: Local Discovery server

Follow the [Local Discovery README](./local_discovery/README.md) for API keys, `.env` setup, and running the server. Summary:

1. Install dependencies and add a `.env` file with `GOOGLE_API_KEY` and `TICKETMASTER_API_KEY` (see [local_discovery/README.md](./local_discovery/README.md#api-keys-and-env)).
2. In MCPJam, click **Add Server**. Use **Connection type** `STDIO` and **Command** (replace `<path>` with your repo path):

   ```bash
   uv --directory <path>/1-build/local_discovery run local_discovery.py
   ```

3. Click **Add server**, then **Connect**. In **Chat**, use **Show me connected tools** to try the demo.
4. Add more tools, resources and prompts to extend functionality

---

## Project structure

```
1-build/
├── README.md                    # This file
├── local_discovery/             # Local Discovery MCP server (demo + take-home)
│   ├── README.md                # Setup, API keys, run instructions, take-home exercise
│   ├── pyproject.toml
│   ├── local_discovery.py       # MCP server entrypoint
│   ├── api_clients.py           # Google Places & Ticketmaster clients
│   ├── GOOGLE_PLACES_SETUP.md
│   ├── TICKETMASTER_SETUP.md
│   ├── API_REFERENCE.md
│   ├── TOOL_IDEAS.md            # Ideas for take-home: add more tools
│   └── .env                     # Create locally; add to .gitignore so you do not commit
└── exercise-notes-server/       # Workshop exercise (~10 min)
    ├── README.md                # Exercise instructions
    ├── pyproject.toml
    └── simple_notes.py          # Starter scaffold (implement list_notes, get_note, delete_note, note resource)
```

---

## Documentation

- **[local_discovery/README.md](./local_discovery/README.md)** — Local Discovery setup, API keys, run instructions, tools/resources overview, take-home exercise.
- **[exercise-notes-server/README.md](./exercise-notes-server/README.md)** — Simple Notes exercise steps and how to run the server.
