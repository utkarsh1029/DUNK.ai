import { useState } from 'react';
import { Brain, Shield, MessageCircle, TrendingUp, Moon, Sun, User } from 'lucide-react';
import { useTheme } from '../contexts/ThemeContext';
import LoginModal from '../components/LoginModal';

const LandingPage = () => {
  const { theme, toggleTheme } = useTheme();
  const [showLoginModal, setShowLoginModal] = useState(false);

  const features = [
    {
      icon: <Brain className="w-8 h-8" />,
      title: 'Built on Google Gemini',
      description: 'I use Google\'s most advanced language model to reason, explain, and respond with smart financial insights — not just generic replies.'
    },
    {
      icon: <TrendingUp className="w-8 h-8" />,
      title: 'Connected to Fi Money',
      description: 'I access your real financial data through Fi\'s MCP — securely and with your consent — so I can give personalized answers that actually make sense.'
    },
    {
      icon: <MessageCircle className="w-8 h-8" />,
      title: 'Ask Me Anything (Money-Wise)',
      description: 'From "What\'s my credit score trend?" to "What if I lose my job?" — I\'m ready with answers, plans, and simulations.'
    },
    {
      icon: <Shield className="w-8 h-8" />,
      title: 'Protected by AI TrisM',
      description: 'I have built-in safeguards to avoid biased, unsafe, or misleading advice—because financial safety is serious.'
    }
  ];

  return (
    <div className="min-h-screen bg-gradient-to-br from-primary-light/20 via-white to-primary/10 dark:from-dark-bg dark:via-dark-bg dark:to-dark-card">
      {/* Header */}
      <header className="fixed top-0 w-full bg-white/80 dark:bg-dark-card/80 backdrop-blur-md border-b border-gray-200 dark:border-dark-border z-50">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="w-10 h-10 bg-primary rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-xl">D</span>
            </div>
            <span className="text-2xl font-bold text-gray-900 dark:text-white">Dunk.ai</span>
          </div>
          
          <div className="flex items-center space-x-4">
            <button 
              onClick={toggleTheme}
              className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-dark-bg transition-colors"
              aria-label="Toggle theme"
            >
              {theme === 'dark' ? (
                <Sun className="w-5 h-5 text-yellow-500" />
              ) : (
                <Moon className="w-5 h-5 text-gray-600" />
              )}
            </button>
            
            <button 
              onClick={() => setShowLoginModal(true)}
              className="flex items-center space-x-2 btn-primary"
            >
              <User className="w-4 h-4" />
              <span>Sign In</span>
            </button>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="pt-32 pb-20 px-6">
        <div className="max-w-7xl mx-auto">
          <div className="grid md:grid-cols-2 gap-12 items-center">
            {/* Left Side - Text */}
            <div className="space-y-8">
              <div className="inline-block px-4 py-2 bg-primary/10 dark:bg-primary/20 rounded-full">
                <span className="text-primary-dark dark:text-primary-light font-semibold">
                  Your Financial AI Agent
                </span>
              </div>
              
              <h1 className="text-5xl md:text-6xl font-bold text-gray-900 dark:text-white leading-tight">
                YOUR MONEY,
                <br />
                <span className="text-primary">OUR RESPONSIBILITY</span>
              </h1>
              
              <p className="text-xl text-gray-600 dark:text-gray-300 leading-relaxed">
                Meet Dunk, your intelligent financial advisor powered by Google Gemini. 
                Get personalized insights, smart recommendations, and complete financial clarity.
              </p>
              
              <div className="flex flex-col sm:flex-row gap-4">
                <button 
                  onClick={() => setShowLoginModal(true)}
                  className="btn-primary text-lg px-8 py-4"
                >
                  Get Started
                </button>
                <button className="btn-secondary text-lg px-8 py-4">
                  Learn More
                </button>
              </div>
            </div>

            {/* Right Side - Visual */}
            <div className="relative">
              <div className="card p-8 space-y-6">
                <div className="flex items-center space-x-3">
                  <div className="w-12 h-12 bg-gradient-to-br from-primary to-primary-dark rounded-full flex items-center justify-center">
                    <Brain className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <h3 className="font-bold text-lg">Hi, I'm Dunk</h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400">Your financial AI agent</p>
                  </div>
                </div>
                
                <div className="space-y-4">
                  <div className="p-4 bg-gray-50 dark:bg-dark-bg rounded-lg">
                    <p className="text-sm text-gray-600 dark:text-gray-300">
                      "What is my current SIP amount?"
                    </p>
                  </div>
                  
                  <div className="p-4 bg-primary/10 dark:bg-primary/20 rounded-lg">
                    <p className="text-sm text-gray-900 dark:text-gray-100">
                      Your current SIP amount is ₹ 2,5 crore.
                    </p>
                  </div>
                </div>

                {/* Decorative elements */}
                <div className="absolute -z-10 top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 bg-primary/20 dark:bg-primary/10 rounded-full blur-3xl"></div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-6 bg-white/50 dark:bg-dark-card/50">
        <div className="max-w-7xl mx-auto">
          <div className="text-center mb-16">
            <h2 className="text-4xl font-bold text-gray-900 dark:text-white mb-4">
              Why Choose Dunk?
            </h2>
            <p className="text-xl text-gray-600 dark:text-gray-300">
              Intelligent features designed for your financial success
            </p>
          </div>

          <div className="grid md:grid-cols-2 gap-8">
            {features.map((feature, index) => (
              <div key={index} className="card hover:shadow-lg transition-shadow">
                <div className="flex items-start space-x-4">
                  <div className="p-3 bg-primary/10 dark:bg-primary/20 rounded-xl text-primary">
                    {feature.icon}
                  </div>
                  <div className="flex-1">
                    <h3 className="text-xl font-bold text-gray-900 dark:text-white mb-2">
                      {feature.title}
                    </h3>
                    <p className="text-gray-600 dark:text-gray-300">
                      {feature.description}
                    </p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-6">
        <div className="max-w-4xl mx-auto text-center">
          <div className="card bg-gradient-to-br from-primary to-primary-dark text-white">
            <h2 className="text-3xl md:text-4xl font-bold mb-4">
              Ready to Take Control of Your Finances?
            </h2>
            <p className="text-xl mb-8 text-white/90">
              Join thousands of users who trust Dunk for their financial decisions
            </p>
            <button 
              onClick={() => setShowLoginModal(true)}
              className="bg-white text-primary hover:bg-gray-100 font-semibold py-4 px-8 rounded-full text-lg transition-all duration-200"
            >
              Start Your Journey
            </button>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-6 border-t border-gray-200 dark:border-dark-border">
        <div className="max-w-7xl mx-auto text-center text-gray-600 dark:text-gray-400">
          <p>&copy; 2025 Dunk.ai. All rights reserved. Your money, our responsibility.</p>
        </div>
      </footer>

      {/* Login Modal */}
      {showLoginModal && (
        <LoginModal onClose={() => setShowLoginModal(false)} />
      )}
    </div>
  );
};

export default LandingPage;

