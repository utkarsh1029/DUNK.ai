# backend/ai_engine/investment_ai.py

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import OllamaLLM

from dunk_ai.tools.investment_navigator.investment import InvestmentNavigator

class InvestmentAI:
    def __init__(self, model_name: str = "deepseek-r1:7b"):
        self.model = OllamaLLM(model=model_name)
        self.navigator = InvestmentNavigator()

    def generate_ai_insight(self, ticker: str):
        try:
            # Fetch data from existing analytics engine
            analytics = self.navigator.get_stock_analytics(ticker)

            if "error" in analytics:
                return {"error": analytics["error"]}
            # Create prompt template for the LLM
            prompt = ChatPromptTemplate.from_template("""
            You are a financial advisor. Based on the following stock analytics,
            provide a concise, professional insight in 3-4 sentences.

            Stock Data: {analytics}

            Your analysis should include:
            - The overall trend (bullish/bearish/stable)
            - Risk level and short-term outlook
            - A simple recommendation (hold/sell/buy)
            """)

            # Format prompt and generate response
            chain = prompt | self.model
            response = chain.invoke({"analytics": analytics})

            return {
                "ticker": ticker,
                "ai_insight": response.strip(),
                "model_used": "DeepSeek R1 via Ollama",
                "confidence": "High"
            }

        except Exception as e:
            return {"error": str(e), "ticker": ticker}
