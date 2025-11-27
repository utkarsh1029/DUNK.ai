import BaseChatLayout from './BaseChatLayout';
import { featurePrompts } from '../../utils/featurePrompts';

const EmergencyFundAssistanceChat = ({ sidebarOpen, setSidebarOpen, user }) => {
  const category = {
    id: 'emergency-fund-assistance',
    title: 'Emergency Fund Assistance',
    description: 'Plan and manage your emergency funds'
  };

  const prompts = featurePrompts['emergency-fund-assistance'];

  const generateResponse = (userInput) => {
    const lowerInput = userInput.toLowerCase();
    
    if (lowerInput.includes('2l') || lowerInput.includes('urgently')) {
      return 'I\'ve checked your available liquid sources for ₹2L:\n\n💰 Available:\n• Liquid Mutual Funds: ₹78,000 (1-2 days)\n• Savings Account: ₹34,000 (Instant)\n• Fixed Deposit (withdrawable): ₹1,00,000 (Same day)\n\n✅ Solution: Combine FDs (₹1L) + Liquid MFs (₹78,000) + Savings (₹22,000)\n\n⚠️ Tip: Avoid breaking PPF (₹3.5L) — it has high long-term returns and penalties.';
    } else if (lowerInput.includes('liquid') || lowerInput.includes('assets')) {
      return 'Your liquid assets breakdown:\n\n🟢 Instant access:\n• Savings Account: ₹34,000\n• Emergency Credit Line: ₹50,000\n\n🟡 1-2 days:\n• Liquid Mutual Funds: ₹78,000\n• FD (withdrawable): ₹1,00,000\n\n🔵 3-7 days:\n• Debt Mutual Funds: ₹62,500\n\nTotal liquid: ₹3,24,500';
    } else if (lowerInput.includes('how much') || lowerInput.includes('emergency fund')) {
      return 'Your current emergency fund: ₹2,50,000\n\nRecommended emergency fund:\n• 6 months of expenses: ₹2,70,000 (6 × ₹45,000)\n• Status: 93% of target ✅\n\nYou need ₹20,000 more to reach the ideal emergency corpus. Consider increasing your monthly savings by ₹2,000.';
    } else if (lowerInput.includes('break') && (lowerInput.includes('fd') || lowerInput.includes('fixed'))) {
      return 'FD Breaking Analysis:\n\nYour FD: ₹1L @ 7.5% (18 months remaining)\n\nIf you break now:\n• Penalty: 1% (₹1,000)\n• Interest loss: ~₹9,000\n• Net loss: ₹10,000\n\n💡 Alternative: Take a loan against FD:\n• Rate: 8.5%\n• No interest loss\n• No penalty\n• Better option! ✅';
    } else if (lowerInput.includes('build')) {
      return '6-month emergency fund plan:\n\nTarget: ₹2,70,000 (6 × ₹45,000)\nCurrent: ₹2,50,000\nGap: ₹20,000\n\n📅 3-month plan:\n• Month 1-3: Save ₹7,000/month\n• Reduce dining: ₹2,000\n• Skip entertainment: ₹1,500\n• Other savings: ₹3,500\n\nYou\'ll reach your target by January 2026! 🎯';
    } else {
      return 'I can help you find emergency funds quickly, analyze liquid assets, plan emergency corpus, and suggest the best sources without penalties. What do you need help with?';
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

export default EmergencyFundAssistanceChat;

