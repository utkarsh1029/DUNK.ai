"""
Loan Clarity Tool Logic – DUNK.ai

This file contains the core calculation logic optimized for API consumption.
"""

import math
from typing import Dict, Any
from .validations import BaseLoanEngineSchema, AdvancedLoanEngineSchema


def get_periods_per_year(frequency: str) -> int:
    """Map repayment frequency string to periods per year."""
    freq_map = {"monthly": 12, "quarterly": 4, "annually": 1}
    if frequency not in freq_map:
        raise ValueError("Invalid repayment frequency. Use monthly/quarterly/annually.")
    return freq_map[frequency]


# --- Flat Rate Method ---
def flat_rate_from_schema(loan: BaseLoanEngineSchema) -> tuple:
    """Calculate loan details using Flat Rate interest method."""
    periods_per_year = get_periods_per_year(loan.repayment_frequency)
    number_of_payments = int(loan.tenure_years * periods_per_year)

    total_interest = (loan.loan_amount * loan.interest_rate * loan.tenure_years) / 100.0
    total_payment = loan.loan_amount + total_interest
    emi = total_payment / number_of_payments

    return round(emi, 2), round(total_interest, 2), round(total_payment, 2), number_of_payments


# --- Reducing Balance Method ---
def reducing_balance_from_schema(loan: BaseLoanEngineSchema) -> tuple:
    """Calculate loan details using Reducing Balance (EMI) interest method."""
    periods_per_year = get_periods_per_year(loan.repayment_frequency)
    number_of_payments = int(loan.tenure_years * periods_per_year)
    
    if number_of_payments <= 0:
        raise ValueError("Number of payments must be greater than 0.")

    periodic_rate = (loan.interest_rate / 100.0) / periods_per_year

    # Safe handle for 0% interest loans
    if periodic_rate == 0:
        emi = loan.loan_amount / number_of_payments
    else:
        # Standard Amortization Formula: P * r * (1+r)^n / ((1+r)^n - 1)
        emi = (loan.loan_amount * periodic_rate * (1 + periodic_rate) ** number_of_payments) / \
              ((1 + periodic_rate) ** number_of_payments - 1)

    total_payment = emi * number_of_payments
    total_interest = total_payment - loan.loan_amount

    return round(emi, 2), round(total_interest, 2), round(total_payment, 2), number_of_payments


