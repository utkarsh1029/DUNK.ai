"""
Loan Clarity Tool – Effective Interest Rate Calculator

This module calculates:
- Effective interest rate including processing fees and other charges
- True cost of borrowing
- APR (Annual Percentage Rate) equivalent
"""

from typing import Dict, Any
from .logic import reducing_balance, flat_rate, get_periods_per_year
import math


def calculate_effective_rate(
    principal: float,
    annual_rate: float,
    tenure_years: float,
    repayment_frequency: str = "monthly",
    processing_fee: float = 0.0,
    other_charges: float = 0.0,
    interest_method: str = "reducing"
) -> float:
    """
    Calculate effective interest rate including all charges.

    Args:
        principal (float): Loan amount
        annual_rate (float): Annual interest rate (%)
        tenure_years (float): Loan tenure in years
        repayment_frequency (str): "monthly", "quarterly", or "annually"
        processing_fee (float): Processing fee amount
        other_charges (float): Other charges (insurance, etc.)
        interest_method (str): "reducing" or "flat"

    Returns:
        float: Effective interest rate (%)
    """
    # Calculate loan details
    if interest_method == "flat":
        emi, total_interest, total_payment, num_payments = flat_rate(
            principal, annual_rate, tenure_years, repayment_frequency
        )
    else:
        emi, total_interest, total_payment, num_payments = reducing_balance(
            principal, annual_rate, tenure_years, repayment_frequency
        )

    # Effective principal (amount actually received after charges)
    effective_principal = principal - processing_fee - other_charges
    if effective_principal <= 0:
        return annual_rate  # Return original rate if charges exceed principal

    # Total amount to be repaid (including all charges)
    total_cost = total_payment + processing_fee + other_charges

    # Calculate effective rate: the rate that would produce the same total cost
    # if applied to the effective principal
    # Effective rate = ((Total cost - Effective principal) / Effective principal) / tenure * 100
    # This accounts for both the interest on full principal and the charges
    total_cost_over_principal = total_cost - effective_principal
    
    if effective_principal > 0 and tenure_years > 0:
        # The effective rate is the rate that, when applied to effective_principal,
        # would give the same total cost
        # We approximate by: rate = (total_cost - effective_principal) / effective_principal / tenure
        # But this is a simple approximation. For reducing balance, we need to account for compounding.
        # A better approximation: effective_rate ≈ nominal_rate * (principal / effective_principal)
        # Plus the charges component spread over tenure
        base_effective_rate = annual_rate * (principal / effective_principal)
        charges_rate_component = ((processing_fee + other_charges) / effective_principal) / tenure_years * 100
        effective_rate = base_effective_rate + charges_rate_component
    else:
        effective_rate = annual_rate

    return round(effective_rate, 2)


def calculate_apr(
    principal: float,
    annual_rate: float,
    tenure_years: float,
    repayment_frequency: str = "monthly",
    processing_fee: float = 0.0,
    other_charges: float = 0.0,
    interest_method: str = "reducing"
) -> Dict[str, Any]:
    """
    Calculate APR (Annual Percentage Rate) including all costs.

    Args:
        principal (float): Loan amount
        annual_rate (float): Annual interest rate (%)
        tenure_years (float): Loan tenure in years
        repayment_frequency (str): "monthly", "quarterly", or "annually"
        processing_fee (float): Processing fee amount
        other_charges (float): Other charges
        interest_method (str): "reducing" or "flat"

    Returns:
        dict: APR details
    """
    # Calculate effective rate
    effective_rate = calculate_effective_rate(
        principal, annual_rate, tenure_years, repayment_frequency,
        processing_fee, other_charges, interest_method
    )

    # Calculate loan details
    if interest_method == "flat":
        emi, total_interest, total_payment, num_payments = flat_rate(
            principal, annual_rate, tenure_years, repayment_frequency
        )
    else:
        emi, total_interest, total_payment, num_payments = reducing_balance(
            principal, annual_rate, tenure_years, repayment_frequency
        )

    total_cost = total_payment + processing_fee + other_charges
    total_charges = processing_fee + other_charges

    return {
        "nominal_rate": round(annual_rate, 2),
        "effective_rate": effective_rate,
        "apr": effective_rate,  # APR is same as effective rate in this context
        "total_charges": round(total_charges, 2),
        "total_cost": round(total_cost, 2),
        "charges_percentage": round((total_charges / principal) * 100, 2) if principal > 0 else 0.0,
        "rate_difference": round(effective_rate - annual_rate, 2)
    }

