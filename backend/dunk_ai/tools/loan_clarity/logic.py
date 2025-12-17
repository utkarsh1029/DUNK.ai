"""
Loan Clarity Tool Logic – DUNK.ai

This file contains the core calculation logic for:
1. Flat Rate Method
2. Reducing Balance Method
3. Prepayment Impact Calculations
4. Early Settlement Calculations
5. EMI Modification Scenarios
6. Helper functions
"""

import math
from typing import Tuple, Dict, Any


# --- Helpers ---
def get_periods_per_year(frequency: str) -> int:
    """
    Map repayment frequency string to periods per year.

    Args:
        frequency (str): Repayment frequency ("monthly", "quarterly", "annually")

    Returns:
        int: Number of periods per year
    """
    freq_map = {"monthly": 12, "quarterly": 4, "annually": 1}
    if frequency not in freq_map:
        raise ValueError("Invalid repayment frequency. Use monthly/quarterly/annually.")
    return freq_map[frequency]


# --- Flat Rate Method ---
def flat_rate(principal, annual_rate, tenure_years, repayment_frequency):
    """
    Calculate loan details using Flat Rate interest method.

    Args:
        principal (float): Loan amount
        annual_rate (float): Annual interest rate (%)
        tenure_years (float): Loan tenure in years
        repayment_frequency (str): "monthly", "quarterly", or "annually"

    Returns:
        tuple: (emi, total_interest, total_payment, number_of_payments)
    """
    from .validations import (
        validate_principal,
        validate_interest_rate,
        validate_tenure,
        validate_repayment_frequency
    )
    
    # Validate inputs
    validate_principal(principal)
    validate_interest_rate(annual_rate)
    validate_tenure(tenure_years)
    validate_repayment_frequency(repayment_frequency)
    
    periods_per_year = get_periods_per_year(repayment_frequency)
    number_of_payments = int(tenure_years * periods_per_year)

    total_interest = (principal * annual_rate * tenure_years) / 100.0
    total_payment = principal + total_interest
    emi = total_payment / number_of_payments

    return round(emi, 2), round(total_interest, 2), round(total_payment, 2), number_of_payments


# --- Reducing Balance Method ---
def reducing_balance(principal, annual_rate, tenure_years, repayment_frequency):
    """
    Calculate loan details using Reducing Balance (EMI) interest method.

    Args:
        principal (float): Loan amount
        annual_rate (float): Annual interest rate (%)
        tenure_years (float): Loan tenure in years
        repayment_frequency (str): "monthly", "quarterly", or "annually"

    Returns:
        tuple: (emi, total_interest, total_payment, number_of_payments)
    """
    from .validations import (
        validate_principal,
        validate_interest_rate,
        validate_tenure,
        validate_repayment_frequency
    )
    
    # Validate inputs
    validate_principal(principal)
    validate_interest_rate(annual_rate)
    validate_tenure(tenure_years)
    validate_repayment_frequency(repayment_frequency)
    
    periods_per_year = get_periods_per_year(repayment_frequency)
    number_of_payments = int(tenure_years * periods_per_year)
    if number_of_payments <= 0:
        raise ValueError("Number of payments must be greater than 0.")

    periodic_rate = (annual_rate / 100.0) / periods_per_year

    # EMI formula: P * r * (1+r)^n / ((1+r)^n -1)
    emi = (principal * periodic_rate * (1 + periodic_rate) ** number_of_payments) / \
          ((1 + periodic_rate) ** number_of_payments - 1)

    total_payment = emi * number_of_payments
    total_interest = total_payment - principal

    return round(emi, 2), round(total_interest, 2), round(total_payment, 2), number_of_payments


