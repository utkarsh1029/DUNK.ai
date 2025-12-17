from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# ✅ Import feature routers
from dunk_ai.api.routes.expense import router as expense_router
from dunk_ai.api.routes.investment import router as investment_router
from dunk_ai.api.routes.loan_clarity import router as loan_router

app = FastAPI(
    title="DUNK.ai Backend API",
    description="Unified backend for Expense Manager, Loan Clarity, Investment Navigator, and more.",
    version="1.0.0",
)

# ✅ Allow frontend (React/Vercel) to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to your frontend URL later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ Register all routers
app.include_router(investment_router)
app.include_router(loan_router)
app.include_router(expense_router)

@app.get("/")
def root():
    return {"message": "🚀 DUNK.ai Backend is up and running!"}

