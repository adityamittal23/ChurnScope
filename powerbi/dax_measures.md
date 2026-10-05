# Power BI DAX Measures Library — Customer Churn & Retention Analytics

## 1. Overview
This library provides production-ready Data Analysis Expressions (DAX) for Power BI. The measures are organized by analytical category: Customer Volume, Churn Performance, Financial/Revenue KPIs, and Segment Risk Prioritization.

All measures operate on the primary fact table: `'Fact_Customers'` (or `'customers_cleaned'`).

---

## 2. Base Customer & Volume Measures

### 2.1 Total Customers
```dax
Total Customers = 
COUNTROWS('Fact_Customers')
```
- **Format:** Whole Number (`#,##0`)
- **Description:** Total number of distinct customer accounts in the active dataset.

### 2.2 Retained Customers
```dax
Retained Customers = 
CALCULATE(
    [Total Customers],
    'Fact_Customers'[Churn] = "No"
)
```
- **Format:** Whole Number (`#,##0`)
- **Description:** Active, retained customer accounts.

### 2.3 Churned Customers
```dax
Churned Customers = 
CALCULATE(
    [Total Customers],
    'Fact_Customers'[Churn] = "Yes"
)
```
- **Format:** Whole Number (`#,##0`)
- **Description:** Customer accounts that have cancelled service.

### 2.4 Churn Rate %
```dax
Churn Rate % = 
DIVIDE(
    [Churned Customers],
    [Total Customers],
    0
)
```
- **Format:** Percentage (`0.00%` or `0.0%`)
- **Description:** Primary retention KPI: proportion of accounts that have churned.

### 2.5 Retention Rate %
```dax
Retention Rate % = 
1 - [Churn Rate %]
```
- **Format:** Percentage (`0.00%`)
- **Description:** Percentage of customer base successfully retained.

---

## 3. Financial & Revenue KPIs

### 3.1 Total Monthly Revenue (MRR)
```dax
Total Monthly Revenue = 
SUM('Fact_Customers'[MonthlyCharges])
```
- **Format:** Currency (`$#,##0.00`)
- **Description:** Aggregate monthly recurring revenue across all customer accounts.

### 3.2 Monthly Revenue at Risk (Lost MRR)
```dax
Monthly Revenue at Risk = 
CALCULATE(
    [Total Monthly Revenue],
    'Fact_Customers'[Churn] = "Yes"
)
```
- **Format:** Currency (`$#,##0.00`)
- **Description:** Monthly recurring revenue lost directly to customer attrition.

### 3.3 Annualized Revenue at Risk (Lost ARR)
```dax
Annual Revenue at Risk = 
[Monthly Revenue at Risk] * 12
```
- **Format:** Currency (`$#,##0.00`)
- **Description:** Annualized recurring run-rate lost due to churn.

### 3.4 % Revenue at Risk
```dax
% Revenue at Risk = 
DIVIDE(
    [Monthly Revenue at Risk],
    [Total Monthly Revenue],
    0
)
```
- **Format:** Percentage (`0.00%`)
- **Description:** Share of monthly recurring revenue lost to churn (benchmark: 30.5%).

### 3.5 Average Monthly Spend (ARPU)
```dax
Average Monthly Spend = 
AVERAGE('Fact_Customers'[MonthlyCharges])
```
- **Format:** Currency (`$#,##0.00`)
- **Description:** Average Revenue Per User (ARPU).

### 3.6 ARPU - Churned Customers
```dax
ARPU - Churned = 
CALCULATE(
    [Average Monthly Spend],
    'Fact_Customers'[Churn] = "Yes"
)
```
- **Format:** Currency (`$#,##0.00`)
- **Description:** Average monthly charge of customers who churned (benchmark: $74.44).

### 3.7 ARPU - Retained Customers
```dax
ARPU - Retained = 
CALCULATE(
    [Average Monthly Spend],
    'Fact_Customers'[Churn] = "No"
)
```
- **Format:** Currency (`$#,##0.00`)
- **Description:** Average monthly charge of retained customers (benchmark: $61.27).

### 3.8 Cumulative Lifetime Revenue
```dax
Total Lifetime Revenue = 
SUM('Fact_Customers'[TotalCharges])
```
- **Format:** Currency (`$#,##0.00`)
- **Description:** Historical cumulative billing recognized across all accounts.

---

## 4. Customer Lifecycle & Behavioral Metrics

### 4.1 Average Customer Tenure
```dax
Average Tenure (Months) = 
AVERAGE('Fact_Customers'[tenure])
```
- **Format:** Decimal Number (`0.0`)
- **Description:** Average tenure in months.

### 4.2 Average Tenure - Churned Customers
```dax
Avg Tenure - Churned = 
CALCULATE(
    [Average Tenure (Months)],
    'Fact_Customers'[Churn] = "Yes"
)
```
- **Format:** Decimal Number (`0.0`)
- **Description:** Lifetime duration before churn (benchmark: 18.0 months).

### 4.3 Average Tenure - Retained Customers
```dax
Avg Tenure - Retained = 
CALCULATE(
    [Average Tenure (Months)],
    'Fact_Customers'[Churn] = "No"
)
```
- **Format:** Decimal Number (`0.0`)
- **Description:** Active customer tenure (benchmark: 37.7 months).

### 4.4 Average Subscribed Services
```dax
Avg Service Count = 
AVERAGE('Fact_Customers'[ServiceCount])
```
- **Format:** Decimal Number (`0.0`)
- **Description:** Mean number of active add-on services per customer.

---

## 5. Strategic Segmentation & Retention Target Measures

### 5.1 High-Value Customers Count
```dax
High Value Customers = 
CALCULATE(
    [Total Customers],
    'Fact_Customers'[CustomerValueSegment] = "High Value"
)
```
- **Format:** Whole Number (`#,##0`)

### 5.2 High-Value Churn Rate %
```dax
High Value Churn Rate % = 
DIVIDE(
    CALCULATE([Churned Customers], 'Fact_Customers'[CustomerValueSegment] = "High Value"),
    CALCULATE([Total Customers], 'Fact_Customers'[CustomerValueSegment] = "High Value"),
    0
)
```
- **Format:** Percentage (`0.0%`)

### 5.3 Active Priority Retention Targets
```dax
Active Priority Retention Targets = 
CALCULATE(
    [Total Customers],
    'Fact_Customers'[Churn] = "No",
    'Fact_Customers'[CustomerValueSegment] = "High Value",
    'Fact_Customers'[Contract] = "Month-to-month"
)
```
- **Format:** Whole Number (`#,##0`)
- **Description:** Active high-value accounts on month-to-month terms that require proactive retention outreach.

### 5.4 Priority Target MRR at Immediate Risk
```dax
Priority Target MRR = 
CALCULATE(
    [Total Monthly Revenue],
    'Fact_Customers'[Churn] = "No",
    'Fact_Customers'[CustomerValueSegment] = "High Value",
    'Fact_Customers'[Contract] = "Month-to-month"
)
```
- **Format:** Currency (`$#,##0.00`)
- **Description:** Active monthly revenue vulnerable to near-term churn if not migrated to term contracts.