# --- Prepayment Impact Calculations ---
def calculate_prepayment_impact(
    principal: float,
    annual_rate: float,
    tenure_years: float,
    repayment_frequency: str,
    payments_made: int,
    prepayment_amount: float,
    interest_method: str = "reducing",
    reduce_emi: bool = True
) -> Dict[str, Any]:
    """
    Calculate the impact of a prepayment on loan.

    Args:
        principal (float): Original loan amount
        annual_rate (float): Annual interest rate (%)
        tenure_years (float): Original loan tenure in years
        repayment_frequency (str): "monthly", "quarterly", or "annually"
        payments_made (int): Number of payments already made
        prepayment_amount (float): Amount to prepay
        interest_method (str): "reducing" or "flat"
        reduce_emi (bool): If True, reduce EMI; if False, reduce tenure

    Returns:
        dict: Contains:
            - original_emi: Original EMI amount
            - outstanding_principal: Principal before prepayment
            - new_principal: Principal after prepayment
            - new_emi: New EMI (if reduce_emi=True)
            - new_tenure_years: New tenure in years (if reduce_emi=False)
            - interest_saved: Total interest saved
            - new_total_payment: New total payment amount
    """
    # Calculate original EMI
    if interest_method == "flat":
        original_emi, _, _, _ = flat_rate(principal, annual_rate, tenure_years, repayment_frequency)
    else:
        original_emi, _, _, _ = reducing_balance(principal, annual_rate, tenure_years, repayment_frequency)

    # Get outstanding principal
    from .schedule import get_outstanding_principal
    outstanding = get_outstanding_principal(
        principal, annual_rate, tenure_years, repayment_frequency,
        payments_made, interest_method
    )

    new_principal = outstanding - prepayment_amount
    if new_principal <= 0:
        return {
            "original_emi": original_emi,
            "outstanding_principal": outstanding,
            "new_principal": 0.0,
            "new_emi": 0.0,
            "new_tenure_years": 0.0,
            "interest_saved": 0.0,
            "new_total_payment": 0.0,
            "message": "Prepayment amount exceeds outstanding principal. Loan can be fully closed."
        }

    periods_per_year = get_periods_per_year(repayment_frequency)
    remaining_payments = int(tenure_years * periods_per_year) - payments_made

    if reduce_emi:
        # Calculate new EMI with same tenure
        remaining_tenure_years = remaining_payments / periods_per_year
        if interest_method == "flat":
            new_emi, _, new_total, _ = flat_rate(
                new_principal, annual_rate, remaining_tenure_years, repayment_frequency
            )
        else:
            new_emi, _, new_total, _ = reducing_balance(
                new_principal, annual_rate, remaining_tenure_years, repayment_frequency
            )

        # Calculate original remaining payment
        original_remaining = original_emi * remaining_payments
        interest_saved = original_remaining - new_total - prepayment_amount

        return {
            "original_emi": original_emi,
            "outstanding_principal": outstanding,
            "new_principal": round(new_principal, 2),
            "new_emi": new_emi,
            "new_tenure_years": remaining_tenure_years,
            "interest_saved": round(max(0, interest_saved), 2),
            "new_total_payment": round(new_total, 2),
            "emi_reduction": round(original_emi - new_emi, 2)
        }
    else:
        # Calculate new tenure with same EMI
        periodic_rate = (annual_rate / 100.0) / periods_per_year

        if interest_method == "reducing":
            # Solve for n: EMI = P * r * (1+r)^n / ((1+r)^n - 1)
            # Rearranging: n = log(1 + P*r/EMI) / log(1+r)
            if periodic_rate > 0:
                new_payments = math.log(1 + (new_principal * periodic_rate / original_emi)) / \
                              math.log(1 + periodic_rate)
                new_payments = int(math.ceil(new_payments))
            else:
                new_payments = int(new_principal / original_emi)
        else:
            # Flat rate: simple division
            total_interest = (new_principal * annual_rate) / 100.0
            total_payment = new_principal + total_interest
            new_payments = int(math.ceil(total_payment / original_emi))

        new_tenure_years = new_payments / periods_per_year
        new_total = original_emi * new_payments

        # Calculate original remaining payment
        original_remaining = original_emi * remaining_payments
        interest_saved = original_remaining - new_total - prepayment_amount

        return {
            "original_emi": original_emi,
            "outstanding_principal": outstanding,
            "new_principal": round(new_principal, 2),
            "new_emi": original_emi,
            "new_tenure_years": round(new_tenure_years, 2),
            "new_payments": new_payments,
            "interest_saved": round(max(0, interest_saved), 2),
            "new_total_payment": round(new_total, 2),
            "tenure_reduction_years": round((remaining_payments / periods_per_year) - new_tenure_years, 2)
        }


# --- Early Settlement Calculations ---
def calculate_early_settlement(
    principal: float,
    annual_rate: float,
    tenure_years: float,
    repayment_frequency: str,
    payments_made: int,
    interest_method: str = "reducing",
    prepayment_charges: float = 0.0
) -> Dict[str, Any]:
    """
    Calculate early settlement amount and savings.

    Args:
        principal (float): Original loan amount
        annual_rate (float): Annual interest rate (%)
        tenure_years (float): Original loan tenure in years
        repayment_frequency (str): "monthly", "quarterly", or "annually"
        payments_made (int): Number of payments already made
        interest_method (str): "reducing" or "flat"
        prepayment_charges (float): Prepayment charges (default: 0)

    Returns:
        dict: Contains:
            - outstanding_principal: Principal amount outstanding
            - settlement_amount: Total amount to pay for early settlement
            - interest_saved: Interest that would have been paid
            - total_savings: Total savings including interest and charges
    """
    from .schedule import get_outstanding_principal

    outstanding = get_outstanding_principal(
        principal, annual_rate, tenure_years, repayment_frequency,
        payments_made, interest_method
    )

    # Calculate original total payment
    if interest_method == "flat":
        _, total_interest, total_payment, total_payments = flat_rate(
            principal, annual_rate, tenure_years, repayment_frequency
        )
    else:
        _, total_interest, total_payment, total_payments = reducing_balance(
            principal, annual_rate, tenure_years, repayment_frequency
        )

    # Calculate amount already paid
    emi, _, _, _ = reducing_balance(principal, annual_rate, tenure_years, repayment_frequency) \
        if interest_method == "reducing" else flat_rate(principal, annual_rate, tenure_years, repayment_frequency)
    amount_paid = emi * payments_made

    # Remaining interest that would be paid
    remaining_payments = total_payments - payments_made
    remaining_interest = total_payment - amount_paid - outstanding

    settlement_amount = outstanding + prepayment_charges
    interest_saved = remaining_interest
    total_savings = interest_saved - prepayment_charges

    return {
        "outstanding_principal": round(outstanding, 2),
        "settlement_amount": round(settlement_amount, 2),
        "prepayment_charges": round(prepayment_charges, 2),
        "interest_saved": round(max(0, interest_saved), 2),
        "total_savings": round(max(0, total_savings), 2),
        "remaining_payments": remaining_payments
    }


