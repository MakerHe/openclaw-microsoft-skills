"""Calendar service for Microsoft 365."""

from __future__ import annotations

from typing import Any

from openclaw_microsoft_m365._base import BaseService

BASE = "https://graph.microsoft.com/v1.0/me"


class Calendar(BaseService):
    """Microsoft Graph Calendar API."""

    def __init__(self, http) -> None:
        super().__init__(http)

    def list_events(self, *, top: int = 10, order_by: str = "start/dateTime desc") -> dict:
        return self._get(f"{BASE}/events", params={"$top": str(top), "$orderby": order_by})

    def list_calendar_view(
        self, start: str, end: str, *, top: int = 50
    ) -> dict:
        return self._get(
            f"{BASE}/calendarView",
            params={"startDateTime": start, "endDateTime": end, "$top": str(top)},
        )

    def get_event(self, event_id: str) -> dict:
        return self._get(f"{BASE}/events/{event_id}")

    def create_event(
        self,
        subject: str,
        *,
        start: str,
        end: str,
        time_zone: str = "UTC",
        body: str | None = None,
        body_type: str = "HTML",
        location: str | None = None,
        attendees: list[str] | None = None,
        is_all_day: bool = False,
        recurrence: dict[str, Any] | None = None,
    ) -> dict:
        event: dict[str, Any] = {
            "subject": subject,
            "start": {"dateTime": start, "timeZone": time_zone},
            "end": {"dateTime": end, "timeZone": time_zone},
        }
        if body:
            event["body"] = {"contentType": body_type, "content": body}
        if location:
            event["location"] = {"displayName": location}
        if attendees:
            event["attendees"] = [
                {"emailAddress": {"address": a}, "type": "required"} for a in attendees
            ]
        if is_all_day:
            event["isAllDay"] = True
        if recurrence:
            event["recurrence"] = recurrence
        return self._post(f"{BASE}/events", json=event)

    def update_event(self, event_id: str, updates: dict[str, Any]) -> dict:
        return self._patch(f"{BASE}/events/{event_id}", json=updates)

    def delete_event(self, event_id: str) -> None:
        self._delete(f"{BASE}/events/{event_id}")

    def accept(self, event_id: str, *, send_response: bool = True) -> None:
        self._post(f"{BASE}/events/{event_id}/accept", json={"sendResponse": send_response})

    def decline(self, event_id: str, *, send_response: bool = True) -> None:
        self._post(f"{BASE}/events/{event_id}/decline", json={"sendResponse": send_response})

    def tentatively_accept(self, event_id: str, *, send_response: bool = True) -> None:
        self._post(
            f"{BASE}/events/{event_id}/tentativelyAccept",
            json={"sendResponse": send_response},
        )

    def get_schedule(
        self,
        schedules: list[str],
        *,
        start: str,
        end: str,
        time_zone: str = "UTC",
        interval: int = 30,
    ) -> dict:
        return self._post(
            f"{BASE}/calendar/getSchedule",
            json={
                "schedules": schedules,
                "startTime": {"dateTime": start, "timeZone": time_zone},
                "endTime": {"dateTime": end, "timeZone": time_zone},
                "availabilityViewInterval": interval,
            },
        )

    def list_calendars(self) -> dict:
        return self._get(f"{BASE}/calendars")

    def find_meeting_times(
        self,
        attendees: list[str],
        *,
        start: str,
        end: str,
        time_zone: str = "UTC",
        duration: str = "PT1H",
    ) -> dict:
        return self._post(
            f"{BASE}/findMeetingTimes",
            json={
                "attendees": [
                    {"emailAddress": {"address": a}, "type": "required"} for a in attendees
                ],
                "timeConstraint": {
                    "timeslots": [
                        {
                            "start": {"dateTime": start, "timeZone": time_zone},
                            "end": {"dateTime": end, "timeZone": time_zone},
                        }
                    ]
                },
                "meetingDuration": duration,
            },
        )
