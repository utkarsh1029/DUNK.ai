from typing import Literal, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from dunk_ai.services.expense_manager import ExpensePlanner


class ExpensePlanRequest(BaseModel):
    monthly_salary: float = Field(..., gt=0)
    rent: float = Field(0, ge=0)
    emi: float = Field(0, ge=0)
    planned_savings: Optional[float] = Field(
        None, ge=0, description="Absolute savings amount in currency"
    )
    savings_ratio: Optional[float] = Field(
        None, ge=0, le=1, description="Savings ratio of spendable income (0-1)"
    )
    age: int = Field(..., gt=0)
    occupation: str
    city_tier: Literal["Tier_1", "Tier_2", "Tier_3"]


router = APIRouter(prefix="/api/expense", tags=["Expense Manager"])
planner = ExpensePlanner()


@router.post("/plan")
def generate_expense_plan(payload: ExpensePlanRequest):
    try:
        result = planner.generate_plan(**payload.dict())
        return result.to_dict()
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

