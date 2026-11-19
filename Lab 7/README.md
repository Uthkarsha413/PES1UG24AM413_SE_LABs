# L6_L7_41 — Laundry Service

Lab 7: Fuzz Testing

## About

A robust Python module that parses laundry orders, averages garment weights, and calculates payable charges after tax and discounts, tested and verified using Hypothesis property-based fuzz testing.

## Files

| File | Description |
|------|-------------|
| `laundry_service.py` | The hardened module under test |
| `test_laundry_service.py` | Fuzz and unit test suite powered by Hypothesis |
| `screenshots/` | Verification and test execution screenshots |

## Running Tests

To run the Hypothesis fuzz tests and unit tests:

```bash
pytest -v test_laundry_service.py
```
