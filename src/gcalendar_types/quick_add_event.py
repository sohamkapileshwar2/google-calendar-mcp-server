from typing import Optional
from pydantic import BaseModel, Field
from enum import Enum

class SendUpdatesEnum(str, Enum):
    all = 'all'
    externalOnly = 'externalOnly'
    none = 'none'

class EventsQuickAddParams(BaseModel):
    """
    Query parameters for POST /calendars/{calendarId}/events/quickAdd.
    Constructs a new event from simple text string.
    """
    text: str = Field(..., description="Free‑form text describing the event")
    sendNotifications: Optional[bool] = Field(
        None,
        description="Deprecated; whether to send notifications (use sendUpdates instead)"
    )
    sendUpdates: Optional[SendUpdatesEnum] = Field(
        None,
        description="Notification policy: 'all', 'externalOnly', or 'none'"
    )

    class Config:
        use_enum_values = True
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "calendarId": "primary",
                "text": "Lunch with Bob tomorrow at noon",
                "sendUpdates": "all"
            }
        }
