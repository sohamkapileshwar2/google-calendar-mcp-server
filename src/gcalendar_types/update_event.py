from typing import List, Optional
from pydantic import BaseModel, Field
from enum import StrEnum

class EventDateTime(BaseModel):
    date: Optional[str] = Field(None, description="All-day date (YYYY-MM-DD)")
    dateTime: Optional[str] = Field(None, description="DateTime in RFC3339")
    timeZone: Optional[str] = Field(None, description="IANA time zone")

class EventReminder(BaseModel):
    method: str = Field(..., description="Reminder method: 'email' or 'popup'")
    minutes: int = Field(..., ge=0, description="Minutes before event")

class EventReminders(BaseModel):
    useDefault: Optional[bool] = Field(None)
    overrides: Optional[List[EventReminder]] = Field(None)

class EventAttendee(BaseModel):
    email: str = Field(..., description="Attendee email")
    displayName: Optional[str] = None
    optional: Optional[bool] = None
    responseStatus: Optional[str] = None

class ConferenceSolutionKey(BaseModel):
    type: str = Field(..., description="Conference type (e.g. 'hangoutsMeet')")

class CreateConferenceRequest(BaseModel):
    conferenceSolutionKey: ConferenceSolutionKey
    requestId: str = Field(..., description="Unique request ID")

class ConferenceData(BaseModel):
    createRequest: Optional[CreateConferenceRequest] = None

class EventUpdateBody(BaseModel):
    summary: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    colorId: Optional[str] = None
    start: Optional[EventDateTime] = None
    end: Optional[EventDateTime] = None
    attendees: Optional[List[EventAttendee]] = None
    reminders: Optional[EventReminders] = None
    recurrence: Optional[List[str]] = None
    conferenceData: Optional[ConferenceData] = None
    anyoneCanAddSelf: Optional[bool] = None
    supportsAttachments: Optional[bool] = None

    class Config:
        schema_extra = {
            "example": {
                "summary": "Updated Meeting",
                "start": {"dateTime": "2025-08-01T09:00:00Z", "timeZone": "UTC"},
                "end":   {"dateTime": "2025-08-01T10:00:00Z", "timeZone": "UTC"},
                "attendees": [{"email": "bob@example.com"}],
                "conferenceData": {
                    "createRequest": {
                        "conferenceSolutionKey": {"type": "hangoutsMeet"},
                        "requestId": "unique-request-id-123"
                    }
                }
            }
        }

class SendUpdatesEnum(StrEnum):
    all = "all"
    externalOnly = "externalOnly"
    none = "none"

class EventsUpdateParams(BaseModel):
    calendar_id: str = Field(..., alias="calendarId")
    event_id: str = Field(..., alias="eventId")
    conferenceDataVersion: Optional[int] = Field(None, ge=0, le=1)
    maxAttendees: Optional[int] = Field(None, ge=1)
    sendNotifications: Optional[bool] = Field(None, description="Deprecated; use sendUpdates")
    sendUpdates: Optional[SendUpdatesEnum] = Field(None)
    supportsAttachments: Optional[bool] = Field(None)

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
