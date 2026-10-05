# Product Requirements Document (PRD)

## Customer Churn & Retention Analytics Platform

**Version:** 1.0  
**Project Type:** Data Analytics / Business Intelligence  
**Target Role:** Data Analyst / Business Analyst  
**Status:** Planned  
**Primary Tools:** Python, SQL, Power BI, Excel/GitHub  
**Expected Duration:** 3–5 days

---

# 1. Project Overview

## 1.1 Project Name

**Customer Churn & Retention Analytics**

## 1.2 Objective

Build an end-to-end customer analytics solution that analyzes customer behavior, identifies factors associated with churn, segments customers based on risk and value, and provides an interactive Power BI dashboard to support customer retention decisions.

The project will demonstrate the complete Data Analyst workflow:

**Raw Data → Data Cleaning → Exploratory Analysis → SQL Analytics → Customer Segmentation → Dashboard → Business Insights**

---

# 2. Business Problem

Customer churn directly affects recurring revenue and customer lifetime value.

A company may know its overall churn rate but still lack answers to important questions such as:

- Which customers are most likely to churn?
- Which customer segments have the highest churn?
- Does customer tenure influence churn?
- Which contract types have the highest churn?
- Which services are associated with higher churn?
- Are high-value customers leaving?
- How much revenue is potentially at risk?
- Which customer segments should receive retention campaigns?

The goal of this project is to transform raw customer data into actionable business insights that can help a company improve customer retention.

---

# 3. Project Goals

## Primary Goals

1. Clean and prepare customer data.
2. Perform exploratory data analysis using Python.
3. Analyze customer behavior using SQL.
4. Calculate meaningful business KPIs.
5. Identify customer segments with different churn behavior.
6. Quantify revenue at risk.
7. Build an interactive Power BI dashboard.
8. Produce actionable business recommendations.
9. Document the entire analysis on GitHub.

## Secondary Goals

- Demonstrate SQL proficiency beyond basic queries.
- Demonstrate practical Power BI/DAX knowledge.
- Demonstrate Python/Pandas data-analysis skills.
- Demonstrate understanding of business metrics.
- Create a project that can be discussed confidently in interviews.

---

# 4. Target Users

Although this is a portfolio project, the hypothetical product is designed for:

### Business Stakeholders

- Business Managers
- Customer Success Teams
- Marketing Teams
- Retention Teams
- Finance Teams
- Senior Management

### Analytical Users

- Data Analysts
- Business Analysts
- Product Analysts

---

# 5. Technology Stack

| Technology | Purpose |
|---|---|
| **Python** | Data cleaning and exploratory analysis |
| **Pandas** | Data manipulation |
| **NumPy** | Numerical operations |
| **Matplotlib / Seaborn** | Exploratory visualizations |
| **SQL** | Business analysis and KPI calculations |
| **MySQL / PostgreSQL** | Analytical database |
| **Power BI** | Interactive dashboard |
| **DAX** | Power BI measures and calculations |
| **Power Query** | Data transformation |
| **Excel** | Optional data inspection/validation |
| **Git/GitHub** | Version control and portfolio |
| **Jupyter Notebook** | Python analysis |

---

# 6. Overall Architecture

```text
                 RAW CUSTOMER DATA
                        │
                        ▼
              ┌───────────────────┐
              │ Data Cleaning     │
              │ Python / Pandas   │
              └─────────┬─────────┘
                        │
                        ▼
              CLEANED CUSTOMER DATA
                 ┌──────┴──────┐
                 │             │
                 ▼             ▼
          SQL DATABASE      Python EDA
                 │             │
                 ▼             ▼
          SQL ANALYSIS    Statistical/
          & KPIs          Exploratory
                 │             │
                 └──────┬──────┘
                        │
                        ▼
                ANALYTICAL DATASET
                        │
                        ▼
                ┌───────────────┐
                │   Power BI    │
                │   Dashboard   │
                └───────┬───────┘
                        │
                        ▼
                BUSINESS INSIGHTS
                        │
                        ▼
              RETENTION STRATEGIES
```

