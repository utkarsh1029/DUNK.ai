import BaseChatLayout from './BaseChatLayout';
import { featurePrompts } from '../../utils/featurePrompts';

const PortfolioManagerChat = ({ sidebarOpen, setSidebarOpen, user }) => {
  const category = {
    id: 'portfolio-manager',
    title: 'Portfolio Manager',
    description: 'Track and optimize your investment portfolio'
  };

  const prompts = featurePrompts['portfolio-manager'];

  const generateResponse = (userInput) => {
    const lowerInput = userInput.toLowerCase();
    
    if (lowerInput.includes('sip') || lowerInput.includes('current')) {
      return 'Based on your current financial data, your total SIP amount is ₹2.5 crore. You have active SIPs across 5 mutual funds with an average return of 12.5% over the last 3 years. Would you like me to analyze your portfolio composition?';
    } else if (lowerInput.includes('breakdown') || lowerInput.includes('allocation')) {
      return 'Your portfolio allocation: Equity Mutual Funds (60% - ₹1.5 Cr), Debt Funds (25% - ₹62.5 L), Gold (10% - ₹25 L), Cash & Others (5% - ₹12.5 L). This is a well-balanced portfolio for your risk profile.';
    } else if (lowerInput.includes('performing') || lowerInput.includes('performance')) {
      return 'Your mutual funds are performing well! Top 3 performers: \n1. Axis Bluechip Fund: +18.2% (1 year)\n2. HDFC Index Fund: +15.8% (1 year)\n3. SBI Small Cap Fund: +22.5% (1 year)\nOverall portfolio return: +12.5% (3-year avg)';
    } else if (lowerInput.includes('return') || lowerInput.includes('roi')) {
      return 'Your overall investment returns: 1-year return: +14.2%, 3-year return: +12.5%, 5-year return: +10.8%. You\'ve outperformed the market by 2.3% on average!';
    } else if (lowerInput.includes('rebalanc')) {
      return 'Portfolio rebalancing suggestion: Your equity allocation has grown to 65% (target: 60%). Consider moving ₹12.5L from equity to debt funds to maintain optimal risk balance. Would you like specific fund recommendations?';
    } else {
      return 'I can help you with portfolio analysis, SIP tracking, fund performance, returns calculation, and rebalancing strategies. What would you like to know about your investments?';
    }
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

export default PortfolioManagerChat;

