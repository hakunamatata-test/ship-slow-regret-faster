# Ticketmaster Discovery API — Setup

This guide walks you through signing up for a Ticketmaster developer account and getting an API key for the Local Discovery MCP server.

---

## 1. Create a Ticketmaster developer account

1. Go to the [Ticketmaster Developer Portal](https://developer.ticketmaster.com/).
2. Click **Sign In** or **Register**.
3. Register a new account:  
   [developer-acct.ticketmaster.com/user/register](https://developer-acct.ticketmaster.com/user/register)
4. Complete the form with:
   - First and last name
   - Company / app name and website URL
   - Email, username, password
   - Country and contact details
   - Agreement to the Terms of Use

---

## 2. Get your API key

1. After logging in, go to the [Ticketmaster Developer Portal](https://developer.ticketmaster.com/).
2. Your **API key** (Consumer Key) is shown in your account or app settings (e.g. under “My Apps” or “API Keys”).
3. If you need to create an app first, use the “Create app” or “Get API key” flow; the key is then listed in your dashboard.
4. Copy the key. You will use it as `TICKETMASTER_API_KEY` in the build `.env` file.

---

## 3. Add the key to the build server

In the `build/` directory, create or edit `.env`:

```env
TICKETMASTER_API_KEY=your_api_key_here
```

Do not commit `.env` to version control.

---

## 4. Discovery API usage

The Local Discovery server uses the **Discovery API v2**:

- **Base URL:** `https://app.ticketmaster.com/discovery/v2/`
- **Authentication:** API key passed as the `apikey` query parameter.
- **Endpoints used:** `events.json`, `events/{id}.json`, `venues.json`, `venues/{id}.json`.

Rate limits and quotas are set by Ticketmaster; check the developer portal or [Discovery API documentation](https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/) for current limits.

---

## References

- [Ticketmaster Developer Portal](https://developer.ticketmaster.com/)
- [Discovery API — Getting started](https://developer.ticketmaster.com/products-and-docs/apis/getting-started)
- [Discovery API v2](https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/)
- [Discovery API — Search events](https://developer.ticketmaster.com/products-and-docs/tutorials/events-search/search_events_with_discovery_api.html)
