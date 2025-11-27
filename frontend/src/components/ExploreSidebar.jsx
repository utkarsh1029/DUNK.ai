import { X, TrendingUp, Wallet, AlertTriangle, Calculator, Shield, BarChart3 } from 'lucide-react';
import { featurePrompts } from '../utils/featurePrompts';

const ExploreSidebar = ({ onClose, onPromptSelect }) => {
  const features = [
    {
      id: 'portfolio-manager',
      icon: <TrendingUp className="w-5 h-5" />,
      title: 'Portfolio Manager',
      description: 'Track and optimize your investment portfolio',
      color: 'text-blue-600 dark:text-blue-400'
    },
    {
      id: 'smart-expense-coach',
      icon: <Wallet className="w-5 h-5" />,
      title: 'Smart Expense Coach',
      description: 'Get insights on your spending patterns',
      color: 'text-green-600 dark:text-green-400'
    },
    {
      id: 'emergency-fund-assistance',
      icon: <Shield className="w-5 h-5" />,
      title: 'Emergency Fund Assistance',
      description: 'Plan and manage your emergency funds',
      color: 'text-red-600 dark:text-red-400'
    },
    {
      id: 'loan-clarity-engine',
      icon: <Calculator className="w-5 h-5" />,
      title: 'Loan Clarity Engine',
      description: 'Calculate and understand loan affordability',
      color: 'text-purple-600 dark:text-purple-400'
    },
    {
      id: 'anomaly-watchdog',
      icon: <AlertTriangle className="w-5 h-5" />,
      title: 'Anomaly Watchdog',
      description: 'Detect unusual transactions and patterns',
      color: 'text-orange-600 dark:text-orange-400'
    },
    {
      id: 'investment-navigator',
      icon: <BarChart3 className="w-5 h-5" />,
      title: 'Investment Navigator',
      description: 'Discover new investment opportunities',
      color: 'text-teal-600 dark:text-teal-400'
    }
  ];

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex justify-end">
      <div className="w-full max-w-md bg-white dark:bg-dark-card h-full overflow-y-auto shadow-2xl">
        {/* Header */}
        <div className="sticky top-0 bg-white dark:bg-dark-card border-b border-gray-200 dark:border-dark-border p-6 z-10">
          <div className="flex items-center justify-between">
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
              Explore
            </h2>
            <button 
              onClick={onClose}
              className="p-2 hover:bg-gray-100 dark:hover:bg-dark-bg rounded-lg transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
          <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
            Choose a feature to get started with personalized prompts
          </p>
        </div>

        {/* Features List */}
        <div className="p-6 space-y-6">
          {features.map(feature => (
            <div key={feature.id} className="space-y-3">
              {/* Feature Header */}
              <div className="flex items-start space-x-3">
                <div className={`p-3 bg-gray-100 dark:bg-dark-bg rounded-xl ${feature.color}`}>
                  {feature.icon}
                </div>
                <div className="flex-1">
                  <h3 className="font-bold text-gray-900 dark:text-white">
                    {feature.title}
                  </h3>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    {feature.description}
                  </p>
                </div>
              </div>

              {/* Prompts for this feature */}
              <div className="ml-14 space-y-2">
                {featurePrompts[feature.id]?.map((prompt, index) => (
                  <button
                    key={index}
                    onClick={() => onPromptSelect(prompt)}
                    className="w-full text-left p-3 rounded-lg bg-gray-50 dark:bg-dark-bg hover:bg-gray-100 dark:hover:bg-gray-800 transition-colors border border-gray-200 dark:border-dark-border"
                  >
                    <p className="text-sm text-gray-700 dark:text-gray-300">
                      {prompt}
                    </p>
                  </button>
                ))}
              </div>
            </div>
          ))}
        </div>

        {/* Footer Info */}
        <div className="p-6 border-t border-gray-200 dark:border-dark-border bg-primary/5 dark:bg-primary/10">
          <div className="flex items-start space-x-3">
            <div className="w-10 h-10 bg-primary/20 rounded-lg flex items-center justify-center flex-shrink-0">
              <Shield className="w-5 h-5 text-primary" />
            </div>
            <div>
              <h4 className="font-semibold text-gray-900 dark:text-white mb-1">
                Protected by AI TrisM
              </h4>
              <p className="text-xs text-gray-600 dark:text-gray-400">
                All responses are verified for safety and accuracy to ensure you receive trustworthy financial advice.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ExploreSidebar;

