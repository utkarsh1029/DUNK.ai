from fastapi import APIRouter, HTTPException
from tools.investment_navigator.investment import InvestmentNavigator

from backend.ai_engine.investment_ai import InvestmentAI

router = APIRouter(prefix="/api/investment", tags=["Investment Navigator"])

inv = InvestmentNavigator()

@router.get("/stock/{ticker}")
def get_stock_details(ticker: str):
    """Fetch full stock analytics (price, RSI, volatility, forecast, etc)."""
    try:
        data = inv.get_stock_analytics(ticker)
        if "error" in data:
            raise HTTPException(status_code=404, detail=data["error"])
        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/summary/{ticker}")
def get_stock_summary(ticker: str):
    """Fetch only AI insight summary (for chatbot or dashboard view)."""
    try:
        data = inv.get_stock_analytics(ticker)
        if "error" in data:
            raise HTTPException(status_code=404, detail=data["error"])
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
        data = inv.get_stock_analytics(ticker)
        if "error" in data:
            raise HTTPException(status_code=404, detail=data["error"])
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

