"""
Comprehensive Unit Tests for Loan Clarity Tool

Tests cover:
- Basic EMI calculations (flat rate and reducing balance)
- Amortization schedule generation
- Prepayment impact calculations
- Early settlement calculations
- EMI and tenure modifications
- Loan comparison
- Tax benefits (India-specific)
- Loan eligibility
- Effective interest rate
"""

import pytest
from datetime import datetime
from dunk_ai.tools.loan_clarity.logic import (
    flat_rate,
    reducing_balance,
    calculate_prepayment_impact,
    calculate_early_settlement,
    modify_emi,
    modify_tenure
)
from dunk_ai.tools.loan_clarity.schedule import (
    generate_amortization_schedule,
    get_outstanding_principal,
    get_year_wise_summary
)
from dunk_ai.tools.loan_clarity.comparison import compare_loans, break_even_analysis
from dunk_ai.tools.loan_clarity.tax_benefits import calculate_tax_benefits, calculate_lifetime_tax_benefits
from dunk_ai.tools.loan_clarity.eligibility import calculate_loan_eligibility, calculate_affordability
from dunk_ai.tools.loan_clarity.effective_rate import calculate_effective_rate, calculate_apr


# ========== Basic EMI Calculation Tests ==========

def test_flat_rate_monthly():
    """Test flat rate calculation for monthly payments"""
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
    """Test flat rate calculation for quarterly payments"""
    emi, total_interest, total_payment, num_pay = flat_rate(
        100000, 12, 2, "quarterly"
    )
    assert num_pay == 8
    assert round(total_payment, 2) == 124000.00
    assert round(total_interest, 2) == 24000.00
    assert round(emi, 2) == 15500.00


def test_reducing_balance_monthly():
    """Test reducing balance calculation for monthly payments"""
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
    """Test reducing balance calculation for annual payments"""
    emi, total_interest, total_payment, num_pay = reducing_balance(
        50000, 10, 2, "annually"
    )
    assert num_pay == 2
    assert round(emi, 2) == pytest.approx(28830.13, rel=1e-2)
    assert round(total_payment, 2) == pytest.approx(57660.26, rel=1e-2)
    assert round(total_interest, 2) == pytest.approx(7660.26, rel=1e-2)


# ========== Amortization Schedule Tests ==========

def test_generate_amortization_schedule():
    """Test amortization schedule generation"""
    schedule = generate_amortization_schedule(
        principal=100000,
        annual_rate=12,
        tenure_years=1,
        repayment_frequency="monthly",
        interest_method="reducing"
    )
    
    assert len(schedule) == 12
    assert schedule[0]["payment_number"] == 1
    assert schedule[0]["opening_balance"] == 100000.0
    assert schedule[-1]["closing_balance"] == pytest.approx(0, abs=1)
    assert schedule[-1]["cumulative_principal"] == pytest.approx(100000, rel=1e-1)


def test_get_outstanding_principal():
    """Test outstanding principal calculation"""
    outstanding = get_outstanding_principal(
        principal=100000,
        annual_rate=12,
        tenure_years=1,
        repayment_frequency="monthly",
        payments_made=6,
        interest_method="reducing"
    )
    
    assert outstanding > 0
    assert outstanding < 100000
    assert outstanding == pytest.approx(50000, rel=0.5)  # Should be around 50% after 6 months


# ========== Prepayment Impact Tests ==========

def test_prepayment_impact_reduce_emi():
    """Test prepayment impact with EMI reduction"""
    result = calculate_prepayment_impact(
        principal=1000000,
        annual_rate=10,
        tenure_years=20,
        repayment_frequency="monthly",
        payments_made=24,
        prepayment_amount=100000,
        interest_method="reducing",
        reduce_emi=True
    )
    
    assert "new_emi" in result
    assert result["new_emi"] < result["original_emi"]
    assert result["interest_saved"] > 0


def test_prepayment_impact_reduce_tenure():
    """Test prepayment impact with tenure reduction"""
    result = calculate_prepayment_impact(
        principal=1000000,
        annual_rate=10,
        tenure_years=20,
        repayment_frequency="monthly",
        payments_made=24,
        prepayment_amount=100000,
        interest_method="reducing",
        reduce_emi=False
    )
    
    assert "new_tenure_years" in result
    assert result["new_tenure_years"] < 20
    assert result["interest_saved"] > 0


# ========== Early Settlement Tests ==========

def test_early_settlement():
    """Test early settlement calculation"""
    result = calculate_early_settlement(
        principal=1000000,
        annual_rate=10,
        tenure_years=20,
        repayment_frequency="monthly",
        payments_made=60,
        interest_method="reducing",
        prepayment_charges=5000
    )
    
    assert "outstanding_principal" in result
    assert "settlement_amount" in result
    assert "interest_saved" in result
    assert result["settlement_amount"] > result["outstanding_principal"]


# ========== EMI Modification Tests ==========

def test_modify_emi():
    """Test EMI modification (calculate new tenure)"""
    result = modify_emi(
        principal=1000000,
        annual_rate=10,
        tenure_years=20,
        repayment_frequency="monthly",
        new_emi=15000,
        interest_method="reducing"
    )
    
    assert "new_tenure_years" in result
    assert result["new_tenure_years"] < 20  # Higher EMI should reduce tenure


