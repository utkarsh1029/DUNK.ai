"""
Loan Clarity Tool – CLI Runner
"""

from .logic import flat_rate, reducing_balance
from . import validations


def main():
    try:
        # Collect and validate inputs step by step
        principal = validations.validate_principal(
            float(input("Enter Loan Amount (Principal): "))
        )

        annual_rate = validations.validate_interest_rate(
            float(input("Enter Annual Interest Rate (%): "))
        )

        tenure_years = validations.validate_tenure(
            float(input("Enter Loan Tenure (in years): "))
        )

        repayment_frequency = validations.validate_repayment_frequency(
            input("Enter Repayment Frequency (monthly/quarterly/annually): ").strip().lower()
        )

        interest_method = validations.validate_interest_method(
            input("Enter Interest Calculation Method (reducing/flat): ").strip().lower()
        )

        # Run selected method
        if interest_method == "flat":
            emi, total_interest, total_payment, num_pay = flat_rate(
                principal, annual_rate, tenure_years, repayment_frequency
            )
        else:
            emi, total_interest, total_payment, num_pay = reducing_balance(
                principal, annual_rate, tenure_years, repayment_frequency
            )

        # Print results
        print("\n💡 Loan Clarity Results")
        print(f"Repayment Frequency: {repayment_frequency.capitalize()}")
        print(f"Total Number of Payments: {num_pay}")
        print(f"EMI per period: ₹ {emi}")
        print(f"Total Interest Payable: ₹ {total_interest}")
        print(f"Total Repayment: ₹ {total_payment}")

    except ValueError as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()