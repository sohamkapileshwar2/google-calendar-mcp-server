
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl


class ServerSettings(BaseSettings):
    """Settings for the Google Calendar MCP server."""

    model_config = SettingsConfigDict(env_prefix="MCP_GOOGLE_CALENDAR_")

    # Server settings
    host: str = "localhost"
    port: int = 8080
    server_url: AnyHttpUrl = AnyHttpUrl("http://localhost:8080")

    def __init__(self, **data):
        """
        Initialize settings with values from environment variables.
        """
        super().__init__(**data)