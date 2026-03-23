# Test Plans

Service: `client.test_plans`

## Plans

```python
result = client.test_plans.list_plans()
result = client.test_plans.get_plan(plan_id)
result = client.test_plans.create_plan(name="Sprint 1 Tests", area_path="MyProject\\Tests", iteration="MyProject\\Sprint 1")
```

## Suites

```python
result = client.test_plans.list_suites(plan_id)
result = client.test_plans.create_suite(plan_id, name="Regression", suite_type="staticTestSuite", parent_suite_id=root_suite_id)
```

Suite types: `staticTestSuite`, `dynamicTestSuite`, `requirementTestSuite`.

## Test Cases / Points

```python
result = client.test_plans.list_test_cases(plan_id, suite_id)
result = client.test_plans.add_test_cases(plan_id, suite_id, work_item_ids=[101, 102])
result = client.test_plans.list_points(plan_id, suite_id)
```

## Runs / Results

```python
result = client.test_plans.list_runs()
result = client.test_plans.create_run(name="Automated Run", plan_id=plan_id, point_ids=[1, 2, 3])
result = client.test_plans.get_run(run_id)
result = client.test_plans.complete_run(run_id)
result = client.test_plans.list_results(run_id)
result = client.test_plans.add_results(run_id, results=[
    {"testCaseTitle": "Login Test", "outcome": "Passed"},
])
```

Outcome values: `Passed`, `Failed`, `Blocked`, `NotApplicable`, `Paused`, `InProgress`.

## Configurations

```python
result = client.test_plans.list_configurations()
```
