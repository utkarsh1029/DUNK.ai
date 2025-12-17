from datetime import date, datetime
from typing import List, Literal, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from dunk_ai.tools.loan_clarity import (
    calculate_affordability,
    calculate_early_settlement,
    calculate_effective_rate,
    calculate_lifetime_tax_benefits,
    calculate_loan_eligibility,
    calculate_prepayment_impact,
    calculate_tax_benefits,
    compare_loans,
    flat_rate,
    generate_amortization_schedule,
    get_outstanding_principal,
    get_year_wise_summary,
    modify_emi,
    modify_tenure,
    reducing_balance,
)
from dunk_ai.tools.loan_clarity.effective_rate import calculate_apr


Frequency = Literal["monthly", "quarterly", "annually"]
InterestMethod = Literal["reducing", "flat"]


class LoanPayload(BaseModel):
    principal: float = Field(..., gt=0)
    annual_rate: float = Field(..., gt=0)
    tenure_years: float = Field(..., gt=0)
    repayment_frequency: Frequency


class LoanPayloadWithMethod(LoanPayload):
    interest_method: InterestMethod = "reducing"


class ScheduleRequest(LoanPayloadWithMethod):
    start_date: Optional[date] = None


class OutstandingRequest(LoanPayloadWithMethod):
    payments_made: int = Field(..., ge=0)


class PrepaymentRequest(LoanPayloadWithMethod):
    payments_made: int = Field(..., ge=0)
    prepayment_amount: float = Field(..., gt=0)
    reduce_emi: bool = True


class EarlySettlementRequest(LoanPayloadWithMethod):
    payments_made: int = Field(..., ge=0)
    prepayment_charges: float = Field(0, ge=0)


class ModifyEmiRequest(LoanPayloadWithMethod):
    new_emi: float = Field(..., gt=0)


class ModifyTenureRequest(LoanPayloadWithMethod):
    new_tenure_years: float = Field(..., gt=0)


class LoanOption(BaseModel):
    principal: float
    annual_rate: float
    tenure_years: float
    repayment_frequency: Frequency
    interest_method: InterestMethod = "reducing"
    processing_fee: float = 0.0
    other_charges: float = 0.0
    loan_name: Optional[str] = None


class LoanComparisonRequest(BaseModel):
    loan_options: List[LoanOption]


class TaxBenefitsRequest(LoanPayloadWithMethod):
    loan_type: Literal["home_loan", "vehicle_loan", "personal_loan"] = "home_loan"
    tax_slab: float = Field(30.0, ge=0, le=30)
    is_first_time_buyer: bool = False
    is_self_occupied: bool = True


class EligibilityRequest(BaseModel):
    monthly_income: float = Field(..., gt=0)
    annual_rate: float = Field(..., gt=0)
    tenure_years: float = Field(..., gt=0)
    repayment_frequency: Frequency = "monthly"
    interest_method: InterestMethod = "reducing"
    existing_emis: float = Field(0, ge=0)
    emi_to_income_ratio: float = Field(0.4, gt=0, le=1)
    age: Optional[int] = Field(None, gt=0)


class AffordabilityRequest(BaseModel):
    desired_loan_amount: float = Field(..., gt=0)
    monthly_income: float = Field(..., gt=0)
    annual_rate: float = Field(..., gt=0)
    tenure_years: float = Field(..., gt=0)
    repayment_frequency: Frequency = "monthly"
    interest_method: InterestMethod = "reducing"
    existing_emis: float = Field(0, ge=0)
    emi_to_income_ratio: float = Field(0.4, gt=0, le=1)


class EffectiveRateRequest(LoanPayloadWithMethod):
    processing_fee: float = Field(0.0, ge=0)
    other_charges: float = Field(0.0, ge=0)


router = APIRouter(prefix="/api/loans", tags=["Loan Clarity"])


