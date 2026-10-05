# Power BI Data Model Architecture & Schema Design

## 1. Overview
The **Customer Churn & Retention Analytics Platform** supports two enterprise modeling options within Power BI Desktop:
1. **Single-Table Analytical Model (`Fact_Customers`):** Highly performant and simple for standard reporting.
2. **Normalized Star-Schema Model:** Adhering to Kimball dimensional modeling principles for enterprise BI scalability.

---

## 2. Star Schema Architecture

```text
                  ┌──────────────────────┐
                  │   Dim_Demographics   │
                  ├──────────────────────┤
                  │ customer_id (PK)     │
                  │ gender               │
                  │ senior_citizen       │
                  │ partner              │
                  │ dependents           │
                  └──────────┬───────────┘
                             │ 1
                             │
                             │ 1
                  ┌──────────┴───────────┐
                  │    Fact_Customers    │
                  ├──────────────────────┤
                  │ customer_id (PK)     │
                  │ tenure               │
                  │ monthly_charges      │
                  │ total_charges        │
                  │ churn                │
                  │ churn_flag           │
                  │ tenure_group         │
                  │ customer_value_seg   │
                  │ strategic_segment    │
                  │ contract_key (FK)    │
                  │ payment_key (FK)     │
                  │ service_key (FK)     │
                  └──────────┬───────────┘
            ┌────────────────┼────────────────┐
          * │ 1            * │ 1            * │ 1
┌───────────┴──────────┐   ┌─┴─────────────┐  └─────────────┬───────────┐
│     Dim_Contract     │   │  Dim_Payment  │                │   Dim_Services│
├──────────────────────┤   ├───────────────┤                ├───────────┤
│ contract_key (PK)    │   │ payment_key   │                │ service_key
│ contract_name        │   │ payment_method│                │ internet_svc
│ contract_category    │   │ payment_cat   │                │ tech_support
└──────────────────────┘   └───────────────┘                │ online_sec
                                                            └───────────┘
```

---

## 3. Dimension & Fact Table Specifications

### 3.1 Fact Table: `Fact_Customers`
- **Granularity:** One row per individual customer subscription account.
- **Attributes:**
  - `customer_id` (Primary Key, VARCHAR)
  - `tenure` (INTEGER, months)
  - `monthly_charges` (FLOAT, current monthly spend)
  - `total_charges` (FLOAT, lifetime cumulative spend)
  - `churn` (VARCHAR, 'Yes' / 'No')
  - `churn_flag` (INTEGER, 1 / 0)
  - `tenure_group` (VARCHAR, '0-12 Months', '13-24 Months', '25-48 Months', '49+ Months')
  - `tenure_cohort` (VARCHAR, 'New (0-1 yr)', etc.)
  - `customer_value_segment` (VARCHAR, 'Low Value', 'Medium Value', 'High Value')
  - `churn_risk_segment` (VARCHAR, 'High Risk', 'Medium Risk', 'Low Risk')
  - `strategic_segment` (VARCHAR, 2x2 Matrix label)
  - `service_count` (INTEGER, count of active add-on products)

### 3.2 Dimension Table: `Dim_Contract`
- `contract_key` (Surrogate Key)
- `contract_name` ('Month-to-month', 'One year', 'Two year')
- `contract_category` ('Short-term / Flexible', 'Long-term / Committed')

### 3.3 Dimension Table: `Dim_PaymentMethod`
- `payment_key` (Surrogate Key)
- `payment_method` ('Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)')
- `payment_category` ('Manual', 'Automatic')

### 3.4 Dimension Table: `Dim_Services`
- `service_key` (Surrogate Key)
- `internet_service` ('Fiber optic', 'DSL', 'No')
- `tech_support` ('Yes', 'No', 'No internet service')
- `online_security` ('Yes', 'No', 'No internet service')
- `streaming_tv` ('Yes', 'No', 'No internet service')
- `streaming_movies` ('Yes', 'No', 'No internet service')

---

## 4. Relationship Cardinality & Filter Behavior

| From (Dimension) | To (Fact) | Cardinality | Cross Filter Direction | Security Filter |
|---|---|---|---|---|
| `Dim_Contract[contract_name]` | `Fact_Customers[contract]` | 1-to-Many (`1:*`) | Single (`Dim -> Fact`) | Disabled |
| `Dim_Payment[payment_method]` | `Fact_Customers[payment_method]` | 1-to-Many (`1:*`) | Single (`Dim -> Fact`) | Disabled |
| `Dim_Services[service_key]` | `Fact_Customers[service_key]` | 1-to-Many (`1:*`) | Single (`Dim -> Fact`) | Disabled |

---

## 5. Performance Optimization & Best Practices
1. **Integer Keys:** Use integer surrogate keys for joins where possible.
2. **Hide Foreign Keys:** Hide all foreign keys and raw flag columns from the report view to provide an intuitive field list for report creators.
3. **Sort By Column:** Ensure `TenureGroup` is sorted by `tenure` or an explicit `tenure_order` integer column so visuals display `0-12 Months`, `13-24 Months`, `25-48 Months`, `49+ Months` chronologically.
4. **Measures Table:** Consolidate all DAX measures into a dedicated `_Measures` table for organization and maintainability.
