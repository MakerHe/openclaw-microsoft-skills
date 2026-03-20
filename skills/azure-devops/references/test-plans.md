# Test Plans & Test Management API

Base: `https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/test` and `_apis/testplan`

## Test Plans

### List Test Plans

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/testplan/plans?api-version=7.1"
```

### Get a Test Plan

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/testplan/plans/{planId}?api-version=7.1"
```

### Create a Test Plan

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X POST -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/testplan/plans?api-version=7.1" \
  -d '{
    "name": "Sprint 1 Test Plan",
    "areaPath": "MyProject\\Team1",
    "iteration": "MyProject\\Sprint 1"
  }'
```

## Test Suites

### List Suites in a Plan

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/testplan/plans/{planId}/suites?api-version=7.1"
```

### Create a Test Suite

```bash
# Static suite
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X POST -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/testplan/plans/{planId}/suites?api-version=7.1" \
  -d '{
    "suiteType": "staticTestSuite",
    "name": "Manual Tests",
    "parentSuite": {"id": {parentSuiteId}}
  }'
```

## Test Cases

### List Test Cases in a Suite

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/testplan/plans/{planId}/suites/{suiteId}/testcase?api-version=7.1"
```

### Add Test Cases to a Suite

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X POST -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/testplan/plans/{planId}/suites/{suiteId}/testcase?api-version=7.1" \
  -d '[{"workItem": {"id": {testCaseWorkItemId}}}]'
```

## Test Runs

### List Test Runs

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/test/runs?api-version=7.1"
```

### Create a Test Run

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X POST -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/test/runs?api-version=7.1" \
  -d '{
    "name": "Sprint 1 Run",
    "plan": {"id": {planId}},
    "pointIds": [1, 2, 3],
    "automated": false
  }'
```

### Get a Test Run

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/test/runs/{runId}?api-version=7.1"
```

### Update Test Run (Complete)

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X PATCH -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/test/runs/{runId}?api-version=7.1" \
  -d '{"state": "Completed"}'
```

## Test Results

### List Results for a Run

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/test/runs/{runId}/results?api-version=7.1"
```

### Add Results

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X POST -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/test/runs/{runId}/results?api-version=7.1" \
  -d '[
    {
      "testCaseTitle": "Login Test",
      "outcome": "Passed",
      "state": "Completed",
      "comment": "All assertions passed"
    }
  ]'
```

Outcome values: `Passed`, `Failed`, `Inconclusive`, `Timeout`, `Aborted`, `Blocked`, `NotExecuted`, `Warning`, `Error`, `NotApplicable`, `Paused`, `InProgress`.

## Test Points

```bash
# List test points for a suite
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/testplan/plans/{planId}/suites/{suiteId}/testpoint?api-version=7.1"
```

## Test Configurations

```bash
# List configurations
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/testplan/configurations?api-version=7.1"
```
