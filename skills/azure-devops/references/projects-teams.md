# Projects & Teams

Service: `client.projects_teams`

## Projects

```python
result = client.projects_teams.list_projects()
result = client.projects_teams.get_project(project_id)
result = client.projects_teams.create_project(name="NewProject", description="A new project", source_control_type="Git", template_type_id="6b724908-ef14-45cf-84f8-768b5384da45")
result = client.projects_teams.update_project(project_id, updates={"description": "Updated"})
client.projects_teams.delete_project(project_id)
```

## Teams

```python
result = client.projects_teams.list_teams()
result = client.projects_teams.get_team(team_id)
result = client.projects_teams.create_team("New Team", description="Team description")
result = client.projects_teams.list_team_members(team_id)
```

## Processes

```python
result = client.projects_teams.list_processes()
result = client.projects_teams.get_process(process_id)
```

## Properties / Areas / Iterations

```python
result = client.projects_teams.get_properties()
result = client.projects_teams.list_areas(depth=10)
result = client.projects_teams.list_iterations(depth=10)
result = client.projects_teams.create_area("New Area")
result = client.projects_teams.create_iteration("Sprint 1", start_date="2025-01-01", finish_date="2025-01-14")
```
