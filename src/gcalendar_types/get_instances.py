from typing import Optional
from pydantic import BaseModel, Field

class EventsInstancesParams(BaseModel):
    """
    Query parameters for GET /calendars/{calendarId}/events/{eventId}/instances.
    All fields are optional.
    """
    alwaysIncludeEmail: Optional[bool] = Field(
        None, description="Deprecated – always ignored"
    )
    maxAttendees: Optional[int] = Field(
        None, ge=1,
        description="Max attendees to include in the response"
    )
    maxResults: Optional[int] = Field(
        None, ge=1, le=2500,
        description="Max number of instances to return (<=2500)"
    )
    originalStart: Optional[str] = Field(
        None,
        description="Filter by original instance start time (RFC3339)"
    )
    pageToken: Optional[str] = Field(
        None, description="Token specifying which result page to return"
    )
    showDeleted: Optional[bool] = Field(
        None,
        description="Include deleted (cancelled) instances"
    )
    timeMax: Optional[str] = Field(
        None,
        description="Upper bound (exclusive) for event start time (RFC3339)"
    )
    timeMin: Optional[str] = Field(
        None,
        description="Lower bound (inclusive) for event end time (RFC3339)"
    )
    timeZone: Optional[str] = Field(
        None, description="Timezone used in the response"
    )

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "calendarId": "primary",
                "eventId": "recurring-event-123",
                "maxResults": 100,
                "timeMin": "2025-06-01T00:00:00-07:00",
                "timeMax": "2025-07-01T00:00:00-07:00",
                "showDeleted": False
            }
        }
