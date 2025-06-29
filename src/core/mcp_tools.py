from typing import Any, Dict
from core.calendar_client import GoogleCalendarClient

from gcalendar_types.update_calendar_list_entry import CalendarListEntryUpdate, CalendarListEntryUpdateQueryParams
from gcalendar_types.insert_calendar_list_entry import CalendarListEntryInsert, CalendarListEntryInsertQueryParams
from gcalendar_types.update_calendar import CalendarUpdateBody
from gcalendar_types.list_events import EventsListParams
from gcalendar_types.get_event import EventGetParams
from gcalendar_types.insert_event import Event, EventsInsertQueryParams
from gcalendar_types.get_instances import EventsInstancesParams
from gcalendar_types.quick_add_event import EventsQuickAddParams
from gcalendar_types.patch_event import EventsPatchParams
from gcalendar_types.update_event import EventUpdateBody, EventsUpdateParams

class GoogleCalendarMCPTools:
    def __init__(self, app, client: GoogleCalendarClient):
        self.app = app
        self.gclient = client

        # Calendar List
        @app.tool(name="list_calendars", description="Returns the calendars on the user's calendar list")
        async def list_calendars() -> Dict[str, Any]:
            return self.gclient.list_calendars()
        
        @app.tool(name="get_calendar_list_entry", description="Returns a calendar from the user's calendar list")
        async def get_calendar_list_entry(calendar_id: str) -> Dict[str, Any]:
            return self.gclient.get_calendar_list_entry(calendar_id)

        @app.tool(name="insert_calendar_list_entry", description="Inserts an existing calendar into the user's calendar list")
        async def insert_calendar_list_entry(calendar_id: str, params: CalendarListEntryInsertQueryParams, body: CalendarListEntryInsert) -> Dict[str, Any]:
            return self.gclient.update_calendar_list(calendar_id, params.model_dump(exclude_none=True), body.model_dump(exclude_none=True))

        @app.tool(name="update_calendar_list_entry", description="Updates an existing calendar on the user's calendar list")
        async def update_calendar_list_entry(calendar_id: str, params: CalendarListEntryUpdateQueryParams, body: CalendarListEntryUpdate) -> Dict[str, Any]:
            return self.gclient.update_calendar_list(calendar_id, params.model_dump(exclude_none=True), body.model_dump(exclude_none=True))

        # Calendars
        @app.tool(name="get_calendar", description="Returns metadata for a calendar")
        async def get_calendar(calendar_id: str,) -> Dict[str, Any]:
            return self.gclient.get_calendar(calendar_id=calendar_id)

        @app.tool(name="insert_calendar", description="Creates a secondary calendar")
        async def insert_calendar(summary: str) -> Dict[str, Any]:
            return self.gclient.insert_calendar(body={"summary": summary})

        @app.tool(name="update_calendar", description="Update a calendar's settings")
        async def update_calendar(calendar_id: str, body: CalendarUpdateBody) -> Dict[str, Any]:
            return self.gclient.update_calendar(calendar_id, body=body)

        # Events
        @app.tool(name="list_events", description="List events on a specified calendar with optional filters")
        async def list_events(calendar_id: str, params: EventsListParams) -> Dict[str, Any]:
            return self.gclient.list_events(calendar_id=calendar_id, params=params.model_dump(exclude_none=True, exclude={"calendar_id"}))

        @app.tool(name="get_event", description="Get a single event by ID")
        async def get_event(calendar_id: str, event_id: str, params: EventGetParams) -> Dict[str, Any]:
            return self.gclient.get_event(calendar_id, event_id, params=params.model_dump(exclude_none=True))

        @app.tool(name="insert_event", description="Create an event")
        async def insert_event(calendar_id: str, params: EventsInsertQueryParams, body: Event) -> Dict[str, Any]:
            return self.gclient.insert_event(calendar_id, params=params.model_dump(exclude_none=True), body=body.model_dump(exclude_none=True))

        @app.tool(name="get_instances", description="Returns instances of the specified recurring event")
        async def get_instances(calendar_id: str, event_id: str, params: EventsInstancesParams) -> Dict[str, Any]:
            return self.gclient.get_instances(calendar_id, event_id, params=params.model_dump(exclude_none=True))

        @app.tool(name="quick_add_event", description="Creates an event based on a simple text string")
        async def quick_add_event(calendar_id: str, params: EventsQuickAddParams) -> Dict[str, Any]:
            return self.gclient.quick_add(calendar_id, params=params.model_dump(exclude_none=True))
        
        @app.tool(name="patch_event", description="Patch fields on an existing event")
        async def patch_event(calendar_id: str, event_id: str, params: EventsPatchParams, body: Event) -> Dict[str, Any]:
            return self.gclient.patch_event(calendar_id, event_id, params=params.model_dump(exclude_none=True) ,body=body.model_dump(exclude_none=True))

        @app.tool(name="update_event", description="Update an existing event. Overrides all fields")
        async def update_event(calendar_id: str, event_id: str, params: EventsUpdateParams, body: EventUpdateBody) -> Dict[str, Any]:
            return self.gclient.update_event(calendar_id, event_id, params=params.model_dump(exclude_none=True) ,body=body.model_dump(exclude_none=True))


        # Settings
        @app.tool(name="list_settings", description="List user settings")
        async def list_settings() -> Dict[str, Any]:
            return self.gclient.list_settings()

        @app.tool(name="get_setting", description="Get one user setting")
        async def get_setting(setting_id: str) -> Dict[str, Any]:
            return self.gclient.get_setting(setting_id)

