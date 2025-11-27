from fastapi import APIRouter, HTTPException, Query

from dunk_ai.services.investment_ai import InvestmentAI
from dunk_ai.tools.investment_navigator.investment import InvestmentNavigator

router = APIRouter(prefix="/api/investment", tags=["Investment Navigator"])

inv = InvestmentNavigator()

def _ensure_success(data):
    if "error" in data:
        raise HTTPException(status_code=404, detail=data["error"])
    return data


@router.get("/stock/{ticker}")
def get_stock_details(ticker: str):
    """Fetch full stock analytics (price, RSI, volatility, forecast, etc)."""
    try:
        data = _ensure_success(inv.get_stock_analytics(ticker))
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/summary/{ticker}")
def get_stock_summary(ticker: str):
    """Fetch only AI insight summary (for chatbot or dashboard view)."""
    try:
        data = _ensure_success(inv.get_stock_analytics(ticker))
        return {
            "ticker": data["ticker"],
            "summary": data["insight_summary"],
            "predicted_trend": data.get("predicted_trend", "N/A")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/plot/{ticker}")
def get_forecast_plot(ticker: str):
    """Return path to generated forecast chart."""
    try:
        data = _ensure_success(inv.get_stock_analytics(ticker))
        return {
            "ticker": ticker,
            "chart_path": data.get("forecast_chart_path"),
            "forecast_confidence": data.get("forecast_confidence")
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/investment/ai_insight/{ticker}")
def get_ai_insight(ticker: str):
    """
    Generate an AI-powered investment insight using DeepSeek R1 via Ollama.
    """
    ai = InvestmentAI()
    result = ai.generate_ai_insight(ticker)
    return result


@router.get("/price/{query}")
def get_live_price(query: str):
    """
    Fetch the latest price snapshot for a stock from Yahoo/NSE/Google.
    """
    try:
        data = _ensure_success(inv.get_stock_price(query))
        return data
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/mutual-fund")
def get_mutual_fund_nav(scheme_name: str = Query(..., alias="scheme")):
    """
    Fetch latest NAV for a mutual fund scheme by name.
    """
    try:
        data = _ensure_success(inv.get_mutual_fund_nav(scheme_name))
        return data
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@router.get("/portfolio/{user_id}")
def get_portfolio(user_id: str):
    """
    Return a placeholder portfolio summary (future hook for DB integration).
    """
    try:
        return inv.portfolio_summary(user_id)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

