"""
Unit tests for Loan Clarity Tool
"""

import pytest
from tools.loan_clarity.logic import flat_rate, reducing_balance


def test_flat_rate_monthly():
    emi, total_interest, total_payment, num_pay = flat_rate(
        principal=100000,       # ₹1,00,000 loan
        annual_rate=10,         # 10% interest
        tenure_years=1,         # 1 year
        repayment_frequency="monthly"
    )
    assert num_pay == 12
    assert round(total_payment, 2) == 110000.00
    assert round(total_interest, 2) == 10000.00
    assert round(emi, 2) == 9166.67


def test_flat_rate_quarterly():
    emi, total_interest, total_payment, num_pay = flat_rate(
        100000, 12, 2, "quarterly"
    )
    assert num_pay == 8
    assert round(total_payment, 2) == 124000.00
    assert round(total_interest, 2) == 24000.00
    assert round(emi, 2) == 15500.00


def test_reducing_balance_monthly():
    emi, total_interest, total_payment, num_pay = reducing_balance(
        principal=100000,
        annual_rate=12,
        tenure_years=1,
        repayment_frequency="monthly"
    )
    assert num_pay == 12
    assert round(emi, 2) == 8884.88   # Standard reducing balance EMI
    assert round(total_payment, 2) == pytest.approx(106618.56, rel=1e-2)
    assert round(total_interest, 2) == pytest.approx(6618.56, rel=1e-2)


def test_reducing_balance_annually():
    emi, total_interest, total_payment, num_pay = reducing_balance(
        50000, 10, 2, "annually"
    )
    assert num_pay == 2
    assert round(emi, 2) == pytest.approx(28830.13, rel=1e-2)
    assert round(total_payment, 2) == pytest.approx(57660.26, rel=1e-2)
    assert round(total_interest, 2) == pytest.approx(7660.26, rel=1e-2)