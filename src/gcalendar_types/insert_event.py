from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field
from enum import StrEnum

# Nested Models

class EventTypeEnum(StrEnum):
    birthday = "birthday"
    default = "default"
    focusTime = "focusTime"
    fromGmail = "fromGmail"
    outOfOffice = "outOfOffice"
    workingLocation = "workingLocation"

class BirthdayTypeEnum(StrEnum):
    anniversary = "biranniversarythday"
    birthday = "birthday"
    custom = "focusTime"
    other = "other"
    self = "self"

class TransparencyEnum(StrEnum):
    opaque = "opaque"
    transparent = "transparent"

class VisibilityEnum(StrEnum):
    default = "default"
    public = "public"
    private = "private"
    confidential = "confidential"

class StatusEnum(StrEnum):
    confirmed = "confirmed"
    tentative = "tentative"
    cancelled = "cancelled"

class ResponseStatusEnum(StrEnum):
    needsAction = "needsAction"
    declined = "declined"
    tentative = "tentative"
    accepted = "accepted"

class GadgetDisplayEnum(StrEnum):
    icon = "icon"
    chip = "chip"

class EventDateTime(BaseModel):
    date: Optional[str] = Field(None, description="All‑day date (YYYY‑MM‑DD)")
    dateTime: Optional[str] = Field(None, description="RFC3339 datetime")
    timeZone: Optional[str] = Field(None, description="IANA time zone name")

class EventReminder(BaseModel):
    method: str
    minutes: int = Field(..., ge=0, le=40320)

class EventReminders(BaseModel):
    useDefault: Optional[bool] = None
    overrides: Optional[List[EventReminder]] = None

class EventAttendee(BaseModel):
    id: Optional[str] = None
    email: str
    displayName: Optional[str] = None
    organizer: Optional[bool] = None
    self: Optional[bool] = Field(None, alias="self")
    resource: Optional[bool] = None
    optional: Optional[bool] = None
    responseStatus: Optional[ResponseStatusEnum] = None
    comment: Optional[str] = None
    additionalGuests: Optional[int] = None

class SourceModel(BaseModel):
    url: Optional[str] = None
    title: Optional[str] = None

class ConferenceSolutionKey(BaseModel):
    type: str

class ConferenceCreateRequest(BaseModel):
    requestId: str
    conferenceSolutionKey: ConferenceSolutionKey

class ConferenceStatus(BaseModel):
    statusCode: Optional[str] = None

class EntryPoint(BaseModel):
    entryPointType: Optional[str] = None
    uri: Optional[str] = None
    label: Optional[str] = None
    pin: Optional[str] = None
    accessCode: Optional[str] = None
    meetingCode: Optional[str] = None
    passcode: Optional[str] = None
    password: Optional[str] = None

class ConferenceSolutionModel(BaseModel):
    key: Optional[Dict[str, str]] = None
    name: Optional[str] = None
    iconUri: Optional[str] = None

class ConferenceData(BaseModel):
    createRequest: Optional[ConferenceCreateRequest] = None
    status: Optional[ConferenceStatus] = None
    entryPoints: Optional[List[EntryPoint]] = None
    conferenceSolution: Optional[ConferenceSolutionModel] = None
    conferenceId: Optional[str] = None
    signature: Optional[str] = None
    notes: Optional[str] = None

class Gadget(BaseModel):
    type: Optional[str] = None
    title: Optional[str] = None
    link: Optional[str] = None
    iconLink: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    display: Optional[GadgetDisplayEnum] = None
    preferences: Optional[Dict[str, str]] = None

class WorkingLocationProperties(BaseModel):
    type: Optional[str] = None
    homeOffice: Optional[Any] = None
    customLocation: Optional[Dict[str, str]] = None
    officeLocation: Optional[Dict[str, Any]] = None

class OutOfOfficeProperties(BaseModel):
    autoDeclineMode: Optional[str] = None
    declineMessage: Optional[str] = None

class FocusTimeProperties(BaseModel):
    autoDeclineMode: Optional[str] = None
    declineMessage: Optional[str] = None
    chatStatus: Optional[str] = None

class BirthdayProperties(BaseModel):
    contact: Optional[str] = None
    type: EventTypeEnum = Field(..., description="One of birthday, anniversary, custom, other, self")
    customTypeName: Optional[str] = None

class EventAttachment(BaseModel):
    fileUrl: Optional[str] = None
    title: Optional[str] = None
    mimeType: Optional[str] = None
    iconLink: Optional[str] = None
    fileId: Optional[str] = None

class Event(BaseModel):
    start: EventDateTime
    end: EventDateTime

    anyoneCanAddSelf: Optional[bool] = None
    attachments: Optional[List[EventAttachment]] = None
    attendees: Optional[List[EventAttendee]] = None
    attendeesOmitted: Optional[bool] = None
    birthdayProperties: Optional[BirthdayProperties] = None
    colorId: Optional[str] = None
    conferenceData: Optional[ConferenceData] = None
    description: Optional[str] = None
    endTimeUnspecified: Optional[bool] = None
    eventType: Optional[EventTypeEnum] = None
    extendedProperties: Optional[Dict[str, Dict[str, str]]] = None
    focusTimeProperties: Optional[FocusTimeProperties] = None
    gadget: Optional[Gadget] = None
    guestsCanInviteOthers: Optional[bool] = None
    guestsCanModify: Optional[bool] = None
    guestsCanSeeOtherGuests: Optional[bool] = None
    hangoutLink: Optional[str] = None
    id: Optional[str] = Field(None, min_length=5, max_length=1024)
    location: Optional[str] = None
    originalStartTime: Optional[EventDateTime] = None
    privateCopy: Optional[bool] = None
    recurrence: Optional[List[str]] = None
    reminders: Optional[EventReminders] = None
    sequence: Optional[int] = None
    source: Optional[SourceModel] = None
    start: EventDateTime
    status: Optional[StatusEnum] = None
    summary: Optional[str] = None
    transparency: Optional[TransparencyEnum] = None
    visibility: Optional[VisibilityEnum] = None
    workingLocationProperties: Optional[WorkingLocationProperties] = None

    class Config:
        use_enum_values = True

class EventsInsertQueryParams(BaseModel):
    """
    Query parameters for POST /calendars/{calendarId}/events (events.insert).
    All fields are optional and correspond to API query parameters.
    """

    conferenceDataVersion: Optional[int] = Field(
        None,
        ge=0,
        le=1,
        description="0 (no conference data) or 1 (support conference data in body)"
    )
    maxAttendees: Optional[int] = Field(
        None,
        ge=1,
        description="Max attendees returned in response"
    )
    sendNotifications: Optional[bool] = Field(
        None,
        description="Deprecated; use sendUpdates"
    )
    sendUpdates: Optional[str] = Field(
        None,
        description="Notification policy: 'all', 'externalOnly', or 'none'"
    )
    supportsAttachments: Optional[bool] = Field(
        None,
        description="Indicates if client supports event attachments"
    )

    class Config:
        schema_extra = {
            "example": {
                "conferenceDataVersion": 1,
                "maxAttendees": 50,
                "sendUpdates": "all",
                "supportsAttachments": True
            }
        }
