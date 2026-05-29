import BaseChatLayout from './BaseChatLayout';
import { featurePrompts } from '../../utils/featurePrompts';
import { API_BASE_URL } from '../../config/api';

const currency = (value) =>
  new Intl.NumberFormat('en-IN', {
    style: 'currency',
    currency: 'INR',
    maximumFractionDigits: 0
  }).format(value);

const AnomalyWatchdogChat = ({ sidebarOpen, setSidebarOpen, user }) => {
  const category = {
    id: 'anomaly-watchdog',
    title: 'Anomaly Watchdog',
    description: 'Detect unusual transactions and patterns'
  };

  const prompts = featurePrompts['anomaly-watchdog'];

  /**
   * Helper utility to transmit verification payloads to our FastAPI route safely
   */
  const executeAnomalyDetection = async (currentTx, recentHistory = [], userProfiles = []) => {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/anomaly/detect`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          current_transaction: currentTx,
          recent_history: recentHistory,
          user_profiles: userProfiles
        })
      });

      if (!response.ok) {
        throw new Error('Backend failed to process transaction assessment matrices.');
      }
      return await response.json();
    } catch (error) {
      console.error('Watchdog API Error:', error);
      return null;
    }
  };

  const generateResponse = async (userInput) => {
    const lowerInput = userInput.toLowerCase();
    const now = new Date();

    // Baseline User Profiles for Z-Score Standard Deviations
    const defaultProfiles = [
      { category: 'shopping', average_spend: 3000, standard_deviation: 1500 },
      { category: 'food', average_spend: 600, standard_deviation: 250 },
      { category: 'entertainment', average_spend: 800, standard_deviation: 300 }
    ];

    // SCENARIO 1: High Spikes / Unusual Volume
    // SCENARIO 1: High Spikes / Unusual Volume
    if (lowerInput.includes('unusual') || lowerInput.includes('suspicious') || lowerInput.includes('large')) {
      const simulatedTx = {
        transaction_id: 'tx_9921',
        amount: 25000,
        category: 'shopping',
        timestamp: now.toISOString(),
        merchant: 'XYZ Premium Store'
      };

      const result = await executeAnomalyDetection(simulatedTx, [], defaultProfiles);
      if (!result) return '⚠️ Security module offline. Verify your Python backend is running.';

      const reasonsList = result.reasons.map(r => `• ${r}`).join('\n');
      return `🔍 Real-Time Transaction Risk Analysis:\n\n` +
             `• Merchant: ${simulatedTx.merchant}\n` +
             `• Amount: ${currency(simulatedTx.amount)}\n` +
             `• Risk Security Score: ${result.risk_score}/100\n` +
             `• Status: ${result.is_anomaly ? '🚨 ANOMALY FLAGGED' : '✅ SECURE'}\n\n` +
             `⚡ Trigger Manifest:\n${reasonsList || '• No volatile parameters triggered.'}\n\n` +
             `Recommendation: If you do not recognize this activity, freeze your card instantly within the account dashboard container.`;
    }

    // SCENARIO 2: Velocity / Double Swipe Charges (THE ONE IN YOUR SCREENSHOT 🎯)
    if (lowerInput.includes('duplicate')) {
      const currentTx = {
        transaction_id: 'tx_5541',
        amount: 450,
        category: 'food',
        timestamp: now.toISOString(),
        merchant: 'Swiggy'
      };

      const doubleTapTime = new Date(now.getTime() - 120000);
      const recentHistory = [{
        transaction_id: 'tx_5540',
        amount: 450,
        category: 'food',
        timestamp: doubleTapTime.toISOString(),
        merchant: 'Swiggy'
      }];

      const result = await executeAnomalyDetection(currentTx, recentHistory, defaultProfiles);
      if (!result) return '⚠️ Security module offline.';

      const reasonsList = result.reasons.map(r => `• ${r}`).join('\n');
      return `🔄 Duplicate Velocity Analysis:\n\n` +
             `• Merchant: ${currentTx.merchant}\n` +
             `• Current Charge: ${currency(currentTx.amount)}\n` +
             `• Risk Security Score: ${result.risk_score}/100\n\n` +
             `⚡ System Diagnostics:\n${reasonsList}\n\n` +
             `💡 Tip: Contact the merchant or bank support with the transaction details above to request a direct credit adjustment refund.`;
    }

    // SCENARIO 3: Suspect Temporal (Late Night Spending)
    if (lowerInput.includes('fraud') || lowerInput.includes('identify') || lowerInput.includes('late night')) {
      const lateNightTime = new Date();
      lateNightTime.setHours(3, 15, 0);

      const simulatedTx = {
        transaction_id: 'tx_7721',
        amount: 12000,
        category: 'entertainment',
        timestamp: lateNightTime.toISOString(),
        merchant: 'NightClub Elite'
      };

      const result = await executeAnomalyDetection(simulatedTx, [], defaultProfiles);
      if (!result) return '⚠️ Security module offline.';

      const reasonsList = result.reasons.map(r => `• ${r}`).join('\n');
      return `🛡️ Off-Peak Fraud Risk Audit:\n\n` +
             `• Merchant: ${simulatedTx.merchant}\n` +
             `• Amount: ${currency(simulatedTx.amount)}\n` +
             `• Execution Window: ${lateNightTime.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})} (Off-Peak Hours)\n` +
             `• Risk Security Score: ${result.risk_score}/100\n\n` +
             `⚡ Trigger Manifest:\n${reasonsList}\n\n` +
             `Would you like me to help enforce time-window locks on high-value offline vendor categories?`;
    }

    // Default Fallback Guide
    return 'I monitor your transaction streams 24/7 for unusual category deviations, duplicate high-velocity swiping, and off-peak anomalies. \n\nTry asking me: \n• *"Check for duplicates"* \n• *"Show me unusual transactions"*';
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