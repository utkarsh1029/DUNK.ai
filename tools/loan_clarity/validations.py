"""
Loan Clarity Tool – Validations

This file contains input validation utilities to ensure
safe and correct values before calculations.
"""

def validate_principal(principal: float):
    """
    Validate principal amount.

    Args:
        principal (float): Loan principal amount

    Returns:
        float: Validated principal

    Raises:
        ValueError: If principal is invalid
    """
    if principal <= 0:
        raise ValueError("Principal must be greater than 0.")
    if principal > 100000000000:  # ₹1 lakh crore limit
        raise ValueError("Principal amount is too large.")
    return principal


def validate_interest_rate(annual_rate: float):
    """
    Validate interest rate.

    Args:
        annual_rate (float): Annual interest rate percentage

    Returns:
        float: Validated interest rate

    Raises:
        ValueError: If interest rate is invalid
    """
    if annual_rate < 0:
        raise ValueError("Interest rate cannot be negative.")
    if annual_rate > 100:  # 100% limit
        raise ValueError("Interest rate seems unreasonably high.")
    return annual_rate


def validate_tenure(tenure_years: float):
    """
    Validate loan tenure.

    Args:
        tenure_years (float): Loan tenure in years

    Returns:
        float: Validated tenure

    Raises:
        ValueError: If tenure is invalid
    """
    if tenure_years <= 0:
        raise ValueError("Loan tenure must be greater than 0.")
    if tenure_years > 50:  # 50 years limit
        raise ValueError("Loan tenure cannot exceed 50 years.")
    return tenure_years


def validate_repayment_frequency(frequency: str):
    """
    Validate repayment frequency.

    Args:
        frequency (str): Repayment frequency string

    Returns:
        str: Validated frequency

    Raises:
        ValueError: If frequency is invalid
    """
    valid_frequencies = ["monthly", "quarterly", "annually"]
    if frequency not in valid_frequencies:
        raise ValueError(f"Invalid repayment frequency. Must be one of: {valid_frequencies}")
    return frequency


def validate_interest_method(method: str):
    """
    Validate interest calculation method.

    Args:
        method (str): Interest method string

    Returns:
        str: Validated method

    Raises:
        ValueError: If method is invalid
    """
    valid_methods = ["reducing", "flat"]
    if method not in valid_methods:
        raise ValueError(f"Invalid interest method. Must be one of: {valid_methods}")
    return method


def validate_payments_made(payments_made: int, total_payments: int):
    """
    Validate number of payments made.

    Args:
        payments_made (int): Number of payments already made
        total_payments (int): Total number of payments

    Returns:
        int: Validated payments made

    Raises:
        ValueError: If payments_made is invalid
    """
    if payments_made < 0:
        raise ValueError("Payments made cannot be negative.")
    if payments_made > total_payments:
        raise ValueError("Payments made cannot exceed total payments.")
    return payments_made


def validate_prepayment_amount(prepayment_amount: float, outstanding_principal: float):
    """
    Validate prepayment amount.

    Args:
        prepayment_amount (float): Prepayment amount
        outstanding_principal (float): Outstanding principal

    Returns:
        float: Validated prepayment amount

    Raises:
        ValueError: If prepayment amount is invalid
    """
    if prepayment_amount < 0:
        raise ValueError("Prepayment amount cannot be negative.")
    if prepayment_amount > outstanding_principal * 1.1:  # Allow 10% buffer for charges
        raise ValueError("Prepayment amount exceeds outstanding principal significantly.")
    return prepayment_amount


def validate_income(income: float):
    """
    Validate income amount.

    Args:
        income (float): Monthly or annual income

    Returns:
        float: Validated income

    Raises:
        ValueError: If income is invalid
    """
    if income <= 0:
        raise ValueError("Income must be greater than 0.")
    return income


def validate_tax_slab(tax_slab: float):
    """
    Validate tax slab percentage.

    Args:
        tax_slab (float): Tax slab percentage

    Returns:
        float: Validated tax slab

    Raises:
        ValueError: If tax slab is invalid
    """
    valid_slabs = [5.0, 10.0, 20.0, 30.0]
    if tax_slab not in valid_slabs:
        raise ValueError(f"Invalid tax slab. Must be one of: {valid_slabs}")
    return tax_slab


def validate_loan_type(loan_type: str):
    """
    Validate loan type.

    Args:
        loan_type (str): Loan type string

    Returns:
        str: Validated loan type

    Raises:
        ValueError: If loan type is invalid
    """
    valid_types = ["home_loan", "personal_loan", "vehicle_loan", "education_loan"]
    if loan_type not in valid_types:
        raise ValueError(f"Invalid loan type. Must be one of: {valid_types}")
    return loan_type