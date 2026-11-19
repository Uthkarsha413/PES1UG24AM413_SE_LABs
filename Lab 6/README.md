# L6_L7_41 — Laundry Service

Lab 6: Code and Branch Coverage

## About

A small Python module that works out extra-weight charges by garment type, speed and membership, checks whether an order can be accepted and reports the drop-off cutoff status.

## Files

| File | Description |
|------|-------------|
| `laundry_service.py` | The module under test |
| `test_laundry_service.py` | Starter test file |
| `CodeCoverageTest_laundry_service_application.py` | Targeted test cases achieving 100% line coverage |
| `BranchCoverageTest_laundry_service_application.py` | Comprehensive test cases covering all edge cases and decision branches (100% branch coverage) |
| `screenshots/` | Terminal output screenshots for code coverage and branch coverage analysis |

## Running Coverage

### Code Coverage
```bash
coverage run -m pytest CodeCoverageTest_laundry_service_application.py
coverage report -m
```

### Branch Coverage
```bash
coverage run --branch -m pytest BranchCoverageTest_laundry_service_application.py
coverage report -m
```
