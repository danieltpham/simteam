### Organisation Chart

This chart displays a point-in-time snapshot of your organisation’s structure, built from a transactional database using custom SQL logic. It updates dynamically based on the date selected in the date picker on the left-hand side. For raw data input, refer to [the relevant FastAPI endpoint](https://simteam.danielpham.com.au/api/docs#/EventLog/get_all_eventlogs_v1_eventlog__get).

### Role Hierarchy

The simulation models a fixed, six-tier hierarchy:
**CEO → VP → Director → Manager → Senior Analyst → Analyst**

Each role has predefined limits on the number of direct reports and supervises only roles immediately below it. Vacant positions are shown as **TEMP** nodes when staffing targets have not yet been met.

### Event Logic & Org Evolution

The organisation evolves through **randomised daily and weekly events**, including: New hires (internal and external), Promotions (with eligibility checks), Resignations or exits, Managerial reassignments

These events are governed by structural rules, succession logic, and team size constraints. The full logic is modularised and maintained in the simulation engine under [`simteam/core`](https://github.com/danieltpham/simteam/tree/main/simteam/core), including:

* `HiringLogic`
* `PromotionLogic`
* `ManagerChangeLogic`
* `VacancyLogic`

Each logic module ensures valid transitions while maintaining organisational consistency over time.

### Visualisation Details

Built using the custom React library from [bumbeishvili/org-chart](https://github.com/bumbeishvili/org-chart). Clicking a node will expand or collapse its subordinates, but does not send feedback to the app.
