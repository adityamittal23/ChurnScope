# Data Dictionary — Customer Churn & Retention Analytics

## 1. Overview
This data dictionary documents the raw customer records and transformed analytical attributes utilized in the **Customer Churn & Retention Analytics Platform**. The dataset originates from the telecommunications customer base, capturing demographics, subscribed products/services, account terms, billing records, and churn status.

- **Total Records:** 7,043
- **Primary Key:** `customer_id` (`customerID`)
- **Target Variable:** `churn` / `churn_flag` (Positive class = 'Yes' / 1)
- **Granularity:** One record per customer account

---

## 2. Raw Schema Definition

| Column Name | Data Type (Raw) | Null Count | Description | Allowed / Unique Values |
|---|---|---|---|---|
| `customerID` | String (VARCHAR) | 0 | Unique customer identifier | Alphanumeric (e.g., `7590-VHVEG`) |
| `gender` | String (VARCHAR) | 0 | Customer gender | `Male`, `Female` |
| `SeniorCitizen` | Integer (INT) | 0 | Binary flag indicating if customer is a senior citizen | `0` (No), `1` (Yes) |
| `Partner` | String (VARCHAR) | 0 | Whether the customer has a partner | `Yes`, `No` |
| `Dependents` | String (VARCHAR) | 0 | Whether the customer has dependents | `Yes`, `No` |
| `tenure` | Integer (INT) | 0 | Number of months the customer has stayed with the company | Integer `0` to `72` |
| `PhoneService` | String (VARCHAR) | 0 | Whether the customer has phone service | `Yes`, `No` |
| `MultipleLines` | String (VARCHAR) | 0 | Whether customer has multiple phone lines | `Yes`, `No`, `No phone service` |
| `InternetService` | String (VARCHAR) | 0 | Customer's internet service provider type | `DSL`, `Fiber optic`, `No` |
| `OnlineSecurity` | String (VARCHAR) | 0 | Whether customer has online security add-on | `Yes`, `No`, `No internet service` |
| `OnlineBackup` | String (VARCHAR) | 0 | Whether customer has online backup add-on | `Yes`, `No`, `No internet service` |
| `DeviceProtection` | String (VARCHAR) | 0 | Whether customer has tech device protection add-on | `Yes`, `No`, `No internet service` |
| `TechSupport` | String (VARCHAR) | 0 | Whether customer has premium technical support add-on | `Yes`, `No`, `No internet service` |
| `StreamingTV` | String (VARCHAR) | 0 | Whether customer streams third-party TV | `Yes`, `No`, `No internet service` |
| `StreamingMovies` | String (VARCHAR) | 0 | Whether customer streams movies | `Yes`, `No`, `No internet service` |
| `Contract` | String (VARCHAR) | 0 | The contract commitment term of the customer | `Month-to-month`, `One year`, `Two year` |
| `PaperlessBilling` | String (VARCHAR) | 0 | Whether customer has opted into paperless billing | `Yes`, `No` |
| `PaymentMethod` | String (VARCHAR) | 0 | Customer's payment method | `Electronic check`, `Mailed check`, `Bank transfer (automatic)`, `Credit card (automatic)` |
| `MonthlyCharges` | Float (FLOAT) | 0 | The amount charged to the customer monthly (USD) | Numeric `18.25` to `118.75` |
| `TotalCharges` | String -> Float | 11 blanks | Total cumulative amount charged to customer (USD) | Numeric `0.00` to `8684.80` |
| `Churn` | String (VARCHAR) | 0 | Churn status: whether customer left in the last month | `Yes`, `No` |

---

## 3. Processed & Derived Analytical Features

To facilitate granular segmentation, statistical exploration, SQL KPIs, and Power BI DAX calculations, the following standardized and engineered features are created during Phase 2:

| Field Name | Type | Formula / Logic | Business Context |
|---|---|---|---|
| `churn_flag` | Integer | `1` if `Churn == 'Yes'` else `0` | Binary indicator enabling mathematical aggregations (`AVG(churn_flag)` = Churn Rate). |
| `senior_citizen_label` | String | `Yes` if `SeniorCitizen == 1` else `No` | User-friendly label for business reporting and slice-and-dice visuals. |
| `tenure_group` | Categorical | `0–12 Months`, `13–24 Months`, `25–48 Months`, `49+ Months` | Standardized tenure buckets specified in the PRD. |
| `tenure_cohort` | Categorical | `New (0-1 yr)`, `Growing (1-2 yrs)`, `Established (2-4 yrs)`, `Loyal (4+ yrs)` | Lifecycle stage categorization. |
| `monthly_revenue` | Float | `MonthlyCharges` | Standardized revenue alias. |
| `annual_revenue` | Float | `MonthlyCharges * 12` | Projected annualized recurring run-rate per account. |
| `revenue_segment` | Categorical | Low (`< $35`), Medium (`$35 - $70`), High (`> $70`) | Value tier based on monthly spend distribution. |
| `contract_category` | Categorical | `Month-to-month`, `One year`, `Two year` | Standardized contract type. |
| `payment_category` | Categorical | `Automatic` (`Bank transfer`, `Credit card`), `Manual` (`Electronic check`, `Mailed check`) | Payment automation indicator (manual payment friction often correlates with churn). |
| `service_count` | Integer | Count of active add-on services (`PhoneService`, `MultipleLines`, `OnlineSecurity`, `OnlineBackup`, `DeviceProtection`, `TechSupport`, `StreamingTV`, `StreamingMovies`) | Measure of product stickiness and customer engagement depth. |
| `has_internet` | Integer | `1` if `InternetService != 'No'` else `0` | Flag for internet-connected customer base. |
| `has_tech_support` | Integer | `1` if `TechSupport == 'Yes'` else `0` | Indicator for critical churn-reducing support package. |
| `has_online_security` | Integer | `1` if `OnlineSecurity == 'Yes'` else `0` | Indicator for critical churn-reducing security package. |
| `churn_risk_segment` | Categorical | Multi-factor risk tier (`High Risk`, `Medium Risk`, `Low Risk`) based on contract tenure and service characteristics. | Risk stratification for tactical interventions. |
| `strategic_segment` | Categorical | 2x2 Value & Risk Quadrant: <br>• `High Value + High Risk` (Retention Priority)<br>• `High Value + Low Risk` (Loyal Champions)<br>• `Low Value + High Risk` (At-Risk Budget)<br>• `Low Value + Low Risk` (Stable Base) | Strategic matrix defining executive retention prioritization. |

---

## 4. Key Metric Calculations & Rules

1. **Overall Churn Rate:**
   $$\text{Churn Rate} = \frac{\sum \text{Churned Customers}}{\text{Total Customers}} \times 100\%$$

2. **Monthly Revenue at Risk:**
   $$\text{Revenue at Risk} = \sum_{\text{Churned Customers}} \text{MonthlyCharges}$$

3. **Annualized Revenue at Risk:**
   $$\text{Annual Revenue at Risk} = \text{Monthly Revenue at Risk} \times 12$$

4. **Average Revenue Per User (ARPU):**
   $$\text{ARPU} = \frac{\sum \text{MonthlyCharges}}{\text{Total Customers}}$$

5. **Customer Lifetime (Months):**
   $$\text{Customer Lifetime} = \text{tenure}$$
