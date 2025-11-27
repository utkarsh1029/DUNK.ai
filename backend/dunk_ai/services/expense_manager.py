"""
Service layer for the Expense Manager tool.

Wraps the interactive CLI logic from `tools/expense_manager/expense.py`
so it can be reused by APIs, MCP tools, or other backends.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional

import joblib
import numpy as np
import pandas as pd


logger = logging.getLogger(__name__)


EXPENSE_CATEGORIES = [
    "Groceries",
    "Transport",
    "Eating_Out",
    "Entertainment",
    "Utilities",
    "Healthcare",
    "Education",
    "Miscellaneous",
]


@dataclass(frozen=True)
class ExpensePlanResult:
    """Structured response returned by :meth:`ExpensePlanner.generate_plan`."""

    salary: float
    fixed_expenses: Dict[str, float]
    spendable_income: float
    planned_savings: float
    disposable_income: float
    savings_guidance: Dict[str, float]
    allocations: Dict[str, float]
    model_metadata: Dict[str, str]

    def to_dict(self) -> Dict[str, float]:
        """Return a JSON-serialisable dict representation."""
        return {
            "salary": self.salary,
            "fixed_expenses": self.fixed_expenses,
            "spendable_income": self.spendable_income,
            "planned_savings": self.planned_savings,
            "disposable_income": self.disposable_income,
            "savings_guidance": self.savings_guidance,
            "allocations": self.allocations,
            "model_metadata": self.model_metadata,
        }


class ExpensePlanner:
    """
    Loads the trained gradient boosting pipeline and generates allocation plans.
    """

    def __init__(self, model_path: Optional[Path] = None):
        if model_path is None:
            model_path = (
                Path(__file__).resolve().parents[1]
                / "tools"
                / "expense_manager"
                / "final_gradient_boosting_pipeline.pkl"
            )
        self.model_path = model_path
        self.model = None
        self.model_error: Optional[str] = None

        if not model_path.exists():
            self.model_error = f"Expense Manager model not found at {model_path}"
        else:
            try:
                self.model = joblib.load(model_path)
            except Exception as exc:  # pragma: no cover - environment-specific
                self.model_error = str(exc)
                logger.warning("Falling back to rule-based allocations: %s", exc)

    def generate_plan(
        self,
        *,
        monthly_salary: float,
        rent: float,
        emi: float,
        planned_savings: Optional[float],
        savings_ratio: Optional[float],
        age: int,
        occupation: str,
        city_tier: str,
    ) -> ExpensePlanResult:
        """
        Compute monthly allocations based on salary, obligations, and demographics.
        """

        self._validate_inputs(
            monthly_salary, rent, emi, planned_savings, savings_ratio, age
        )

        fixed_expenses = rent + emi
        spendable_income = monthly_salary - fixed_expenses

        savings_target = self._resolve_savings_target(
            spendable_income, planned_savings, savings_ratio
        )
        disposable_income = spendable_income - savings_target

        allocations = self._predict_allocations(
            age, occupation, city_tier, disposable_income
        )

        guidance = {
            "minimum_20_percent": round(spendable_income * 0.20, 2),
            "recommended_25_percent": round(spendable_income * 0.25, 2),
            "strong_30_percent": round(spendable_income * 0.30, 2),
        }

        return ExpensePlanResult(
            salary=round(monthly_salary, 2),
            fixed_expenses={"rent": round(rent, 2), "emi": round(emi, 2)},
            spendable_income=round(spendable_income, 2),
            planned_savings=round(savings_target, 2),
            disposable_income=round(disposable_income, 2),
            savings_guidance=guidance,
            allocations=allocations,
            model_metadata={
                "path": str(self.model_path),
                "type": "GradientBoosting",
                "loaded": self.model is not None,
                "fallback_reason": self.model_error,
                
            },
        )

    # ------------------------------------------------------------------ #
    # Internal helpers
    # ------------------------------------------------------------------ #

    def _validate_inputs(
        self,
        salary: float,
        rent: float,
        emi: float,
        planned_savings: Optional[float],
        savings_ratio: Optional[float],
        age: int,
    ) -> None:
        if salary <= 0:
            raise ValueError("Monthly salary must be greater than zero.")
        if rent < 0 or emi < 0:
            raise ValueError("Rent and EMI cannot be negative.")
        if rent + emi >= salary:
            raise ValueError("Fixed expenses exceed or equal salary.")
        if planned_savings is not None and planned_savings < 0:
            raise ValueError("Planned savings cannot be negative.")
        if savings_ratio is not None and not 0 <= savings_ratio <= 1:
            raise ValueError("Savings ratio must be between 0 and 1.")
        if age <= 0:
            raise ValueError("Age must be a positive integer.")
        if planned_savings is not None and savings_ratio is not None:
            raise ValueError("Provide either planned_savings or savings_ratio, not both.")

    def _resolve_savings_target(
        self,
        spendable_income: float,
        planned_savings: Optional[float],
        savings_ratio: Optional[float],
    ) -> float:
        if planned_savings is not None:
            savings = planned_savings
        elif savings_ratio is not None:
            savings = spendable_income * savings_ratio
        else:
            savings = spendable_income * 0.25  # default recommendation

        if savings >= spendable_income:
            raise ValueError("Savings cannot exceed spendable income.")

        return round(savings, 2)

    def _predict_allocations(
        self,
        age: int,
        occupation: str,
        city_tier: str,
        disposable_income: float,
    ) -> Dict[str, float]:
        features = pd.DataFrame(
            [
                {
                    "Age": age,
                    "Occupation": occupation.strip(),
                    "City_Tier": city_tier.strip(),
                    "Disposable_Income": disposable_income,
                }
            ]
        )

        if self.model is None:
            weights = np.full(len(EXPENSE_CATEGORIES), 1 / len(EXPENSE_CATEGORIES))
        else:
            predicted_percentages: np.ndarray = self.model.predict(features)[0]
            sanitized = np.clip(predicted_percentages, 0, None)
            total = sanitized.sum()
            if total <= 0:
                weights = np.full_like(sanitized, 1 / len(sanitized), dtype=float)
            else:
                weights = sanitized / total

        allocations = (weights * disposable_income).round(2)
        return {
            category: float(amount)
            for category, amount in zip(EXPENSE_CATEGORIES, allocations.tolist())
        }