---

# 7. Project Phases

# Phase 1 — Project Setup & Dataset Understanding

### Objective

Understand the dataset, business context, available fields, and analytical questions.

### Tasks

- Select customer churn dataset.
- Inspect dataset dimensions.
- Understand each column.
- Identify target variable.
- Identify numerical and categorical variables.
- Understand relationships between fields.
- Define business questions.

### Expected Output

- Dataset documentation
- Data dictionary
- Initial business questions
- Project scope

### Deliverable

`docs/data_dictionary.md`

---

# Phase 2 — Data Cleaning & Preparation

### Objective

Prepare reliable analytical data.

### Tasks

- Load dataset using Pandas.
- Inspect missing values.
- Detect duplicate records.
- Correct data types.
- Standardize categorical values.
- Handle missing numerical values.
- Validate customer IDs.
- Check negative/invalid values.
- Identify potential outliers.
- Create derived variables.

### Example Derived Features

```text
Tenure Group
Monthly Revenue
Annual Revenue
Customer Value Segment
Contract Category
Service Count
Payment Category
Churn Flag
```

### Example Tenure Groups

```text
0–12 Months
13–24 Months
25–48 Months
49+ Months
```

### Deliverables

```text
data/processed/customers_cleaned.csv
notebooks/01_data_cleaning.ipynb
```

---

# Phase 3 — Exploratory Data Analysis

### Objective

Understand customer behavior and discover patterns associated with churn.

### Questions

### Customer Demographics

- What is the customer distribution?
- Which demographic groups have the highest churn?

### Contract

- Which contract type has the highest churn?
- Are month-to-month customers more likely to leave?

### Tenure

- Does churn decrease as tenure increases?
- Which tenure group has the highest churn?

### Services

- Does the number of subscribed services affect churn?
- Which services are associated with higher churn?

### Payment

- Does payment method influence churn?

### Revenue

- Do high-paying customers churn more?
- What is the average monthly revenue of churned customers?

### Visualizations

Create:

- Churn distribution
- Churn by contract
- Churn by tenure
- Churn by payment method
- Churn by service
- Churn by demographic segment
- Revenue distribution
- Customer lifetime distribution

### Deliverable

```text
notebooks/02_exploratory_analysis.ipynb
reports/eda_summary.md
```

---

# Phase 4 — SQL Analytics

### Objective

Demonstrate practical SQL skills by answering business questions directly from the analytical database.

### SQL Concepts

The project should demonstrate:

- SELECT
- WHERE
- GROUP BY
- HAVING
- CASE
- JOIN
- Subqueries
- CTEs
- Window Functions
- RANK
- DENSE_RANK
- ROW_NUMBER
- SUM
- AVG
- COUNT
- COUNT DISTINCT
- COALESCE
- Date functions

---

## Core SQL Questions

### Q1 — Overall Churn Rate

Calculate:

```text
Churned Customers / Total Customers
```

---

### Q2 — Churn by Contract

Find:

```text
Contract Type
Total Customers
Churned Customers
Churn Rate
```

---

### Q3 — Churn by Tenure

Identify the tenure groups with the highest churn.

---

### Q4 — Revenue at Risk

Calculate monthly revenue associated with customers who churned.

---

### Q5 — High-Value Churn

Identify customers who:

- Have high monthly revenue
- Have high tenure/value
- Have churned

---

### Q6 — Service-Based Churn

Compare churn across different services.

---

### Q7 — Customer Segmentation

Create segments such as:

```text
High Value
Medium Value
Low Value
```

based on customer revenue.

---

### Q8 — Top At-Risk Segments

Use SQL ranking/window functions to identify the segments with the highest churn.

---

### Q9 — Payment Method Analysis

Compare churn rate across payment methods.

---

### Q10 — Retention Opportunity

Identify customer groups with:

```text
High Customer Value
+
High Churn Rate
```

