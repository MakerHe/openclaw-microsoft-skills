# Git Repos

Service: `client.git_repos`

## Repositories

```python
result = client.git_repos.list_repos()
result = client.git_repos.get_repo(repo_id)
result = client.git_repos.create_repo("new-repo")
client.git_repos.delete_repo(repo_id)
```

## Branches / Tags

```python
result = client.git_repos.list_branches(repo_id)
result = client.git_repos.list_tags(repo_id)
result = client.git_repos.create_branch(repo_id, branch_name="feature/x", source_branch="main")
result = client.git_repos.delete_branch(repo_id, branch_name="feature/x", object_id="commit-sha")
```

## Commits

```python
result = client.git_repos.list_commits(repo_id, branch="main")
result = client.git_repos.get_commit(repo_id, commit_id)
result = client.git_repos.get_commit_diffs(repo_id, base_version="main", target_version="feature/x")
```

## File Content / Directory

```python
content = client.git_repos.get_file(repo_id, path="src/main.py", branch="main")
result = client.git_repos.list_directory(repo_id, path="/", branch="main")
```

## Pull Requests

```python
result = client.git_repos.list_pull_requests(repo_id, status="active", top=20)
result = client.git_repos.get_pull_request(repo_id, pr_id)
result = client.git_repos.create_pull_request(
    repo_id, source_branch="refs/heads/feature/x", target_branch="refs/heads/main",
    title="My PR", description="Description",
)
result = client.git_repos.update_pull_request(repo_id, pr_id, updates={"status": "completed"})
result = client.git_repos.add_reviewer(repo_id, pr_id, reviewer_id, vote=0)
```

Vote values: `10` (approved), `5` (approved with suggestions), `0` (no vote), `-5` (waiting), `-10` (rejected).

## PR Threads / Work Items

```python
result = client.git_repos.list_pr_threads(repo_id, pr_id)
result = client.git_repos.create_pr_thread(repo_id, pr_id, content="Review comment")
result = client.git_repos.list_pr_work_items(repo_id, pr_id)
```

## Push

```python
result = client.git_repos.push(repo_id, ref_updates, commits)
```
