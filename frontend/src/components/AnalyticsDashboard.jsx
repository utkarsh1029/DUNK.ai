import { X, TrendingUp, TrendingDown, Wallet, PiggyBank, CreditCard, BarChart3, DollarSign, AlertCircle } from 'lucide-react';

const AnalyticsDashboard = ({ onClose }) => {
  // Dummy data for analytics
  const metrics = [
    {
      title: 'Total Portfolio Value',
      value: '₹2.5 Cr',
      change: '+12.5%',
      trend: 'up',
      icon: <TrendingUp className="w-6 h-6" />,
      color: 'text-green-600 dark:text-green-400',
      bgColor: 'bg-green-500/10'
    },
    {
      title: 'Monthly Expenses',
      value: '₹45,230',
      change: '+8.2%',
      trend: 'up',
      icon: <Wallet className="w-6 h-6" />,
      color: 'text-orange-600 dark:text-orange-400',
      bgColor: 'bg-orange-500/10'
    },
    {
      title: 'Savings This Month',
      value: '₹32,770',
      change: '+15.3%',
      trend: 'up',
      icon: <PiggyBank className="w-6 h-6" />,
      color: 'text-blue-600 dark:text-blue-400',
      bgColor: 'bg-blue-500/10'
    },
    {
      title: 'Active Loans EMI',
      value: '₹18,500',
      change: '-5.2%',
      trend: 'down',
      icon: <CreditCard className="w-6 h-6" />,
      color: 'text-purple-600 dark:text-purple-400',
      bgColor: 'bg-purple-500/10'
    }
  ];

  const investments = [
    { name: 'Equity Mutual Funds', value: 60, amount: '₹1.5 Cr', color: 'bg-blue-500' },
    { name: 'Debt Funds', value: 25, amount: '₹62.5 L', color: 'bg-green-500' },
    { name: 'Gold', value: 10, amount: '₹25 L', color: 'bg-yellow-500' },
    { name: 'Cash & Others', value: 5, amount: '₹12.5 L', color: 'bg-gray-500' }
  ];

  const recentTransactions = [
    { type: 'Credit', description: 'Salary Credited', amount: '₹78,000', date: 'Oct 10, 2025', icon: <DollarSign className="w-4 h-4" />, color: 'text-green-600' },
    { type: 'Debit', description: 'Rent Payment', amount: '₹15,000', date: 'Oct 09, 2025', icon: <TrendingDown className="w-4 h-4" />, color: 'text-red-600' },
    { type: 'Debit', description: 'Grocery Shopping', amount: '₹4,230', date: 'Oct 08, 2025', icon: <TrendingDown className="w-4 h-4" />, color: 'text-red-600' },
    { type: 'Credit', description: 'Mutual Fund Returns', amount: '₹12,500', date: 'Oct 07, 2025', icon: <DollarSign className="w-4 h-4" />, color: 'text-green-600' }
  ];

  const alerts = [
    { type: 'warning', message: 'Credit card payment due in 3 days', icon: <AlertCircle className="w-5 h-5" /> },
    { type: 'info', message: 'You exceeded your dining budget by 12%', icon: <TrendingUp className="w-5 h-5" /> }
  ];

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4 overflow-y-auto">
      <div className="bg-white dark:bg-dark-card rounded-2xl max-w-7xl w-full max-h-[95vh] overflow-y-auto shadow-2xl my-4">
        {/* Header */}
        <div className="sticky top-0 bg-white dark:bg-dark-card border-b border-gray-200 dark:border-dark-border p-6 z-10">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-3xl font-bold text-gray-900 dark:text-white flex items-center">
                <BarChart3 className="w-8 h-8 mr-3 text-primary" />
                Financial Analytics
              </h2>
              <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                Your complete financial overview and insights
              </p>
            </div>
            <button 
              onClick={onClose}
              className="p-2 hover:bg-gray-100 dark:hover:bg-dark-bg rounded-lg transition-colors"
            >
              <X className="w-6 h-6" />
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* Key Metrics Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {metrics.map((metric, index) => (
              <div key={index} className="card hover:shadow-lg transition-shadow">
                <div className="flex items-start justify-between mb-3">
                  <div className={`${metric.bgColor} p-3 rounded-xl ${metric.color}`}>
                    {metric.icon}
                  </div>
                  <span className={`text-sm font-semibold ${metric.trend === 'up' ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'}`}>
                    {metric.change}
                  </span>
                </div>
                <h3 className="text-2xl font-bold text-gray-900 dark:text-white mb-1">
                  {metric.value}
                </h3>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  {metric.title}
                </p>
              </div>
            ))}
          </div>

          <div className="grid lg:grid-cols-3 gap-6">
            {/* Portfolio Allocation */}
            <div className="lg:col-span-2 card">
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4 flex items-center">
                <BarChart3 className="w-5 h-5 mr-2 text-primary" />
                Portfolio Allocation
              </h3>
              <div className="space-y-4">
                {investments.map((investment, index) => (
                  <div key={index}>
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                        {investment.name}
                      </span>
                      <span className="text-sm font-semibold text-gray-900 dark:text-white">
                        {investment.amount} ({investment.value}%)
                      </span>
                    </div>
                    <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3 overflow-hidden">
                      <div 
                        className={`h-full ${investment.color} transition-all duration-500`}
                        style={{ width: `${investment.value}%` }}
                      ></div>
                    </div>
                  </div>
                ))}
              </div>
              
              {/* Summary */}
              <div className="mt-6 pt-4 border-t border-gray-200 dark:border-dark-border">
                <div className="flex items-center justify-between">
                  <span className="font-semibold text-gray-900 dark:text-white">Total Portfolio</span>
                  <span className="text-xl font-bold text-primary">₹2.5 Crore</span>
                </div>
              </div>
            </div>

            {/* Alerts & Notifications */}
            <div className="card">
              <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4 flex items-center">
                <AlertCircle className="w-5 h-5 mr-2 text-orange-500" />
                Alerts
              </h3>
              <div className="space-y-3">
                {alerts.map((alert, index) => (
                  <div 
                    key={index}
                    className={`p-4 rounded-lg ${
                      alert.type === 'warning' 
                        ? 'bg-orange-50 dark:bg-orange-900/20 border border-orange-200 dark:border-orange-800' 
                        : 'bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800'
                    }`}
                  >
                    <div className="flex items-start space-x-3">
                      <div className={alert.type === 'warning' ? 'text-orange-600 dark:text-orange-400' : 'text-blue-600 dark:text-blue-400'}>
                        {alert.icon}
                      </div>
                      <p className="text-sm text-gray-700 dark:text-gray-300 flex-1">
                        {alert.message}
                      </p>
                    </div>
                  </div>
                ))}
              </div>

              {/* Quick Stats */}
              <div className="mt-6 space-y-3">
                <div className="flex items-center justify-between p-3 bg-primary/5 rounded-lg">
                  <span className="text-sm text-gray-700 dark:text-gray-300">Credit Score</span>
                  <span className="font-bold text-primary">780</span>
                </div>
                <div className="flex items-center justify-between p-3 bg-green-500/5 rounded-lg">
                  <span className="text-sm text-gray-700 dark:text-gray-300">Emergency Fund</span>
                  <span className="font-bold text-green-600 dark:text-green-400">₹2.5L</span>
                </div>
                <div className="flex items-center justify-between p-3 bg-blue-500/5 rounded-lg">
                  <span className="text-sm text-gray-700 dark:text-gray-300">Monthly SIP</span>
                  <span className="font-bold text-blue-600 dark:text-blue-400">₹25,000</span>
                </div>
              </div>
            </div>
          </div>

          {/* Recent Transactions */}
          <div className="card">
            <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4 flex items-center">
              <Wallet className="w-5 h-5 mr-2 text-primary" />
              Recent Transactions
            </h3>
            <div className="space-y-3">
              {recentTransactions.map((transaction, index) => (
                <div 
                  key={index}
                  className="flex items-center justify-between p-4 hover:bg-gray-50 dark:hover:bg-dark-bg rounded-lg transition-colors"
                >
                  <div className="flex items-center space-x-4">
                    <div className={`p-2 rounded-lg ${transaction.color} bg-gray-100 dark:bg-dark-bg`}>
                      {transaction.icon}
                    </div>
                    <div>
                      <p className="font-medium text-gray-900 dark:text-white">
                        {transaction.description}
                      </p>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        {transaction.date}
                      </p>
                    </div>
                  </div>
                  <div className={`text-right`}>
                    <p className={`font-bold ${transaction.color}`}>
                      {transaction.type === 'Debit' ? '-' : '+'}{transaction.amount}
                    </p>
                    <p className="text-xs text-gray-500 dark:text-gray-400">
                      {transaction.type}
                    </p>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Spending by Category */}
          <div className="card">
            <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-4">
              Spending by Category (This Month)
            </h3>
            <div className="grid md:grid-cols-3 gap-4">
              {[
                { category: 'Food & Dining', amount: '₹15,830', percentage: 35, color: 'bg-red-500' },
                { category: 'Shopping', amount: '₹11,307', percentage: 25, color: 'bg-purple-500' },
                { category: 'Entertainment', amount: '₹6,784', percentage: 15, color: 'bg-pink-500' },
                { category: 'Transportation', amount: '₹4,523', percentage: 10, color: 'bg-blue-500' },
                { category: 'Bills & Utilities', amount: '₹4,523', percentage: 10, color: 'bg-yellow-500' },
                { category: 'Others', amount: '₹2,261', percentage: 5, color: 'bg-gray-500' }
              ].map((item, index) => (
                <div key={index} className="p-4 bg-gray-50 dark:bg-dark-bg rounded-lg">
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-sm font-medium text-gray-700 dark:text-gray-300">
                      {item.category}
                    </span>
                    <span className="text-xs text-gray-500 dark:text-gray-400">
                      {item.percentage}%
                    </span>
                  </div>
                  <p className="text-lg font-bold text-gray-900 dark:text-white mb-2">
                    {item.amount}
                  </p>
                  <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                    <div 
                      className={`h-full ${item.color} rounded-full transition-all duration-500`}
                      style={{ width: `${item.percentage}%` }}
                    ></div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AnalyticsDashboard;

