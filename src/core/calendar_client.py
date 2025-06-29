import httpx
from typing import Any, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class GoogleCalendarClient:
    API_BASE = "https://www.googleapis.com/calendar/v3"

    def __init__(self, access_token: str):
        self.client = httpx.Client(headers={
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        })
    
    # --- ACL ---
    def list_acl(self, calendar_id: str) -> Dict[str, Any]:
        return self._get(f"/calendars/{calendar_id}/acl")
    def get_acl(self, calendar_id: str, rule_id: str) -> Dict[str, Any]:
        return self._get(f"/calendars/{calendar_id}/acl/{rule_id}")
    def insert_acl(self, calendar_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._post(f"/calendars/{calendar_id}/acl", body=body)
    def delete_acl(self, calendar_id: str, rule_id: str) -> None:
        self._delete(f"/calendars/{calendar_id}/acl/{rule_id}")
    def patch_acl(self, calendar_id: str, rule_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._patch(f"/calendars/{calendar_id}/acl/{rule_id}", body=body)
    def update_acl(self, calendar_id: str, rule_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._put(f"/calendars/{calendar_id}/acl/{rule_id}", body=body)
    def watch_acl(self, calendar_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._post(f"/calendars/{calendar_id}/acl/watch", body=body)

    # --- CalendarList ---
    def list_calendars(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._get("/users/me/calendarList", params=params)
    def get_calendar_list_entry(self, calendar_id: str) -> Dict[str, Any]:
        return self._get(f"/users/me/calendarList/{calendar_id}")
    def insert_calendar_list(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._post("/users/me/calendarList", body=body)
    def delete_calendar_list(self, calendar_id: str) -> None:
        self._delete(f"/users/me/calendarList/{calendar_id}")
    def patch_calendar_list(self, calendar_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._patch(f"/users/me/calendarList/{calendar_id}", body=body)
    def update_calendar_list(self, calendar_id: str, params, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._put(f"/users/me/calendarList/{calendar_id}", params=params ,body=body)
    def watch_calendar_list(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._post("/users/me/calendarList/watch", body=body)

    # --- Calendars ---
    def get_calendar(self, calendar_id: str) -> Dict[str, Any]:
        return self._get(f"/calendars/{calendar_id}")
    def insert_calendar(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._post("/calendars", body=body)
    def update_calendar(self, calendar_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._put(f"/calendars/{calendar_id}", body=body)
    def patch_calendar(self, calendar_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._patch(f"/calendars/{calendar_id}", body=body)
    def delete_calendar(self, calendar_id: str) -> None:
        self._delete(f"/calendars/{calendar_id}")

    # --- Channels ---
    def watch(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._post("/channels/watch", body=body)
    def stop(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._post("/channels/stop", body=body)

    # --- Colors ---
    def get_colors(self) -> Dict[str, Any]:
        return self._get("/colors")

    # --- Events ---
    def list_events(self, calendar_id: str = "primary", params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._get(f"/calendars/{calendar_id}/events", params=params)
    def get_event(self, calendar_id: str, event_id: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._get(f"/calendars/{calendar_id}/events/{event_id}", params=params)
    def insert_event(self, calendar_id: str, body: Dict[str, Any], params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._post(f"/calendars/{calendar_id}/events", params=params, body=body)
    def update_event(self, calendar_id: str, event_id: str, body: Dict[str, Any], params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._put(f"/calendars/{calendar_id}/events/{event_id}", params=params, body=body)
    def get_instances(self, calendar_id: str, event_id: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._get(f"/calendars/{calendar_id}/events/{event_id}/instances", params=params)
    def patch_event(self, calendar_id: str, event_id: str, body: Dict[str, Any], params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._patch(f"/calendars/{calendar_id}/events/{event_id}", params=params, body=body)
    def delete_event(self, calendar_id: str, event_id: str, params: Optional[Dict[str, Any]] = None) -> None:
        self._delete(f"/calendars/{calendar_id}/events/{event_id}", params=params)
    def import_event(self, calendar_id: str, body: Dict[str, Any], params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._post(f"/calendars/{calendar_id}/events/import", params=params, body=body)
    def quick_add(self, calendar_id: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._post(f"/calendars/{calendar_id}/events/quickAdd", params={**(params or {})})
    def move_event(self, calendar_id: str, event_id: str, destination: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._post(
            f"/calendars/{calendar_id}/events/{event_id}/move",
            params={**(params or {}), "destination": destination}
        )
    def watch_events(self, calendar_id: str, body: Dict[str, Any], params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._post(f"/calendars/{calendar_id}/events/watch", params=params, body=body)

    # --- FreeBusy ---
    def query_freebusy(self, body: Dict[str, Any]) -> Dict[str, Any]:
        return self._post("/freeBusy", body=body)

    # --- Settings ---
    def list_settings(self, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        return self._get("/users/me/settings", params=params)
    def get_setting(self, setting: str) -> Dict[str, Any]:
        return self._get(f"/users/me/settings/{setting}")

    # --- Internal helpers ---
    def _get(self, path: str, params: Optional[Dict[str, Any]] = None) -> Any:
        resp = self.client.get(self.API_BASE + path, params=params or {})
        logger.info(f"GET Resonse with status {resp.status_code}")
        # resp.raise_for_status()
        return resp.json()

    def _post(self, path: str, params: Optional[Dict[str, Any]] = None, body: Optional[Dict[str, Any]] = None) -> Any:
        resp = self.client.post(self.API_BASE + path, params=params or {}, json=body or {})
        logger.info(f"POST Resonse with status {resp.status_code} - {resp.json()}")
        # resp.raise_for_status()
        return resp.json()

    def _put(self, path: str, params: Optional[Dict[str, Any]] = None, body: Optional[Dict[str, Any]] = None) -> Any:
        resp = self.client.put(self.API_BASE + path, params=params or {}, json=body or {})
        logger.info(f"PUT Resonse with status {resp.status_code} - {resp.json()}")
        # resp.raise_for_status()
        return resp.json()

    def _patch(self, path: str, params: Optional[Dict[str, Any]] = None, body: Optional[Dict[str, Any]] = None) -> Any:
        resp = self.client.patch(self.API_BASE + path, params=params or {}, json=body or {})
        logger.info(f"PATCH Resonse with status {resp.status_code} - {resp.json()}")
        # resp.raise_for_status()
        return resp.json()

    def _delete(self, path: str, params: Optional[Dict[str, Any]] = None) -> None:
        resp = self.client.delete(self.API_BASE + path, params=params or {})
        logger.info(f"DELETE Resonse with status {resp.status_code}")
        resp.raise_for_status()
