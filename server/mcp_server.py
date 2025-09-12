"""
MCP Server – DUNK.ai

This server registers available tools (starting with Loan Clarity)
so that an LLM can call them through the MCP protocol.
"""

import asyncio
from mcp.server.fastmcp import FastMCP
from tools.loan_clarity.logic import flat_rate, reducing_balance

# Initialize MCP server
mcp = FastMCP("dunk-mcp-server")


# Loan Clarity Tool
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


if __name__ == "__main__":
    asyncio.run(mcp.run())