# --- Prepayment Impact Calculations ---
def calculate_prepayment_impact(loan: AdvancedLoanEngineSchema, reduce_emi: bool = True) -> Dict[str, Any]:
    """Calculate the impact of a prepayment on a loan using clean business schemas."""
    
    # Core variables
    principal = loan.loan_amount
    annual_rate = loan.interest_rate
    tenure_years = loan.tenure_years
    repayment_frequency = loan.repayment_frequency
    interest_method = loan.interest_method
    payments_made = loan.payments_made
    prepayment_amount = loan.prepayment_amount

    # Get baseline original tracking
    if interest_method == "flat":
        original_emi, _, _, _ = flat_rate_from_schema(loan)
    else:
        original_emi, _, _, _ = reducing_balance_from_schema(loan)

    # Fetch outstanding balance from your schedule engine layout
    from .schedule import get_outstanding_principal
    outstanding = get_outstanding_principal(
        principal, annual_rate, tenure_years, repayment_frequency,
        payments_made, interest_method
    )

    new_principal = outstanding - prepayment_amount
    if new_principal <= 0:
        return {
            "original_emi": original_emi,
            "outstanding_principal": round(outstanding, 2),
            "new_principal": 0.0,
            "new_emi": 0.0,
            "new_tenure_years": 0.0,
            "interest_saved": round(max(0.0, outstanding - prepayment_amount), 2),
            "message": "Prepayment covers outstanding principal completely. Close loan container."
        }

    periods_per_year = get_periods_per_year(repayment_frequency)
    remaining_payments = int(tenure_years * periods_per_year) - payments_made

    if reduce_emi:
        remaining_tenure_years = remaining_payments / periods_per_year
        temp_schema = BaseLoanEngineSchema(
            loan_amount=new_principal,
            interest_rate=annual_rate,
            tenure_years=remaining_tenure_years,
            monthly_income=loan.monthly_income,
            repayment_frequency=repayment_frequency,
            interest_method=interest_method,
            loan_type=loan.loan_type
        )

        if interest_method == "flat":
            new_emi, _, new_total, _ = flat_rate_from_schema(temp_schema)
        else:
            new_emi, _, new_total, _ = reducing_balance_from_schema(temp_schema)

        original_remaining = original_emi * remaining_payments
        interest_saved = original_remaining - new_total - prepayment_amount

        return {
            "original_emi": original_emi,
            "outstanding_principal": round(outstanding, 2),
            "new_principal": round(new_principal, 2),
            "new_emi": new_emi,
            "new_tenure_years": round(remaining_tenure_years, 2),
            "interest_saved": round(max(0, interest_saved), 2),
            "emi_reduction": round(original_emi - new_emi, 2)
        }
    else:
        periodic_rate = (annual_rate / 100.0) / periods_per_year

        if interest_method == "reducing":
            if periodic_rate > 0:
                interest_ratio = (new_principal * periodic_rate) / original_emi
                if interest_ratio >= 1.0:
                    raise ValueError("EMI is too low to pay off interest accrued on new principal balance.")
                
                new_payments = -math.log(1 - interest_ratio) / math.log(1 + periodic_rate)
                new_payments = int(math.ceil(new_payments))
            else:
                new_payments = int(math.ceil(new_principal / original_emi))
        else:
            total_interest = (new_principal * annual_rate * (remaining_payments / periods_per_year)) / 100.0
            new_payments = int(math.ceil((new_principal + total_interest) / original_emi))

        new_tenure_years = new_payments / periods_per_year
        new_total = original_emi * new_payments
        original_remaining = original_emi * remaining_payments
        interest_saved = original_remaining - new_total - prepayment_amount

        return {
            "original_emi": original_emi,
            "outstanding_principal": round(outstanding, 2),
            "new_principal": round(new_principal, 2),
            "new_emi": original_emi,
            "new_tenure_years": round(new_tenure_years, 2),
            "interest_saved": round(max(0, interest_saved), 2),
            "tenure_reduction_years": round(max(0, (remaining_payments / periods_per_year) - new_tenure_years), 2)
        }


# --- EMI Modification Scenarios ---
def modify_emi(loan: BaseLoanEngineSchema, new_emi: float) -> Dict[str, Any]:
    """Calculate new tenure when EMI is modified (Amortization Bug Fixed)."""
    if loan.interest_method == "flat":
        original_emi, _, _, _ = flat_rate_from_schema(loan)
    else:
        original_emi, _, _, _ = reducing_balance_from_schema(loan)

    periods_per_year = get_periods_per_year(loan.repayment_frequency)
    periodic_rate = (loan.interest_rate / 100.0) / periods_per_year

    if loan.interest_method == "reducing":
        if periodic_rate > 0:
            interest_ratio = (loan.loan_amount * periodic_rate) / new_emi
            if interest_ratio >= 1.0:
                raise ValueError("New EMI is too low. It doesn't cover the minimum monthly interest accrued.")
            
            new_payments = -math.log(1 - interest_ratio) / math.log(1 + periodic_rate)
            new_payments = int(math.ceil(new_payments))
        else:
            new_payments = int(math.ceil(loan.loan_amount / new_emi))
    else:
        total_interest = (loan.loan_amount * loan.interest_rate * loan.tenure_years) / 100.0
        total_payment = loan.loan_amount + total_interest
        new_payments = int(math.ceil(total_payment / new_emi))

    new_tenure_years = new_payments / periods_per_year

    return {
        "original_emi": original_emi,
        "new_emi": new_emi,
        "original_tenure_years": loan.tenure_years,
        "new_tenure_years": round(new_tenure_years, 2),
        "tenure_change_years": round(new_tenure_years - loan.tenure_years, 2)
    }