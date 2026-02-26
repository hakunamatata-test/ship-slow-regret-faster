# Tool ideas

This document outlines ideas for **additional tools and features** that you can implement to extend this MCP server's capabilities.


## Ideas for additional tools 

### Unique value
1. `autocomplete_places` - Better UX than basic search
2. `get_detailed_reviews` - More structured than tips
3. `get_special_opening_hours` - Holiday hours
4. `get_google_maps_link` - Direct Maps integration

### Useful features
5. `check_business_status` - Moved/closed tracking
6. `get_secondary_opening_hours` - Multiple schedules
7. `get_review_summary` - Aggregated stats

### Nice to have
8. `compare_places_detailed` - Enhanced comparison
9. `find_places_along_route` - Route-based search
10. `get_place_editorial_summary` - Google descriptions

---

## Implementation Notes

### Field Masks (Important!)
Google Places API (New) requires **field masks** - you must specify exactly which fields you want:

```python
fields = [
    "displayName",
    "formattedAddress",
    "rating",
    "userRatingCount",
    "currentOpeningHours",
    "reviews",
    "priceLevel",
    "businessStatus",
    "editorialSummary"
]
```

**Benefits**:
- Lower costs (only pay for fields you use)
- Faster responses
- Better control over data

### Session Tokens for Autocomplete
- Generate UUID v4 for each autocomplete session
- Use same token for autocomplete requests and place selection
- Groups billing for better pricing

### Rate Limits
- Varies by API method and pricing tier
- Check current limits in Google Cloud Console
- Implement exponential backoff for rate limit errors

### Cost Optimization
- Use field masks to request only needed fields
- Cache place details (Place IDs are stable)
- Use session tokens for autocomplete
- Batch requests when possible

---

## Code Example Structure

```python
@mcp.tool()
async def autocomplete_places(
    input_text: str,
    location: str | None = None,
    types: list[str] | None = None,
    session_token: str | None = None
) -> str:
    """Provide intelligent place autocomplete as user types.
    
    Args:
        input_text: User's partial input text
        location: Bias results toward this location
        types: Filter by place types (restaurant, museum, etc.)
        session_token: Session token for billing grouping (UUID v4)
    """
    url = "https://places.googleapis.com/v1/places:autocomplete"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": GOOGLE_PLACES_API_KEY,
        "X-Goog-FieldMask": "suggestions.placePrediction.placeId,suggestions.placePrediction.text"
    }
    
    data = {
        "input": input_text,
    }
    
    if location:
        data["locationBias"] = {"location": {"lat": lat, "lng": lng}}
    
    if types:
        data["includedPrimaryTypes"] = types
    
    if session_token:
        data["sessionToken"] = session_token
    
    # Make request and format results
    # ...
```

---

## Autocomplete & Search Enhancement Tools

### 1. `autocomplete_places`
**Purpose**: Provide intelligent place autocomplete as user types
**Unique Feature**: Session-based pricing and better predictions
**API**: Google Places API Autocomplete (New)
**Parameters**:
- `input` (str): User's partial input text
- `location` (str, optional): Bias results toward location
- `types` (list, optional): Filter by place types (restaurant, museum, etc.)
- `session_token` (str, optional): Session token for billing grouping

**Benefits**:
- More accurate predictions than basic search
- Session tokens group autocomplete + selection for better pricing
- Supports place and query predictions
- Location biasing for better local results

**Example Use Cases**:
- "As user types 'Starbucks', show autocomplete suggestions"
- "Autocomplete restaurants near user's location"

---

## Reviews & Ratings Tools

### 2. `get_detailed_reviews`
**Purpose**: Get structured reviews with ratings, text, author info, and time
**Unique Feature**: Google's extensive review database
**API**: Google Places API Place Details
**Parameters**:
- `place_id` (str): Google Place ID
- `limit` (int, optional): Number of reviews (default: 5)
- `sort_by` (str, optional): "most_relevant" or "newest"

**Returns**: 
- Review text, rating (1-5), author name, author photo
- Relative time description ("2 weeks ago")
- Language of review
- More structured than Foursquare tips

**Example Use Cases**:
- "Show me recent reviews for this restaurant"
- "What are people saying about this place?"

---

### 3. `get_review_summary`
**Purpose**: Get aggregated review statistics
**API**: Google Places API Place Details
**Parameters**:
- `place_id` (str): Google Place ID

**Returns**:
- Overall rating (0-5)
- Total review count
- Rating distribution (how many 5-star, 4-star, etc.)
- Review summary if available

**Example Use Cases**:
- "What's the overall rating breakdown?"
- "How many reviews does this place have?"

---

## Opening Hours & Schedule Tools

### 4. `get_special_opening_hours`
**Purpose**: Get special/holiday hours that differ from regular schedule
**Unique Feature**: Special days and holiday hours
**API**: Google Places API Place Details
**Parameters**:
- `place_id` (str): Google Place ID
- `date` (str, optional): Specific date to check (YYYY-MM-DD)

**Returns**:
- Regular hours
- Special days (holidays, events with different hours)
- Next 7 days schedule
- Secondary opening hours (if applicable)

**Example Use Cases**:
- "Is this place open on Christmas?"
- "What are the special hours this week?"

---

### 5. `get_secondary_opening_hours`
**Purpose**: Get different schedules for different services (drive-through, dining room, etc.)
**Unique Feature**: Multiple schedules per place
**API**: Google Places API Place Details
**Parameters**:
- `place_id` (str): Google Place ID

**Returns**:
- Primary hours (main service)
- Secondary hours (drive-through, delivery, etc.)
- Service type labels

**Example Use Cases**:
- "What are the drive-through hours vs dining room hours?"
- "When is delivery available?"

---

