
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import GradientBoostingRegressor
import joblib

DATA_PATH = "/content/correctly_modified_data.csv"
df = pd.read_csv(DATA_PATH)

cols_to_drop = [
    'Income', 'Rent', 'Loan_Repayment', 'Insurance',
    'Desired_Savings_Percentage', 'Desired_Savings',
    'TotalExpenditure', 'predicted_disposableincome'
]

df = df.drop(columns=[c for c in cols_to_drop if c in df.columns], errors='ignore')

expense_cols = ['Groceries', 'Transport', 'Eating_Out', 'Entertainment',
                'Utilities', 'Healthcare', 'Education', 'Miscellaneous']

for col in expense_cols:
    df[col] = df[col] / df['Disposable_Income']

X = df[['Age', 'Occupation', 'City_Tier', 'Disposable_Income']]
y = df[expense_cols]

from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.compose import ColumnTransformer

preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), ['Occupation', 'City_Tier']),
        ('num', StandardScaler(), ['Age', 'Disposable_Income'])
    ]
)
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import r2_score, mean_absolute_error
from sklearn.pipeline import Pipeline # Import Pipeline

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, shuffle=True
)

gb_regressor = GradientBoostingRegressor(
    n_estimators=400,
    learning_rate=0.05,
    max_depth=3,     # ↓ from 5 to 3
    min_samples_split=4,
    min_samples_leaf=2,
    subsample=0.9,
    random_state=42
)

gb_model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', MultiOutputRegressor(gb_regressor))
])

print(" Training the Gradient Boosting model...")
gb_model.fit(X_train, y_train)
print("Model training complete!")
y_pred = gb_model.predict(X_test)

r2 = r2_score(y_test, y_pred, multioutput='variance_weighted')
mae = mean_absolute_error(y_test, y_pred)

print("\n Model Evaluation Results:")
print(f"R² Score (Test Data): {r2:.3f}")
print(f"Mean Absolute Error: {mae:.3f}")

train_pred = gb_model.predict(X_train)
train_r2 = r2_score(y_train, train_pred, multioutput='variance_weighted')
test_r2 = r2_score(y_test, y_pred, multioutput='variance_weighted')

print(f"Training R²: {train_r2:.3f}")
print(f"Testing  R²: {test_r2:.3f}")
print(f"Difference: {abs(train_r2 - test_r2):.3f}")

import joblib
joblib.dump(gb_model, "final_gradient_boosting_pipeline.pkl")
print(" Model saved successfully as final_gradient_boosting_pipeline.pkl")