These become the highest-priority retention targets.

### Deliverable

```text
sql/
├── 01_basic_analysis.sql
├── 02_churn_analysis.sql
├── 03_customer_segmentation.sql
├── 04_revenue_analysis.sql
├── 05_advanced_analysis.sql
└── 06_business_questions.sql
```

---

# Phase 5 — Customer Segmentation

### Objective

Move beyond simple churn calculations and identify meaningful customer groups.

## Segmentation Dimensions

### 1. Tenure

```text
New
Growing
Established
Loyal
```

### 2. Revenue

```text
Low Value
Medium Value
High Value
```

### 3. Churn Risk

```text
Low Risk
Medium Risk
High Risk
```

### 4. Customer Type

Combine dimensions to identify strategic segments.

Example:

```text
High Value + High Risk
High Value + Low Risk
Low Value + High Risk
Low Value + Low Risk
```

---

# Phase 6 — Power BI Data Model

### Objective

Create the analytical model required for the dashboard.

## Main Table

```text
Customer
```

Potential future expansion:

```text
Customer
   │
   ├── Transactions
   │
   ├── Services
   │
   └── Support
```

For the first version, a clean customer fact table is sufficient.

---

# 7. Power BI Measures

Create DAX measures such as:

### Total Customers

```text
COUNT(Customer[CustomerID])
```

### Churned Customers

```text
CALCULATE(
    COUNT(Customer[CustomerID]),
    Customer[Churn] = "Yes"
)
```

### Churn Rate

```text
DIVIDE(
    [Churned Customers],
    [Total Customers]
)
```

### Total Revenue

```text
SUM(Customer[MonthlyCharges])
```

### Revenue at Risk

Revenue associated with churned customers.

### Average Monthly Revenue

```text
AVERAGE(Customer[MonthlyCharges])
```

Additional measures can be added as the dashboard develops.

---

# Phase 7 — Power BI Dashboard

## Dashboard Structure

Create **3 pages**.

---

## Page 1 — Executive Overview

### KPI Cards

```text
Total Customers
Churned Customers
Churn Rate
Monthly Revenue
Revenue at Risk
Average Customer Revenue
```

### Visualizations

- Churn trend
- Churn by contract
- Churn by tenure
- Churn by customer segment
- Revenue at risk by segment

### Filters

- Contract
- Gender
- Tenure
- Payment Method
- Services
- Customer Segment

---

# Page 2 — Churn Analysis

### Visualizations

- Churn by contract
- Churn by tenure
- Churn by payment method
- Churn by internet/service type
- Churn by demographic
- Churn by number of services

### Goal

Answer:

> **Who is most likely to churn?**

---

# Page 3 — Customer Value & Retention

### Visualizations

- Customer value distribution
- Revenue by segment
- Revenue at risk
- High-value churn customers
- High-risk/high-value quadrant

### Goal

Answer:

> **Where should the business focus retention efforts?**

---

# Phase 8 — Business Insights

This phase is extremely important.

The project should not end with:

> "The dashboard shows that churn is 26%."

Instead, translate findings into business recommendations.

### Example Insight

```text
Finding:
Month-to-month customers show significantly higher churn.

Business Interpretation:
Customers without long-term commitments have lower switching costs.

Recommendation:
Offer targeted incentives for customers to transition
to longer-term contracts.
```

Another:

```text
Finding:
High-value customers represent a significant portion of
revenue at risk.

Recommendation:
Prioritize retention campaigns for high-value/high-risk
customers rather than treating every customer equally.
```

---

# Phase 9 — Validation & Quality Checks

Before publishing:

### Data Validation

- Check row counts.
- Check duplicate customers.
- Verify null values.
- Verify churn totals.
- Compare Python and SQL results.
- Compare SQL and Power BI KPIs.

### Dashboard Validation

Ensure:

- Filters work.
- KPIs update correctly.
- Percentages are formatted correctly.
- No broken visuals.
- No misleading charts.
- Dashboard is readable.