### 6. `check_if_open_at_time`
**Purpose**: Check if a place is open at a specific date/time
**API**: Google Places API Place Details
**Parameters**:
- `place_id` (str): Google Place ID
- `datetime` (str): Date and time to check (ISO 8601 format)

**Returns**: Boolean indicating if place is open at that time

**Example Use Cases**:
- "Is this restaurant open at 8 PM tomorrow?"
- "Will this place be open on New Year's Day?"

---

## Location & Navigation Tools

### 7. `get_google_maps_link`
**Purpose**: Generate Google Maps links for places
**Unique Feature**: Direct Google Maps integration
**API**: Google Places API Place Details
**Parameters**:
- `place_id` (str): Google Place ID
- `link_type` (str, optional): "directions", "place", or "search"

**Returns**: Google Maps URL for:
- Viewing place on Google Maps
- Getting directions
- Sharing location

**Example Use Cases**:
- "Get directions link for this restaurant"
- "Share this place on Google Maps"

---

### 8. `find_places_along_route`
**Purpose**: Find places along a route between two points
**API**: Google Places API + Directions API
**Parameters**:
- `origin` (str): Starting location
- `destination` (str): Ending location
- `category` (str, optional): Type of place to find
- `radius` (int, optional): Search radius from route (meters)

**Returns**: Places near the route with distance from route

**Example Use Cases**:
- "Find restaurants along my route"
- "Show me gas stations on the way"

---

## Business Information Tools

### 9. `check_business_status`
**Purpose**: Check if a business is operational, closed, or moved
**Unique Feature**: Business status tracking
**API**: Google Places API Place Details
**Parameters**:
- `place_id` (str): Google Place ID

**Returns**:
- Business status (OPERATIONAL, CLOSED_PERMANENTLY, CLOSED_TEMPORARILY)
- If moved: new location information (`movedPlace`, `movedPlaceId`)
- Last updated timestamp

**Example Use Cases**:
- "Is this business still open?"
- "Did this restaurant move?"

---

## Advanced Search Tools

### 10. `search_with_price_level`
**Purpose**: Search filtered by price level with Google's price data
**API**: Google Places API Text Search / Nearby Search
**Parameters**:
- `location` (str): City name or address
- `min_price` (int, optional): Minimum price level (0-4)
- `max_price` (int, optional): Maximum price level (0-4)
- `type` (str, optional): Place type

**Returns**: Places with price level indicators ($ to $$$$)

---

### 11. `search_by_rating_range`
**Purpose**: Search places within a rating range
**API**: Google Places API Text Search / Nearby Search
**Parameters**:
- `location` (str): City name or address
- `min_rating` (float): Minimum rating (0.0-5.0)
- `max_rating` (float, optional): Maximum rating (0.0-5.0)
- `type` (str, optional): Place type

**Returns**: Places filtered by rating

---

## Integration & Utility Tools

### 12. `get_place_id_from_coordinates`
**Purpose**: Convert coordinates to Google Place ID
**API**: Google Places API Place Details (reverse geocoding)
**Parameters**:
- `latitude` (float): Latitude
- `longitude` (float): Longitude

**Returns**: Google Place ID for the location

**Use Case**: When you have coordinates and need Place ID for other API calls

---

### 13. `batch_get_place_details`
**Purpose**: Get details for multiple places efficiently
**API**: Google Places API Place Details (multiple calls)
**Parameters**:
- `place_ids` (list): List of Google Place IDs (up to 20)

**Returns**: Details for all requested places

**Note**: Implement as wrapper that makes multiple API calls efficiently

---

## Comparison & Analysis Tools

### 14. `compare_places_detailed`
**Purpose**: Compare multiple places with detailed metrics
**API**: Google Places API Place Details (multiple)
**Parameters**:
- `place_ids` (list): List of Google Place IDs (2-5 places)
- `compare_fields` (list, optional): Fields to compare (rating, price, reviews, etc.)

**Returns**: Side-by-side comparison with:
- Ratings and review counts
- Price levels
- Opening hours
- Distance from reference point
- Key attributes

---

### 15. `find_places_similar_to`
**Purpose**: Find places similar to a given place using Google's data
**API**: Google Places API Text Search / Nearby Search
**Parameters**:
- `place_id` (str): Reference Google Place ID
- `radius` (int, optional): Search radius (meters, default: 2000)
- `limit` (int, optional): Number of results (default: 10)

**Implementation**: 
1. Get place details for reference place
2. Extract place type, price level, rating range
3. Search nearby with similar criteria

**Returns**: Places with similar characteristics

---

## Unique Google-Specific Features

### 16. `get_place_editorial_summary`
**Purpose**: Get Google's editorial summary/description of a place
**Unique Feature**: Google-generated place descriptions
**API**: Google Places API Place Details
**Parameters**:
- `place_id` (str): Google Place ID

**Returns**: Editorial summary text (if available)

**Example Use Cases**:
- "Tell me about this place"
- "Get a description of this restaurant"

---

### 17. `check_place_verification_status`
**Purpose**: Check if a place is verified by Google
**API**: Google Places API Place Details
**Parameters**:
- `place_id` (str): Google Place ID

**Returns**: Verification status and business ownership info

---

## Resources

- **Google Places API Documentation**: https://developers.google.com/maps/documentation/places/web-service
- **Place Data Fields**: https://developers.google.com/maps/documentation/places/web-service/data-fields
- **Autocomplete (New)**: https://developers.google.com/maps/documentation/places/web-service/place-autocomplete
- **Place Photos (New)**: https://developers.google.com/maps/documentation/places/web-service/place-photos
- **Session Tokens**: https://developers.google.com/maps/documentation/places/web-service/session-tokens
- **Field Masks Guide**: https://developers.google.com/maps/documentation/places/web-service/choose-fields

---
