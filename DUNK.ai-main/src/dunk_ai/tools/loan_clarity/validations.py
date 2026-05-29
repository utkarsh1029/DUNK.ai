"""
Loan Clarity Tool – Validations
Enforces strict parameter bounds and types for full-stack API integration.
"""
from typing import Literal, Optional
# FIXED: Added missing model_validator import to prevent a NameError crash
from pydantic import BaseModel, Field, field_validator, model_validator

class BaseLoanEngineSchema(BaseModel):
    # Core Fields with Bounds Enforced
    loan_amount: float = Field(
        ..., 
        gt=0, 
        le=100_000_000_000, 
        description="Loan principal requested (Max ₹1 Lakh Crore)"
    )
    # Flexible fallback configurations for cleaner chat UI handling
    interest_rate: float = Field(
        default=8.5, 
        ge=0, 
        le=100, 
        description="Annual interest rate percentage"
    )
    tenure_years: float = Field(
        default=20.0, 
        gt=0, 
        le=50, 
        description="Loan tenure in years"
    )
    monthly_income: float = Field(
        ..., 
        gt=0, 
        description="User's net monthly income"
    )

    repayment_frequency: Literal["monthly", "quarterly", "annually"] = "monthly"
    interest_method: Literal["reducing", "flat"] = "reducing"
    loan_type: Literal["home_loan", "personal_loan", "vehicle_loan", "education_loan"] = "home_loan"


class AdvancedLoanEngineSchema(BaseLoanEngineSchema):
    # Tracking fields for prepayment/amortization logic
    payments_made: int = Field(default=0, ge=0)
    prepayment_amount: float = Field(default=0.0, ge=0)
    tax_slab: float = Field(default=5.0, description="Tax slab percentage")

    @field_validator("tax_slab")
    @classmethod
    def validate_tax_slabs(cls, value: float) -> float:
        valid_slabs = [5.0, 10.0, 20.0, 30.0]
        if value not in valid_slabs:
            raise ValueError(f"Invalid tax slab. Must be one of: {valid_slabs}")
        return value

    @model_validator(mode="after")
    def validate_prepayment_and_payments(self) -> "AdvancedLoanEngineSchema":
        # Cross-field logical validation
        total_payments_calculated = self.tenure_years * 12
        if self.payments_made > total_payments_calculated:
            raise ValueError("Payments made cannot exceed total calculated loan tenure periods.")
        return self