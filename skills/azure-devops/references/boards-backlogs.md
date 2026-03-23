# Boards & Backlogs

Service: `client.boards_backlogs`

## Boards

```python
result = client.boards_backlogs.list_boards()
result = client.boards_backlogs.get_board(board_id)
result = client.boards_backlogs.get_columns(board_id)
result = client.boards_backlogs.update_columns(board_id, columns=[...])
result = client.boards_backlogs.get_rows(board_id)
```

## Backlogs

```python
result = client.boards_backlogs.list_backlogs()
result = client.boards_backlogs.get_backlog_items(backlog_id)
```

## Iterations / Sprints

```python
result = client.boards_backlogs.list_iterations()
result = client.boards_backlogs.get_current_iteration()
result = client.boards_backlogs.get_iteration_work_items(iteration_id)
result = client.boards_backlogs.get_iteration_capacity(iteration_id)
result = client.boards_backlogs.add_iteration(iteration_id)
```

## Team Settings

```python
result = client.boards_backlogs.get_settings()
result = client.boards_backlogs.update_settings(settings={...})
result = client.boards_backlogs.get_team_field_values()
```
