"""
Loan Clarity Tool Logic – DUNK.ai

This file contains the core calculation logic for:
1. Flat Rate Method
2. Reducing Balance Method
+ Helper functions
"""

# --- Helpers ---
def get_periods_per_year(frequency: str) -> int:
    """
    Map repayment frequency string to periods per year.
    """
    freq_map = {"monthly": 12, "quarterly": 4, "annually": 1}
    if frequency not in freq_map:
        raise ValueError("Invalid repayment frequency. Use monthly/quarterly/annually.")
    return freq_map[frequency]


# --- Flat Rate Method ---
def flat_rate(principal, annual_rate, tenure_years, repayment_frequency):
    periods_per_year = get_periods_per_year(repayment_frequency)
    number_of_payments = int(tenure_years * periods_per_year)

    total_interest = (principal * annual_rate * tenure_years) / 100.0
    total_payment = principal + total_interest
    emi = total_payment / number_of_payments

    return round(emi, 2), round(total_interest, 2), round(total_payment, 2), number_of_payments


# --- Reducing Balance Method ---
def reducing_balance(principal, annual_rate, tenure_years, repayment_frequency):
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