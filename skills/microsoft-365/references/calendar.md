# Calendar

Service: `client.calendar` — Permissions: `Calendars.ReadWrite`

## List Events

```python
result = client.calendar.list_events(top=10, order_by="start/dateTime desc")
```

## Calendar View (Date Range)

```python
result = client.calendar.list_calendar_view(
    start_date_time="2025-01-01T00:00:00Z",
    end_date_time="2025-01-31T23:59:59Z",
)
```

## Get / Delete an Event

```python
result = client.calendar.get_event(event_id)
result = client.calendar.delete_event(event_id)
```

## Create an Event

```python
result = client.calendar.create_event(
    subject="Team Meeting",
    start="2025-06-15T14:00:00",
    end="2025-06-15T15:00:00",
    timezone="UTC",
    body="<p>Agenda items</p>",
    attendees=["colleague@example.com"],
    location="Conference Room A",
    is_online=False,
)

# Recurring event
result = client.calendar.create_event(
    subject="Weekly Standup",
    start="2025-06-16T09:00:00",
    end="2025-06-16T09:30:00",
    recurrence={
        "pattern": {"type": "weekly", "interval": 1, "daysOfWeek": ["monday"]},
        "range": {"type": "endDate", "startDate": "2025-06-16", "endDate": "2025-12-31"},
    },
)
```

## Update an Event

```python
result = client.calendar.update_event(event_id, updates={
    "subject": "Updated Title",
    "location": {"displayName": "Room B"},
})
```

## Accept / Decline / Tentatively Accept

```python
result = client.calendar.accept(event_id, send_response=True)
result = client.calendar.decline(event_id, send_response=True)
result = client.calendar.tentatively_accept(event_id, send_response=True)
```

## Free/Busy Schedule

```python
result = client.calendar.get_schedule(
    schedules=["user1@example.com", "user2@example.com"],
    start="2025-06-15T09:00:00",
    end="2025-06-15T18:00:00",
    timezone="UTC",
    availability_view_interval=30,
)
```

## List Calendars

```python
result = client.calendar.list_calendars()
```

## Find Meeting Times

```python
result = client.calendar.find_meeting_times(
    attendees=["colleague@example.com"],
    duration_minutes=60,
    start="2025-06-16T09:00:00",
    end="2025-06-16T18:00:00",
)
```
