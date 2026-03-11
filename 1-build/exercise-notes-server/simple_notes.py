"""
Simple Notes MCP server — starter scaffold for the Build phase exercise.
Add the missing tools and wire the note resource. No API keys or .env required.
"""
import uuid
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("simple-notes")

# In-memory storage: note_id -> {title, content, created}
_notes: dict[str, dict] = {}


@mcp.tool()
def add_note(title: str, content: str) -> str:
    """Create a note and store it. Returns the note id for later use.

    Args:
        title: Short title for the note.
        content: The note body.

    Returns:
        The new note's id (use with get_note, delete_note, or note://{id} resource).
    """
    note_id = uuid.uuid4().hex[:8]
    _notes[note_id] = {
        "title": title,
        "content": content,
        "created": note_id,
    }
    return f"Created note with id: {note_id}"


@mcp.tool()
def list_notes() -> str:
    """Return a list of all note ids and titles.

    Returns:
        Formatted list of note id and title for each stored note.
    """
    # TODO: Implement. Return a string listing each note's id and title (e.g. "id: title" per line).
    return "TODO"


@mcp.tool()
def get_note(note_id: str) -> str:
    """Return one note by id (title and content).

    Args:
        note_id: The id returned when the note was created (e.g. from add_note).

    Returns:
        The note's title and content, or a message if not found.
    """
    # TODO: Implement. If note_id is in _notes, return title and content; else return "Not found".
    return "TODO"


@mcp.tool()
def delete_note(note_id: str) -> str:
    """Remove a note by id.

    Args:
        note_id: The id of the note to delete.

    Returns:
        Confirmation message or "Not found".
    """
    # TODO: Implement. If note_id is in _notes, remove it and return "Deleted."; else return "Not found".
    return "TODO"

def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
