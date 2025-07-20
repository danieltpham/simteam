# 🧩 Simulation Engine Requirements

## 📘 Overview

The simulation models the evolution of a company’s workforce over time, capturing daily events such as hiring, promotions, role changes, and departures. It maintains a hierarchical organisational structure and enforces role-specific rules, quotas, and succession dynamics.

---

## 📅 Simulation Timeframe

* **Start Date**: 2025-01-01
* **Duration**: User-specified (e.g. 365 days)
* **Granularity**: Daily

---

## 👤 Roles and Hierarchy

| Role           | Level | Reports To    | Has Dept | Has Team | Quota Limit |
| -------------- | ----- | ------------- | -------- | -------- | ----------- |
| CEO            | 0     | —             | ❌        | ❌        | 1           |
| VP             | 1     | CEO           | ❌        | ❌        | 3           |
| Director       | 2     | VP            | ✅        | ❌        | ≤5/VP       |
| Manager        | 3     | Director      | ✅        | ✅        | ≤5/Director |
| Senior Analyst | 4     | Manager or SA | ✅        | ✅        | Unlimited   |
| Analyst        | 5     | Manager or SA | ✅        | ✅        | Unlimited   |

---

## 📈 Simulation Logic

### 1. **Event Types**

* `employed`: new hire
* `promoted`: internal promotion to higher role
* `change`: change of manager (same role)
* `left`: employee leaves the company

### 2. **Daily Event Count**

* Number of events per day is sampled from a **Poisson(λ = 1.5)** distribution, capped at 8.
* No more than 3 events of the same type per day.

### 3. **Event Distribution**

| Event Type | Trigger Rules                                                                 |
| ---------- | ----------------------------------------------------------------------------- |
| `employed` | Triggered if total headcount < 100. Probability ∝ (100 - current count) / 100 |
| `left`     | Cannot occur until ≥30 employees exist                                        |
| `promoted` | Randomly chosen from eligible employees with roles from VP down to Analyst    |
| `change`   | Randomly assigned to change direct manager                                    |

---

## 🧮 Hiring Rules

### Hiring Prioritisation

* Prioritise **lower-level roles** when multiple roles are under quota.
* Vacancy fill priority: Analyst > SA > Manager > Director > VP > CEO

### Vacancy Fill Strategies

| Role           | Fill Logic                           |
| -------------- | ------------------------------------ |
| CEO, VP        | Likely external hire                 |
| Director       | Prefer promotion from Manager        |
| Manager        | 50/50 promotion from SA vs new hire  |
| Senior Analyst | 50/50 promotion from Analyst vs hire |
| Analyst        | Always hire externally               |

---

## ⏳ Vacancy Rules

* If a role with direct reports becomes vacant:

  * It must be filled **within 14 days**
  * If not filled by promotion, fallback to hire
* Reporting employees are reassigned to the new manager

---

## 🔄 Weekly Guarantees

* At least **1 event per week** (forced if no events by Sunday)

---

## 🧠 Probabilistic Logic Summary

* Daily event count: `Poisson(λ=1.5)`, truncated at 8
* Event type draw: max 3 per type per day
* Hiring probability scales with unfilled quota
* Vacancy resolution prioritised based on promotion likelihood

---

## 🗃️ Employee State Tracking

Each employee maintains:

* `emp_id`
* `role`
* `manager_id`
* `department`, `team` (optional by role)
* `hire_date`
* `active` flag
* `history`: list of all events with timestamps

---

## 📤 Output & Export

* Full event log table:

  * `employee_id`, `event_type`, `date`, `role`, `manager_id`, `department`, `team`
* Snapshots:

  * State of org chart on any given day
  * Summary metrics (headcount, composition by role, etc.)

---

## 🧪 Design Goals

* 🧠 Realistic simulation of role succession and structural evolution
* 🕹️ Interactive and explainable: supports logs, visual diff, user inspection
* 🧱 Modular, extensible, fully OOP
* 🚀 Efficient for up to 100 employees and 1 year of daily steps