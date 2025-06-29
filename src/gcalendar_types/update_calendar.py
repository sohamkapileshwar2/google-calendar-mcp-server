from typing import Optional
from pydantic import BaseModel, Field

class CalendarUpdateBody(BaseModel):
    """
    Request body schema for updating calendar metadata:

    Fields are optional—only include those you intend to change.
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
        description="Geographic location of the calendar as free‑form text"
    )
    timeZone: Optional[str] = Field(
        None,
        description="Primary IANA time zone (e.g., 'Europe/Zurich')"
    )

    class Config:
        schema_extra = {
            "example": {
                "summary": "Work Calendar",
                "description": "Calendar for work events and schedule",
                "location": "Berlin, Germany",
                "timeZone": "Europe/Berlin"
            }
        }
