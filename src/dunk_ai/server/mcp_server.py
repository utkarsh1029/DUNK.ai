"""
MCP Server – DUNK.ai

This server registers available tools for Loan Clarity module
so that an LLM can call them through the MCP protocol.

Available Tools:
1. loan_clarity - Basic EMI calculation
2. generate_amortization_schedule - Detailed repayment schedule
3. calculate_prepayment_impact - Prepayment analysis
4. calculate_early_settlement - Early settlement calculator
5. modify_emi - Calculate new tenure for modified EMI
6. modify_tenure - Calculate new EMI for modified tenure
7. compare_loans - Compare multiple loan options
8. calculate_tax_benefits - Tax benefits calculator (India)
9. calculate_loan_eligibility - Loan eligibility calculator
10. calculate_effective_rate - Effective interest rate calculator
11. investment_get_stock_price - Live stock snapshot
12. investment_get_stock_analytics - Technical analytics + forecast
13. investment_get_mutual_fund_nav - Mutual fund NAV lookup
14. investment_portfolio_summary - Placeholder holdings summary
15. investment_ai_insight - LLM-generated market insight
16. expense_generate_plan - Personalized budgeting allocations
"""

import asyncio
from datetime import datetime
from typing import Any, Dict, List

from mcp.server.fastmcp import FastMCP

from dunk_ai.services.expense_manager import ExpensePlanner
from dunk_ai.services.investment_ai import InvestmentAI
from dunk_ai.tools.investment_navigator.investment import InvestmentNavigator
from dunk_ai.tools.loan_clarity import (
    flat_rate,
    reducing_balance,
    generate_amortization_schedule,
    calculate_prepayment_impact,
    calculate_early_settlement,
    modify_emi,
    modify_tenure,
    compare_loans,
    calculate_tax_benefits,
    calculate_loan_eligibility,
    calculate_effective_rate,
    calculate_affordability,
)

# Initialize MCP server
mcp = FastMCP("dunk-mcp-server")
navigator = InvestmentNavigator()
expense_planner = ExpensePlanner()
investment_ai = InvestmentAI()


# 1. Basic Loan Clarity Tool
@mcp.tool()
async def loan_clarity(
    principal: float,
    annual_rate: float,
    tenure_years: float,
    repayment_frequency: str,
    interest_method: str
) -> dict:
    """
    Loan Clarity Tool – calculates EMI, interest, and repayment schedule.

    Args:
        principal (float): Loan amount
        annual_rate (float): Annual interest rate (%)
        tenure_years (float): Loan tenure in years
        repayment_frequency (str): "monthly", "quarterly", or "annually"
        interest_method (str): "reducing" or "flat"

    Returns:
        dict: EMI, total interest, total repayment, and number of payments
    """
    if interest_method == "flat":
        emi, total_interest, total_payment, num_pay = flat_rate(
            principal, annual_rate, tenure_years, repayment_frequency
        )
    else:
        emi, total_interest, total_payment, num_pay = reducing_balance(
            principal, annual_rate, tenure_years, repayment_frequency
        )

    return {
        "emi": emi,
        "total_interest": total_interest,
        "total_payment": total_payment,
        "number_of_payments": num_pay,
        "repayment_frequency": repayment_frequency
    }


# 2. Amortization Schedule Generator
@mcp.tool()
async def generate_amortization_schedule_tool(
    principal: float,
    annual_rate: float,
    tenure_years: float,
    repayment_frequency: str,
    interest_method: str = "reducing",
    start_date: str = None
) -> dict:
    """
    Generate detailed amortization schedule for a loan.

    Args:
        principal (float): Loan amount
        annual_rate (float): Annual interest rate (%)
        tenure_years (float): Loan tenure in years
        repayment_frequency (str): "monthly", "quarterly", or "annually"
        interest_method (str): "reducing" or "flat" (default: "reducing")
        start_date (str): Start date in YYYY-MM-DD format (default: today)

    Returns:
        dict: Complete amortization schedule with period-by-period breakdown
    """
    start_dt = None
    if start_date:
        start_dt = datetime.strptime(start_date, "%Y-%m-%d")

    schedule = generate_amortization_schedule(
        principal, annual_rate, tenure_years, repayment_frequency,
        interest_method, start_dt
    )

    return {
        "schedule": schedule,
        "total_payments": len(schedule),
        "summary": {
            "total_principal": schedule[-1]["cumulative_principal"] if schedule else 0,
            "total_interest": schedule[-1]["cumulative_interest"] if schedule else 0,
            "total_payment": schedule[-1]["cumulative_principal"] + schedule[-1]["cumulative_interest"] if schedule else 0
        }
    }


