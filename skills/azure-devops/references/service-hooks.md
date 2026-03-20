# Service Hooks API

Base: `https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/hooks`

## List Subscriptions

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/hooks/subscriptions?api-version=7.1"
```

## Get a Subscription

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/hooks/subscriptions/{subscriptionId}?api-version=7.1"
```

## Create a Subscription (Webhook)

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X POST -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/hooks/subscriptions?api-version=7.1" \
  -d '{
    "publisherId": "tfs",
    "eventType": "workitem.updated",
    "resourceVersion": "1.0",
    "consumerId": "webHooks",
    "consumerActionId": "httpRequest",
    "publisherInputs": {
      "projectId": "{projectId}",
      "areaPath": "",
      "workItemType": ""
    },
    "consumerInputs": {
      "url": "https://example.com/webhook"
    }
  }'
```

Common event types:
- `workitem.created` — Work item created
- `workitem.updated` — Work item updated
- `workitem.deleted` — Work item deleted
- `workitem.commented` — Comment added to work item
- `git.push` — Code pushed
- `git.pullrequest.created` — PR created
- `git.pullrequest.updated` — PR updated
- `git.pullrequest.merged` — PR merged
- `build.complete` — Build completed
- `ms.vss-release.release-created-event` — Release created
- `ms.vss-release.deployment-completed-event` — Deployment completed

Publisher IDs:
- `tfs` — Work items, Git, Build
- `rm` — Release Management
- `ms.vss-pipelines.pipeline-resource-event` — Pipeline resources

Consumer IDs:
- `webHooks` — Generic webhook
- `slack` — Slack
- `teams` — Microsoft Teams
- `azureStorageQueue` — Azure Storage Queue
- `azureServiceBus` — Azure Service Bus
- `jenkins` — Jenkins
- `zendesk` — Zendesk

## Update a Subscription

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X PUT -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/hooks/subscriptions/{subscriptionId}?api-version=7.1" \
  -d '{
    "publisherId": "tfs",
    "eventType": "workitem.updated",
    "consumerId": "webHooks",
    "consumerActionId": "httpRequest",
    "consumerInputs": {
      "url": "https://example.com/new-webhook"
    }
  }'
```

## Delete a Subscription

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X DELETE \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/hooks/subscriptions/{subscriptionId}?api-version=7.1"
```

## List Publishers

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/hooks/publishers?api-version=7.1"
```

## List Consumers

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/hooks/consumers?api-version=7.1"
```

## Test Notification

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X POST -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/hooks/testnotifications?api-version=7.1" \
  -d '{
    "subscriptionId": "{subscriptionId}"
  }'
```

## List Notifications (History)

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/_apis/hooks/subscriptions/{subscriptionId}/notifications?api-version=7.1"
```
