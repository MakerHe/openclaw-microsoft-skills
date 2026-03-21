#!/usr/bin/env bash
# =============================================================================
# Microsoft 365 Skill — Smoke Tests
# =============================================================================
# Prerequisites:
#   - MICROSOFT_CLIENT_ID, MICROSOFT_TENANT_ID set
#   - A valid Graph API access token in $ACCESS_TOKEN
#     (use Device Code Flow: skills/shared/auth/device-code-flow.md)
#
# Usage:
#   export ACCESS_TOKEN="eyJ0..."
#   bash tests/microsoft-365/smoke-test.sh
#
# Or run a single test:
#   bash tests/microsoft-365/smoke-test.sh outlook_read
# =============================================================================

set -uo pipefail

API="https://graph.microsoft.com/v1.0"
PASS=0
FAIL=0
SKIP=0
RESULTS=()

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
check_token() {
  if [ -z "${ACCESS_TOKEN:-}" ]; then
    echo "ERROR: ACCESS_TOKEN is not set."
    echo "Run Device Code Flow first (see skills/shared/auth/device-code-flow.md)"
    exit 1
  fi
}

graph_get() {
  curl -s -H "Authorization: Bearer $ACCESS_TOKEN" "$API$1"
}

graph_post() {
  local endpoint="$1"
  local body="$2"
  curl -s -w "\n%{http_code}" -X POST \
    -H "Authorization: Bearer $ACCESS_TOKEN" \
    -H "Content-Type: application/json" \
    "$API$endpoint" -d "$body"
}

# Parse response: body on all lines except last, status code on last line
parse_response() {
  local response="$1"
  RESP_BODY=$(echo "$response" | sed '$d')
  RESP_CODE=$(echo "$response" | tail -1)
}

report() {
  local test_name="$1"
  local status="$2"  # PASS / FAIL / SKIP
  local detail="${3:-}"

  case "$status" in
    PASS) ((PASS++)); icon="✅" ;;
    FAIL) ((FAIL++)); icon="❌" ;;
    SKIP) ((SKIP++)); icon="⏭️" ;;
  esac

  RESULTS+=("$icon $test_name — $status${detail:+ ($detail)}")
  echo "$icon [$status] $test_name${detail:+ — $detail}"
}

# ---------------------------------------------------------------------------
# Test: Outlook — Read inbox
# ---------------------------------------------------------------------------
test_outlook_read() {
  echo ""
  echo "── Outlook: Read inbox ──"
  local result
  result=$(graph_get '/me/mailFolders/inbox/messages?$top=3&$select=subject,from,receivedDateTime&$orderby=receivedDateTime%20desc')
  local count
  count=$(echo "$result" | jq '.value | length' 2>/dev/null || echo "0")

  if [ "$count" -gt 0 ]; then
    report "outlook_read" "PASS" "returned $count messages"
    echo "$result" | jq -r '.value[] | "  • \(.subject) [\(.from.emailAddress.address)]"' 2>/dev/null
  else
    local err
    err=$(echo "$result" | jq -r '.error.message // empty' 2>/dev/null)
    report "outlook_read" "FAIL" "${err:-no messages or error}"
  fi
}

# ---------------------------------------------------------------------------
# Test: Outlook — Send mail
# ---------------------------------------------------------------------------
test_outlook_send() {
  echo ""
  echo "── Outlook: Send mail ──"
  local ts
  ts=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  local body
  body=$(cat <<EOF
{
  "message": {
    "subject": "[Smoke Test] M365 Skill — Outlook Send ($ts)",
    "body": {"contentType": "Text", "content": "Automated smoke test at $ts"},
    "toRecipients": [{"emailAddress": {"address": "Mylene.Russel@mahk.org"}}]
  }
}
EOF
)
  local response
  response=$(graph_post "/me/sendMail" "$body")
  parse_response "$response"

  if [ "$RESP_CODE" = "202" ]; then
    report "outlook_send" "PASS" "HTTP $RESP_CODE"
  else
    local err
    err=$(echo "$RESP_BODY" | jq -r '.error.message // empty' 2>/dev/null)
    report "outlook_send" "FAIL" "HTTP $RESP_CODE${err:+ — $err}"
  fi
}

# ---------------------------------------------------------------------------
# Test: OneNote — List notebooks
# ---------------------------------------------------------------------------
test_onenote_list() {
  echo ""
  echo "── OneNote: List notebooks ──"
  local result
  result=$(graph_get '/me/onenote/notebooks?$select=displayName,createdDateTime&$top=5')
  local count
  count=$(echo "$result" | jq '.value | length' 2>/dev/null || echo "-1")

  if [ "$count" -ge 0 ]; then
    report "onenote_list" "PASS" "found $count notebooks"
    echo "$result" | jq -r '.value[] | "  • \(.displayName)"' 2>/dev/null
  else
    local err
    err=$(echo "$result" | jq -r '.error.message // empty' 2>/dev/null)
    report "onenote_list" "FAIL" "${err:-unexpected response}"
  fi
}

