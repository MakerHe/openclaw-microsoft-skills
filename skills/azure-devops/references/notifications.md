# Notifications API

Base: `https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/notification`

## Subscriptions

### List My Subscriptions

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/notification/subscriptions?api-version=7.1"
```

### Get a Subscription

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/notification/subscriptions/{subscriptionId}?api-version=7.1"
```

### Create a Subscription

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X POST -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/notification/subscriptions?api-version=7.1" \
  -d '{
    "description": "Notify on build failures",
    "filter": {
      "type": "Expression",
      "filterModel": {
        "clauses": [{
          "logicalOperator": "",
          "fieldName": "Build.Result",
          "operator": "=",
          "value": "Failed",
          "index": 1
        }]
      }
    },
    "channel": {
      "type": "EmailHtml"
    },
    "scope": {
      "id": "{projectId}"
    }
  }'
```

### Update a Subscription

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X PUT -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/notification/subscriptions/{subscriptionId}?api-version=7.1" \
  -d '{
    "status": "disabled"
  }'
```

### Delete a Subscription

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X DELETE \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/notification/subscriptions/{subscriptionId}?api-version=7.1"
```

## Event Types

### List Event Types

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/notification/eventtypes?api-version=7.1"
```

## Notification Statistics

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/notification/subscriptions/{subscriptionId}/diagnostics?api-version=7.1-preview.1"
```

## Global Notification Settings

```bash
# Get settings
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/notification/settings?api-version=7.1-preview.1"
```

## Subscriber (User Notification Settings)

```bash
# Get subscriber info
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/notification/subscribers/{subscriberId}?api-version=7.1-preview.1"

# Update subscriber delivery preferences
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X PATCH -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/notification/subscribers/{subscriberId}?api-version=7.1-preview.1" \
  -d '{"deliveryPreference": "preferredEmailAddress"}'
```
