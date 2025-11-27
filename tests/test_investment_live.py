# tests/test_investment_live.py

from tools.investment_navigator.investment import InvestmentNavigator

def test_live_data():
    inv = InvestmentNavigator()

    print("\n--- 🔹 Live Stock Price ---")
    print(inv.get_stock_price("TCS.NS"))

    print("\n--- 🔹 Live Mutual Fund NAV ---")
    print(inv.get_mutual_fund_nav("Parag Parikh Flexi Cap"))

def test_stock_analytics():
    inv = InvestmentNavigator()
    result = inv.get_stock_price("INFY.NS")
    print("\n--- 🔹 Stock Analytics ---")
    print(result)

def test_stock_analytics():
    from tools.investment_navigator.investment import InvestmentNavigator
    inv = InvestmentNavigator()

    print("\n--- 🔍 Stock Analytics Demo ---")
    result = inv.get_stock_analytics("INFY.NS")
    print(result)


if __name__ == "__main__":
    test_live_data()
