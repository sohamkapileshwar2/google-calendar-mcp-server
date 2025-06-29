from mcp.server.fastmcp import FastMCP
from mcp.server.auth.middleware.auth_context import get_access_token
from settings import ServerSettings
from core.session_manager import SessionManager
from core.calendar_client import GoogleCalendarClient
from core.mcp_tools import GoogleCalendarMCPTools

import logging

logger = logging.getLogger(__name__)

def main(port: int = "8080", host: str = "localhost") -> tuple[FastMCP, str]:
    """Create a simple FastMCP server with Google OAuth."""

    """Run the simple Google MCP server."""
    logging.basicConfig(level=logging.INFO)

    try:
        # No hardcoded credentials - all from environment variables
        settings = ServerSettings(host=host, port=port)
    except ValueError as e:
        logger.error("Failed to load settings. Make sure environment variables are set:")
        logger.error(f"Error: {e}")
        return None, f"Error loading settings: {e}"

    session_manager = SessionManager()
    if len(session_manager.sessions.keys()) < 1:
        return None, f"Session does not exist: Launch the Google OAuth Server to create a session"
    session_id = list(session_manager.sessions.keys())[0]

    app = FastMCP(
        name="Google Calendar MCP Server",
        instructions="A Google Calendar MCP Server using OAuth authentication",
        host=settings.host,
        port=settings.port,
    )

    credentials = session_manager.get_credentials(session_id=session_id)
    gcalendar_client = GoogleCalendarClient(credentials["token"])

    tools = GoogleCalendarMCPTools(app=app, client=gcalendar_client)

    return app, None


if __name__ == "__main__":

    transport="streamable-http"
    mcp_server, error = main()

    if error:
        logger.error(f"Error starting server {error}")
    else:
        logger.info(f"Starting server with {transport} transport")
        mcp_server.run(transport=transport)
