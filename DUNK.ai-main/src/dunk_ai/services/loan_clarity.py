"""
Loan Clarity Service – DUNK.ai
Orchestrates AI intent parsing and interfaces with underlying calculation engines.
"""

import json
from typing import Dict, Any, Optional

# Import your validated schemas and calculation math
from dunk_ai.tools.loan_clarity.validations import BaseLoanEngineSchema
from dunk_ai.tools.loan_clarity.logic import (
    reducing_balance_from_schema,
    flat_rate_from_schema
)

class LoanClarityService:
    def __init__(self, llm_client=None):
        """
        Initializes the service with your backend LLM client instance.
        """
        self.llm_client = llm_client

    def get_tool_definition(self) -> dict:
        """
        Returns the structured JSON schema definition that tells the LLM 
        exactly how to extract variables from raw user conversation text.
        """
        return {
            "name": "calculate_loan_analytics",
            "description": "Extracts loan parameters from the user's message to calculate EMI and affordability metrics.",
            "parameters": {
                "type": "object",
                "properties": {
                    "loan_amount": {
                        "type": "number",
                        "description": "The total principal amount of the loan requested by the user."
                    },
                    "interest_rate": {
                        "type": "number",
                        "description": "The annual interest rate percentage (e.g., 8.5)."
                    },
                    "tenure_years": {
                        "type": "number",
                        "description": "The length or duration of the loan term specified in years."
                    },
                    "interest_method": {
                        "type": "string",
                        "enum": ["reducing", "flat"],
                        "default": "reducing",
                        "description": "The method used to calculate interest amortization."
                    },
                    "repayment_frequency": {
                        "type": "string",
                        "enum": ["monthly", "quarterly", "annually"],
                        "default": "monthly"
                    }
                },
                "required": ["loan_amount"]
            }
        }

    def process_structured_emi_calculation(self, payload_data: dict) -> Dict[str, Any]:
        """Executes core loan calculations using safe validations."""
        loan_spec = BaseLoanEngineSchema(**payload_data)
        
        if loan_spec.interest_method == "flat":
            emi, total_interest, total_payment, total_periods = flat_rate_from_schema(loan_spec)
        else:
            emi, total_interest, total_payment, total_periods = reducing_balance_from_schema(loan_spec)
            
        foir_ratio = (emi / loan_spec.monthly_income) * 100
        is_safe = foir_ratio <= 45.0
        
        return {
            "emi": emi,
            "total_interest_payable": total_interest,
            "total_repayment": total_payment,
            "total_payments_count": total_periods,
            "affordability": {
                "foir_percentage": round(foir_ratio, 2),
                "status": "Safe" if is_safe else "High Leverage Risk"
            }
        }

    def process_chat_intent(self, user_prompt: str, monthly_income: float) -> str:
        """
        Takes a raw conversational prompt, extracts financial figures using the LLM,
        runs the math engine, and structures a polished message back for the Chat UI window.
        """
        if not self.llm_client:
            return "Loan clarity conversational engine is currently offline."

        # 1. Instruct the model using your tool schema definitions
        messages = [
            {"role": "system", "content": "You are DUNK.ai's financial voice. Use the provided tools to extract numbers and execute exact math."},
            {"role": "user", "content": user_prompt}
        ]
        
        # 2. Call your LLM backend with tool execution enabled
        response = self.llm_client.chat.completions.create(
            model="gpt-4o",  # Or your chosen model configuration
            messages=messages,
            tools=[{"type": "function", "function": self.get_tool_definition()}],
            tool_choice="auto"
        )
        
        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        # 3. Handle the scenario where the LLM successfully hits your math tool trigger
        if tool_calls:
            extracted_arguments = json.loads(tool_calls[0].function.arguments)
            
            # Inject user's runtime profile variables (like income) for full evaluation context
            extracted_arguments["monthly_income"] = monthly_income
            
            try:
                # 4. Run the underlying mathematical algorithms safely!
                metrics = self.process_structured_emi_calculation(extracted_arguments)
                
                # 5. Build a perfectly formatted chat response to render on your frontend screen
                return (
                    f"### 📊 Your Loan Analysis Summary\n\n"
                    f"* **Estimated Monthly EMI:** ₹{metrics['emi']:,}\n"
                    f"* **Total Interest Component:** ₹{metrics['total_interest_payable']:,}\n"
                    f"* **Total Gross Repayment Amount:** ₹{metrics['total_repayment']:,}\n\n"
                    f"⚡ **Affordability Check:** Your Fixed Obligation-to-Income Ratio (FOIR) is **{metrics['affordability']['foir_percentage']}%**. "
                    f"This is classified as **{metrics['affordability']['status']}** relative to your current monthly intake profile."
                )
            except Exception as e:
                return "I ran into an issue parsing those numbers. Could you please double-check your loan parameters?"
        
        # Fallback if it's a general question without metrics (e.g., "What is a reducing balance loan?")
        return response_message.content