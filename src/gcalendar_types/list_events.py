from typing import List, Optional
from pydantic import BaseModel, Field

class EventsListParams(BaseModel):
    """
    Parameters for GET /calendars/{calendarId}/events (events.list).
    Only include fields you want to set; all are optional.
    """

    # Filters
    timeMin: Optional[str] = Field(None, description="RFC3339 lower bound (inclusive)")
    timeMax: Optional[str] = Field(None, description="RFC3339 upper bound (exclusive)")
    q: Optional[str] = Field(None, description="Free text search terms for event fields")
    updatedMin: Optional[str] = Field(None, description="RFC3339 lower bound for event last modification time")
    iCalUID: Optional[str] = Field(None, description="Return events sharing this iCalendar UID")
    eventType: Optional[str] = Field(
        None,
        description="Type of events to return: 'default', 'outOfOffice', 'focusTime', 'workingLocation'"
    )
    # Output control
    maxResults: Optional[int] = Field(None, description="Maximum number of events returned on one page")
    pageToken: Optional[str] = Field(None, description="Pagination token from previous result")
    # Event expansion
    singleEvents: Optional[bool] = Field(None, description="Expand recurring events into instances")
    orderBy: Optional[str] = Field(None, description="Sort order: 'startTime' or 'updated'")
    showDeleted: Optional[bool] = Field(None, description="Include cancelled events")
    showHiddenInvitations: Optional[bool] = Field(None, description="Include hidden invitations")
    syncToken: Optional[str] = Field(None, description="Token for incremental sync")
    timeZone: Optional[str] = Field(None, description="Time zone for interpreting start/end times")
    privateExtendedProperty: Optional[List[str]] = Field(
        None,
        description="Private extended property filters: propertyName=value"
    )
    sharedExtendedProperty: Optional[List[str]] = Field(
        None,
        description="Shared extended property filters: propertyName=value"
    )

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "timeMin": "2025-06-01T00:00:00Z",
                "timeMax": "2025-07-01T00:00:00Z",
                "q": "meeting",
                "singleEvents": True,
                "orderBy": "startTime",
                "maxResults": 50,
                "showDeleted": False,
                "timeZone": "UTC"
            }
        }
