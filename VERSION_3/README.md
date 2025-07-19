# Todo App with Full Test Coverage

## Test Architecture

├── tests/
│ ├── test_controller.py # 42 tests (90% coverage)
│ ├── test_exporter.py # 5 tests (100%)
│ ├── test_history.py # 5 tests (100%)
│ ├── test_importer.py # 4 tests (100%)
│ ├── test_integration.py # 1 E2E test
│ ├── test_model.py # 21 tests (97%)
│ └── test_view.py # 6 tests (82%)
└── coverage/ # 92% total
text


### Running Tests

**Basic test suite:**
```bash
pytest -v tests/

With coverage report:
bash

pytest --cov=src --cov-report=html tests/
open htmlcov/index.html

Key Test Patterns

    Mocking:

        Filesystem operations

        User inputs

        Model-view interactions

    Fixtures:

        sample_todo: Standard todo item

        empty_model: Fresh model instance

        real_controller: Full integrated controller

    Verification:
    python

# Example assertion patterns
assert "1" in model.todos
assert "Error" in capsys.readouterr().out
mock_error.assert_called_once_with("Invalid choice")