# Lab 5: Static Code Analysis — Reflection

**Name:** Uthkarsha  
**SRN:** PES1UG24AM413  
**Section:** AIML G  
**Program:** Flight Reservation System

## 1. What is static code analysis?

Static code analysis is the process of examining source code without executing the program. It helps identify possible bugs, insecure coding patterns, maintainability problems, and style violations early in development. In this lab, the original flight reservation program was reviewed for problems that could affect reliability and security.

## 2. What are the purposes of Pylint, Bandit, and Flake8?

- **Pylint** checks general code quality, naming conventions, missing documentation, unused variables/imports, and programming-practice issues.
- **Bandit** checks Python source code for common security risks, such as dangerous expression evaluation and unsafe use of system commands.
- **Flake8** checks Python style and formatting, including whitespace, blank lines, and line length.

The tools complement one another because they focus on different categories of issues.

## 3. What improvements were made to the program?

The code was updated to remove unsafe `eval()` use, avoid building a shell command from a filename, remove a hard-coded token, use a cryptographically stronger source for boarding PINs, replace MD5 with SHA-256, and fix the mutable default list. File output now uses a context manager and UTF-8 encoding. The code also uses snake_case function names, documentation strings, input validation, and a main guard. The updated program passed syntax compilation and a basic execution check during preparation.

Actual Pylint, Bandit, and Flake8 scores must be recorded after running those tools locally; they are not reported here because the tools could not be installed in the preparation environment.

## 4. Why is static code analysis useful, and what did this lab demonstrate?

Static analysis is useful because it can reveal defects and risky patterns before a program is deployed. It supports readability, maintainability, consistent formatting, and safer coding practices. This lab demonstrated that no single tool checks every aspect of a program: Pylint focuses on broad code quality, Bandit focuses on security patterns, and Flake8 focuses on style. Running all three before and after changes gives repeatable evidence of improvement.
