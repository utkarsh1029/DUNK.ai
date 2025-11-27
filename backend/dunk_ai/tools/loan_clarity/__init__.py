"""
Loan Clarity Tool – DUNK.ai

Comprehensive loan calculation and analysis tool with:
- EMI calculations (flat rate and reducing balance)
- Amortization schedules
- Prepayment and early settlement analysis
- Loan comparison
- Tax benefits calculator (India-specific)
- Loan eligibility calculator
- Effective interest rate calculator
"""

# Core logic
from .logic import (
    flat_rate,
    reducing_balance,
    calculate_prepayment_impact,
    calculate_early_settlement,
    modify_emi,
    modify_tenure,
    get_periods_per_year
)

# Schedule generation
from .schedule import (
    generate_amortization_schedule,
    get_outstanding_principal,
    get_year_wise_summary
)

# Loan comparison
from .comparison import (
    compare_loans,
    break_even_analysis
)

# Tax benefits
from .tax_benefits import (
    calculate_tax_benefits,
    calculate_lifetime_tax_benefits
)

# Eligibility
from .eligibility import (
    calculate_loan_eligibility,
    calculate_affordability
)

# Effective rate
from .effective_rate import (
    calculate_effective_rate,
    calculate_apr
)

# Validations
from .validations import (
    validate_principal,
    validate_interest_rate,
    validate_tenure,
    validate_repayment_frequency,
    validate_interest_method,
    validate_payments_made,
    validate_prepayment_amount,
    validate_income,
    validate_tax_slab,
    validate_loan_type
)

__all__ = [
    # Core calculations
    "flat_rate",
    "reducing_balance",
    "get_periods_per_year",
    # Prepayment and settlement
    "calculate_prepayment_impact",
    "calculate_early_settlement",
    # EMI modifications
    "modify_emi",
    "modify_tenure",
    # Schedule
    "generate_amortization_schedule",
    "get_outstanding_principal",
    "get_year_wise_summary",
    # Comparison
    "compare_loans",
    "break_even_analysis",
    # Tax benefits
    "calculate_tax_benefits",
    "calculate_lifetime_tax_benefits",
    # Eligibility
    "calculate_loan_eligibility",
    "calculate_affordability",
    # Effective rate
    "calculate_effective_rate",
    "calculate_apr",
    # Validations
    "validate_principal",
    "validate_interest_rate",
    "validate_tenure",
    "validate_repayment_frequency",
    "validate_interest_method",
    "validate_payments_made",
    "validate_prepayment_amount",
    "validate_income",
    "validate_tax_slab",
    "validate_loan_type",
]