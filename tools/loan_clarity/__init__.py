"""
Loan Clarity Tool – DUNK.ai
"""
from .logic import flat_rate, reducing_balance
from .validations import (
    validate_principal,
    validate_interest_rate,
    validate_tenure,
    validate_repayment_frequency,
    validate_interest_method,
)

__all__ = [
    "flat_rate",
    "reducing_balance",
    "validate_principal",
    "validate_interest_rate",
    "validate_tenure",
    "validate_repayment_frequency",
    "validate_interest_method",
]