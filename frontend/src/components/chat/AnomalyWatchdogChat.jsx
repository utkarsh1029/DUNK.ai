import BaseChatLayout from './BaseChatLayout';
import { featurePrompts } from '../../utils/featurePrompts';

const AnomalyWatchdogChat = ({ sidebarOpen, setSidebarOpen, user }) => {
  const category = {
    id: 'anomaly-watchdog',
    title: 'Anomaly Watchdog',
    description: 'Detect unusual transactions and patterns'
  };

  const prompts = featurePrompts['anomaly-watchdog'];

  const generateResponse = (userInput) => {
    const lowerInput = userInput.toLowerCase();
    
    if (lowerInput.includes('unusual') || lowerInput.includes('suspicious')) {
      return '🔍 Unusual transactions detected:\n\n⚠️ High Priority:\n• Oct 10: ₹25,000 to "XYZ Store" (3x your avg purchase)\n• Oct 8: ₹15,000 international transaction (unusual pattern)\n\n⚡ Medium Priority:\n• Oct 12: 3 consecutive ATM withdrawals (₹10K each)\n• Oct 11: Late night transaction at 2:30 AM\n\nRecommendation: Review these transactions and report if unrecognized.';
    } else if (lowerInput.includes('large') || lowerInput.includes('alert')) {
      return '💰 Large spending alerts (Last 7 days):\n\n1. Oct 12: ₹45,000 - "Electronics Store"\n   • 450% above avg electronics spend\n   • Flagged: High value\n\n2. Oct 10: ₹25,000 - "Fashion Retail"\n   • 312% above avg shopping\n\n3. Oct 9: ₹18,000 - "Restaurant"\n   • Single largest dining transaction\n\nTotal unusual spending: ₹88,000 (194% of weekly average)';
    } else if (lowerInput.includes('duplicate')) {
      return '🔄 Duplicate charges detected:\n\n1. Netflix Subscription:\n   • Oct 1: ₹799\n   • Oct 3: ₹799 (Duplicate!)\n\n2. Swiggy Order #4523:\n   • Oct 8: ₹450\n   • Oct 8: ₹450 (Same day duplicate)\n\nTotal duplicate charges: ₹2,048\n💡 Tip: Contact merchants for refund. I can help you draft the request.';
    } else if (lowerInput.includes('subscription') || lowerInput.includes('recurring')) {
      return '📱 Your recurring subscriptions (Monthly):\n\n✅ Active:\n• Netflix: ₹799\n• Spotify: ₹119\n• Amazon Prime: ₹299\n• Gym: ₹2,000\n• Magazine: ₹500\n\n⚠️ Unused (Last 3 months):\n• Adobe Creative: ₹1,680 💸\n• Gaming Pass: ₹699 💸\n\nPotential savings: ₹2,379/month by canceling unused subscriptions!';
    } else if (lowerInput.includes('fraud') || lowerInput.includes('identify')) {
      return '🛡️ Fraud detection analysis:\n\n✅ Your account is secure.\n\n⚡ Recent suspicious patterns:\n• 3 transactions from new locations\n• 1 international transaction (first time)\n• 2 large purchases (above pattern)\n\nRecommendations:\n1. Enable 2-factor authentication\n2. Set transaction limits\n3. Enable location-based alerts\n4. Review linked devices\n\nWould you like me to help set these up?';
    } else {
      return 'I monitor your transactions 24/7 for unusual patterns, duplicate charges, fraudulent activity, and unused subscriptions. What would you like me to check?';
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

export default AnomalyWatchdogChat;

