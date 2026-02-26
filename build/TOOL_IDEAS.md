# Tool ideas

Ideas for **additional tools** to extend the Local Discovery MCP server. All use **free** APIs: Ticketmaster Discovery API (free with key) and Google Places API (free-tier eligible; see [GOOGLE_PLACES_TOOLS.md](./GOOGLE_PLACES_TOOLS.md) for SKU details).

---

## Ideas list

| # | Tool | API(s) |
|---|------|--------|
| 1 | `search_attractions` | Ticketmaster |
| 2 | `get_attraction_details` | Ticketmaster |
| 3 | `find_events_by_classification` | Ticketmaster |
| 4 | `find_events_near_location` | Ticketmaster |
| 5 | `get_attraction_events` | Ticketmaster |
| 6 | `find_venues_by_keyword` | Ticketmaster |
| 7 | `find_restaurants_near_event_venue` | Ticketmaster + Google Places |
| 8 | `plan_dinner_and_event` | Ticketmaster + Google Places |
| 9 | `get_google_maps_link` | None (URL only) |
| 10 | `get_detailed_reviews` | Google Places |
| 11 | `get_special_opening_hours` | Google Places |
| 12 | `autocomplete_places` | Google Places |

---

## Ticketmaster Discovery API

All use the free [Discovery API v2](https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/) (`apikey` in query). Base URL: `https://app.ticketmaster.com/discovery/v2/`.

### 1. `search_attractions`
**Purpose:** Search for artists, teams, or acts by keyword.  
**API:** `GET attractions.json`  
**Parameters:** `keyword`, `classification_id` (optional), `limit`.  
**Returns:** Attraction name, ID, type, URL.  
**Example:** "Find Taylor Swift as an attraction", "Search for NBA teams".

---

### 2. `get_attraction_details`
**Purpose:** Get details for one attraction by ID.  
**API:** `GET attractions/{id}.json`  
**Parameters:** `attraction_id`.  
**Returns:** Name, type, URL, classifications; optionally embedded events.  
**Example:** "Tell me more about this artist".

---

### 3. `find_events_by_classification`
**Purpose:** Find events by category (Music, Sports, Arts & Theatre, Film) without a text keyword.  
**API:** `GET events.json` with `classificationName`, `city`, `countryCode`, `startDateTime`, `endDateTime`.  
**Parameters:** `city`, `country`, `classification_name`, `start_date`, `end_date`, `limit`.  
**Returns:** Event name, date, venue, ID, URL.  
**Example:** "Show me music events in Seattle", "Sports events in London next month".

---

### 4. `find_events_near_location`
**Purpose:** Find events by latitude/longitude and radius ("events near me").  
**API:** `GET events.json` with `latlong`, `radius`, `unit`.  
**Parameters:** `latitude`, `longitude`, `radius` (miles), `unit`, `start_date`, `limit`.  
**Returns:** Events within radius with name, date, venue, ID, URL.  
**Example:** "What's happening near me this weekend?"

---

### 5. `get_attraction_events`
**Purpose:** List upcoming events for a given attraction (artist or team).  
**API:** `GET events.json` with `attractionId`.  
**Parameters:** `attraction_id`, `country`, `limit`.  
**Returns:** Event name, date, venue, city, URL.  
**Example:** "When is Taylor Swift touring next?", "Upcoming games for this team".

---

### 6. `find_venues_by_keyword`
**Purpose:** Search venues by name or keyword (not just city).  
**API:** `GET venues.json` with `keyword`, `countryCode`, `city`.  
**Parameters:** `keyword`, `country`, `city`, `limit`.  
**Returns:** Venue name, address, ID, URL.  
**Example:** "Find venues named Apollo", "Stadiums in Texas".

---

## Combined — Ticketmaster + Google Places