# ---------------------------------------------------------------------------
# Test: OneNote — Create notebook
# ---------------------------------------------------------------------------
test_onenote_create() {
  echo ""
  echo "── OneNote: Create notebook ──"
  local ts
  ts=$(date -u +"%Y%m%d-%H%M%S")
  local response
  response=$(graph_post "/me/onenote/notebooks" "{\"displayName\": \"SmokeTest-$ts\"}")
  parse_response "$response"

  if [ "$RESP_CODE" = "201" ]; then
    local name
    name=$(echo "$RESP_BODY" | jq -r '.displayName // empty' 2>/dev/null)
    report "onenote_create" "PASS" "created '$name'"
  else
    local err
    err=$(echo "$RESP_BODY" | jq -r '.error.message // empty' 2>/dev/null)
    report "onenote_create" "FAIL" "HTTP $RESP_CODE${err:+ — $err}"
  fi
}

# ---------------------------------------------------------------------------
# Test: SharePoint — Get root site
# ---------------------------------------------------------------------------
test_sharepoint_root() {
  echo ""
  echo "── SharePoint: Get root site ──"
  local result
  result=$(graph_get '/sites/root?$select=displayName,webUrl')
  local name
  name=$(echo "$result" | jq -r '.displayName // empty' 2>/dev/null)

  if [ -n "$name" ]; then
    local url
    url=$(echo "$result" | jq -r '.webUrl' 2>/dev/null)
    report "sharepoint_root" "PASS" "$name ($url)"
  else
    local err
    err=$(echo "$result" | jq -r '.error.message // empty' 2>/dev/null)
    report "sharepoint_root" "FAIL" "${err:-unexpected response}"
  fi
}

# ---------------------------------------------------------------------------
# Test: SharePoint — Search sites
# ---------------------------------------------------------------------------
test_sharepoint_search() {
  echo ""
  echo "── SharePoint: Search sites ──"
  local result
  result=$(graph_get '/sites?search=*&$top=5&$select=displayName,webUrl')
  local count
  count=$(echo "$result" | jq '.value | length' 2>/dev/null || echo "-1")

  if [ "$count" -gt 0 ]; then
    report "sharepoint_search" "PASS" "found $count sites"
    echo "$result" | jq -r '.value[] | "  • \(.displayName) — \(.webUrl)"' 2>/dev/null
  elif [ "$count" -eq 0 ]; then
    report "sharepoint_search" "PASS" "0 sites (empty tenant)"
  else
    local err
    err=$(echo "$result" | jq -r '.error.message // empty' 2>/dev/null)
    report "sharepoint_search" "FAIL" "${err:-unexpected response}"
  fi
}

# ---------------------------------------------------------------------------
# Test: Teams — List joined teams
# ---------------------------------------------------------------------------
test_teams_list() {
  echo ""
  echo "── Teams: List joined teams ──"
  local result
  result=$(graph_get '/me/joinedTeams?$select=displayName,id')
  local count
  count=$(echo "$result" | jq '.value | length' 2>/dev/null || echo "-1")

  if [ "$count" -gt 0 ]; then
    report "teams_list" "PASS" "joined $count teams"
    echo "$result" | jq -r '.value[] | "  • \(.displayName)"' 2>/dev/null
    # Export first team for subsequent tests
    TEAM_ID=$(echo "$result" | jq -r '.value[0].id')
    TEAM_NAME=$(echo "$result" | jq -r '.value[0].displayName')
  elif [ "$count" -eq 0 ]; then
    report "teams_list" "SKIP" "no teams joined"
  else
    local err
    err=$(echo "$result" | jq -r '.error.message // empty' 2>/dev/null)
    report "teams_list" "FAIL" "${err:-unexpected response}"
  fi
}

# ---------------------------------------------------------------------------
# Test: Teams — List channels & send channel message
# ---------------------------------------------------------------------------
test_teams_channel_message() {
  echo ""
  echo "── Teams: Channel message ──"
  if [ -z "${TEAM_ID:-}" ]; then
    report "teams_channel_message" "SKIP" "no team available"
    return
  fi

  # List channels
  local channels
  channels=$(graph_get "/teams/$TEAM_ID/channels?\$select=displayName,id")
  local ch_count
  ch_count=$(echo "$channels" | jq '.value | length' 2>/dev/null || echo "0")
  echo "  Channels in '$TEAM_NAME': $ch_count"

  if [ "$ch_count" -eq 0 ]; then
    report "teams_channel_message" "SKIP" "no channels"
    return
  fi

  # Use General channel if available, otherwise first channel
  local channel_id channel_name
  channel_id=$(echo "$channels" | jq -r '[.value[] | select(.displayName == "General")][0].id // .value[0].id')
  channel_name=$(echo "$channels" | jq -r '[.value[] | select(.displayName == "General")][0].displayName // .value[0].displayName')

  local ts
  ts=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  local response
  response=$(graph_post "/teams/$TEAM_ID/channels/$channel_id/messages" \
    "{\"body\": {\"content\": \"[Smoke Test] Channel message at $ts\"}}")
  parse_response "$response"

  if [ "$RESP_CODE" = "201" ]; then
    report "teams_channel_message" "PASS" "sent to '$channel_name' (HTTP $RESP_CODE)"
  else
    local err
    err=$(echo "$RESP_BODY" | jq -r '.error.message // empty' 2>/dev/null)
    report "teams_channel_message" "FAIL" "HTTP $RESP_CODE${err:+ — $err}"
  fi
}

