# tools/investment_navigator/investment.py
import logging
import warnings
from datetime import datetime
from pathlib import Path
from typing import Any, Dict

import matplotlib

matplotlib.use("Agg")

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import numpy as np
import requests
import yfinance as yf
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tools.sm_exceptions import ConvergenceWarning, ValueWarning

# 🔇 Silence all statsmodels warnings globally
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", category=ValueWarning)
warnings.filterwarnings("ignore", category=ConvergenceWarning)
warnings.filterwarnings("ignore", message="A date index has been provided")
warnings.filterwarnings("ignore", message="No supported index is available")
warnings.filterwarnings("ignore", message="Prediction results will be given with an integer index")
warnings.filterwarnings("ignore", message="Maximum Likelihood optimization failed")

# ✅ Suppress statsmodels' internal logs too
logging.getLogger("statsmodels").setLevel(logging.CRITICAL)

PROJECT_ROOT = Path(__file__).resolve().parents[4]
PLOTS_DIR = PROJECT_ROOT / "assets" / "plots"

class InvestmentNavigator:
    """
    Investment Navigator with live market and mutual fund data.
    """

    def __init__(self):
        pass

    def resolve_ticker(self, name: str) -> str:
        query = name.strip().lower().replace(" ", "")

        # --- Local fallback map ---
        fallback_map = {
            "reliance": "RELIANCE.NS",
            "tcs": "TCS.NS",
            "tatamotors": "TATAMOTORS.NS",
            "infosys": "INFY.NS",
            "hdfcbank": "HDFCBANK.NS",
            "icicibank": "ICICIBANK.NS",
            "sbi": "SBIN.NS",
            "hcl": "HCLTECH.NS",
            "wipro": "WIPRO.NS",
            "lt": "LT.NS",
            "itc": "ITC.NS",
            "tata steel": "TATASTEEL.NS",
            "adani ports": "ADANIPORTS.NS",
            "adani enterprises": "ADANIENT.NS",
            "adani power": "ADANIPOWER.NS",
            "adani total gas": "ATGL.NS",
            "adani green": "ADANIGREEN.NS",
            "zomato": "ZOMATO.NS",
            "nykaa": "NYKAA.NS",
            "hdfc life": "HDFCLIFE.NS",
            "axis bank": "AXISBANK.NS",
            "bajaj finance": "BAJFINANCE.NS",
            "maruti": "MARUTI.NS",
            "mahindra": "M&M.NS",
            "nestle": "NESTLEIND.NS",
            "hindustan unilever": "HINDUNILVR.NS",
            "asian paints": "ASIANPAINT.NS",
            "ultratech cement": "ULTRACEMCO.NS",
            "titan": "TITAN.NS",
            "coal india": "COALINDIA.NS",
            "ongc": "ONGC.NS",
            "indusind bank": "INDUSINDBK.NS",
            "ntpc": "NTPC.NS",
            "power grid": "POWERGRID.NS",
            "jsw steel": "JSWSTEEL.NS",
            "bharat petroleum": "BPCL.NS",
            "hindalco": "HINDALCO.NS",
            "cipla": "CIPLA.NS",
            "sun pharma": "SUNPHARMA.NS",
            "dr reddy": "DRREDDY.NS",
            "tvs motor": "TVSMOTOR.NS",
            "eicher motors": "EICHERMOT.NS",
            "divis labs": "DIVISLAB.NS",
            "tata power": "TATAPOWER.NS",
            "apollo hospitals": "APOLLOHOSP.NS",
            "kotak bank": "KOTAKBANK.NS"
        }

        # --- Try live Yahoo search first ---

        try:
            url = f"https://query2.finance.yahoo.com/v1/finance/search?q={query}"
            headers = {"User-Agent": "Mozilla/5.0"}  # ✅ Add this
            response = requests.get(url, headers=headers, timeout=5)
            data = response.json()

            if "quotes" in data and data["quotes"]:
                symbol = data["quotes"][0]["symbol"]
                print(f"[resolve_ticker] ✅ Yahoo found {symbol} for '{name}'")
                return symbol

        except Exception as e:
            print(f"[resolve_ticker] ⚠️ Yahoo lookup failed: {e}")

        # --- Fallback handling ---
        fallback_symbol = fallback_map.get(query)
        if fallback_symbol:
           print(f"[resolve_ticker] 🔁 Fallback used: {fallback_symbol}")
           return fallback_symbol

        guessed_symbol = query.upper() + ".NS"
        print(f"[resolve_ticker] 🧩 Guessing ticker: {guessed_symbol}")
        return guessed_symbol

    def get_stock_price(self, query: str) -> Dict[str, Any]:
        """
        Fetch live stock price by name or ticker.
        Example: 'Reliance' or 'TCS.NS' both work.
        """
        try:
            # Auto-resolve ticker from name
            ticker = self.resolve_ticker(query)
            print(f"[get_stock_price] 🔍 Checking {ticker} via Yahoo Finance...")

            stock = yf.Ticker(ticker)
            data = stock.history(period="5d")

            # ✅ Handle Yahoo failures and force NSE fallback
            if data is None or data.empty or "Close" not in data.columns or len(data["Close"].dropna()) < 2:
               print(f"[get_stock_price] ⚠️ Yahoo data unavailable for {ticker}, switching to NSE fallback...")
               nse_result = self.get_nse_price(ticker)

               # ✅ If NSE worked, return that
               if "error" not in nse_result:
                   return nse_result

               # 🚨 If NSE also failed, use Google as final fallback
               print(f"[get_stock_price] ⚠️ NSE fallback failed for {ticker}, switching to Google Finance...")
               google_result = self.get_google_price(ticker)
               return google_result
            
            # ✅ Defensive checks
            latest = data["Close"].dropna().iloc[-1]
            previous = data["Close"].dropna().iloc[-2]

            if np.isnan(latest) or np.isnan(previous):
               print(f"[get_stock_price] ⚠️ Invalid Yahoo price data for {ticker}, switching to NSE fallback...")
               nse_result = self.get_nse_price(ticker)
               if "error" not in nse_result:
                    return nse_result
               print(f"[get_stock_price] ⚠️ NSE fallback failed for {ticker}, switching to Google Finance...")
               return self.get_google_price(ticker)
            
            
            # ✅ Normal Yahoo path
            day_change = latest - previous
            day_change_percent = (day_change / previous) * 100
            trend = "Bullish" if day_change > 0 else "Bearish" if day_change < 0 else "Neutral"


            print(f"[get_stock_price] ✅ Yahoo Finance data fetched successfully for {ticker}")
            return {
            "ticker": ticker,
            "current_price": round(float(latest), 2),
            "previous_close": round(float(previous), 2),
            "day_change": round(float(day_change), 2),
            "day_change_percent": round(float(day_change_percent), 2),
            "trend": trend,
            "currency": "INR",
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "note": "Live data + analytics from Yahoo Finance",
            "source": "Yahoo Finance"
        }

        except Exception as e:
            print(f"[get_stock_price] ⚠️ Yahoo failed entirely, using NSE fallback for {query}. Error: {e}")
            nse_result = self.get_nse_price(ticker)
            if "error" not in nse_result:
                return nse_result
            print(f"[get_stock_price] ⚠️ NSE fallback failed for {ticker}, switching to Google Finance...")
            return self.get_google_price(ticker)
        
    def get_nse_price(self, symbol: str):
        """
        Fetch live stock price from NSE India API (robust version with cookie + header spoof).
        """
        try:
           symbol_enc = symbol.replace(".NS", "").upper()
           url = f"https://www.nseindia.com/api/quote-equity?symbol={symbol_enc}"

           headers = {
               "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:118.0) Gecko/20100101 Firefox/118.0",
               "Accept": "application/json, text/plain, */*",
               "Accept-Language": "en-US,en;q=0.9",
               "Referer": f"https://www.nseindia.com/get-quotes/equity?symbol={symbol_enc}",
               "Connection": "keep-alive",
               "Accept-Encoding": "gzip, deflate, br"
            }
            # ✅ Start a session and get initial cookies
           session = requests.Session()
           session.get("https://www.nseindia.com", headers=headers, timeout=10)

            # ✅ Now make the actual quote request
           response = session.get(url, headers=headers, timeout=10)

           if response.status_code == 200:
                try:
                   data = response.json()
                except ValueError:
                   return {"error": "NSE returned non-JSON data (likely blocked)", "ticker": symbol}

                price_info = data.get("priceInfo", {})
                if not price_info:
                   return {"error": f"NSE returned empty price data for {symbol}"}

                last_price = price_info.get("lastPrice")
                prev_close = price_info.get("previousClose")

                if last_price is None or prev_close is None:
                   return {"error": f"NSE missing key fields for {symbol}"}

                change = last_price - prev_close
                change_percent = (change / prev_close) * 100
                trend = "Bullish" if change > 0 else "Bearish" if change < 0 else "Neutral"

                print(f"[get_nse_price] ✅ NSE live data fetched successfully for {symbol_enc}")
                return {
                    "ticker": symbol_enc + ".NS",
                    "current_price": round(last_price, 2),
                    "previous_close": round(prev_close, 2),
                    "day_change": round(change, 2),
                    "day_change_percent": round(change_percent, 2),
                    "trend": trend,
                    "currency": "INR",
                    "note": "Live data from NSE India API",
                    "source": "NSE"
                }

           return {"error": f"NSE returned HTTP {response.status_code}", "ticker": symbol}

        except Exception as e:
            return {"error": f"NSE fallback failed: {str(e)}", "ticker": symbol}
    
    def get_google_price(self, symbol: str):
        """
        Fallback: Fetch live stock price from Google Finance (web-scraping method).
        Works for NSE, BSE, and global tickers.
        """
        try:
            import re
            from bs4 import BeautifulSoup

            # Clean symbol name
            symbol_enc = symbol.replace(".NS", "").replace(".BO", "").upper()

            # Build Google Finance URL
            url = f"https://www.google.com/finance/quote/{symbol_enc}:NSE"

            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
                "Accept-Language": "en-US,en;q=0.9",
            }

            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                return {"error": f"Google returned HTTP {response.status_code}", "ticker": symbol}

            # Parse HTML
            soup = BeautifulSoup(response.text, "html.parser")

            # Look for the current price span (Google's HTML pattern)
            price_tag = soup.find("div", {"class": "YMlKec"})
            if not price_tag:
                return {"error": f"Google Finance price not found for {symbol}"}

            current_price = float(re.sub(r"[^\d.]", "", price_tag.text))

            print(f"[get_google_price] ✅ Google Finance data fetched successfully for {symbol_enc}")

            return {
                "ticker": symbol_enc + ".NS",
                "current_price": current_price,
                "previous_close": None,
                "day_change": None,
                "day_change_percent": None,
                "trend": "N/A",
                "currency": "INR",
                "note": "Live data from Google Finance",
                "source": "Google Finance"
            }

        except Exception as e:
            return {"error": f"Google fallback failed: {e}", "ticker": symbol}

    

    def get_stock_analytics(self, ticker: str):
        """
        Fetch detailed stock analytics including returns, volatility, RSI, and trend indicators.
        """
        import pandas as pd

        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="6mo")

            if hist.empty or "Close" not in hist.columns:
               return {"error": "No data found for ticker", "ticker": ticker}

            # --- Calculate core metrics ---
            current_price = hist["Close"].iloc[-1]
            prev_close = hist["Close"].iloc[-2]
            day_change = current_price - prev_close
            day_change_percent = round((day_change / prev_close) * 100, 2)

            # --- Moving Averages ---
            sma_20 = round(hist["Close"].tail(20).mean(), 2)
            sma_50 = round(hist["Close"].tail(50).mean(), 2)

            # --- Volatility (annualized %)
            daily_returns = hist["Close"].pct_change().dropna()
            volatility = round(np.std(daily_returns) * np.sqrt(252) * 100, 2)

            # --- RSI Calculation (14-day)
            delta = hist["Close"].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = round(100 - (100 / (1 + rs.iloc[-1])), 2)

            # --- Returns ---
            def safe_return(period):
                if len(hist) > period:
                    return round(((hist["Close"].iloc[-1] - hist["Close"].iloc[-period]) / hist["Close"].iloc[-period]) * 100, 2)
                return None

            one_week_return = safe_return(5)
            one_month_return = safe_return(22)
            three_month_return = safe_return(66)

            # --- 52-week High/Low ---
            one_year = stock.history(period="1y")
            high_52w = one_year["Close"].max()
            low_52w = one_year["Close"].min()

            # --- Trend Summary ---
            if rsi > 70:
                trend_signal = "Overbought - Possible Bearish Reversal"
            elif rsi < 30:
                trend_signal = "Oversold - Possible Bullish Reversal"
            elif current_price > sma_20 > sma_50:
                trend_signal = "Strong Bullish Momentum"
            elif current_price < sma_20 < sma_50:
                trend_signal = "Strong Bearish Momentum"
            else:
                trend_signal = "Neutral / Sideways"

            # --- AI/LLM-Friendly Summary ---
            insight = (
                f"{ticker} is currently trading at ₹{round(current_price, 2)}. "
                f"The RSI is {rsi}, indicating {trend_signal.lower()}. "
                f"1-month return is {one_month_return}%, and volatility is {volatility}% annually."
            )

            result = {
                "ticker": ticker,
                "current_price": round(current_price, 2),
                "day_change_%": day_change_percent,
                "rsi": rsi,
                "sma_20": sma_20,
                "sma_50": sma_50,
                "volatility_%": volatility,
                "one_week_return_%": one_week_return,
                "one_month_return_%": one_month_return,
                "three_month_return_%": three_month_return,
                "52_week_high": round(high_52w, 2),
                "52_week_low": round(low_52w, 2),
                "trend_summary": trend_signal,
                "insight_summary": insight,
                "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            # ✅ Convert NumPy and pandas numeric types before returning
            for key, value in list(result.items()):
                if isinstance(value, (np.generic, np.float32, np.float64, np.int32, np.int64)):
                    result[key] = float(value)
                elif isinstance(value, (list, tuple)):
                    result[key] = [float(v) if isinstance(v, (np.generic, np.float32, np.float64, np.int32, np.int64)) else v for v in value]

            # --- 7-Day Forecast using ARIMA ---
            
            try:
                close_series = hist["Close"].dropna()
                if len(close_series) > 30:  # need at least 1 month of data
                    model = ARIMA(close_series, order=(2, 1, 2))
                    fitted = model.fit()
                    forecast = fitted.forecast(steps=7)
                    forecast_list = [round(float(x), 2) for x in forecast]

                    predicted_change = ((forecast_list[-1] - current_price) / current_price) * 100
                    predicted_trend = (
                        "Bullish" if predicted_change > 1
                        else "Bearish" if predicted_change < -1
                        else "Stable"
                    )

                    result["forecast_next_7d"] = forecast_list
                    result["predicted_change_%"] = round(predicted_change, 2)
                    result["predicted_trend"] = predicted_trend
                    result["forecast_confidence"] = "Moderate"
            except Exception as fe:
                result["forecast_error"] = str(fe)

            if "predicted_trend" in result:
                result["insight_summary"] += f" Based on ARIMA forecasting, the stock is expected to show a {result['predicted_trend'].lower()} trend over the next 7 days."

            # ✅ Final cleanup: convert NumPy numeric types (including ARIMA outputs)
            for k, v in list(result.items()):
                if isinstance(v, (np.generic, np.float32, np.float64, np.int32, np.int64)):
                    result[k] = float(v)
                elif isinstance(v, (list, tuple)):
                    result[k] = [
                    float(x) if isinstance(x, (np.generic, np.float32, np.float64, np.int32, np.int64)) else x
                    for x in v
                    ]

            try:
                PLOTS_DIR.mkdir(parents=True, exist_ok=True)

                plt.style.use("dark_background")  # 🌙 enable dark theme
                fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(11, 8), sharex=True, gridspec_kw={'height_ratios': [3, 1]})
                fig.suptitle(f"{ticker} — Price Trend, Forecast & RSI", fontsize=15, fontweight='bold', color='white')

                # --- Price chart (Top)
                ax1.plot(hist.index, hist["Close"], color='cyan', linewidth=2, label="Historical Price")
                ax1.plot(hist.index[-20:], hist["Close"].tail(20), color='orange', linestyle='--', label="Recent 20-Day Trend")

                if "forecast_next_7d" in result:
                    forecast_range = range(len(hist), len(hist) + 7)
                    ax1.plot(forecast_range, result["forecast_next_7d"], '--', color='lime', label="Forecast (7D)")

                ax1.axhline(result["sma_20"], color='deepskyblue', linestyle='--', linewidth=1, label="SMA-20")
                ax1.axhline(result["sma_50"], color='violet', linestyle='--', linewidth=1, label="SMA-50")

                ax1.set_ylabel("Price (₹)", color="white", fontsize=10)
                ax1.legend(loc="upper left", fontsize=9, facecolor="black", edgecolor="gray")
                ax1.grid(True, linestyle='--', alpha=0.3)

                # --- RSI chart (Bottom)
                ax2.plot(hist.index, 100 - (100 / (1 + (gain / loss))), label="RSI (14D)", color="magenta", linewidth=1.5)
                ax2.axhline(70, color='green', linestyle='--', linewidth=1, label="Overbought (70)")
                ax2.axhline(30, color='red', linestyle='--', linewidth=1, label="Oversold (30)")

                ax2.set_ylabel("RSI", color="white", fontsize=10)
                ax2.set_xlabel("Date", color="white", fontsize=10)
                ax2.legend(loc="upper left", fontsize=9, facecolor="black", edgecolor="gray")
                ax2.grid(True, linestyle='--', alpha=0.3)

                plt.xticks(rotation=45, color="white")
                plt.yticks(color="white")
                plt.tight_layout()

                plot_path = str(PLOTS_DIR / f"{ticker}_forecast_rsi_dark.png")
                # --- Add AI-generated caption at bottom ---
                ai_caption = (
                    f"AI Forecast: {result.get('predicted_trend', 'N/A')} trend expected over next 7 days "
                    f"({result.get('predicted_change_%', 0)}% change). "
                    f"Volatility: {result.get('volatility_%', 0)}% | RSI: {result.get('rsi', 0)}"
                )
                fig.text(0.5, 0.02, ai_caption, ha='center', fontsize=9, color='lightgray', style='italic')

                plt.savefig(plot_path, bbox_inches='tight', facecolor='black')
                plt.close()

                result["forecast_chart_path"] = plot_path
            except Exception as ce:
                result["chart_error"] = str(ce)


            return result  # 👈 stays at the very end

        except Exception as e:
            return {"error": str(e), "ticker": ticker}

    def get_mutual_fund_nav(self, scheme_name: str) -> Dict[str, Any]:
        """
        Fetch mutual fund NAV using mfapi.in
        Example: Parag Parikh Flexi Cap Fund
        """
        try:
            search_url = f"https://api.mfapi.in/mf/search?q={scheme_name}"
            search_response = requests.get(search_url).json()
            if not search_response:
                return {"error": f"No mutual fund found for '{scheme_name}'"}

            scheme_code = search_response[0]["schemeCode"]
            nav_url = f"https://api.mfapi.in/mf/{scheme_code}"
            nav_response = requests.get(nav_url).json()

            latest_nav = nav_response["data"][0]
            return {
                "scheme_name": nav_response["meta"]["scheme_name"],
                "latest_nav": latest_nav["nav"],
                "date": latest_nav["date"],
                "note": "Live NAV from mfapi.in"
            }
        except Exception as e:
            return {"error": str(e)}

    def portfolio_summary(self, user_id: str) -> Dict[str, Any]:
        """
        Dummy summary for now. Later link with MongoDB.
        """
        return {
            "user_id": user_id,
            "total_value": 0,
            "assets": {},
            "note": "To be implemented: pull user's holdings and compute live value"
        }