def _handle_errors(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc


@router.post("/emi/flat")
def calculate_flat_rate_emi(payload: LoanPayload):
    emi, total_interest, total_payment, number_of_payments = _handle_errors(
        flat_rate, **payload.dict()
    )
    return {
        "emi": emi,
        "total_interest": total_interest,
        "total_payment": total_payment,
        "number_of_payments": number_of_payments,
    }


@router.post("/emi/reducing")
def calculate_reducing_balance_emi(payload: LoanPayload):
    emi, total_interest, total_payment, number_of_payments = _handle_errors(
        reducing_balance, **payload.dict()
    )
    return {
        "emi": emi,
        "total_interest": total_interest,
        "total_payment": total_payment,
        "number_of_payments": number_of_payments,
    }


@router.post("/schedule")
def generate_schedule(payload: ScheduleRequest):
    start_dt = (
        datetime.combine(payload.start_date, datetime.min.time())
        if payload.start_date
        else None
    )
    schedule = _handle_errors(
        generate_amortization_schedule,
        payload.principal,
        payload.annual_rate,
        payload.tenure_years,
        payload.repayment_frequency,
        payload.interest_method,
        start_dt,
    )
    summary = get_year_wise_summary(schedule)
    return {"schedule": schedule, "yearly_summary": summary}


@router.post("/schedule/outstanding")
def outstanding_principal(payload: OutstandingRequest):
    outstanding = _handle_errors(
        get_outstanding_principal,
        payload.principal,
        payload.annual_rate,
        payload.tenure_years,
        payload.repayment_frequency,
        payload.payments_made,
        payload.interest_method,
    )
    return {"outstanding_principal": outstanding}


@router.post("/prepayment")
def prepayment_impact(payload: PrepaymentRequest):
    result = _handle_errors(
        calculate_prepayment_impact,
        payload.principal,
        payload.annual_rate,
        payload.tenure_years,
        payload.repayment_frequency,
        payload.payments_made,
        payload.prepayment_amount,
        payload.interest_method,
        payload.reduce_emi,
    )
    return result


@router.post("/early-settlement")
def early_settlement(payload: EarlySettlementRequest):
    result = _handle_errors(
        calculate_early_settlement,
        payload.principal,
        payload.annual_rate,
        payload.tenure_years,
        payload.repayment_frequency,
        payload.payments_made,
        payload.interest_method,
        payload.prepayment_charges,
    )
    return result


@router.post("/modify/emi")
def modify_emi_amount(payload: ModifyEmiRequest):
    result = _handle_errors(
        modify_emi,
        payload.principal,
        payload.annual_rate,
        payload.tenure_years,
        payload.repayment_frequency,
        payload.new_emi,
        payload.interest_method,
    )
    return result


@router.post("/modify/tenure")
def modify_tenure(payload: ModifyTenureRequest):
    result = _handle_errors(
        modify_tenure,
        payload.principal,
        payload.annual_rate,
        payload.tenure_years,
        payload.repayment_frequency,
        payload.new_tenure_years,
        payload.interest_method,
    )
    return result


@router.post("/compare")
def compare_loan_options(payload: LoanComparisonRequest):
    if not payload.loan_options:
        raise HTTPException(status_code=400, detail="At least one loan option is required.")
    result = _handle_errors(compare_loans, [option.dict() for option in payload.loan_options])
    return result


@router.post("/tax-benefits")
def tax_benefits(payload: TaxBenefitsRequest):
    result = _handle_errors(
        calculate_tax_benefits,
        payload.principal,
        payload.annual_rate,
        payload.tenure_years,
        payload.repayment_frequency,
        payload.loan_type,
        payload.interest_method,
        payload.tax_slab,
        payload.is_first_time_buyer,
        payload.is_self_occupied,
    )
    lifetime = _handle_errors(
        calculate_lifetime_tax_benefits,
        payload.principal,
        payload.annual_rate,
        payload.tenure_years,
        payload.repayment_frequency,
        payload.loan_type,
        payload.interest_method,
        payload.tax_slab,
        payload.is_first_time_buyer,
        payload.is_self_occupied,
    )
    return {"annual": result, "lifetime": lifetime}


@router.post("/eligibility")
def loan_eligibility(payload: EligibilityRequest):
    result = _handle_errors(
        calculate_loan_eligibility,
        payload.monthly_income,
        payload.annual_rate,
        payload.tenure_years,
        payload.repayment_frequency,
        payload.interest_method,
        payload.existing_emis,
        payload.emi_to_income_ratio,
        payload.age,
    )
    return result


@router.post("/affordability")
def loan_affordability(payload: AffordabilityRequest):
    result = _handle_errors(
        calculate_affordability,
        payload.desired_loan_amount,
        payload.monthly_income,
        payload.annual_rate,
        payload.tenure_years,
        payload.repayment_frequency,
        payload.interest_method,
        payload.existing_emis,
        payload.emi_to_income_ratio,
    )
    return result


@router.post("/effective-rate")
def effective_rate(payload: EffectiveRateRequest):
    effective_rate_value = _handle_errors(
        calculate_effective_rate,
        payload.principal,
        payload.annual_rate,
        payload.tenure_years,
        payload.repayment_frequency,
        payload.processing_fee,
        payload.other_charges,
        payload.interest_method,
    )
    apr_details = calculate_apr(
        payload.principal,
        payload.annual_rate,
        payload.tenure_years,
        payload.repayment_frequency,
        payload.processing_fee,
        payload.other_charges,
        payload.interest_method,
    )
    return {"effective_rate": effective_rate_value, "apr_details": apr_details}

