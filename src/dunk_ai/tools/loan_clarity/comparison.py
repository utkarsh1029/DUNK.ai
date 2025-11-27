"""
Loan Clarity Tool – Loan Comparison Module

This module provides functionality to compare multiple loan options:
- Side-by-side comparison of loan offers
- Total cost analysis
- Best option recommendation
- Break-even analysis
"""

from typing import List, Dict, Any
from .logic import reducing_balance, flat_rate


def compare_loans(loan_options: List[Dict[str, Any]]) -> Dict[str, Any]:
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
        dict: Contains:
            - comparisons: List of detailed comparison for each loan
            - best_option: Index and details of best loan option
            - summary: Summary statistics
    """
    comparisons = []
    
    for idx, loan in enumerate(loan_options):
        principal = loan["principal"]
        annual_rate = loan["annual_rate"]
        tenure_years = loan["tenure_years"]
        repayment_frequency = loan.get("repayment_frequency", "monthly")
        interest_method = loan.get("interest_method", "reducing")
        processing_fee = loan.get("processing_fee", 0.0)
        other_charges = loan.get("other_charges", 0.0)
        loan_name = loan.get("loan_name", f"Loan {idx + 1}")

        # Calculate loan details
        if interest_method == "flat":
            emi, total_interest, total_payment, num_payments = flat_rate(
                principal, annual_rate, tenure_years, repayment_frequency
            )
        else:
            emi, total_interest, total_payment, num_payments = reducing_balance(
                principal, annual_rate, tenure_years, repayment_frequency
            )

        # Calculate effective cost
        total_cost = total_payment + processing_fee + other_charges
        effective_cost = total_cost - principal

        # Calculate effective interest rate (including charges)
        from .effective_rate import calculate_effective_rate
        effective_rate = calculate_effective_rate(
            principal, annual_rate, tenure_years, repayment_frequency,
            processing_fee, other_charges, interest_method
        )

        comparisons.append({
            "loan_name": loan_name,
            "principal": principal,
            "annual_rate": annual_rate,
            "tenure_years": tenure_years,
            "emi": emi,
            "total_interest": total_interest,
            "total_payment": total_payment,
            "processing_fee": processing_fee,
            "other_charges": other_charges,
            "total_cost": round(total_cost, 2),
            "effective_cost": round(effective_cost, 2),
            "effective_rate": round(effective_rate, 2),
            "number_of_payments": num_payments
        })

    # Find best option (lowest total cost)
    best_idx = min(range(len(comparisons)), key=lambda i: comparisons[i]["total_cost"])
    best_option = comparisons[best_idx]

    # Calculate summary statistics
    total_costs = [c["total_cost"] for c in comparisons]
    total_interests = [c["total_interest"] for c in comparisons]
    emis = [c["emi"] for c in comparisons]

    summary = {
        "number_of_options": len(loan_options),
        "lowest_total_cost": round(min(total_costs), 2),
        "highest_total_cost": round(max(total_costs), 2),
        "average_total_cost": round(sum(total_costs) / len(total_costs), 2),
        "lowest_emi": round(min(emis), 2),
        "highest_emi": round(max(emis), 2),
        "lowest_interest": round(min(total_interests), 2),
        "highest_interest": round(max(total_interests), 2)
    }

    return {
        "comparisons": comparisons,
        "best_option": {
            "index": best_idx,
            "loan_name": best_option["loan_name"],
            "total_cost": best_option["total_cost"],
            "emi": best_option["emi"],
            "savings_vs_highest": round(max(total_costs) - best_option["total_cost"], 2)
        },
        "summary": summary
    }


def break_even_analysis(
    loan1: Dict[str, Any],
    loan2: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Perform break-even analysis between two loan options.

    Args:
        loan1 (dict): First loan option
        loan2 (dict): Second loan option

    Returns:
        dict: Break-even analysis results
    """
    # Calculate EMIs
    if loan1.get("interest_method", "reducing") == "flat":
        emi1, _, total1, _ = flat_rate(
            loan1["principal"], loan1["annual_rate"],
            loan1["tenure_years"], loan1.get("repayment_frequency", "monthly")
        )
    else:
        emi1, _, total1, _ = reducing_balance(
            loan1["principal"], loan1["annual_rate"],
            loan1["tenure_years"], loan1.get("repayment_frequency", "monthly")
        )

    if loan2.get("interest_method", "reducing") == "flat":
        emi2, _, total2, _ = flat_rate(
            loan2["principal"], loan2["annual_rate"],
            loan2["tenure_years"], loan2.get("repayment_frequency", "monthly")
        )
    else:
        emi2, _, total2, _ = reducing_balance(
            loan2["principal"], loan2["annual_rate"],
            loan2["tenure_years"], loan2.get("repayment_frequency", "monthly")
        )

    # Add charges
    total1 += loan1.get("processing_fee", 0) + loan1.get("other_charges", 0)
    total2 += loan2.get("processing_fee", 0) + loan2.get("other_charges", 0)

    # Calculate difference
    emi_diff = abs(emi1 - emi2)
    total_diff = abs(total1 - total2)

    # Determine which is better
    if total1 < total2:
        better_loan = "Loan 1"
        savings = total2 - total1
    else:
        better_loan = "Loan 2"
        savings = total1 - total2

    return {
        "loan1": {
            "emi": emi1,
            "total_cost": round(total1, 2)
        },
        "loan2": {
            "emi": emi2,
            "total_cost": round(total2, 2)
        },
        "emi_difference": round(emi_diff, 2),
        "total_cost_difference": round(total_diff, 2),
        "better_option": better_loan,
        "savings": round(savings, 2),
        "break_even_months": round(total_diff / emi_diff, 2) if emi_diff > 0 else None
    }