---

# Phase 10 — GitHub Documentation

The GitHub repository should look like a professional analytics project rather than a collection of files.

README should contain:

1. Project Overview
2. Business Problem
3. Objectives
4. Dataset
5. Technologies
6. Data Pipeline
7. Data Cleaning
8. SQL Analysis
9. Power BI Dashboard
10. Key Insights
11. Business Recommendations
12. Project Structure
13. How to Reproduce
14. Future Improvements

---

# 8. Final Project Folder Structure

```text
customer-churn-retention-analytics/
│
├── README.md
├── LICENSE
├── .gitignore
│
├── data/
│   ├── raw/
│   │   └── customer_churn.csv
│   │
│   └── processed/
│       └── customers_cleaned.csv
│
├── notebooks/
│   ├── 01_data_cleaning.ipynb
│   ├── 02_exploratory_analysis.ipynb
│   └── 03_customer_segmentation.ipynb
│
├── sql/
│   ├── 01_basic_analysis.sql
│   ├── 02_churn_analysis.sql
│   ├── 03_customer_segmentation.sql
│   ├── 04_revenue_analysis.sql
│   ├── 05_advanced_analysis.sql
│   └── 06_business_questions.sql
│
├── powerbi/
│   └── customer_churn_dashboard.pbix
│
├── reports/
│   ├── business_insights.md
│   └── data_dictionary.md
│
├── screenshots/
│   ├── executive_dashboard.png
│   ├── churn_analysis.png
│   └── retention_analysis.png
│
└── docs/
    └── project_architecture.md
```

---

# 9. Data Pipeline

```text
                    RAW CSV
                       │
                       ▼
               Python / Pandas
                       │
              ┌────────┴────────┐
              │                 │
              ▼                 ▼
        Data Cleaning        EDA
              │                 │
              └────────┬────────┘
                       │
                       ▼
                Cleaned Dataset
                       │
                       ▼
                  SQL Database
                       │
                       ▼
              SQL Business Analysis
                       │
                       ▼
             Analytical Dataset
                       │
                       ▼
                   Power BI
                       │
                       ▼
              Interactive Dashboard
                       │
                       ▼
             Business Recommendations
```

---

# 10. Key KPIs

The final dashboard should contain approximately **6–10 meaningful KPIs**.

### Customer KPIs

- Total Customers
- Active Customers
- Churned Customers
- Churn Rate

### Revenue KPIs

- Total Monthly Revenue
- Average Monthly Revenue
- Revenue from Churned Customers
- Revenue at Risk

### Retention KPIs

- Average Customer Tenure
- High-Value Customer Churn Rate
- High-Risk Customer Count

Avoid filling the dashboard with unnecessary metrics.

---

# 11. Business Questions the Final Project Must Answer

By the end of the project, a recruiter should be able to look at your dashboard and find answers to:

### Customer Behavior

1. Who are our customers?
2. How long do they stay?
3. Which services do they use?

### Churn

4. What is our overall churn rate?
5. Which customer groups churn most?
6. What characteristics are associated with churn?

### Revenue

7. How much revenue is associated with churn?
8. Which customer segments represent the greatest revenue risk?

### Retention

9. Which customers should we prioritize?
10. What actions could potentially reduce churn?

---

# 12. Success Criteria

The project will be considered complete when:

### Data

- [ ] Dataset is cleaned.
- [ ] Missing values handled.
- [ ] Duplicate records checked.
- [ ] Data types validated.
- [ ] Derived features created.

### Python

- [ ] EDA completed.
- [ ] At least 8–10 meaningful visualizations.
- [ ] Key patterns documented.

### SQL

- [ ] Basic analytical queries completed.
- [ ] Aggregations used.
- [ ] CASE statements used.
- [ ] CTEs used.
- [ ] Window functions used.
- [ ] Business questions answered.

### Power BI

