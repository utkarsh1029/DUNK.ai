import BaseChatLayout from './BaseChatLayout';
import { featurePrompts } from '../../utils/featurePrompts';
import { API_BASE_URL } from '../../config/api';

const fallbackTickerMap = {
  reliance: 'RELIANCE.NS',
  tcs: 'TCS.NS',
  tatagold: 'TATAGOLD.NS',
  suzlon: 'SUZLON.NS',
  tatamotors: 'TATAMOTORS.NS',
  infosys: 'INFY.NS',
  hdfcbank: 'HDFCBANK.NS',
  icicibank: 'ICICIBANK.NS',
  sbi: 'SBIN.NS',
  wipro: 'WIPRO.NS',
  itc: 'ITC.NS',
  hdfc: 'HDFCBANK.NS',
  kotak: 'KOTAKBANK.NS',
  axis: 'AXISBANK.NS',
  tata: 'TCS.NS',
  mahindra: 'M&M.NS'
};

const currency = (value) =>
  new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 2
  }).format(value);

const detectTicker = (input) => {
  const explicit = input.match(/([A-Z]{2,10}\.NS)/i);
  if (explicit) return explicit[1].toUpperCase();

  const tokens = input
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, ' ')
    .split(/\s+/);

  for (const token of tokens) {
    if (fallbackTickerMap[token]) {
      return fallbackTickerMap[token];
    }
  }

  const capitalised = input.match(/\b([A-Z]{3,8})\b/);
  if (capitalised) return `${capitalised[1].toUpperCase()}.NS`;

  return 'TCS.NS';
};

const fetchJson = async (url) => {
  try {
    const response = await fetch(url);
    if (!response.ok) {
      const body = await response.json().catch(() => ({}));
      throw new Error(body.detail ?? 'Unable to fetch investment data.');
    }
    return response.json();
  } catch (error) {
    // Re-throw with more context if needed
    if (error instanceof Error) {
      throw error;
    }
    throw new Error('Network error: Unable to fetch investment data.');
  }
};

const InvestmentNavigatorChat = ({ sidebarOpen, setSidebarOpen, user }) => {
  const category = {
    id: 'investment-navigator',
    title: 'Investment Navigator',
    description: 'Discover new investment opportunities'
  };

  const prompts = featurePrompts['investment-navigator'];

  const formatStockAnalytics = (data) => {
    if (!data || !data.ticker) {
      return 'Unable to format stock analytics: missing data.';
    }
    const returns = ['one_week_return_%', 'one_month_return_%', 'three_month_return_%']
      .map((key) => (data[key] != null ? `${key.replace(/_/g, ' ')}: ${data[key]}%` : null))
      .filter(Boolean)
      .join('\n');

    return `Analytics for ${data.ticker}:\n• Price: ${currency(
      data.current_price || 0
    )}\n• Day change: ${data['day_change_%'] ?? 'N/A'}%\n• RSI: ${data.rsi ?? 'N/A'}\n• SMA20/SMA50: ${data.sma_20 ?? 'N/A'} / ${data.sma_50 ?? 'N/A'}\n• Volatility: ${data['volatility_%'] ?? 'N/A'}%\n• 52w range: ${currency(
      data['52_week_low'] || 0
    )} - ${currency(data['52_week_high'] || 0)}\n${returns ? `\n${returns}` : ''}\nTrend: ${
      data.trend_summary || 'N/A'
    }\nInsight: ${data.insight_summary || 'N/A'}`;
  };

  const generateResponse = async (userInput) => {
    const lowerInput = userInput.toLowerCase();

    if (lowerInput.includes('mutual') || lowerInput.includes('nav')) {
      const schemeMatch = userInput.match(/(?:for|of)\s+([A-Za-z\s]+)$/i);
      const scheme =
        (schemeMatch ? schemeMatch[1] : userInput).trim() || 'Parag Parikh Flexi Cap';
      const params = new URLSearchParams({ scheme });
      const data = await fetchJson(
        `${API_BASE_URL}/api/investment/mutual-fund?${params.toString()}`
      );
      return `Latest NAV for ${data.scheme_name || scheme}:\n• NAV: ₹${data.latest_nav || 'N/A'}\n• Date: ${data.date || 'N/A'}\nSource: ${data.note || 'N/A'}`;
    }

    const ticker = detectTicker(userInput);

    if (lowerInput.includes('price') || lowerInput.includes('live')) {
      const data = await fetchJson(
        `${API_BASE_URL}/api/investment/price/${encodeURIComponent(ticker)}`
      );
      return `Live snapshot for ${data.ticker || ticker} (${data.source || 'Unknown'}):\n• Current price: ${currency(
        data.current_price || 0
      )}\n• Previous close: ${currency(
        data.previous_close || data.current_price || 0
      )}\n• Intraday change: ${data.day_change_percent ?? 'N/A'}%\nTrend: ${data.trend || 'N/A'}`;
    }

    if (lowerInput.includes('insight') || lowerInput.includes('summary')) {
      const data = await fetchJson(
        `${API_BASE_URL}/api/investment/ai_insight/${encodeURIComponent(ticker)}`
      );
      return `AI insight for ${data.ticker || ticker} (${data.provider || data.model_used || 'Unknown'}):\n${data.ai_insight || 'No insight available.'}`;
    }

    if (lowerInput.includes('chart') || lowerInput.includes('plot') || lowerInput.includes('forecast')) {
      const data = await fetchJson(
        `${API_BASE_URL}/api/investment/plot/${encodeURIComponent(ticker)}`
      );
      let chartPath = data.chart_path || '';
      const assetsIndex = chartPath.indexOf('/assets/');
      if (assetsIndex >= 0) {
        chartPath = chartPath.slice(assetsIndex);
      }
      const absolutePath = chartPath.startsWith('http')
        ? chartPath
        : `${API_BASE_URL.replace(/\/$/, '')}/${chartPath.replace(/^\//, '')}`;
      return {
        type: 'image',
        url: absolutePath,
        caption: `Forecast chart for ${ticker} (confidence: ${data.forecast_confidence || 'N/A'})`
      };
    }

    const analytics = await fetchJson(
      `${API_BASE_URL}/api/investment/stock/${encodeURIComponent(ticker)}`
    );
    const aiInsight = await fetchJson(
      `${API_BASE_URL}/api/investment/ai_insight/${encodeURIComponent(ticker)}`
    );

    return `${formatStockAnalytics(analytics)}\n\nAI says:\n${aiInsight.ai_insight}`;
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

export default InvestmentNavigatorChat;

