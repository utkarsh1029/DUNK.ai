from pathlib import Path

import joblib
import pandas as pd

MODEL_PATH = Path(__file__).with_name("final_gradient_boosting_pipeline.pkl")

model = joblib.load(MODEL_PATH)

print(" Hi! I’m your Smart Expense Assistant.\nLet’s plan your monthly budget together!\n")

salary = float(input(" What is your monthly salary (in ₹)? "))

rent = float(input(" Enter your monthly rent (₹0 if none): "))
emi = float(input(" Enter your total monthly EMIs (₹0 if none): "))

fixed_expenses = rent + emi
spendable = salary - fixed_expenses

if spendable <= 0:
    print("\n Your fixed expenses exceed your salary! Please recheck your inputs.")
else:
    print(f"\n Your available spendable income after rent and EMI: ₹{spendable:.2f}")

    print("\n Based on modern budgeting rules:")
    print("   → Minimum savings (20%)  : ₹{:.2f}".format(spendable * 0.20))
    print("   → Recommended savings (25%): ₹{:.2f}".format(spendable * 0.25))
    print("   → Strong savings (30%)    : ₹{:.2f}".format(spendable * 0.30))

    choice = float(input("\n How much would you like to save this month (in ₹)? "))

    disposable_income = spendable - choice
    if disposable_income <= 0:
        print("\n Savings exceed spendable income! Try again.")
    else:
        print(f"\n Your disposable income for the month: ₹{disposable_income:.2f}")

        
        age = int(input("\n Enter your age: "))
        occupation = input(" Enter your occupation (e.g., Student, Self Employeed, Professional, Retired): ").strip()
        city_tier = input(" Enter your city tier (Tier_1 / Tier_2 / Tier_3): ").strip()

       
        new_user = pd.DataFrame([{
            'Age': age,
            'Occupation': occupation,
            'City_Tier': city_tier,
            'Disposable_Income': disposable_income
        }])

        predicted_percentages = model.predict(new_user)[0]


        import numpy as np
        predicted_percentages = np.clip(predicted_percentages, 0, None)  # Remove negatives
        total = predicted_percentages.sum()
        if total > 0:
            predicted_percentages = predicted_percentages / total
        else:
            predicted_percentages = np.ones_like(predicted_percentages) / len(predicted_percentages)

        categories = ['Groceries','Transport','Eating_Out','Entertainment',
              'Utilities','Healthcare','Education','Miscellaneous']

        allocations = (predicted_percentages * disposable_income).round(2)

        print("\n Here’s your personalized monthly budget plan:\n")
        for cat, amt in zip(categories, allocations):
            print(f"  • {cat:15s} → ₹{amt}")

        print("\n Summary:")
        print(f"  Total Disposable: ₹{disposable_income:.2f}")
        print(f"  Total Suggested Spend: ₹{allocations.sum():.2f}")
        print(f"  Total Savings: ₹{choice:.2f}")
        print("\n Stay smart with your spending, and remember — consistency is key!")
