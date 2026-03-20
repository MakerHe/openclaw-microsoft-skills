# Git Repositories & Pull Requests API

Base: `https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/git`

## Repositories

### List Repositories

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/git/repositories?api-version=7.1"
```

### Get a Repository

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/git/repositories/{repoId}?api-version=7.1"
```

### Create a Repository

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X POST -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/git/repositories?api-version=7.1" \
  -d '{"name": "my-new-repo"}'
```

### Delete a Repository

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X DELETE \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/git/repositories/{repoId}?api-version=7.1"
```

## Branches (Refs)

### List Branches

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/git/repositories/{repoId}/refs?filter=heads/&api-version=7.1"
```

### List Tags

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/git/repositories/{repoId}/refs?filter=tags/&api-version=7.1"
```

### Create/Delete a Branch

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X POST -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/git/repositories/{repoId}/refs?api-version=7.1" \
  -d '[
    {
      "name": "refs/heads/new-branch",
      "oldObjectId": "0000000000000000000000000000000000000000",
      "newObjectId": "{sourceCommitId}"
    }
  ]'
```

To delete, set `newObjectId` to `0000000000000000000000000000000000000000` and `oldObjectId` to the current commit.

## Commits

### List Commits

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/git/repositories/{repoId}/commits?searchCriteria.itemVersion.version=main&api-version=7.1"
```

### Get a Commit

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/git/repositories/{repoId}/commits/{commitId}?api-version=7.1"
```

### Get Commit Diffs

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/git/repositories/{repoId}/diffs/commits?baseVersion=main&targetVersion=feature-branch&api-version=7.1"
```

## Items (File Content)

### Get File Content

```bash
# Get file as text
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/git/repositories/{repoId}/items?path=/README.md&api-version=7.1"

# Get file as JSON metadata
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/git/repositories/{repoId}/items?path=/README.md&includeContent=true&api-version=7.1" \
  -H "Accept: application/json"
```

### List Directory

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/git/repositories/{repoId}/items?scopePath=/src&recursionLevel=OneLevel&api-version=7.1" \
  -H "Accept: application/json"
```

## Pull Requests

### List Pull Requests

```bash
# Active PRs
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/git/repositories/{repoId}/pullrequests?searchCriteria.status=active&api-version=7.1"

# All PRs by creator
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/git/repositories/{repoId}/pullrequests?searchCriteria.creatorId={userId}&api-version=7.1"
```

### Get a Pull Request

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/git/repositories/{repoId}/pullrequests/{prId}?api-version=7.1"
```

### Create a Pull Request

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X POST -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/git/repositories/{repoId}/pullrequests?api-version=7.1" \
  -d '{
    "sourceRefName": "refs/heads/feature-branch",
    "targetRefName": "refs/heads/main",
    "title": "My Pull Request",
    "description": "Description of changes",
    "reviewers": [{"id": "{reviewerUserId}"}]
  }'
```

### Update a Pull Request

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X PATCH -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/git/repositories/{repoId}/pullrequests/{prId}?api-version=7.1" \
  -d '{
    "title": "Updated title",
    "description": "Updated description",
    "status": "completed",
    "lastMergeSourceCommit": {"commitId": "{commitId}"},
    "completionOptions": {
      "mergeStrategy": "squash",
      "deleteSourceBranch": true,
      "mergeCommitMessage": "Merged PR"
    }
  }'
```

Status values: `active`, `abandoned`, `completed`.

### Add a Reviewer

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X PUT -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/git/repositories/{repoId}/pullrequests/{prId}/reviewers/{reviewerId}?api-version=7.1" \
  -d '{"vote": 0}'
```

Vote values: `10` (approved), `5` (approved with suggestions), `0` (no vote), `-5` (waiting for author), `-10` (rejected).

### PR Comments (Threads)

```bash
# List threads
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/git/repositories/{repoId}/pullrequests/{prId}/threads?api-version=7.1"

# Create a thread
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X POST -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/git/repositories/{repoId}/pullrequests/{prId}/threads?api-version=7.1" \
  -d '{
    "comments": [{"parentCommentId": 0, "content": "Review comment here", "commentType": 1}],
    "status": 1
  }'
```

Thread status: `1` (active), `2` (fixed), `3` (won't fix), `4` (closed), `5` (by design), `6` (pending).

### PR Work Items

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/git/repositories/{repoId}/pullrequests/{prId}/workitems?api-version=7.1"
```

## Push (Create/Update Files)

```bash
curl -s -u ":$AZURE_DEVOPS_PAT" \
  -X POST -H "Content-Type: application/json" \
  "https://dev.azure.com/$AZURE_DEVOPS_ORG/$AZURE_DEVOPS_PROJECT/_apis/git/repositories/{repoId}/pushes?api-version=7.1" \
  -d '{
    "refUpdates": [{"name": "refs/heads/main", "oldObjectId": "{currentCommitId}"}],
    "commits": [{
      "comment": "Add file via API",
      "changes": [{
        "changeType": "add",
        "item": {"path": "/newfile.txt"},
        "newContent": {"content": "File content here", "contentType": "rawtext"}
      }]
    }]
  }'
```

Change types: `add`, `edit`, `delete`, `rename`.
