"""
Loan Clarity Tool – Validations

This file contains input validation utilities to ensure
safe and correct values before calculations.
"""

def validate_principal(principal: float):
    if principal <= 0:
        raise ValueError("Principal must be greater than 0.")
    return principal


def validate_interest_rate(annual_rate: float):
    if annual_rate < 0:
        raise ValueError("Interest rate cannot be negative.")
    return annual_rate


def validate_tenure(tenure_years: float):
    if tenure_years <= 0:
        raise ValueError("Loan tenure must be greater than 0.")
    return tenure_years


def validate_repayment_frequency(frequency: str):
    valid_frequencies = ["monthly", "quarterly", "annually"]
    if frequency not in valid_frequencies:
        raise ValueError(f"Invalid repayment frequency. Must be one of: {valid_frequencies}")
    return frequency


def validate_interest_method(method: str):
    valid_methods = ["reducing", "flat"]
    if method not in valid_methods:
        raise ValueError(f"Invalid interest method. Must be one of: {valid_methods}")
    return method