### 7. `find_restaurants_near_event_venue`
**Purpose:** Given an event or venue, find restaurants near that venue (dinner before/after the show).  
**APIs:** Ticketmaster `GET events/{id}.json` or `venues/{id}.json` for venue address/lat-long; then Google Places Text Search (or Nearby) with location bias.  
**Parameters:** `event_id` or `venue_id`, `place_type` (e.g. restaurant, cafe), `limit`.  
**Returns:** Venue info + list of places (name, address, place_id) near the venue.  
**Example:** "Find restaurants near the venue for this concert".

---

### 8. `plan_dinner_and_event`
**Purpose:** In one city and date range, suggest both events and restaurants (plan a night out).  
**APIs:** Ticketmaster `GET events.json` (city, country, start/end date); Google Places `searchText` (e.g. "restaurants in {city}").  
**Parameters:** `city`, `country`, `start_date`, `end_date`, `event_limit`, `place_limit`.  
**Returns:** Short list of events (name, date, venue, URL) and list of restaurants (name, address, place_id).  
**Example:** "Plan a night out in San Francisco this Saturday — dinner and a show".

---

## Google Places API 

All use [Google Places API (New)](https://developers.google.com/maps/documentation/places/web-service) with field masks. Prefer Essentials/Pro fields to stay within free tier (see [GOOGLE_PLACES_TOOLS.md](./GOOGLE_PLACES_TOOLS.md)).

### 9. `get_google_maps_link`
**Purpose:** Generate Google Maps links for a place (directions, place page, or search).  
**API:** None — build URL from `place_id` (e.g. `https://www.google.com/maps/place/?q=place_id:{id}` or directions variant).  
**Parameters:** `place_id`, `link_type` (optional: "place", "directions", "search").  
**Returns:** Google Maps URL.  
**Example:** "Get directions link for this restaurant".

---

### 10. `get_detailed_reviews`
**Purpose:** Get structured reviews (rating, text, author, time) for a place.  
**API:** Place Details with `reviews` in field mask (Pro SKU).  
**Parameters:** `place_id`, `limit`, `sort_by` (optional).  
**Returns:** Review text, rating, author name, relative time.  
**Example:** "Show me recent reviews for this restaurant".

---

### 11. `get_special_opening_hours`
**Purpose:** Get regular and special/holiday hours for a place.  
**API:** Place Details with opening hours fields (Pro SKU).  
**Parameters:** `place_id`, `date` (optional).  
**Returns:** Regular hours, special days, next 7 days if available.  
**Example:** "Is this place open on Christmas?", "Special hours this week".

---

### 12. `autocomplete_places`
**Purpose:** Place autocomplete as the user types (better UX than full search).  
**API:** Places API Autocomplete (New); use session token when followed by Place Details for pricing.  
**Parameters:** `input`, `location` (optional), `types` (optional), `session_token` (optional).  
**Returns:** List of place suggestions (place_id, text).  
**Example:** "Autocomplete restaurants near me".

---

## Implementation notes

- **Ticketmaster:** Reuse `api_clients.py` pattern (country normalization, async httpx). Responses often use `_embedded.{resource}`. Respect [rate limits](https://developer.ticketmaster.com/support/faq).
- **Google Places:** Use field masks; billing is by highest SKU requested. Essentials (10k free/mo) vs Pro (5k free/mo) — see [GOOGLE_PLACES_TOOLS.md](./GOOGLE_PLACES_TOOLS.md). Session tokens for autocomplete when linking to Place Details.
- **Combined tools:** Call Ticketmaster first for venue/event context, then Google Places with location bias or city query; return a single formatted response.

---

## Resources

- **Ticketmaster Discovery API v2:** https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/
- **Ticketmaster API Explorer:** https://developer.ticketmaster.com/api-explorer/v2
- **Ticketmaster FAQs:** https://developer.ticketmaster.com/support/faq
- **Google Places API (New):** https://developers.google.com/maps/documentation/places/web-service
- **Google Place Data Fields & SKUs:** https://developers.google.com/maps/documentation/places/web-service/data-fields
- **Free-tier tool list (Google):** [GOOGLE_PLACES_TOOLS.md](./GOOGLE_PLACES_TOOLS.md)