- [ ] Dashboard contains 3 pages.
- [ ] KPI cards created.
- [ ] DAX measures created.
- [ ] Interactive filters implemented.
- [ ] Dashboard visually polished.

### Business Analysis

- [ ] At least 5 meaningful insights identified.
- [ ] At least 5 actionable recommendations documented.

### GitHub

- [ ] Professional README.
- [ ] Clean folder structure.
- [ ] Screenshots included.
- [ ] SQL scripts documented.
- [ ] Reproducible workflow documented.

---

# 13. Resume Deliverable

Final resume entry should look approximately like:

**Customer Churn & Retention Analytics | Python, SQL, Power BI**

- Analyzed **5,000+ customer records** using Python and SQL to identify churn patterns across customer tenure, contracts, services, payment methods, and revenue segments.
- Developed an interactive **Power BI dashboard** with DAX-based KPIs for churn rate, customer segmentation, revenue at risk, and retention performance.
- Identified high-risk customer segments and translated analytical findings into **data-driven retention recommendations** focused on reducing churn and protecting high-value revenue.

The exact numbers should be based on the actual dataset and results rather than invented.

---

# 14. Interview Preparation Deliverables

The project should prepare you to answer:

### Python

- How did you clean the dataset?
- How did you handle missing values?
- Why did you use Pandas?
- What patterns did EDA reveal?

### SQL

- How did you calculate churn rate?
- Why did you use a CTE?
- Where did you use window functions?
- How would you find the top 10 highest-risk segments?

### Power BI

- Why did you choose these KPIs?
- What DAX measures did you create?
- Why did you choose these visualizations?
- How did you design the dashboard?

### Business

- What is the biggest driver of churn?
- Which customers should the company prioritize?
- How would you reduce churn?
- What additional data would improve the analysis?

---

# 15. Future Scope

The first version should remain an **analytics project**, but the following can be added later:

### Version 2

- Automated data refresh
- More detailed customer cohorts
- Customer lifetime value analysis
- Retention campaign analysis

### Version 3

Add a predictive component:

```text
Customer Data
      ↓
Feature Engineering
      ↓
Churn Prediction Model
      ↓
Probability of Churn
      ↓
Power BI
      ↓
Retention Prioritization
```

Possible models:

- Logistic Regression
- Random Forest
- XGBoost

However, predictive ML is **not required for Version 1**.

---

# 16. Recommended Development Timeline

## Day 1

### Morning
- Dataset selection
- Data understanding
- Data cleaning

### Afternoon
- EDA
- Initial visualizations

### Evening
- SQL database setup
- Basic SQL queries

---

## Day 2

### Morning
- Advanced SQL
- Customer segmentation

### Afternoon
- DAX measures
- Power BI data model

### Evening
- Dashboard Page 1
- Dashboard Page 2

---

## Day 3

### Morning
- Dashboard Page 3
- Dashboard refinement

### Afternoon
- Business insights
- Recommendations

### Evening
- GitHub README
- Screenshots
- Resume bullets
- Final validation

---

# 17. Final Technology Stack

```text
                    CUSTOMER CHURN
                         │
          ┌──────────────┼──────────────┐
          │              │              │
          ▼              ▼              ▼
       PYTHON           SQL          POWER BI
          │              │              │
       Pandas         MySQL/         DAX
       NumPy          PostgreSQL     Power Query
       Matplotlib
          │              │              │
          └──────────────┼──────────────┘
                         ▼
                BUSINESS INSIGHTS
                         │
                         ▼
                 RETENTION STRATEGY
```

---

# 18. Definition of Done

The project is **not complete merely because the Power BI dashboard works**.

It is complete when a recruiter can open the GitHub repository and understand:

**What was the business problem?**

↓

**What data was used?**

↓

**How was it cleaned?**

↓

**How was it analyzed with Python?**

↓

**How was SQL used?**

↓

**What does the dashboard show?**

↓

**What did you discover?**

↓

**What should the business do about it?**

That end-to-end story is the primary objective of this project.