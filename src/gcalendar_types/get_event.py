from typing import Optional
from pydantic import BaseModel, Field

class EventGetParams(BaseModel):
    """
    Params for GET /calendars/{calendarId}/events/{eventId}
    """
    alwaysIncludeEmail: Optional[bool] = Field(
        None,
        description="Ignored; always returns email fields"
    )
    maxAttendees: Optional[int] = Field(
        None,
        description="Max number of attendees included in the response"
    )
    timeZone: Optional[str] = Field(
        None,
        description="Timezone used in the response (defaults to calendar's timezone)"
    )

    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "calendarId": "primary",
                "eventId": "abcd1234",
                "maxAttendees": 10,
                "timeZone": "Europe/Berlin"
            }
        }
