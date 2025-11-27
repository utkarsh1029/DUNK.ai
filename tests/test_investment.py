# tests/test_investment.py

from tools.investment_navigator.investment import InvestmentNavigator

def test_get_stock_price():
    tool = InvestmentNavigator()
    result = tool.get_stock_price("TCS")
    print("Stock price test result:", result)

def test_portfolio_summary():
    tool = InvestmentNavigator()
    result = tool.portfolio_summary("user123")
    print("Portfolio summary test result:", result)


if __name__ == "__main__":
    test_get_stock_price()
    test_portfolio_summary()
