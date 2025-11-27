import BaseChatLayout from './BaseChatLayout';
import { featurePrompts } from '../../utils/featurePrompts';
import { API_BASE_URL } from '../../config/api';

const currency = (value) =>
  new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0
  }).format(value);

const parseAmount = (input, keywords) => {
  for (const keyword of keywords) {
    const regex = new RegExp(`${keyword}\\D*(₹|rs\\.?|rupees)?\\s*([\\d,]+)`, 'i');
    const match = input.match(regex);
    if (match) {
      return Number(match[2].replace(/,/g, ''));
    }
  }
  return undefined;
};

const parsePercentage = (input) => {
  const match = input.match(/(\d{1,2})\s*%/);
  return match ? Number(match[1]) / 100 : undefined;
};

const SmartExpenseCoachChat = ({ sidebarOpen, setSidebarOpen, user }) => {
  const category = {
    id: 'smart-expense-coach',
    title: 'Smart Expense Coach',
    description: 'Get insights on your spending patterns'
  };

  const prompts = featurePrompts['smart-expense-coach'];

  const buildPayload = (userInput) => {
    const lower = userInput.toLowerCase();

    const salary =
      parseAmount(userInput, ['salary', 'income', 'monthly']) || 80000;
    const rent = parseAmount(userInput, ['rent']) || 20000;
    const emi = parseAmount(userInput, ['emi', 'loan']) || 15000;
    const plannedSavings = parseAmount(userInput, ['save', 'savings']) || 10000;
    const ratio =
      parsePercentage(userInput) ||
      (lower.includes('savings ratio') ? 0.25 : undefined);

    return {
      monthly_salary: salary,
      rent,
      emi,
      planned_savings: ratio ? null : plannedSavings,
      savings_ratio: ratio ?? null,
      age: parseAmount(userInput, ['age']) || 30,
      occupation: user?.occupation || 'Professional',
      city_tier: /tier[_-\s]?2/i.test(userInput)
        ? 'Tier_2'
        : /tier[_-\s]?3/i.test(userInput)
          ? 'Tier_3'
          : 'Tier_1'
    };
  };

  const formatPlan = (plan) => {
    const { fixed_expenses, savings_guidance, allocations } = plan;
    const allocationLines = Object.entries(allocations)
      .map(
        ([categoryName, amount]) =>
          `• ${categoryName.replace(/_/g, ' ')}: ${currency(amount)}`
      )
      .join('\n');

    return `Here is your personalised expense plan:\n\nSalary: ${currency(
      plan.salary
    )}\nSpendable income: ${currency(plan.spendable_income)}\nPlanned savings: ${currency(
      plan.planned_savings
    )}\nDisposable income: ${currency(plan.disposable_income)}\n\nFixed expenses:\n• Rent: ${currency(
      fixed_expenses.rent
    )}\n• EMI: ${currency(
      fixed_expenses.emi
    )}\n\nSavings guardrails:\n• Minimum 20%: ${currency(
      savings_guidance.minimum_20_percent
    )}\n• Recommended 25%: ${currency(
      savings_guidance.recommended_25_percent
    )}\n• Strong 30%: ${currency(
      savings_guidance.strong_30_percent
    )}\n\nSuggested allocations:\n${allocationLines}\n\nModel: ${
      plan.model_metadata.loaded ? 'AI-driven plan' : 'Rule-based fallback'
    }`;
  };

  const generateResponse = async (userInput) => {
    const payload = buildPayload(userInput);
    const response = await fetch(`${API_BASE_URL}/api/expense/plan`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });

    if (!response.ok) {
      const errorBody = await response.json().catch(() => ({}));
      throw new Error(
        errorBody.detail?.[0]?.msg || 'Unable to generate plan right now.'
      );
    }

    const data = await response.json();
    return formatPlan(data);
  };

  return (
    <BaseChatLayout
      category={category}
      prompts={prompts}
      generateResponse={generateResponse}
      sidebarOpen={sidebarOpen}
      setSidebarOpen={setSidebarOpen}
      user={user}
    />
  );
};

export default SmartExpenseCoachChat;

