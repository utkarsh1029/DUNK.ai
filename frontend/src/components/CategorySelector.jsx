import { X, TrendingUp, Wallet, AlertTriangle, Calculator, Shield, BarChart3 } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const CategorySelector = ({ onClose, onSelectCategory }) => {
  const navigate = useNavigate();
  const categories = [
    {
      id: 'portfolio-manager',
      icon: <TrendingUp className="w-6 h-6" />,
      title: 'Portfolio Manager',
      description: 'Track and optimize your investment portfolio',
      color: 'bg-blue-500',
      textColor: 'text-blue-600 dark:text-blue-400'
    },
    {
      id: 'smart-expense-coach',
      icon: <Wallet className="w-6 h-6" />,
      title: 'Smart Expense Coach',
      description: 'Get insights on your spending patterns',
      color: 'bg-green-500',
      textColor: 'text-green-600 dark:text-green-400'
    },
    {
      id: 'emergency-fund-assistance',
      icon: <Shield className="w-6 h-6" />,
      title: 'Emergency Fund Assistance',
      description: 'Plan and manage your emergency funds',
      color: 'bg-red-500',
      textColor: 'text-red-600 dark:text-red-400'
    },
    {
      id: 'loan-clarity-engine',
      icon: <Calculator className="w-6 h-6" />,
      title: 'Loan Clarity Engine',
      description: 'Calculate and understand loan affordability',
      color: 'bg-purple-500',
      textColor: 'text-purple-600 dark:text-purple-400'
    },
    {
      id: 'anomaly-watchdog',
      icon: <AlertTriangle className="w-6 h-6" />,
      title: 'Anomaly Watchdog',
      description: 'Detect unusual transactions and patterns',
      color: 'bg-orange-500',
      textColor: 'text-orange-600 dark:text-orange-400'
    },
    {
      id: 'investment-navigator',
      icon: <BarChart3 className="w-6 h-6" />,
      title: 'Investment Navigator',
      description: 'Discover new investment opportunities',
      color: 'bg-teal-500',
      textColor: 'text-teal-600 dark:text-teal-400'
    }
  ];

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-white dark:bg-dark-card rounded-2xl max-w-4xl w-full max-h-[90vh] overflow-y-auto shadow-2xl">
        {/* Header */}
        <div className="sticky top-0 bg-white dark:bg-dark-card border-b border-gray-200 dark:border-dark-border p-6 z-10">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                Select a Category
              </h2>
              <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                Choose the financial feature you want to chat about
              </p>
            </div>
            <button 
              onClick={onClose}
              className="p-2 hover:bg-gray-100 dark:hover:bg-dark-bg rounded-lg transition-colors"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
        </div>

        {/* Categories Grid */}
        <div className="p-6 grid md:grid-cols-2 gap-4">
          {categories.map(category => (
            <button
              key={category.id}
              onClick={() => {
                onClose();
                navigate(`/chat/${category.id}`);
              }}
              className="card text-left hover:shadow-xl transition-all group hover:scale-[1.02] border-2 border-transparent hover:border-primary"
            >
              <div className="flex items-start space-x-4">
                <div className={`${category.color} p-4 rounded-xl text-white flex-shrink-0`}>
                  {category.icon}
                </div>
                <div className="flex-1 min-w-0">
                  <h3 className={`font-bold text-lg mb-2 ${category.textColor}`}>
                    {category.title}
                  </h3>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    {category.description}
                  </p>
                </div>
              </div>
            </button>
          ))}
        </div>
      </div>
    </div>
  );
};

export default CategorySelector;