# --- EMI Modification Scenarios ---
def modify_emi(
    principal: float,
    annual_rate: float,
    tenure_years: float,
    repayment_frequency: str,
    new_emi: float,
    interest_method: str = "reducing"
) -> Dict[str, Any]:
    """
    Calculate new tenure when EMI is modified.

    Args:
        principal (float): Loan amount
        annual_rate (float): Annual interest rate (%)
        tenure_years (float): Original tenure in years
        repayment_frequency (str): "monthly", "quarterly", or "annually"
        new_emi (float): New EMI amount
        interest_method (str): "reducing" or "flat"

    Returns:
        dict: Contains:
            - original_emi: Original EMI
            - new_emi: New EMI
            - original_tenure_years: Original tenure
            - new_tenure_years: New tenure
            - tenure_change_years: Change in tenure
    """
    # Get original EMI
    if interest_method == "flat":
        original_emi, _, _, _ = flat_rate(principal, annual_rate, tenure_years, repayment_frequency)
    else:
        original_emi, _, _, _ = reducing_balance(principal, annual_rate, tenure_years, repayment_frequency)

    periods_per_year = get_periods_per_year(repayment_frequency)
    periodic_rate = (annual_rate / 100.0) / periods_per_year

    if interest_method == "reducing":
        # Calculate new tenure: n = log(1 + P*r/EMI) / log(1+r)
        if periodic_rate > 0 and new_emi > principal * periodic_rate:
            new_payments = math.log(1 + (principal * periodic_rate / new_emi)) / math.log(1 + periodic_rate)
            new_payments = int(math.ceil(new_payments))
        else:
            raise ValueError("New EMI is too low. Cannot calculate tenure.")
    else:
        # Flat rate: simple calculation
        total_interest = (principal * annual_rate) / 100.0
        total_payment = principal + total_interest
        new_payments = int(math.ceil(total_payment / new_emi))

    new_tenure_years = new_payments / periods_per_year

    return {
        "original_emi": original_emi,
        "new_emi": new_emi,
        "original_tenure_years": tenure_years,
        "new_tenure_years": round(new_tenure_years, 2),
        "tenure_change_years": round(new_tenure_years - tenure_years, 2),
        "new_payments": new_payments
    }


def modify_tenure(
    principal: float,
    annual_rate: float,
    tenure_years: float,
    repayment_frequency: str,
    new_tenure_years: float,
    interest_method: str = "reducing"
) -> Dict[str, Any]:
    """
    Calculate new EMI when tenure is modified.

    Args:
        principal (float): Loan amount
        annual_rate (float): Annual interest rate (%)
        tenure_years (float): Original tenure in years
        repayment_frequency (str): "monthly", "quarterly", or "annually"
        new_tenure_years (float): New tenure in years
        interest_method (str): "reducing" or "flat"

    Returns:
        dict: Contains:
            - original_emi: Original EMI
            - new_emi: New EMI
            - original_tenure_years: Original tenure
            - new_tenure_years: New tenure
            - emi_change: Change in EMI
    """
    # Get original EMI
    if interest_method == "flat":
        original_emi, _, _, _ = flat_rate(principal, annual_rate, tenure_years, repayment_frequency)
    else:
        original_emi, _, _, _ = reducing_balance(principal, annual_rate, tenure_years, repayment_frequency)

    # Calculate new EMI
    if interest_method == "flat":
        new_emi, _, _, _ = flat_rate(principal, annual_rate, new_tenure_years, repayment_frequency)
    else:
        new_emi, _, _, _ = reducing_balance(principal, annual_rate, new_tenure_years, repayment_frequency)

    return {
        "original_emi": original_emi,
        "new_emi": new_emi,
        "original_tenure_years": tenure_years,
        "new_tenure_years": new_tenure_years,
        "emi_change": round(new_emi - original_emi, 2)
    }