def test_modify_tenure():
    """Test tenure modification (calculate new EMI)"""
    result = modify_tenure(
        principal=1000000,
        annual_rate=10,
        tenure_years=20,
        repayment_frequency="monthly",
        new_tenure_years=15,
        interest_method="reducing"
    )
    
    assert "new_emi" in result
    assert result["new_emi"] > result["original_emi"]  # Shorter tenure should increase EMI


# ========== Loan Comparison Tests ==========

def test_compare_loans():
    """Test loan comparison"""
    loan_options = [
        {
            "principal": 1000000,
            "annual_rate": 10,
            "tenure_years": 20,
            "repayment_frequency": "monthly",
            "interest_method": "reducing",
            "processing_fee": 10000,
            "loan_name": "Bank A"
        },
        {
            "principal": 1000000,
            "annual_rate": 9.5,
            "tenure_years": 20,
            "repayment_frequency": "monthly",
            "interest_method": "reducing",
            "processing_fee": 15000,
            "loan_name": "Bank B"
        }
    ]
    
    result = compare_loans(loan_options)
    
    assert "comparisons" in result
    assert "best_option" in result
    assert len(result["comparisons"]) == 2
    assert result["best_option"]["index"] >= 0


# ========== Tax Benefits Tests ==========

def test_calculate_tax_benefits():
    """Test tax benefits calculation for home loan"""
    result = calculate_tax_benefits(
        principal=5000000,
        annual_rate=8.5,
        tenure_years=20,
        repayment_frequency="monthly",
        loan_type="home_loan",
        interest_method="reducing",
        tax_slab=30.0,
        is_first_time_buyer=False,
        is_self_occupied=True
    )
    
    assert "section_24_deduction" in result
    assert "section_80c_deduction" in result
    assert "tax_savings" in result
    assert result["tax_savings"] > 0


def test_tax_benefits_first_time_buyer():
    """Test tax benefits for first-time home buyer"""
    result = calculate_tax_benefits(
        principal=3500000,
        annual_rate=8.5,
        tenure_years=20,
        repayment_frequency="monthly",
        loan_type="home_loan",
        interest_method="reducing",
        tax_slab=30.0,
        is_first_time_buyer=True,
        is_self_occupied=True
    )
    
    assert "section_80eea_deduction" in result
    assert result["section_80eea_deduction"] >= 0


# ========== Loan Eligibility Tests ==========

def test_calculate_loan_eligibility():
    """Test loan eligibility calculation"""
    result = calculate_loan_eligibility(
        monthly_income=100000,
        annual_rate=10,
        tenure_years=20,
        repayment_frequency="monthly",
        interest_method="reducing",
        existing_emis=20000,
        emi_to_income_ratio=0.4
    )
    
    assert "maximum_loan_amount" in result
    assert "available_emi" in result
    assert result["maximum_loan_amount"] > 0
    assert result["available_emi"] == 20000  # 40% of 100000 - 20000 existing


def test_calculate_affordability():
    """Test affordability check"""
    result = calculate_affordability(
        desired_loan_amount=5000000,
        monthly_income=200000,
        annual_rate=10,
        tenure_years=20,
        repayment_frequency="monthly",
        interest_method="reducing",
        existing_emis=30000,
        emi_to_income_ratio=0.4
    )
    
    assert "is_affordable" in result
    assert "required_emi" in result
    assert isinstance(result["is_affordable"], bool)


# ========== Effective Rate Tests ==========

def test_calculate_effective_rate():
    """Test effective interest rate calculation"""
    effective_rate = calculate_effective_rate(
        principal=1000000,
        annual_rate=10,
        tenure_years=20,
        repayment_frequency="monthly",
        processing_fee=10000,
        other_charges=5000,
        interest_method="reducing"
    )
    
    assert effective_rate > 10  # Should be higher than nominal rate due to charges
    assert effective_rate < 15  # Should be reasonable


def test_calculate_apr():
    """Test APR calculation"""
    result = calculate_apr(
        principal=1000000,
        annual_rate=10,
        tenure_years=20,
        repayment_frequency="monthly",
        processing_fee=10000,
        other_charges=5000,
        interest_method="reducing"
    )
    
    assert "effective_rate" in result
    assert "apr" in result
    assert result["apr"] > result["nominal_rate"]


# ========== Edge Cases and Error Handling ==========

def test_zero_principal_error():
    """Test that zero principal raises error"""
    with pytest.raises(ValueError):
        flat_rate(0, 10, 1, "monthly")


def test_negative_interest_rate_error():
    """Test that negative interest rate raises error"""
    with pytest.raises(ValueError):
        reducing_balance(100000, -5, 1, "monthly")


def test_invalid_frequency_error():
    """Test that invalid frequency raises error"""
    with pytest.raises(ValueError):
        flat_rate(100000, 10, 1, "weekly")


def test_prepayment_exceeds_outstanding():
    """Test prepayment that exceeds outstanding principal"""
    result = calculate_prepayment_impact(
        principal=100000,
        annual_rate=10,
        tenure_years=1,
        repayment_frequency="monthly",
        payments_made=0,
        prepayment_amount=200000,
        interest_method="reducing",
        reduce_emi=True
    )
    
    assert "message" in result
    assert result["new_principal"] == 0.0
