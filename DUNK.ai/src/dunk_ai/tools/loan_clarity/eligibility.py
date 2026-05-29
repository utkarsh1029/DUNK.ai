"""
Loan Clarity Tool – Loan Eligibility Calculator

This module calculates:
- Maximum loan eligibility based on income
- Maximum EMI capacity
- Debt-to-income ratio
- Recommended loan amount based on affordability
"""

from typing import Dict, Any
from .logic import reducing_balance, get_periods_per_year


def calculate_loan_eligibility(
    monthly_income: float,
    annual_rate: float,
    tenure_years: float,
    repayment_frequency: str = "monthly",
    interest_method: str = "reducing",
    existing_emis: float = 0.0,
    emi_to_income_ratio: float = 0.4,
    age: int = None,
    max_tenure_by_age: int = 65
) -> Dict[str, Any]:
    """
    Calculate maximum loan eligibility based on income and other factors.

    Args:
        monthly_income (float): Monthly net income
        annual_rate (float): Annual interest rate (%)
        tenure_years (float): Desired loan tenure in years
        repayment_frequency (str): "monthly", "quarterly", or "annually"
        interest_method (str): "reducing" or "flat"
        existing_emis (float): Existing EMI obligations
        emi_to_income_ratio (float): Maximum EMI to income ratio (default: 0.4 = 40%)
        age (int): Current age (for tenure adjustment)
        max_tenure_by_age (int): Maximum age until which loan can be active

    Returns:
        dict: Contains:
            - maximum_emi: Maximum EMI capacity
            - available_emi: Available EMI after existing obligations
            - maximum_loan_amount: Maximum eligible loan amount
            - recommended_loan_amount: Recommended loan amount (80% of max)
            - emi_to_income_ratio_used: EMI to income ratio
            - debt_to_income_ratio: Total debt to income ratio
    """
    # Adjust tenure based on age if provided
    if age is not None:
        max_tenure = max_tenure_by_age - age
        tenure_years = min(tenure_years, max_tenure)
        if tenure_years <= 0:
            return {
                "error": "Loan tenure cannot exceed retirement age",
                "maximum_emi": 0.0,
                "available_emi": 0.0,
                "maximum_loan_amount": 0.0,
                "recommended_loan_amount": 0.0
            }

    # Calculate maximum EMI capacity
    maximum_emi = monthly_income * emi_to_income_ratio
    available_emi = maximum_emi - existing_emis

    if available_emi <= 0:
        return {
            "maximum_emi": round(maximum_emi, 2),
            "available_emi": 0.0,
            "maximum_loan_amount": 0.0,
            "recommended_loan_amount": 0.0,
            "message": "Existing EMIs exceed maximum capacity. Cannot avail new loan."
        }

    # Calculate maximum loan amount from available EMI
    periods_per_year = get_periods_per_year(repayment_frequency)
    periodic_rate = (annual_rate / 100.0) / periods_per_year
    number_of_payments = int(tenure_years * periods_per_year)

    if interest_method == "reducing":
        # Reverse EMI formula: P = EMI * ((1+r)^n - 1) / (r * (1+r)^n)
        if periodic_rate > 0:
            maximum_loan_amount = available_emi * \
                ((1 + periodic_rate) ** number_of_payments - 1) / \
                (periodic_rate * (1 + periodic_rate) ** number_of_payments)
        else:
            maximum_loan_amount = available_emi * number_of_payments
    else:
        # Flat rate: P = (EMI * n) / (1 + r * n)
        total_interest_rate = (annual_rate / 100.0) * tenure_years
        maximum_loan_amount = (available_emi * number_of_payments) / (1 + total_interest_rate)

    recommended_loan_amount = maximum_loan_amount * 0.8  # 80% of max for safety

    # Calculate debt-to-income ratio
    total_debt = existing_emis + available_emi
    debt_to_income_ratio = total_debt / monthly_income if monthly_income > 0 else 0

    return {
        "monthly_income": round(monthly_income, 2),
        "maximum_emi": round(maximum_emi, 2),
        "existing_emis": round(existing_emis, 2),
        "available_emi": round(available_emi, 2),
        "maximum_loan_amount": round(maximum_loan_amount, 2),
        "recommended_loan_amount": round(recommended_loan_amount, 2),
        "emi_to_income_ratio_used": round(emi_to_income_ratio * 100, 2),
        "debt_to_income_ratio": round(debt_to_income_ratio * 100, 2),
        "tenure_years": tenure_years
    }


def calculate_affordability(
    desired_loan_amount: float,
    monthly_income: float,
    annual_rate: float,
    tenure_years: float,
    repayment_frequency: str = "monthly",
    interest_method: str = "reducing",
    existing_emis: float = 0.0,
    emi_to_income_ratio: float = 0.4
) -> Dict[str, Any]:
    """
    Check if a desired loan amount is affordable.

    Args:
        desired_loan_amount (float): Desired loan amount
        monthly_income (float): Monthly net income
        annual_rate (float): Annual interest rate (%)
        tenure_years (float): Loan tenure in years
        repayment_frequency (str): "monthly", "quarterly", or "annually"
        interest_method (str): "reducing" or "flat"
        existing_emis (float): Existing EMI obligations
        emi_to_income_ratio (float): Maximum EMI to income ratio

    Returns:
        dict: Affordability analysis
    """
    # Calculate EMI for desired loan
    if interest_method == "flat":
        from .logic import flat_rate
        emi, _, _, _ = flat_rate(desired_loan_amount, annual_rate, tenure_years, repayment_frequency)
    else:
        emi, _, _, _ = reducing_balance(desired_loan_amount, annual_rate, tenure_years, repayment_frequency)

    total_emi = emi + existing_emis
    maximum_emi = monthly_income * emi_to_income_ratio
    is_affordable = total_emi <= maximum_emi

    # Calculate how much loan is affordable
    eligibility = calculate_loan_eligibility(
        monthly_income, annual_rate, tenure_years, repayment_frequency,
        interest_method, existing_emis, emi_to_income_ratio
    )

    return {
        "desired_loan_amount": round(desired_loan_amount, 2),
        "required_emi": round(emi, 2),
        "total_emi_with_existing": round(total_emi, 2),
        "maximum_emi_capacity": round(maximum_emi, 2),
        "is_affordable": is_affordable,
        "affordable_loan_amount": round(eligibility["maximum_loan_amount"], 2),
        "shortfall": round(desired_loan_amount - eligibility["maximum_loan_amount"], 2) if not is_affordable else 0.0,
        "emi_to_income_ratio_actual": round((total_emi / monthly_income) * 100, 2) if monthly_income > 0 else 0.0
    }


