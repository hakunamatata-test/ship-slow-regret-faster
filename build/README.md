# BUILD the MCP

This phase focuses on **building** a real MCP (Model Context Protocol) server: **Local Discovery & Events**. You will run it through [**MCPJam Inspector**](https://github.com/MCPJam/inspector), and interact with it via chat and tools.

**Story:** *"Help me discover local restaurants, events, and activities. Find places, check dine-in/delivery/vegetarian options, and explore events and venues in my area."*

The server exposes tools and resources so an AI (or user) can search for restaurant (Google Places), check dining options for those places, and search for events and venues (Ticketmaster Discovery). Stored place and event IDs are exposed as MCP resources for follow-up queries.

---

## Prerequisites

- **uv** (Python package manager) — [install](https://docs.astral.sh/uv/getting-started/installation/)
- **Node.js** and **npm** (for MCPJam Inspector) — [install](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm)  
  On macOS, if `npx` is not available after installing Node.js:
  ```bash
  brew update && brew install node
  ```
- This repo cloned locally

---

## Troubleshooting: npm / Node.js on macOS

If you hit errors with **npm** or **Node.js** on a Mac during the Build phase, try the following.

**You may not need `npm install`.** For this workshop you only need **Node and npm** so that **`npx @mcpjam/inspector@latest`** works (npx runs the Inspector without a global install). If something is asking you to run `npm install` in a project, that may be from another step; for MCPJam Inspector, `npx` is enough.

1. **Check Node and npm**
   ```bash
   node -v    # expect v18 or newer
   npm -v
   npx -v
   ```
   If any of these fail, Node isn’t installed or isn’t on your `PATH`.

2. **Install or reinstall Node (Homebrew)**
   ```bash
   brew update
   brew install node
   ```
   Then close and reopen your terminal and run `node -v` and `npx -v` again.

3. **Permission errors (EACCES)**
   - Don’t use `sudo npm install` or `sudo npx`.
   - If you get EACCES when npm writes to a directory, either:
     - Use a version manager so everything lives under your home directory: [nvm](https://github.com/nvm-sh/nvm) or [fnm](https://github.com/Schniz/fnm): install Node with that, then use `npx` in a new shell; or
     - Fix npm’s global prefix: [npm docs – fixing permissions](https://docs.npmjs.com/resolving-eacces-permissions-errors-when-installing-packages-globally).

4. **Native build / compile errors**
   Some packages need build tools. On macOS, install Xcode Command Line Tools:
   ```bash
   xcode-select --install
   ```
   Then retry.

5. **Network / proxy**
   If you’re on a corporate network or proxy, npm may need configuration (e.g. `npm config set proxy ...` / `https-proxy`). Ask your IT for the proxy URL and use [npm config](https://docs.npmjs.com/cli/v10/commands/npm-config).

6. **Clear npm cache and retry**
   ```bash
   npm cache clean --force
   npx @mcpjam/inspector@latest
   ```

If it still fails, share the **exact command** you ran and the **full error message** (or a screenshot) with the facilitators.

---

## 1. Install dependencies

From the repo root:

```bash
uv sync --directory build
```

Or from inside `build/`:

```bash
cd build && uv sync
```

---

## 2. API keys and .env

Create a `.env` file inside `build/` (and keep it out of version control). Required variables:

| Variable | Purpose |
|----------|---------|
| `GOOGLE_API_KEY` | Google Cloud API key with **Places API (New)** enabled. |
| `TICKETMASTER_API_KEY` | Ticketmaster Discovery API key. |

Example `.env`:

```env
GOOGLE_API_KEY=your_google_api_key
TICKETMASTER_API_KEY=your_ticketmaster_key
```

- **Google Places API:** See **[GOOGLE_PLACES_SETUP.md](./GOOGLE_PLACES_SETUP.md)** for creating a project, enabling the API, and creating an API key.
- **Ticketmaster Discovery API:** See **[TICKETMASTER_SETUP.md](./TICKETMASTER_SETUP.md)** for signing up and getting an API key.

---

## 3. Run MCPJam Inspector

1. Start MCPJam Inspector:

   ```bash
   npx @mcpjam/inspector@latest
   ```

2. MCPJam Inspector will open up in your browser
3. Sign in to use freely available models.

---

## 4. Add and run the Local Discovery server

1. In MCPJam, click **Add Server**.
2. Configure:
   - **Server name:** e.g. `Local Discovery`
   - **Connection type:** `STDIO` (since the server is run locally)
   - **Command:** (replace `<path>` with the absolute path to your repo, e.g. `/Users/you/ship-fast-regret-faster`):

   ```bash
   uv --directory <path>/build run local_discovery.py
   ```

3. Click **Add server**, then **Connect**.
4. In **Chat**, use **Show me connected tools** to see and use the tools.

---

## Overview

The server uses two external APIs:

- **Google Places API (New)** — place search and place details (dine-in, delivery, takeout, vegetarian, etc.).
- **Ticketmaster Discovery API** — events and venues (search by city, keyword, date range; event/venue details).

---

## Tools

| Tool | Description |
|------|-------------|
| `find_restaurants` | Search restaurants or coffee shops in a city (Google Places). Results are stored for follow-up tools. |
| `check_dine_in_delivery_options` | Check which places offer dine-in, delivery, or takeout (by place IDs or `"latest"`). |
| `check_vegetarian_options` | Check which places serve vegetarian/vegan (by place IDs or `"latest"`). |
| `find_events_in_city` | Find events in a city (Ticketmaster). |
| `find_events_by_keyword` | Find events in a city matching a keyword (artist, team, show name). |
| `find_events_by_date_range` | Find events in a city between two dates. |
| `get_event_details_ticketmaster` | Full event details by ID (price range, venue address, URL). |
| `find_venues_in_city` | Find venues (arenas, theaters, clubs) in a city. |
| `get_venue_details_ticketmaster` | Full venue details by ID. |
| `find_events_at_venue` | Upcoming events at a specific venue. |

## Resources

- **`place://{key}`** — Stored place IDs (e.g. `place://latest` after a place search).
- **`event://{key}`** — Stored event IDs (e.g. `event://latest` after an event search).

## Prompts

- **`plan_concert_and_dinner`** - Prompt to plan a concert and dinner in a given city
- **`full_day_plan`** - Prompt to plan a full day in a given city on a given date. Includes coffee, event and dinner.

---

## Architecture

- **FastMCP** (`mcp.server.fastmcp`) for tool and resource registration.
- **Async HTTP** via `httpx` in `api_clients.py` for Google Places and Ticketmaster.
- **In-memory storage** for the latest place and event IDs; exposed as resources `place://latest` and `event://latest`.
- **Error handling** for missing API keys and failed requests.

---

## Rate limits

- **Google Places API:** Subject to Google Cloud quotas and SKU-based billing (Essentials/Pro). Use field masks to limit requested fields and stay within free tier where possible.
- **Ticketmaster Discovery API:** Subject to Ticketmaster rate limits; check the [developer portal](https://developer.ticketmaster.com/) for current quotas.
- Stay within provider limits to avoid throttling or extra charges.

---

## Project structure

```
build/
├── README.md                 # This file
├── GOOGLE_PLACES_SETUP.md    # Google Places API key setup
├── TICKETMASTER_SETUP.md     # Ticketmaster Discovery API key setup
├── API_REFERENCE.md          # API endpoints and auth reference
├── GOOGLE_PLACES_TOOLS.md    # Optional: extra Google Places tool ideas (free-tier)
├── ADDITIONAL_TOOLS.md       # Optional: more tool ideas
├── TOOL_IDEAS.md             # Optional: tool backlog
├── pyproject.toml            # Project and dependencies (uv)
├── uv.lock                   # Locked dependencies
├── local_discovery.py        # MCP server (tools, resources, entrypoint)
├── api_clients.py            # Google Places & Ticketmaster API clients
├── google_searchtext_response.json  # Sample response (reference)
└── .env                      # API keys (create locally; do not commit)
```

---

## Documentation

- **[GOOGLE_PLACES_SETUP.md](./GOOGLE_PLACES_SETUP.md)** — How to get and configure a Google Places API key.
- **[TICKETMASTER_SETUP.md](./TICKETMASTER_SETUP.md)** — How to get a Ticketmaster Discovery API key.
- **[API_REFERENCE.md](./API_REFERENCE.md)** — API endpoints and authentication used by the server.
- **[TOOL_IDEAS.md](./TOOL_IDEAS.md)** - Ideas to add more tools to this server
