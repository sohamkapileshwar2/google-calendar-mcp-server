from typing import Optional
from pydantic import BaseModel, Field


class CalendarInsertBody(BaseModel):
    """
    Schema for creating a new calendar via POST /calendars
    """
    summary: Optional[str] = Field(
        None,
        description="Title of the calendar"
    )
    description: Optional[str] = Field(
        None,
        description="Description of the calendar"
    )
    location: Optional[str] = Field(
        None,
        description="Geographic location of the calendar"
    )
    timeZone: Optional[str] = Field(
        None,
        description="Primary time zone of the calendar (IANA format)"
    )

    class Config:
        schema_extra = {
            "example": {
                "summary": "Team Calendar",
                "description": "Calendar for team events and meetings",
                "location": "New York, USA",
                "timeZone": "America/New_York"
            }
        }