# ---------------------------------------------------------------------------
# Test: Teams — 1-1 chat
# ---------------------------------------------------------------------------
test_teams_1on1_chat() {
  echo ""
  echo "── Teams: 1-1 chat ──"

  # Get my ID
  local my_id
  my_id=$(graph_get '/me?$select=id' | jq -r '.id // empty' 2>/dev/null)
  if [ -z "$my_id" ]; then
    report "teams_1on1_chat" "FAIL" "cannot get own user ID"
    return
  fi

  # Find another user
  local users other_id other_name
  users=$(graph_get '/users?$top=10&$select=displayName,id,userPrincipalName')
  other_id=$(echo "$users" | jq -r --arg me "$my_id" '[.value[] | select(.id != $me)][0].id // empty')
  other_name=$(echo "$users" | jq -r --arg me "$my_id" '[.value[] | select(.id != $me)][0].displayName // empty')

  if [ -z "$other_id" ]; then
    report "teams_1on1_chat" "SKIP" "no other users in tenant"
    return
  fi

  echo "  Target: $other_name ($other_id)"

  # Create 1-1 chat
  local chat_body
  chat_body=$(cat <<EOF
{
  "chatType": "oneOnOne",
  "members": [
    {"@odata.type": "#microsoft.graph.aadUserConversationMember", "roles": ["owner"], "user@odata.bind": "https://graph.microsoft.com/v1.0/users('$my_id')"},
    {"@odata.type": "#microsoft.graph.aadUserConversationMember", "roles": ["owner"], "user@odata.bind": "https://graph.microsoft.com/v1.0/users('$other_id')"}
  ]
}
EOF
)
  local response
  response=$(graph_post "/chats" "$chat_body")
  parse_response "$response"

  local chat_id
  chat_id=$(echo "$RESP_BODY" | jq -r '.id // empty' 2>/dev/null)

  if [ -z "$chat_id" ] || [ "$chat_id" = "null" ]; then
    local err
    err=$(echo "$RESP_BODY" | jq -r '.error.message // empty' 2>/dev/null)
    report "teams_1on1_chat" "FAIL" "cannot create chat${err:+ — $err}"
    return
  fi

  # Send message
  local ts
  ts=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
  response=$(graph_post "/chats/$chat_id/messages" \
    "{\"body\": {\"content\": \"[Smoke Test] 1-1 chat with $other_name at $ts\"}}")
  parse_response "$response"

  if [ "$RESP_CODE" = "201" ]; then
    report "teams_1on1_chat" "PASS" "sent to $other_name (HTTP $RESP_CODE)"
  else
    local err
    err=$(echo "$RESP_BODY" | jq -r '.error.message // empty' 2>/dev/null)
    report "teams_1on1_chat" "FAIL" "HTTP $RESP_CODE${err:+ — $err}"
  fi
}

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
main() {
  check_token

  echo "============================================"
  echo " Microsoft 365 Skill — Smoke Tests"
  echo " $(date -u +"%Y-%m-%d %H:%M:%S UTC")"
  echo "============================================"

  # Verify identity
  local me
  me=$(graph_get '/me?$select=displayName,userPrincipalName')
  echo "Authenticated as: $(echo "$me" | jq -r '"\(.displayName) (\(.userPrincipalName))"' 2>/dev/null)"
  echo ""

  # If a specific test is requested, run only that
  if [ -n "${1:-}" ]; then
    "test_$1"
  else
    test_outlook_read
    test_outlook_send
    test_onenote_list
    test_onenote_create
    test_sharepoint_root
    test_sharepoint_search
    test_teams_list
    test_teams_channel_message
    test_teams_1on1_chat
  fi

  # Summary
  echo ""
  echo "============================================"
  echo " SUMMARY: $PASS passed, $FAIL failed, $SKIP skipped"
  echo "============================================"
  for r in "${RESULTS[@]}"; do
    echo "  $r"
  done
  echo ""

  if [ "$FAIL" -gt 0 ]; then
    exit 1
  fi
}

main "$@"
