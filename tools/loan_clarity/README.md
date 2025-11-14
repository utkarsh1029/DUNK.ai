# Loan Clarity Module - Complete Documentation

## Overview

The Loan Clarity module is a comprehensive loan calculation and analysis tool that provides detailed insights into loan repayment, prepayment strategies, tax benefits, and eligibility calculations. It supports both flat rate and reducing balance interest calculation methods.

## Features

### 1. Core Loan Calculations
- **Flat Rate Method**: Simple interest calculation where interest is calculated on the original principal
- **Reducing Balance Method**: Standard EMI calculation where interest is calculated on outstanding principal

### 2. Amortization Schedule
- Period-by-period breakdown of loan payments
- Shows principal, interest, and balance for each payment
- Cumulative tracking of principal and interest paid
- Support for monthly, quarterly, and annual payments

### 3. Prepayment Analysis
- Calculate impact of prepayment on EMI or tenure
- Interest savings calculation
- Support for both EMI reduction and tenure reduction strategies

### 4. Early Settlement
- Calculate outstanding principal at any point
- Settlement amount including charges
- Interest savings from early closure

### 5. EMI Modification
- Calculate new tenure when EMI is changed
- Calculate new EMI when tenure is modified
- Impact analysis of modifications

### 6. Loan Comparison
- Compare multiple loan options side-by-side
- Best option recommendation
- Break-even analysis between loans

### 7. Tax Benefits Calculator (India-specific)
- Section 24(b): Interest deduction (up to ₹2 lakh for self-occupied)
- Section 80C: Principal repayment deduction (up to ₹1.5 lakh)
- Section 80EEA: Additional interest for first-time home buyers (up to ₹1.5 lakh)
- Section 80EEB: EV loan interest deduction (up to ₹1.5 lakh)
- Lifetime tax benefits calculation

### 8. Loan Eligibility
- Maximum loan amount based on income
- EMI capacity calculation
- Debt-to-income ratio analysis
- Affordability check for desired loan amount

### 9. Effective Interest Rate
- Calculate true cost of borrowing including charges
- APR (Annual Percentage Rate) calculation
- Processing fees and other charges integration

## Module Structure

```
loan_clarity/
├── __init__.py          # Package exports
├── logic.py             # Core calculation functions
├── schedule.py          # Amortization schedule generation
├── comparison.py        # Loan comparison tools
├── tax_benefits.py      # Tax benefits calculator
├── eligibility.py       # Loan eligibility calculator
├── effective_rate.py    # Effective interest rate calculator
├── validations.py       # Input validation utilities
└── __main__.py          # CLI interface
```

## Usage Examples

### Basic EMI Calculation

```python
from tools.loan_clarity import reducing_balance, flat_rate

# Reducing balance method
emi, total_interest, total_payment, num_payments = reducing_balance(
    principal=1000000,
    annual_rate=10,
    tenure_years=20,
    repayment_frequency="monthly"
)

# Flat rate method
emi, total_interest, total_payment, num_payments = flat_rate(
    principal=1000000,
    annual_rate=10,
    tenure_years=20,
    repayment_frequency="monthly"
)
```

### Amortization Schedule

```python
from tools.loan_clarity import generate_amortization_schedule
from datetime import datetime

schedule = generate_amortization_schedule(
    principal=1000000,
    annual_rate=10,
    tenure_years=20,
    repayment_frequency="monthly",
    interest_method="reducing",
    start_date=datetime(2024, 1, 1)
)

# Each entry in schedule contains:
# - payment_number
# - payment_date
# - opening_balance
# - emi
# - principal_paid
# - interest_paid
# - closing_balance
# - cumulative_principal
# - cumulative_interest
```

### Prepayment Impact

```python
from tools.loan_clarity import calculate_prepayment_impact

# Reduce EMI after prepayment
result = calculate_prepayment_impact(
    principal=1000000,
    annual_rate=10,
    tenure_years=20,
    repayment_frequency="monthly",
    payments_made=24,
    prepayment_amount=100000,
    interest_method="reducing",
    reduce_emi=True  # Set to False to reduce tenure instead
)
```

### Loan Comparison

```python
from tools.loan_clarity import compare_loans

loan_options = [
    {
        "principal": 1000000,
        "annual_rate": 10,
        "tenure_years": 20,
        "repayment_frequency": "monthly",
        "interest_method": "reducing",
        "processing_fee": 10000,
        "loan_name": "Bank A"
    },
    {
        "principal": 1000000,
        "annual_rate": 9.5,
        "tenure_years": 20,
        "repayment_frequency": "monthly",
        "interest_method": "reducing",
        "processing_fee": 15000,
        "loan_name": "Bank B"
    }
]

comparison = compare_loans(loan_options)
print(f"Best option: {comparison['best_option']['loan_name']}")
```

### Tax Benefits (India)

```python
from tools.loan_clarity import calculate_tax_benefits

benefits = calculate_tax_benefits(
    principal=5000000,
    annual_rate=8.5,
    tenure_years=20,
    repayment_frequency="monthly",
    loan_type="home_loan",
    interest_method="reducing",
    tax_slab=30.0,
    is_first_time_buyer=True,
    is_self_occupied=True
)

print(f"Annual tax savings: ₹{benefits['tax_savings']}")
```

### Loan Eligibility

```python
from tools.loan_clarity import calculate_loan_eligibility

eligibility = calculate_loan_eligibility(
    monthly_income=100000,
    annual_rate=10,
    tenure_years=20,
    repayment_frequency="monthly",
    interest_method="reducing",
    existing_emis=20000,
    emi_to_income_ratio=0.4
)

print(f"Maximum loan amount: ₹{eligibility['maximum_loan_amount']}")
```

## MCP Tools

The module exposes 10 MCP tools for LLM integration:

1. `loan_clarity` - Basic EMI calculation
2. `generate_amortization_schedule_tool` - Detailed repayment schedule
3. `calculate_prepayment_impact_tool` - Prepayment analysis
4. `calculate_early_settlement_tool` - Early settlement calculator
5. `modify_emi_tool` - Calculate new tenure for modified EMI
6. `modify_tenure_tool` - Calculate new EMI for modified tenure
7. `compare_loans_tool` - Compare multiple loan options
8. `calculate_tax_benefits_tool` - Tax benefits calculator
9. `calculate_loan_eligibility_tool` - Loan eligibility calculator
10. `calculate_effective_rate_tool` - Effective interest rate calculator

## Input Validation

All functions include comprehensive input validation:
- Principal must be positive and reasonable
- Interest rate must be non-negative and reasonable
- Tenure must be positive and within limits
- Repayment frequency must be valid
- Interest method must be "reducing" or "flat"

## Testing

Run tests with:
```bash
pytest tests/test_loan_clarity.py
```

Tests cover:
- Basic EMI calculations
- Amortization schedules
- Prepayment scenarios
- Early settlement
- EMI/tenure modifications
- Loan comparison
- Tax benefits
- Eligibility calculations
- Edge cases and error handling

## Notes

- All monetary values are in the same currency (default: INR ₹)
- Interest rates are in percentage (e.g., 10 for 10%)
- Dates use ISO format (YYYY-MM-DD)
- Tax benefits are India-specific and follow current tax laws
- Calculations use standard financial formulas
- Rounding is applied to 2 decimal places for currency values

## Future Enhancements

Potential additions:
- Export to CSV/JSON formats
- Visualization of loan breakdown
- Step-up/step-down EMI support
- Floating rate calculations
- Grace period support
- Loan restructuring scenarios


