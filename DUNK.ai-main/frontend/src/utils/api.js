/**
 * DUNK.ai API Client Bridge
 * Handles asynchronous HTTP networking with our FastAPI production backend.
 */

const BASE_URL = "http://localhost:8000/api/loans";

export const loanApi = {
  /**
   * Sends raw user financial metrics to the backend reducing balance calculation engine.
   */
  calculateReducingEMI: async (principal, annualRate, tenureYears, frequency = "monthly") => {
    try {
      const response = await fetch(`${BASE_URL}/emi/reducing`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          principal: parseFloat(principal),
          annual_rate: parseFloat(annualRate),
          tenure_years: parseFloat(tenureYears),
          repayment_frequency: frequency,
        }),
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || "Failed to calculate loan metrics.");
      }

      return await response.json();
    } catch (error) {
      console.error("Loan API Error [Reducing EMI]:", error);
      throw error;
    }
  },

  /**
   * Simulates capital prepayment impacts on outstanding loan horizons.
   */
  calculatePrepayment: async (payload) => {
    try {
      const response = await fetch(`${BASE_URL}/prepayment`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          principal: parseFloat(payload.principal),
          annual_rate: parseFloat(payload.annualRate),
          tenure_years: parseFloat(payload.tenureYears),
          repayment_frequency: payload.frequency || "monthly",
          payments_made: parseInt(payload.paymentsMade),
          prepayment_amount: parseFloat(payload.prepaymentAmount),
          interest_method: payload.interestMethod || "reducing",
          reduce_emi: payload.reduceEmi ?? true
        }),
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || "Failed to calculate prepayment impact.");
      }

      return await response.json();
    } catch (error) {
      console.error("Loan API Error [Prepayment]:", error);
      throw error;
    }
  },

  sendChatMessage: async (messageText, monthlyIncome = 100000) => {
    try {
      // Temporarily routing to a structured testing fallback or your upcoming /chat route
      // Let's use the explicit modify/emi or a universal chat endpoint if you have one.
      // For a direct test of text intent via backend, we'll hit your active endpoint wrapper:
      const response = await fetch(`http://localhost:8000/api/loans/modify/emi`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          principal: 5000000,          // Sample baseline parameters for testing
          annual_rate: 8.5,
          tenure_years: 20,
          repayment_frequency: "monthly",
          interest_method: "reducing",
          new_emi: parseFloat(messageText) || 45000 // Tries to read numeric entries directly
        }),
      });

      if (!response.ok) {
        const errData = await response.json();
        throw new Error(errData.detail || "Failed to process chat message.");
      }
      return await response.json();
    } catch (error) {
      console.error("Chat API Error:", error);
      throw error;
    }
  }
};
