# DUNK.ai

DunkAI is an intelligent financial agent that connects to user accounts, aggregates real-time financial data, and provides personalized insights across budgeting, loan analysis, and investments. It combines FastAPI services, LangChain-powered AI, and MCP-accessible tools.

## Project Structure

```
.
├── assets/                  # Generated artifacts (plots, reports, etc.)
│   └── plots/
├── requirements/
│   └── backend.txt          # FastAPI backend dependencies
├── backend/
│   └── dunk_ai/
│       ├── __init__.py
│       ├── api/             # FastAPI application + routers
│       │   ├── __init__.py
│       │   ├── main.py
│       │   └── routes/
│       ├── services/        # AI/service layer abstractions
│       │   ├── __init__.py
│       │   └── investment_ai.py
│       ├── tools/           # Reusable financial tools (loan, investment, expense)
│       │   ├── __init__.py
│       │   ├── investment_navigator/
│       │   ├── loan_clarity/
│       │   ├── expense_manager/
│       │   └── whatif_simulator/
│       └── server/          # MCP server exposing tools
│           ├── __init__.py
│           └── mcp_server.py
├── tests/                   # Pytest suites for each tool
│   ├── conftest.py
│   ├── test_investment.py
│   ├── test_investment_live.py
│   └── test_loan_clarity.py
├── pyproject.toml
└── requirements.txt         # Top-level dev + MCP dependencies
```

## Getting Started

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements/backend.txt
   ```

2. **Run FastAPI backend**
   ```bash
   uvicorn dunk_ai.api.main:app --reload
   ```

3. **Expose MCP server (Loan Clarity tools)**
   ```bash
   python -m dunk_ai.server.mcp_server
   ```

4. **Execute tests**
   ```bash
   pytest
   ```

## Key Components

- `dunk_ai.tools.loan_clarity`: Comprehensive loan EMI, amortization, and tax analysis suite.
- `dunk_ai.tools.investment_navigator`: Live stock analytics, forecasting, and AI-powered insights.
- `dunk_ai.tools.expense_manager`: Budget assistant backed by a gradient boosting model.
- `dunk_ai.services.investment_ai`: LangChain + Ollama pipeline that summarizes analytics.
- `dunk_ai.services.expense_manager`: Programmatic interface to the budget planner model.
- `dunk_ai.api`: FastAPI-based REST surface that orchestrates tool responses.

Assets such as forecast plots are written to `assets/plots`, ensuring generated media stays outside the Python package.

## REST API Surface

| Router | Prefix | Highlights |
| ------ | ------ | ---------- |
| Investment Navigator | `/api/investment` | Stock analytics, AI insight, live price lookup, mutual fund NAV, placeholder portfolio summary |
| Loan Clarity | `/api/loans` | Flat/reducing EMI calculators, amortization schedule + outstanding balance, prepayment, early settlement, EMI/tenure modifications, loan comparison, tax + eligibility helpers, effective-rate/APR |
| Expense Manager | `/api/expense` | `POST /plan` returns personalised allocations, savings guidance, and metadata |

Each endpoint returns JSON-formatted outputs from the underlying tool modules so other services (frontends, MCP clients, workflows) can consume them directly.
