from typing import Optional
from pydantic import BaseModel, Field
from enum import StrEnum

class SendUpdatesEnum(StrEnum):
    all = 'all'
    externalOnly = 'externalOnly'
    none = 'none'

class EventsPatchParams(BaseModel):
    """
    Query parameters for PATCH /calendars/{calendarId}/events/{eventId}.
    """
    alwaysIncludeEmail: Optional[bool] = Field(
        None, description="Deprecated; always ignored but included for compat"
    )
    conferenceDataVersion: Optional[int] = Field(
        None, ge=0, le=1,
        description="Support for conference data in body: 0 or 1"
    )
    maxAttendees: Optional[int] = Field(
        None, ge=1,
        description="Maximum attendees returned in response"
    )
    sendNotifications: Optional[bool] = Field(
        None, description="Deprecated; use sendUpdates instead"
    )
    sendUpdates: Optional[SendUpdatesEnum] = Field(
        None, description="Notification policy for guests"
    )
    supportsAttachments: Optional[bool] = Field(
        None, description="Whether client supports event attachments"
    )

    class Config:
        use_enum_values = True
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "calendarId": "primary",
                "eventId": "abc123",
                "conferenceDataVersion": 1,
                "sendUpdates": "all",
                "supportsAttachments": True
            }
        }