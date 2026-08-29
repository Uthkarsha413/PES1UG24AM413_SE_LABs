# PES1UG24AM413_SE_LAB_1

**Software Engineering — Lab 1: Requirements Engineering & UML Use-Case Modelling**
Problem Statement #33 | Retail, E-Commerce & Finance
**Micro-Lending & Peer Credit Risk Assessor**

## Problem Context

A peer-to-peer micro-finance platform that calculates borrower risk scores using heuristic rules, generates structured repayment schedules, and triggers automated default warnings.

**Stakeholders / Actors:** Borrower, Peer Lender

## Deliverables

| Deliverable | Contents |
|---|---|
| Requirements Table | 5 Functional Requirements (FR-001–FR-005) and 2 Non-Functional Requirements (NFR-001, NFR-002), each with ID, Type, Description, Priority, Acceptance Criteria, and Rationale |
| UML Use-Case Diagram | All actors and primary use cases, including at least one `«include»` and one `«extend»` relationship |
| Use-Case Flow Specification | 1-page flow for one core use case — Preconditions, Postconditions, Main Success Scenario, and one Alternate Flow |

## Repo Contents

- `SE_Lab1_Solution_PS33.docx` / `.pdf` — full solution document (requirements table, use-case diagram, and flow specification)

## Summary of the Solution

**Actors:** Borrower and Peer Lender (primary); Risk Scoring Engine and Notification Service (supporting system actors)

**Use cases modelled:** Submit Loan Application, Compute Credit Risk & Assign Tier, Browse & Fund Loan Requests, Generate Repayment Schedule, Make Repayment, Send Notification, Monitor Repayments & Detect Default, Send Default Warning, Request Loan Restructuring

**Relationships:**
- `«include»`: Submit Loan Application → Compute Credit Risk & Assign Tier
- `«include»`: Browse & Fund Loan Requests → Generate Repayment Schedule
- `«include»`: Make Repayment → Send Notification
- `«extend»`: Send Default Warning extends Monitor Repayments & Detect Default

**Core flow documented:** UC-01 – Submit Loan Application, with an alternate flow for applications that fail the risk assessment.

---
**Name:** Uthkarsha
**SRN:** PES1UG24AM413
