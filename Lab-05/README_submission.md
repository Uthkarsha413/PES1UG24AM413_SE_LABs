# Lab 5 Submission — Flight Reservation System

**Name:** Uthkarsha  
**SRN:** PES1UG24AM413  
**Section:** AIML G

## Files
- `flight_reservation_system.py` — cleaned version of your assigned program.
- `issues.md` — issue table based on the original flight reservation code.
- `reflection.md` — reflection answers.
- `Lab5_Static_Code_Analysis_Report.pdf` — formatted report in a structure similar to the reference submission.

## Run the program
```bash
python flight_reservation_system.py
```

## Generate the actual static-analysis reports
Install the tools in your own Python environment:
```bash
python -m pip install pylint bandit flake8
```

Run the baseline tools against your original file (keep a copy of the original first):
```bash
pylint flight_reservation_system_original.py > pylint_before.txt
bandit -r flight_reservation_system_original.py > bandit_before.txt
flake8 flight_reservation_system_original.py > flake8_before.txt
```

Run the tools against the cleaned file:
```bash
pylint flight_reservation_system.py > pylint_after.txt
bandit -r flight_reservation_system.py > bandit_after.txt
flake8 flight_reservation_system.py > flake8_after.txt
```

Check the output and update the report with the actual scores/findings. Do not report a score or a clean tool run unless the tools actually produced that result.
