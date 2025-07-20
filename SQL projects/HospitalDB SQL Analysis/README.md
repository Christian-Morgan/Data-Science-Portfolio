## Project Overview

I focused on simulating real-world analysis that a hospital operations team might need, using SQL to dig into trends around patient visits, treatment timelines, and doctor performance.

The primary goal was to **practice complex SQL** with a focus on:

- **Common Table Expressions (CTEs)**
- **Window Functions** (e.g., `LAG`, `LEAD`, `RANK`)
- **Date/time calculations**
- **Aggregations, joins, and filters**

---

## Key Questions Answered

- What is the **average number of appointments per patient**?
- What are the **most common reasons for visits** and **busiest days of the week**?
- What is the **average time between a patient’s first and second visit**?
- Which doctors have the **longest average gaps between appointments** (low utilization)?
- What is the **cancellation rate** for each doctor?
- What’s the **average cost per treatment type**?
- What’s the **monthly revenue** and how is it distributed by doctor?
- How do **billed vs paid amounts** compare?

---

## Tools & Techniques

- Microsoft SQL Server
- CTEs for modular query design
- Window functions for time-based analysis
- Grouping, filtering, and conditional logic
- Aggregate functions (AVG, COUNT, STDEV, etc.)
- Subqueries and cross joins

## HospitalDB Schema

<img width="1115" height="717" alt="hospitaldb_schema" src="https://github.com/user-attachments/assets/ef951db4-1344-4923-bd79-0d274822a689" />