# 3. Prepayment Impact Calculator
@mcp.tool()
async def calculate_prepayment_impact_tool(
    principal: float,
    annual_rate: float,
    tenure_years: float,
    repayment_frequency: str,
    payments_made: int,
    prepayment_amount: float,
    interest_method: str = "reducing",
    reduce_emi: bool = True
) -> dict:
    """
    Calculate the impact of a prepayment on loan (reduce EMI or reduce tenure).

    Args:
        principal (float): Original loan amount
        annual_rate (float): Annual interest rate (%)
        tenure_years (float): Original loan tenure in years
        repayment_frequency (str): "monthly", "quarterly", or "annually"
        payments_made (int): Number of payments already made
        prepayment_amount (float): Amount to prepay
        interest_method (str): "reducing" or "flat" (default: "reducing")
        reduce_emi (bool): If True, reduce EMI; if False, reduce tenure (default: True)

    Returns:
        dict: Prepayment impact analysis
    """
    return calculate_prepayment_impact(
        principal, annual_rate, tenure_years, repayment_frequency,
        payments_made, prepayment_amount, interest_method, reduce_emi
    )


# 4. Early Settlement Calculator
@mcp.tool()
async def calculate_early_settlement_tool(
    principal: float,
    annual_rate: float,
    tenure_years: float,
    repayment_frequency: str,
    payments_made: int,
    interest_method: str = "reducing",
    prepayment_charges: float = 0.0
) -> dict:
    """
    Calculate early settlement amount and savings.

    Args:
        principal (float): Original loan amount
        annual_rate (float): Annual interest rate (%)
        tenure_years (float): Original loan tenure in years
        repayment_frequency (str): "monthly", "quarterly", or "annually"
        payments_made (int): Number of payments already made
        interest_method (str): "reducing" or "flat" (default: "reducing")
        prepayment_charges (float): Prepayment charges (default: 0)

    Returns:
        dict: Early settlement analysis with savings
    """
    return calculate_early_settlement(
        principal, annual_rate, tenure_years, repayment_frequency,
        payments_made, interest_method, prepayment_charges
    )


# 5. Modify EMI Tool
@mcp.tool()
async def modify_emi_tool(
    principal: float,
    annual_rate: float,
    tenure_years: float,
    repayment_frequency: str,
    new_emi: float,
    interest_method: str = "reducing"
) -> dict:
    """
    Calculate new tenure when EMI is modified.

    Args:
        principal (float): Loan amount
        annual_rate (float): Annual interest rate (%)
        tenure_years (float): Original tenure in years
        repayment_frequency (str): "monthly", "quarterly", or "annually"
        new_emi (float): New EMI amount
        interest_method (str): "reducing" or "flat" (default: "reducing")

    Returns:
        dict: New tenure and change analysis
    """
    return modify_emi(
        principal, annual_rate, tenure_years, repayment_frequency,
        new_emi, interest_method
    )


# 6. Modify Tenure Tool
@mcp.tool()
async def modify_tenure_tool(
    principal: float,
    annual_rate: float,
    tenure_years: float,
    repayment_frequency: str,
    new_tenure_years: float,
    interest_method: str = "reducing"
) -> dict:
    """
    Calculate new EMI when tenure is modified.

    Args:
        principal (float): Loan amount
        annual_rate (float): Annual interest rate (%)
        tenure_years (float): Original tenure in years
        repayment_frequency (str): "monthly", "quarterly", or "annually"
        new_tenure_years (float): New tenure in years
        interest_method (str): "reducing" or "flat" (default: "reducing")

    Returns:
        dict: New EMI and change analysis
    """
    return modify_tenure(
        principal, annual_rate, tenure_years, repayment_frequency,
        new_tenure_years, interest_method
    )


# 7. Compare Loans Tool
@mcp.tool()
async def compare_loans_tool(
    loan_options: List[Dict[str, Any]]
) -> dict:
    """
    Compare multiple loan options and recommend the best one.

    Args:
        loan_options (List[Dict]): List of loan options, each containing:
            - principal (float): Loan amount
            - annual_rate (float): Annual interest rate (%)
            - tenure_years (float): Loan tenure in years
            - repayment_frequency (str): "monthly", "quarterly", or "annually"
            - interest_method (str): "reducing" or "flat"
            - processing_fee (float, optional): Processing fee
            - other_charges (float, optional): Other charges
            - loan_name (str, optional): Name/identifier for the loan

    Returns:
        dict: Detailed comparison and best option recommendation
    """
    return compare_loans(loan_options)


# 8. Tax Benefits Calculator
@mcp.tool()
async def calculate_tax_benefits_tool(
    principal: float,
    annual_rate: float,
    tenure_years: float,
    repayment_frequency: str,
    loan_type: str = "home_loan",
    interest_method: str = "reducing",
    tax_slab: float = 30.0,
    is_first_time_buyer: bool = False,
    is_self_occupied: bool = True
) -> dict:
    """
    Calculate tax benefits for a loan (India-specific).

    Args:
        principal (float): Loan amount
        annual_rate (float): Annual interest rate (%)
        tenure_years (float): Loan tenure in years
        repayment_frequency (str): "monthly", "quarterly", or "annually"
        loan_type (str): "home_loan", "vehicle_loan", or "personal_loan" (default: "home_loan")
        interest_method (str): "reducing" or "flat" (default: "reducing")
        tax_slab (float): Income tax slab percentage 5, 10, 20, or 30 (default: 30)
        is_first_time_buyer (bool): Whether first-time home buyer (default: False)
        is_self_occupied (bool): Whether property is self-occupied (default: True)

    Returns:
        dict: Tax benefits analysis including deductions and savings
    """
    return calculate_tax_benefits(
        principal, annual_rate, tenure_years, repayment_frequency,
        loan_type, interest_method, tax_slab, is_first_time_buyer, is_self_occupied
    )


