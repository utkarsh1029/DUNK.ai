from dunk_ai.services.expense_manager import ExpensePlanner


def test_expense_plan_generates_allocations():
    planner = ExpensePlanner()
    plan = planner.generate_plan(
        monthly_salary=100000,
        rent=20000,
        emi=10000,
        planned_savings=15000,
        savings_ratio=None,
        age=30,
        occupation="Professional",
        city_tier="Tier_1",
    )

    assert plan.disposable_income > 0
    assert len(plan.allocations) == 8
    assert abs(sum(plan.allocations.values()) - plan.disposable_income) < 1

