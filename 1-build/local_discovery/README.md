# Local Discovery (Demo + Take home exercise)

The Local Discovery MCP server helps you discover local restaurants, events, and activities in a city or area. It uses Google Places API and Ticketmaster Discovery API in its tools to expose this functionality. Using this MCP server, an AI app or user can search for restaurants and dining options(Google Places), and search for events and venues (Ticketmaster Discovery). Stored place and event IDs are exposed as MCP resources for follow-up queries.

Both of these APIs are free to use, and require you to sign up and add the API keys for the server to work as expected. Find more in [API keys and .env](## API keys and .env)

Run the server using MCPJam Inspector, and interact with it via chat and tools. Extend the functionality by adding more tools, resources and prompts using ideas in [TOOL_IDEAS.md](TOOL_IDEAS.md)

## Prerequisite

Complete the workshop setup from [SETUP INSTRUCTIONS](../../README.md)


## API keys and .env

Create a `.env` file inside `1-build/local_discovery`. Make sure to add `.env` to `.gitignore` to avoid committing secrets to the repo. Required variables:

| Variable | Purpose |
|----------|---------|
| `GOOGLE_API_KEY` | Google Cloud API key with **Places API (New)** enabled. |
| `TICKETMASTER_API_KEY` | Ticketmaster Discovery API key. |

Example `.env`:

```env
GOOGLE_API_KEY=your_google_api_key
TICKETMASTER_API_KEY=your_ticketmaster_key
```

- **Google Places API:** See **[GOOGLE_PLACES_SETUP.md](GOOGLE_PLACES_SETUP.md)** for creating a project, enabling the API, and creating an API key.
- **Ticketmaster Discovery API:** See **[TICKETMASTER_SETUP.md](TICKETMASTER_SETUP.md)** for signing up and getting an API key.

---

## Run MCPJam Inspector

1. Start MCPJam Inspector:

   ```bash
   npx @mcpjam/inspector@latest
   ```

2. MCPJam Inspector will open up in your browser
3. Sign in to use freely available models.

---

## Add and run the Local Discovery server

1. In MCPJam, click **Add Server**.
2. Configure:
   - **Server name:** e.g. `Local Discovery`
   - **Connection type:** `STDIO` (since the server is run locally)
   - **Command:** (replace `<path-to-repo>` with your repo path, e.g. `/Users/you/ship-slow-regret-faster`):

   ```bash
   uv --directory <path-to-repo>/1-build/local_discovery run local_discovery.py
   ```

3. Click **Add server**, then **Connect**.
4. In **Chat**, use **Show me connected tools** to see and use the tools.

---

## Take home exercise

Extend the functionality by adding more tools, resources and prompts using ideas in [TOOL_IDEAS.md](TOOL_IDEAS.md)

---

## Server Overview

The server uses two external APIs:

- **Google Places API (New)** — place search and place details (dine-in, delivery, takeout, vegetarian, etc.).
- **Ticketmaster Discovery API** — events and venues (search by city, keyword, date range; event/venue details).

---

### Tools

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

### Resources

- **`place://{key}`** — Stored place IDs (e.g. `place://latest` after a place search).
- **`event://{key}`** — Stored event IDs (e.g. `event://latest` after an event search).

### Prompts

- **`plan_concert_and_dinner`** - Prompt to plan a concert and dinner in a given city
- **`full_day_plan`** - Prompt to plan a full day in a given city on a given date. Includes coffee, event and dinner.

---

### Architecture

- **FastMCP** (`mcp.server.fastmcp`) for tool and resource registration.
- **Async HTTP** via `httpx` in `api_clients.py` for Google Places and Ticketmaster.
- **In-memory storage** for the latest place and event IDs; exposed as resources `place://latest` and `event://latest`.
- **Error handling** for missing API keys and failed requests.

---

### Rate limits

- **Google Places API:** Subject to Google Cloud quotas and SKU-based billing (Essentials/Pro). Use field masks to limit requested fields and stay within free tier where possible.
- **Ticketmaster Discovery API:** Subject to Ticketmaster rate limits; check the [developer portal](https://developer.ticketmaster.com/) for current quotas.
- Stay within provider limits to avoid throttling or extra charges.

---

### Project structure

```
local_discovery/
├── README.md                      # This file
├── pyproject.toml                 # Project and dependencies (uv)
├── uv.lock                        # Locked dependencies
├── requirements.txt               # Pip-style deps (optional; uv uses pyproject.toml)
├── local_discovery.py             # MCP server entrypoint (tools, resources, prompts)
├── api_clients.py                 # Google Places & Ticketmaster API clients
├── google_searchtext_response.json # Sample response (reference)
├── GOOGLE_PLACES_SETUP.md         # Google Places API key setup
├── TICKETMASTER_SETUP.md          # Ticketmaster Discovery API key setup
├── API_REFERENCE.md               # API endpoints and auth reference
├── TOOL_IDEAS.md                  # Ideas to add more tools (take-home exercise)
└── .env                           # API keys (create locally; do not commit)
```

---

## Documentation

- **[GOOGLE_PLACES_SETUP.md](./GOOGLE_PLACES_SETUP.md)** — How to get and configure a Google Places API key.
- **[TICKETMASTER_SETUP.md](./TICKETMASTER_SETUP.md)** — How to get a Ticketmaster Discovery API key.
- **[API_REFERENCE.md](./API_REFERENCE.md)** — API endpoints and authentication used by the server.
- **[TOOL_IDEAS.md](./TOOL_IDEAS.md)** - Ideas to add more tools to this server
