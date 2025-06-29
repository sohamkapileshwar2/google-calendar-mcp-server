from typing import List, Optional
from pydantic import BaseModel, Field

class CalendarListEntryUpdateQueryParams(BaseModel):
    """
    Query Parameter Schema for updating a CalendarList entry (PUT /users/me/calendarList/{calendarId})
    Fields are all optional—only include what you're changing.
    """
    colorRgbFormat: Optional[bool] = Field(
        None,
        description="Whether to use the foregroundColor and backgroundColor fields to write the calendar colors (RGB)."
    )

class CalendarListEntryReminder(BaseModel):
    """Default reminder in CalendarListEntry."""
    method: str = Field(..., description="Reminder method, e.g. 'email' or 'popup'")
    minutes: int = Field(..., ge=0, le=40320, description="Minutes before event")

class CalendarListEntryUpdate(BaseModel):
    """
    Schema for updating a CalendarList entry (PUT /users/me/calendarList/{calendarId})
    Fields are all optional—only include what you're changing.
    """
    backgroundColor: Optional[str] = Field(
        None,
        description="Hex format; requires colorRgbFormat=true to set"
    )
    colorId: Optional[str] = Field(
        None,
        description="Index-based color ID; superseded by background/foreground when using RGB"
    )
    defaultReminders: Optional[List[CalendarListEntryReminder]] = Field(
        None,
        description="List of default reminders for events in this calendar"
    )
    foregroundColor: Optional[str] = Field(
        None,
        description="Hex format for foreground color; requires colorRgbFormat=true"
    )
    hidden: Optional[bool] = Field(
        None,
        description="Whether this calendar is hidden"
    )
    selected: Optional[bool] = Field(
        None,
        description="Whether this calendar is selected/displayed"
    )

    class Config:
        schema_extra = {
            "example": {
                "backgroundColor": "#ff9800",
                "foregroundColor": "#000000",
                "colorId": "9",
                "defaultReminders": [
                    {"method": "email", "minutes": 30}
                ],
                "hidden": False,
                "selected": True
            }
        }
