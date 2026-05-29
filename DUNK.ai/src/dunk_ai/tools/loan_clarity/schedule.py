"""
Loan Clarity Tool – Amortization Schedule Generator

This module generates detailed amortization schedules showing:
- Period-by-period breakdown (payment number, opening balance, EMI, principal, interest, closing balance)
- Cumulative interest and principal paid
- Support for all repayment frequencies
- Date-based schedules with proper period calculations
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any
from .logic import reducing_balance, get_periods_per_year


def generate_amortization_schedule(
    principal: float,
    annual_rate: float,
    tenure_years: float,
    repayment_frequency: str,
    interest_method: str = "reducing",
    start_date: datetime = None
) -> List[Dict[str, Any]]:
    """
    Generate a complete amortization schedule for a loan.

    Args:
        principal (float): Loan amount
        annual_rate (float): Annual interest rate (%)
        tenure_years (float): Loan tenure in years
        repayment_frequency (str): "monthly", "quarterly", or "annually"
        interest_method (str): "reducing" or "flat" (default: "reducing")
        start_date (datetime): Start date of the loan (default: today)

    Returns:
        List[Dict]: List of dictionaries, each containing:
            - payment_number: Payment sequence number
            - payment_date: Date of payment
            - opening_balance: Principal balance at start of period
            - emi: EMI amount for this period
            - principal_paid: Principal portion of EMI
            - interest_paid: Interest portion of EMI
            - closing_balance: Principal balance at end of period
            - cumulative_principal: Total principal paid so far
            - cumulative_interest: Total interest paid so far
    """
    if start_date is None:
        start_date = datetime.now()

    periods_per_year = get_periods_per_year(repayment_frequency)
    number_of_payments = int(tenure_years * periods_per_year)

    # Calculate EMI
    if interest_method == "flat":
        from .logic import flat_rate
        emi, _, _, _ = flat_rate(principal, annual_rate, tenure_years, repayment_frequency)
    else:
        emi, _, _, _ = reducing_balance(principal, annual_rate, tenure_years, repayment_frequency)

    schedule = []
    current_balance = principal
    cumulative_principal = 0.0
    cumulative_interest = 0.0
    periodic_rate = (annual_rate / 100.0) / periods_per_year

    # Calculate date increment based on frequency
    if repayment_frequency == "monthly":
        date_increment = timedelta(days=30)  # Approximate month
    elif repayment_frequency == "quarterly":
        date_increment = timedelta(days=90)  # Approximate quarter
    else:  # annually
        date_increment = timedelta(days=365)  # Approximate year

    current_date = start_date

    for payment_num in range(1, number_of_payments + 1):
        opening_balance = round(current_balance, 2)

        if interest_method == "flat":
            # Flat rate: interest is constant, principal increases
            total_interest = (principal * annual_rate * tenure_years) / 100.0
            interest_paid = round(total_interest / number_of_payments, 2)
            principal_paid = round(emi - interest_paid, 2)
        else:
            # Reducing balance: interest decreases, principal increases
            interest_paid = round(current_balance * periodic_rate, 2)
            principal_paid = round(emi - interest_paid, 2)

        # Ensure principal doesn't exceed remaining balance
        if principal_paid > current_balance:
            principal_paid = round(current_balance, 2)
            interest_paid = round(emi - principal_paid, 2)
            emi_adjusted = round(principal_paid + interest_paid, 2)
        else:
            emi_adjusted = emi

        closing_balance = round(current_balance - principal_paid, 2)
        # Ensure closing balance doesn't go negative
        if closing_balance < 0:
            closing_balance = 0.0
            principal_paid = round(current_balance, 2)
            emi_adjusted = round(principal_paid + interest_paid, 2)

        cumulative_principal += principal_paid
        cumulative_interest += interest_paid

        schedule.append({
            "payment_number": payment_num,
            "payment_date": current_date.strftime("%Y-%m-%d"),
            "opening_balance": opening_balance,
            "emi": round(emi_adjusted, 2),
            "principal_paid": principal_paid,
            "interest_paid": interest_paid,
            "closing_balance": closing_balance,
            "cumulative_principal": round(cumulative_principal, 2),
            "cumulative_interest": round(cumulative_interest, 2)
        })

        current_balance = closing_balance
        current_date += date_increment

        # Break if loan is fully paid
        if closing_balance <= 0:
            break

    return schedule


def get_outstanding_principal(
    principal: float,
    annual_rate: float,
    tenure_years: float,
    repayment_frequency: str,
    payments_made: int,
    interest_method: str = "reducing"
) -> float:
    """
    Calculate outstanding principal after a certain number of payments.

    Args:
        principal (float): Original loan amount
        annual_rate (float): Annual interest rate (%)
        tenure_years (float): Loan tenure in years
        repayment_frequency (str): "monthly", "quarterly", or "annually"
        payments_made (int): Number of payments already made
        interest_method (str): "reducing" or "flat"

    Returns:
        float: Outstanding principal amount
    """
    if payments_made <= 0:
        return principal

    periods_per_year = get_periods_per_year(repayment_frequency)
    total_payments = int(tenure_years * periods_per_year)

    if payments_made >= total_payments:
        return 0.0

    if interest_method == "reducing":
        periodic_rate = (annual_rate / 100.0) / periods_per_year
        emi, _, _, _ = reducing_balance(principal, annual_rate, tenure_years, repayment_frequency)

        # Outstanding principal formula: P * ((1+r)^n - (1+r)^p) / ((1+r)^n - 1)
        # where n = total payments, p = payments made
        outstanding = principal * (
            ((1 + periodic_rate) ** total_payments - (1 + periodic_rate) ** payments_made) /
            ((1 + periodic_rate) ** total_payments - 1)
        )
        return round(outstanding, 2)
    else:
        # Flat rate: simple calculation
        from .logic import flat_rate
        emi, total_interest, total_payment, _ = flat_rate(
            principal, annual_rate, tenure_years, repayment_frequency
        )
        total_paid = emi * payments_made
        outstanding = total_payment - total_paid
        return round(max(0, outstanding), 2)


def get_year_wise_summary(
    schedule: List[Dict[str, Any]]
) -> List[Dict[str, Any]]:
    """
    Generate year-wise summary from amortization schedule.

    Args:
        schedule (List[Dict]): Complete amortization schedule

    Returns:
        List[Dict]: Year-wise summary with:
            - year: Year number
            - total_principal: Principal paid in this year
            - total_interest: Interest paid in this year
            - total_payment: Total payment in this year
            - closing_balance: Balance at end of year
    """
    year_wise = {}
    current_year = None

    for entry in schedule:
        payment_date = datetime.strptime(entry["payment_date"], "%Y-%m-%d")
        year = payment_date.year

        if year not in year_wise:
            year_wise[year] = {
                "year": year,
                "total_principal": 0.0,
                "total_interest": 0.0,
                "total_payment": 0.0,
                "closing_balance": entry["closing_balance"]
            }

        year_wise[year]["total_principal"] += entry["principal_paid"]
        year_wise[year]["total_interest"] += entry["interest_paid"]
        year_wise[year]["total_payment"] += entry["emi"]
        year_wise[year]["closing_balance"] = entry["closing_balance"]

    # Round values
    for year_data in year_wise.values():
        year_data["total_principal"] = round(year_data["total_principal"], 2)
        year_data["total_interest"] = round(year_data["total_interest"], 2)
        year_data["total_payment"] = round(year_data["total_payment"], 2)
        year_data["closing_balance"] = round(year_data["closing_balance"], 2)

    return sorted(year_wise.values(), key=lambda x: x["year"])


