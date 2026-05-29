import math
from fastapi import APIRouter, HTTPException, Query

from dunk_ai.services.investment_ai import InvestmentAI
from dunk_ai.tools.investment_navigator.investment import InvestmentNavigator

router = APIRouter(prefix="/api/investment", tags=["Investment Navigator"])

inv = InvestmentNavigator()


def _sanitize_data(obj):
    """
    Recursively loops through dicts, lists, and floats to safely replace 
    JSON-breaking NaN, Infinity, and -Infinity values with a safe None (null).
    """
    if isinstance(obj, dict):
        return {k: _sanitize_data(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [_sanitize_data(x) for x in obj]
    elif isinstance(obj, float):
        if math.isnan(obj) or math.isinf(obj):
            return None  # Converts smoothly into valid 'null' inside JSON output strings
    return obj


def _ensure_success(data):
    if "error" in data:
        raise HTTPException(status_code=404, detail=data["error"])
    
    # ⚡ THE CRITICAL FIX: Run the deep sanitation pass right here 
    # before returning the payload to any route handler.
    return _sanitize_data(data)


@router.get("/stock/{ticker}")
def get_stock_details(ticker: str):
    """Fetch full stock analytics (price, RSI, volatility, forecast, etc)."""
    try:
        data = _ensure_success(inv.get_stock_analytics(ticker))
        return data
    except HTTPException:
        raise
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
    except HTTPException:
        raise
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
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/ai_insight/{ticker}")
def get_ai_insight(ticker: str):
    """
    Generate an AI-powered investment insight using DeepSeek R1 via Ollama.
    """
    try:
        ai = InvestmentAI()
        result = ai.generate_ai_insight(ticker)
        # Sanitizing AI output just in case the LLM returned structured mathematical matrices
        return _sanitize_data(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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
        data = inv.portfolio_summary(user_id)
        return _sanitize_data(data)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc