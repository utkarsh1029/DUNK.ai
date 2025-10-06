# tools/investment_navigator/investment.py

from typing import Dict, Any
import random
from datetime import datetime

class InvestmentNavigator:
    """
    Dummy version of Investment Navigator.
    Simulates stock prices, mutual fund NAVs, and portfolio summaries.
    """

    def __init__(self):
        pass

    def get_stock_price(self, ticker: str) -> Dict[str, Any]:
        """Return a random stock price (for demo only)"""
        return {
            "ticker": ticker,
            "current_price": round(random.uniform(100, 2000), 2),
            "52_week_high": round(random.uniform(2000, 3000), 2),
            "52_week_low": round(random.uniform(50, 100), 2),
            "currency": "INR",
            "note": "Dummy data (replace with live API later)"
        }

    def get_mutual_fund_nav(self, fund_name: str) -> Dict[str, Any]:
        """Return a fake NAV for a given mutual fund"""
        return {
            "fund_name": fund_name,
            "latest_nav": round(random.uniform(10, 100), 2),
            "date": datetime.today().strftime("%Y-%m-%d"),
            "note": "Dummy data (replace with AMFI API later)"
        }

    def portfolio_summary(self, user_id: str) -> Dict[str, Any]:
        """Return a fake portfolio summary"""
        stocks_value = round(random.uniform(50000, 200000), 2)
        mf_value = round(random.uniform(20000, 100000), 2)
        total = stocks_value + mf_value

        return {
            "user_id": user_id,
            "total_value": total,
            "assets": {
                "stocks": stocks_value,
                "mutual_funds": mf_value
            },
            "diversification": {
                "stocks": f"{(stocks_value/total)*100:.2f}%",
                "mutual_funds": f"{(mf_value/total)*100:.2f}%"
            },
            "note": "Dummy data (replace with MongoDB later)"
        }
