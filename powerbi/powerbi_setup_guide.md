# Power BI Dashboard Setup & Visual Design Guide

## 1. Quick-Start Setup (Under 5 Minutes)

### Step 1: Open Power BI Desktop
1. Launch Power BI Desktop.
2. Click **Get Data** -> **Text/CSV**.
3. Select `data/processed/customers_cleaned.csv` from the project repository.
4. Click **Load** (or **Transform Data** to inspect column data types in Power Query).

### Step 2: Validate Data Types
Ensure the following column types are properly mapped:
- `MonthlyCharges` / `MonthlyRevenue`: Decimal Number (Currency)
- `TotalCharges`: Decimal Number (Currency)
- `tenure`: Whole Number
- `ServiceCount`: Whole Number
- `Churn`: Text ('Yes' / 'No')
- `ChurnFlag`: Whole Number (1 / 0)

### Step 3: Create the Dedicated Measures Table
1. In the **Home** tab, click **Enter Data**.
2. Name the table `_Measures` and click **Load**.
3. Right-click `_Measures` and select **New Measure** to copy-paste the DAX formulas from [`powerbi/dax_measures.md`](dax_measures.md).

---

## 2. Dashboard Page Blueprint

The dashboard is structured into **3 core pages** designed for executive decision-makers, product managers, and retention specialists.

### Page 1 — Executive Overview
- **Objective:** Provide a high-level corporate snapshot of churn incidence, customer volume, and direct financial exposure.
- **Top KPI Banner (Cards):**
  1. `[Total Customers]` -> **7,043**
  2. `[Churned Customers]` -> **1,869**
  3. `[Churn Rate %]` -> **26.54%**
  4. `[Total Monthly Revenue]` -> **$456.12K**
  5. `[Monthly Revenue at Risk]` -> **$139.13K**
  6. `[ARPU (Average Monthly Spend)]` -> **$64.76**
- **Main Visuals:**
  - **Donut Chart:** Overall Churn Proportion (Retained 73.5% vs Churned 26.5%).
  - **Clustered Column Chart:** Churn by Contract Type (Month-to-month: 42.7%, One year: 11.3%, Two year: 2.8%).
  - **Stacked Bar Chart:** Churn Rate by Tenure Group (0-12m: 47.7%, 13-24m: 28.7%, 25-48m: 20.6%, 49+m: 9.2%).
  - **Bar Chart:** Annualized Revenue at Risk by Strategic Segment.
- **Slicers (Top/Left Bar):**
  - Contract Type (`Contract`)
  - Customer Value Tier (`CustomerValueSegment`)
  - Payment Method (`PaymentMethod`)
  - Internet Service (`InternetService`)

---

### Page 2 — Churn Analysis (Behavioral & Product Deep-Dive)
- **Objective:** Identify the core structural and behavioral factors driving customer cancellations.
- **Key Questions Answered:** *Who is leaving, and why?*
- **Visuals:**
  - **Bar Chart (Horizontal):** Churn Rate by Payment Method (Electronic Check: 45.3% vs Automatic Credit Card: 15.2%).
  - **Grouped Bar Chart:** Internet Service Type vs Tech Support Status (Highlighting Fiber Optic vulnerability).
  - **Line Chart with Markers:** Number of Subscribed Services (0 to 8) vs Churn Rate (Demonstrating product stickiness).
  - **2x2 Grid:** Churn Rates across Demographics (Senior Citizen, Partner, Dependents, Gender).
  - **Density / Boxplot:** Monthly Charge distribution of Churned vs Retained customers ($74.44 avg vs $61.27).

---

### Page 3 — Customer Value & Retention Prioritization
- **Objective:** Direct tactical interventions toward accounts that yield the highest ROI on retention spend.
- **Key Questions Answered:** *Where should Customer Success focus retention budgets?*
- **Visuals:**
  - **Matrix Visual:** 2x2 Strategic Quadrant:
    - Rows: `CustomerValueSegment` (High, Medium, Low)
    - Columns: `ChurnRiskSegment` (High Risk, Medium Risk, Low Risk)
    - Values: `[Total Customers]`, `[Churn Rate %]`, `[Monthly Revenue at Risk]`
  - **Top High-Value Active At-Risk Table:**
    - Fields: `customerID`, `MonthlyCharges`, `tenure`, `Contract`, `InternetService`, `TechSupport`, `PaymentMethod`
    - Filtered to: `Churn = "No"`, `CustomerValueSegment = "High Value"`, `Contract = "Month-to-month"`
    - Sorted by: `MonthlyCharges` DESC
  - **Waterfall / Gauge Chart:** Potential Revenue Recoverable through 10% and 20% Churn Reduction Scenarios.

---

## 3. Styling & Color Palette Standards

| UI Element | Hex Code | Color Sample / Description |
|---|---|---|
| **Background** | `#F8F9FA` | Light subtle gray canvas |
| **Card / Visual Fill** | `#FFFFFF` | Clean white containers with subtle shadow |
| **Primary Navy** | `#1E3A8A` | Professional executive navy headers |
| **Alert Red (Churn)** | `#DC2626` | Churn indicators, risk alerts, lost revenue |
| **Success Green (Retained)** | `#16A34A` | Retained customer volume, active revenue |
| **Warning Orange** | `#F59E0B` | Medium risk tier, 1-year contract cohorts |
| **Text Dark** | `#1F2937` | High contrast charcoal typography |
