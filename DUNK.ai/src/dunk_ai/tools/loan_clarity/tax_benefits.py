"""
Loan Clarity Tool – Tax Benefits Calculator (India-specific)

This module calculates tax benefits for home loans in India:
- Section 24(b): Interest deduction (up to ₹2 lakh for self-occupied, no limit for let-out)
- Section 80C: Principal repayment deduction (up to ₹1.5 lakh)
- Section 80EEA: Additional interest deduction for first-time home buyers (up to ₹1.5 lakh)
- Section 80EEB: Interest deduction for electric vehicle loans (up to ₹1.5 lakh)
- Net cost after tax benefits
"""

from typing import Dict, Any
from .logic import reducing_balance, flat_rate


def calculate_tax_benefits(
    principal: float,
    annual_rate: float,
    tenure_years: float,
    repayment_frequency: str,
    loan_type: str = "home_loan",
    interest_method: str = "reducing",
    tax_slab: float = 30.0,
    is_first_time_buyer: bool = False,
    is_self_occupied: bool = True,
    financial_year: int = None
) -> Dict[str, Any]:
    """
    Calculate tax benefits for a loan (India-specific).

    Args:
        principal (float): Loan amount
        annual_rate (float): Annual interest rate (%)
        tenure_years (float): Loan tenure in years
        repayment_frequency (str): "monthly", "quarterly", or "annually"
        loan_type (str): "home_loan", "vehicle_loan", or "personal_loan"
        interest_method (str): "reducing" or "flat"
        tax_slab (float): Income tax slab percentage (5, 10, 20, 30)
        is_first_time_buyer (bool): Whether first-time home buyer (for Section 80EEA)
        is_self_occupied (bool): Whether property is self-occupied (for Section 24)
        financial_year (int): Financial year (default: current year)

    Returns:
        dict: Contains:
            - annual_interest: Annual interest payment
            - annual_principal: Annual principal repayment
            - section_24_deduction: Interest deduction under Section 24(b)
            - section_80c_deduction: Principal deduction under Section 80C
            - section_80eea_deduction: Additional interest deduction (if applicable)
            - section_80eeb_deduction: EV loan interest deduction (if applicable)
            - total_tax_deduction: Total tax deduction amount
            - tax_savings: Actual tax saved
            - net_interest_cost: Interest cost after tax benefits
    """
    from datetime import datetime
    if financial_year is None:
        financial_year = datetime.now().year

    # Calculate loan details
    if interest_method == "flat":
        emi, total_interest, total_payment, num_payments = flat_rate(
            principal, annual_rate, tenure_years, repayment_frequency
        )
    else:
        emi, total_interest, total_payment, num_payments = reducing_balance(
            principal, annual_rate, tenure_years, repayment_frequency
        )

    # Calculate annual amounts (approximate)
    periods_per_year = 12 if repayment_frequency == "monthly" else (4 if repayment_frequency == "quarterly" else 1)
    annual_emi = emi * periods_per_year
    annual_interest = total_interest / tenure_years
    annual_principal = annual_emi - annual_interest

    # Section 24(b): Interest deduction
    if loan_type == "home_loan":
        if is_self_occupied:
            section_24_deduction = min(annual_interest, 200000)  # ₹2 lakh limit
        else:
            section_24_deduction = annual_interest  # No limit for let-out
    else:
        section_24_deduction = 0.0

    # Section 80C: Principal repayment deduction (only for home loans)
    if loan_type == "home_loan":
        section_80c_deduction = min(annual_principal, 150000)  # ₹1.5 lakh limit
    else:
        section_80c_deduction = 0.0

    # Section 80EEA: Additional interest for first-time home buyers
    section_80eea_deduction = 0.0
    if loan_type == "home_loan" and is_first_time_buyer:
        # Additional ₹1.5 lakh interest deduction
        # Only if property value < ₹45 lakh and loan < ₹35 lakh
        if principal <= 3500000:  # ₹35 lakh
            section_80eea_deduction = min(annual_interest - section_24_deduction, 150000)

    # Section 80EEB: Electric vehicle loan interest deduction
    section_80eeb_deduction = 0.0
    if loan_type == "vehicle_loan":
        # Assuming it's an EV loan (would need explicit flag in real implementation)
        section_80eeb_deduction = min(annual_interest, 150000)  # ₹1.5 lakh limit

    # Total deduction
    total_tax_deduction = section_24_deduction + section_80c_deduction + \
                         section_80eea_deduction + section_80eeb_deduction

    # Tax savings
    tax_savings = total_tax_deduction * (tax_slab / 100.0)

    # Net interest cost
    net_interest_cost = annual_interest - tax_savings

    return {
        "annual_interest": round(annual_interest, 2),
        "annual_principal": round(annual_principal, 2),
        "section_24_deduction": round(section_24_deduction, 2),
        "section_80c_deduction": round(section_80c_deduction, 2),
        "section_80eea_deduction": round(section_80eea_deduction, 2),
        "section_80eeb_deduction": round(section_80eeb_deduction, 2),
        "total_tax_deduction": round(total_tax_deduction, 2),
        "tax_savings": round(tax_savings, 2),
        "net_interest_cost": round(max(0, net_interest_cost), 2),
        "tax_slab_percentage": tax_slab
    }


def calculate_lifetime_tax_benefits(
    principal: float,
    annual_rate: float,
    tenure_years: float,
    repayment_frequency: str,
    loan_type: str = "home_loan",
    interest_method: str = "reducing",
    tax_slab: float = 30.0,
    is_first_time_buyer: bool = False,
    is_self_occupied: bool = True
) -> Dict[str, Any]:
    """
    Calculate total tax benefits over the entire loan tenure.

    Args:
        principal (float): Loan amount
        annual_rate (float): Annual interest rate (%)
        tenure_years (float): Loan tenure in years
        repayment_frequency (str): "monthly", "quarterly", or "annually"
        loan_type (str): "home_loan", "vehicle_loan", or "personal_loan"
        interest_method (str): "reducing" or "flat"
        tax_slab (float): Income tax slab percentage
        is_first_time_buyer (bool): Whether first-time home buyer
        is_self_occupied (bool): Whether property is self-occupied

    Returns:
        dict: Lifetime tax benefits summary
    """
    # Calculate annual benefits
    annual_benefits = calculate_tax_benefits(
        principal, annual_rate, tenure_years, repayment_frequency,
        loan_type, interest_method, tax_slab, is_first_time_buyer, is_self_occupied
    )

    # Calculate total over tenure
    lifetime_tax_savings = annual_benefits["tax_savings"] * tenure_years
    lifetime_deduction = annual_benefits["total_tax_deduction"] * tenure_years

    # Calculate total interest
    if interest_method == "flat":
        _, total_interest, _, _ = flat_rate(principal, annual_rate, tenure_years, repayment_frequency)
    else:
        _, total_interest, _, _ = reducing_balance(principal, annual_rate, tenure_years, repayment_frequency)

    net_interest_after_tax = total_interest - lifetime_tax_savings

    return {
        "total_interest": round(total_interest, 2),
        "lifetime_tax_savings": round(lifetime_tax_savings, 2),
        "lifetime_deduction": round(lifetime_deduction, 2),
        "net_interest_after_tax": round(max(0, net_interest_after_tax), 2),
        "tax_benefit_percentage": round((lifetime_tax_savings / total_interest) * 100, 2) if total_interest > 0 else 0.0
    }


