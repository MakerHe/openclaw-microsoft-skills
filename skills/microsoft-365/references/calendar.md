# Calendar API

Base path: `https://graph.microsoft.com/v1.0/me`

Permissions: `Calendars.ReadWrite`

## List Events

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/events?\$top=10&\$orderby=start/dateTime%20desc" | jq '.value[] | {subject, start: .start.dateTime, end: .end.dateTime, location: .location.displayName}'
```

## List Events in Date Range (Calendar View)

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/calendarView?startDateTime=2025-01-01T00:00:00Z&endDateTime=2025-01-31T23:59:59Z&\$top=50" | jq '.value[] | {subject, start: .start.dateTime, end: .end.dateTime}'
```

## Get an Event

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/events/{event-id}" | jq '{subject, body: .body.content, start, end, location, attendees}'
```

## Create an Event

```bash
curl -s -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/me/events" \
  -d '{
    "subject": "Team Meeting",
    "body": {"contentType": "HTML", "content": "<p>Agenda items here</p>"},
    "start": {"dateTime": "2025-06-15T14:00:00", "timeZone": "UTC"},
    "end": {"dateTime": "2025-06-15T15:00:00", "timeZone": "UTC"},
    "location": {"displayName": "Conference Room A"},
    "attendees": [
      {
        "emailAddress": {"address": "colleague@example.com", "name": "Colleague"},
        "type": "required"
      }
    ]
  }'
```

## Create an All-Day Event

```bash
curl -s -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/me/events" \
  -d '{
    "subject": "Company Holiday",
    "isAllDay": true,
    "start": {"dateTime": "2025-12-25T00:00:00", "timeZone": "UTC"},
    "end": {"dateTime": "2025-12-26T00:00:00", "timeZone": "UTC"}
  }'
```

## Create a Recurring Event

```bash
curl -s -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/me/events" \
  -d '{
    "subject": "Weekly Standup",
    "start": {"dateTime": "2025-06-16T09:00:00", "timeZone": "UTC"},
    "end": {"dateTime": "2025-06-16T09:30:00", "timeZone": "UTC"},
    "recurrence": {
      "pattern": {"type": "weekly", "interval": 1, "daysOfWeek": ["monday"]},
      "range": {"type": "endDate", "startDate": "2025-06-16", "endDate": "2025-12-31"}
    }
  }'
```

## Update an Event

```bash
curl -s -X PATCH -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/me/events/{event-id}" \
  -d '{
    "subject": "Updated Meeting Title",
    "location": {"displayName": "Conference Room B"}
  }'
```

## Delete an Event

```bash
curl -s -X DELETE -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/events/{event-id}"
```

## Accept/Decline/Tentatively Accept an Event

```bash
# Accept
curl -s -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/me/events/{event-id}/accept" \
  -d '{"sendResponse": true}'

# Decline
curl -s -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/me/events/{event-id}/decline" \
  -d '{"sendResponse": true}'

# Tentatively accept
curl -s -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/me/events/{event-id}/tentativelyAccept" \
  -d '{"sendResponse": true}'
```

## Get Free/Busy Schedule

```bash
curl -s -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/me/calendar/getSchedule" \
  -d '{
    "schedules": ["user1@example.com", "user2@example.com"],
    "startTime": {"dateTime": "2025-06-15T09:00:00", "timeZone": "UTC"},
    "endTime": {"dateTime": "2025-06-15T18:00:00", "timeZone": "UTC"},
    "availabilityViewInterval": 30
  }'
```

## List Calendars

```bash
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://graph.microsoft.com/v1.0/me/calendars" | jq '.value[] | {id, name, color}'
```

## Find Meeting Times

```bash
curl -s -X POST -H "Authorization: Bearer $ACCESS_TOKEN" \
  -H "Content-Type: application/json" \
  "https://graph.microsoft.com/v1.0/me/findMeetingTimes" \
  -d '{
    "attendees": [
      {"emailAddress": {"address": "colleague@example.com"}, "type": "required"}
    ],
    "timeConstraint": {
      "timeslots": [
        {
          "start": {"dateTime": "2025-06-16T09:00:00", "timeZone": "UTC"},
          "end": {"dateTime": "2025-06-16T18:00:00", "timeZone": "UTC"}
        }
      ]
    },
    "meetingDuration": "PT1H"
  }'
```