# 9. Loan Eligibility Calculator
@mcp.tool()
async def calculate_loan_eligibility_tool(
    monthly_income: float,
    annual_rate: float,
    tenure_years: float,
    repayment_frequency: str = "monthly",
    interest_method: str = "reducing",
    existing_emis: float = 0.0,
    emi_to_income_ratio: float = 0.4,
    age: int = None
) -> dict:
    """
    Calculate maximum loan eligibility based on income.

    Args:
        monthly_income (float): Monthly net income
        annual_rate (float): Annual interest rate (%)
        tenure_years (float): Desired loan tenure in years
        repayment_frequency (str): "monthly", "quarterly", or "annually" (default: "monthly")
        interest_method (str): "reducing" or "flat" (default: "reducing")
        existing_emis (float): Existing EMI obligations (default: 0)
        emi_to_income_ratio (float): Maximum EMI to income ratio (default: 0.4 = 40%)
        age (int, optional): Current age (for tenure adjustment)

    Returns:
        dict: Maximum loan eligibility and affordability analysis
    """
    return calculate_loan_eligibility(
        monthly_income, annual_rate, tenure_years, repayment_frequency,
        interest_method, existing_emis, emi_to_income_ratio, age
    )


# 10. Effective Interest Rate Calculator
@mcp.tool()
async def calculate_effective_rate_tool(
    principal: float,
    annual_rate: float,
    tenure_years: float,
    repayment_frequency: str = "monthly",
    processing_fee: float = 0.0,
    other_charges: float = 0.0,
    interest_method: str = "reducing"
) -> dict:
    """
    Calculate effective interest rate including all charges.

    Args:
        principal (float): Loan amount
        annual_rate (float): Annual interest rate (%)
        tenure_years (float): Loan tenure in years
        repayment_frequency (str): "monthly", "quarterly", or "annually" (default: "monthly")
        processing_fee (float): Processing fee amount (default: 0)
        other_charges (float): Other charges (default: 0)
        interest_method (str): "reducing" or "flat" (default: "reducing")

    Returns:
        dict: Effective interest rate and APR details
    """
    from dunk_ai.tools.loan_clarity.effective_rate import calculate_apr
    return calculate_apr(
        principal, annual_rate, tenure_years, repayment_frequency,
        processing_fee, other_charges, interest_method
    )


# 11. Investment Navigator – Live Price
@mcp.tool()
async def investment_get_stock_price(query: str) -> Dict[str, Any]:
    """
    Get the latest stock price snapshot using Investment Navigator.
    """
    return navigator.get_stock_price(query)


# 12. Investment Navigator – Analytics
@mcp.tool()
async def investment_get_stock_analytics(ticker: str) -> Dict[str, Any]:
    """
    Fetch full stock analytics (RSI, volatility, forecast, etc.).
    """
    return navigator.get_stock_analytics(ticker)


# 13. Investment Navigator – Mutual Fund NAV
@mcp.tool()
async def investment_get_mutual_fund_nav(scheme_name: str) -> Dict[str, Any]:
    """
    Fetch the latest NAV for a given mutual fund scheme.
    """
    return navigator.get_mutual_fund_nav(scheme_name)


# 14. Investment Navigator – Portfolio Summary
@mcp.tool()
async def investment_portfolio_summary(user_id: str) -> Dict[str, Any]:
    """
    Return a placeholder portfolio summary for future DB integration.
    """
    return navigator.portfolio_summary(user_id)


# 15. Investment AI Insight
@mcp.tool()
async def investment_ai_insight(ticker: str) -> Dict[str, Any]:
    """
    Generate a concise AI-powered investment insight via DeepSeek/Ollama.
    """
    return investment_ai.generate_ai_insight(ticker)


# 16. Expense Manager – Budget Plan
@mcp.tool()
async def expense_generate_plan(
    monthly_salary: float,
    rent: float = 0.0,
    emi: float = 0.0,
    planned_savings: float = None,
    savings_ratio: float = None,
    age: int = 30,
    occupation: str = "Professional",
    city_tier: str = "Tier_1",
) -> Dict[str, Any]:
    """
    Generate a personalised monthly budget allocation plan.

    Provide either `planned_savings` (absolute currency) or `savings_ratio`
    (0-1 of spendable income). If neither is supplied, 25% is reserved.
    """
    result = expense_planner.generate_plan(
        monthly_salary=monthly_salary,
        rent=rent,
        emi=emi,
        planned_savings=planned_savings,
        savings_ratio=savings_ratio,
        age=age,
        occupation=occupation,
        city_tier=city_tier,
    )
    return result.to_dict()


if __name__ == "__main__":
    asyncio.run(mcp.run())