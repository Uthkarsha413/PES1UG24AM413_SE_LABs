# Lab 5: Static Code Analysis — Issue Documentation

**Name:** Uthkarsha  
**SRN:** PES1UG24AM413  
**Section:** AIML G  
**Program:** Flight Reservation System

Line numbers below refer to the original `flight_reservation_system.py` supplied for the lab. Confirm the exact tool-reported line numbers after running the tools locally.

| Issue | Type | Original line(s) | Description | Fix Approach |
|---|---|---:|---|---|
| Arbitrary expression evaluation with `eval()` | Security — High | 47 | Evaluating a supplied string can execute arbitrary Python expressions. | Replaced the expression string with a numeric surcharge rate and validated that it is between 0 and 1. |
| Shell command constructed from a filename | Security — High | 63 | Passing a filename into `os.system()` can allow shell interpretation of special characters. | Removed the shell command; the function now exports the manifest and prints a normal status message. |
| Hard-coded secret token | Security — High | 75, 84 | A secret embedded in source code can be exposed through code sharing or logs. | Removed the hard-coded token and stopped printing secrets. A real application should load secrets from a protected environment or secret manager. |
| Insecure / non-cryptographic PIN generation | Security — Medium | 56 | `random.randint()` is not intended for security-sensitive PIN generation. | Replaced it with `secrets.randbelow()` to generate a four-digit PIN. |
| MD5 used for passenger identifier digest | Security | 52 | MD5 is a weak hash function and should not be selected for security-sensitive uses. | Replaced MD5 with SHA-256. A plain hash is not a substitute for secure storage of sensitive identifiers. |
| Mutable default argument | Bug / Reliability | 15 | `baggage_tags=[]` reuses the same list between calls, so records can leak across bookings. | Changed the default to `None` and creates a fresh list inside the function. |
| Bare `except` hides errors | Reliability | 27–32 | The broad exception handler suppresses all exceptions, making failures difficult to detect. | Replaced it with explicit dictionary lookup and a clear `False` return for unknown flights. |
| File opened without context manager or encoding | Quality / Portability | 60–62 | Manual closing can be skipped on errors, and the encoding depends on the environment. | Used `Path.open()` in a `with` statement with `encoding="utf-8"`. |
| Unused import and variable | Style / Maintainability | 4, 36 | `math` and `airport_fee` are not used. | Removed the unused import and variable. |
| Function names do not follow snake_case | Style | 15, 27, 35, 45, 51, 55, 59, 66 | CamelCase names are inconsistent with common Python naming conventions. | Renamed functions to snake_case. |
| Missing module/function documentation and main guard | Maintainability | Multiple | Purpose and function behaviour are not documented, and importing the file immediately runs the demo. | Added docstrings and moved the demonstration behind `if __name__ == "__main__":`. |
| Flight and fee input validation | Reliability | 17, 45–48 | Invalid flight numbers or invalid surcharge inputs can cause confusing failures. | Added known-flight checks and validation for surcharge rates and negative luggage weights. |
| Style / formatting violations | Style | Multiple | Original code has long lines and inconsistent spacing. | Reformatted the code and wrapped long lines. |

## Verification note

The cleaned program was syntax-compiled and run as a basic smoke test while preparing this submission. Pylint, Bandit, and Flake8 were not installed in the preparation environment, and package installation could not reach the package index. Therefore, no numeric before/after tool scores are claimed here. Run the commands in `README_submission.md` in your own Python environment and attach the actual reports before submission.
