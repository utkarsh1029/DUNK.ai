import { useState, useEffect, useRef } from 'react';
import { 
  Menu, X, Send, Plus, Moon, Sun, User, LogOut, 
  Settings, Brain, History, ChevronRight, Paperclip, Smile, BarChart3
} from 'lucide-react';
import { useTheme } from '../contexts/ThemeContext';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import ExploreSidebar from '../components/ExploreSidebar';
import CategorySelector from '../components/CategorySelector';
import AnalyticsDashboard from '../components/AnalyticsDashboard';
import { featurePrompts } from '../utils/featurePrompts';

const ChatPage = () => {
  const { theme, toggleTheme } = useTheme();
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [exploreOpen, setExploreOpen] = useState(false);
  const [analyticsOpen, setAnalyticsOpen] = useState(false);
  const [categorySelector, setCategorySelector] = useState(false);
  const [currentCategory, setCurrentCategory] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [chatHistory, setChatHistory] = useState([]);
  const [currentChatId, setCurrentChatId] = useState(null);
  const messagesEndRef = useRef(null);

  // Load chat history from localStorage
  useEffect(() => {
    try {
      const savedHistory = localStorage.getItem('dunk-chat-history');
      if (savedHistory) {
        setChatHistory(JSON.parse(savedHistory));
      }
    } catch (error) {
      // If parsing fails, start with empty history
      setChatHistory([]);
    }
  }, []);

  // Save chat history to localStorage
  useEffect(() => {
    if (chatHistory.length > 0) {
      try {
        localStorage.setItem('dunk-chat-history', JSON.stringify(chatHistory));
      } catch (error) {
        // Silently fail if localStorage is unavailable
      }
    }
  }, [chatHistory]);

  // Auto scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Handle sending message
  const handleSend = async () => {
    if (!input.trim()) return;

    const now = Date.now();
    const timestamp = new Date().toISOString();
    
    const userMessage = {
      id: now,
      role: 'user',
      content: input,
      timestamp
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');

    // Simulate AI response
    setTimeout(() => {
      const aiResponse = generateAIResponse(input);
      const aiMessage = {
        id: now + 1,
        role: 'assistant',
        content: aiResponse,
        timestamp
      };
      setMessages(prev => [...prev, aiMessage]);

      // Update chat history with latest messages
      const updatedMessages = [...messages, userMessage, aiMessage];
      updateChatHistory(updatedMessages);
    }, 1000);
  };

  // Generate AI response based on input
  const generateAIResponse = (userInput) => {
    const lowerInput = userInput.toLowerCase();
    
    if (lowerInput.includes('sip')) {
      return 'Based on your current financial data, your total SIP amount is ₹2.5 crore. You have active SIPs across 5 mutual funds with an average return of 12.5% over the last 3 years. Would you like me to analyze your portfolio composition?';
    } else if (lowerInput.includes('loan') || lowerInput.includes('afford')) {
      return 'Based on your current monthly income of ₹78,000 and existing obligations, your safe EMI range is ₹20,000-₹25,000. A ₹50L loan over 20 years at 8.5% interest would cost ~₹43,400/month — which exceeds your healthy limit. Recommendation: Lower the loan amount to ₹30L or increase down payment.';
    } else if (lowerInput.includes('expense') || lowerInput.includes('spending')) {
      return 'I\'ve analyzed your spending patterns. Your top categories are: Food & Dining (35%), Shopping (25%), and Entertainment (15%). You\'re spending 12% more than last month. I recommend setting up spending alerts for dining expenses.';
    } else if (lowerInput.includes('emergency') || lowerInput.includes('fund')) {
      return 'I\'ve checked your available sources: Liquid Mutual Funds: ₹78,000, Savings Account: ₹34,000, Fixed Deposit (withdrawable): ₹1L. You can meet the amount by combining FDs + MFs. Tip: Avoid breaking the PPF — it has a high long-term return.';
    } else if (lowerInput.includes('investment') || lowerInput.includes('portfolio')) {
      return 'Your current portfolio allocation: Equity (60%), Debt (25%), Gold (10%), Cash (5%). Based on your risk profile and goals, this is well-balanced. However, I recommend increasing your debt allocation by 5% for better stability.';
    } else {
      return 'I understand you\'re asking about your finances. I have access to your real financial data through Fi\'s MCP and can help you with personalized insights about SIPs, loans, expenses, emergency funds, investments, and more. How can I assist you specifically?';
    }
  };

  // Update chat history
  const updateChatHistory = (currentMessages) => {
    if (!currentMessages || currentMessages.length === 0) return;

    const firstMessage = currentMessages[0];
    const chatTitle = (firstMessage?.content || '').slice(0, 50) + '...';
    const chatData = {
      id: currentChatId || Date.now(),
      title: chatTitle,
      messages: currentMessages,
      category: currentCategory,
      timestamp: new Date().toISOString()
    };

    setChatHistory(prev => {
      const existingIndex = prev.findIndex(chat => chat.id === chatData.id);
      if (existingIndex >= 0) {
        const updated = [...prev];
        updated[existingIndex] = chatData;
        return updated;
      }
      return [chatData, ...prev];
    });

    if (!currentChatId) {
      setCurrentChatId(chatData.id);
    }
  };

  // Start new chat
  const startNewChat = () => {
    setCategorySelector(true);
  };

  // Handle category selection
  const handleCategorySelect = (category) => {
    setCurrentCategory(category);
    setMessages([]);
    setCurrentChatId(null);
    setCategorySelector(false);
    setSidebarOpen(false);
  };

  // Load chat from history
  const loadChat = (chat) => {
    setMessages(chat.messages);
    setCurrentChatId(chat.id);
    setCurrentCategory(chat.category);
    setSidebarOpen(false);
  };

  // Get filtered chat history by category
  const filteredChatHistory = currentCategory 
    ? chatHistory.filter(chat => chat.category?.id === currentCategory.id)
    : chatHistory;

  // Handle prompt selection
  const handlePromptSelect = (prompt) => {
    setInput(prompt);
    setExploreOpen(false);
  };

  // Handle logout
  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <div className="flex h-screen bg-gray-50 dark:bg-dark-bg">
      {/* History Sidebar */}
      <div className={`${sidebarOpen ? 'w-64' : 'w-0'} transition-all duration-300 overflow-hidden bg-white dark:bg-dark-card border-r border-gray-200 dark:border-dark-border flex flex-col`}>
        <div className="p-4 border-b border-gray-200 dark:border-dark-border">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-primary rounded-lg flex items-center justify-center">
                <span className="text-white font-bold">D</span>
              </div>
              <span className="font-bold text-gray-900 dark:text-white">Dunk.ai</span>
            </div>
            <button 
              onClick={() => setSidebarOpen(false)}
              className="p-1 hover:bg-gray-100 dark:hover:bg-dark-bg rounded"
            >
              <X className="w-5 h-5" />
            </button>
          </div>
          
          <button 
            onClick={startNewChat}
            className="w-full btn-primary flex items-center justify-center space-x-2"
          >
            <Plus className="w-4 h-4" />
            <span>New Chat</span>
          </button>
        </div>

        {/* Chat History */}
        <div className="flex-1 overflow-y-auto p-2">
          <div className="text-xs font-semibold text-gray-500 dark:text-gray-400 px-2 py-2 flex items-center">
            <History className="w-4 h-4 mr-2" />
            {currentCategory ? `${currentCategory.title} Chats` : 'Recent Chats'}
          </div>
          {filteredChatHistory.map(chat => (
            <button
              key={chat.id}
              onClick={() => loadChat(chat)}
              className={`w-full text-left p-3 rounded-lg hover:bg-gray-100 dark:hover:bg-dark-bg transition-colors mb-1 ${
                currentChatId === chat.id ? 'bg-gray-100 dark:bg-dark-bg' : ''
              }`}
            >
              <div className="text-sm font-medium text-gray-900 dark:text-white truncate">
                {chat.title}
              </div>
              <div className="flex items-center justify-between text-xs text-gray-500 dark:text-gray-400">
                <span>{new Date(chat.timestamp).toLocaleDateString()}</span>
                {chat.category && (
                  <span className="text-xs px-2 py-0.5 bg-primary/10 text-primary rounded">
                    {chat.category.title.split(' ')[0]}
                  </span>
                )}
              </div>
            </button>
          ))}
          {filteredChatHistory.length === 0 && (
            <div className="text-center text-sm text-gray-500 dark:text-gray-400 py-8">
              No chats yet in this category
            </div>
          )}
        </div>

        {/* User Profile Section */}
        <div className="p-4 border-t border-gray-200 dark:border-dark-border">
          <div className="flex items-center space-x-3 mb-3">
            <div className="w-10 h-10 bg-primary/20 rounded-full flex items-center justify-center">
              <User className="w-5 h-5 text-primary" />
            </div>
            <div className="flex-1 min-w-0">
              <div className="text-sm font-medium text-gray-900 dark:text-white truncate">
                {user?.name || 'User'}
              </div>
              <div className="text-xs text-gray-500 dark:text-gray-400 truncate">
                {user?.phone}
              </div>
            </div>
          </div>
          
          <div className="flex space-x-2">
            <button 
              onClick={() => navigate('/profile')}
              className="flex-1 p-2 hover:bg-gray-100 dark:hover:bg-dark-bg rounded-lg transition-colors"
              title="Settings"
            >
              <Settings className="w-4 h-4 mx-auto" />
            </button>
            <button 
              onClick={toggleTheme}
              className="flex-1 p-2 hover:bg-gray-100 dark:hover:bg-dark-bg rounded-lg transition-colors"
              title="Toggle theme"
            >
              {theme === 'dark' ? (
                <Sun className="w-4 h-4 mx-auto text-yellow-500" />
              ) : (
                <Moon className="w-4 h-4 mx-auto" />
              )}
            </button>
            <button 
              onClick={handleLogout}
              className="flex-1 p-2 hover:bg-red-50 dark:hover:bg-red-900/20 text-red-600 rounded-lg transition-colors"
              title="Logout"
            >
              <LogOut className="w-4 h-4 mx-auto" />
            </button>
          </div>
        </div>
      </div>

      {/* Main Chat Area */}
      <div className="flex-1 flex flex-col">
        {/* Header */}
        <div className="bg-white dark:bg-dark-card border-b border-gray-200 dark:border-dark-border p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              {!sidebarOpen && (
                <button 
                  onClick={() => setSidebarOpen(true)}
                  className="p-2 hover:bg-gray-100 dark:hover:bg-dark-bg rounded-lg"
                >
                  <Menu className="w-5 h-5" />
                </button>
              )}
              <div>
                <h1 className="text-xl font-bold text-gray-900 dark:text-white">
                  {currentCategory ? currentCategory.title : (messages.length > 0 ? 'Chat' : 'Hi, I\'m Dunk, your financial AI agent')}
                </h1>
                {currentCategory && (
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    {currentCategory.description}
                  </p>
                )}
              </div>
            </div>
            
            <div className="flex items-center space-x-2">
              {currentCategory && (
                <button 
                  onClick={() => {
                    setCurrentCategory(null);
                    setMessages([]);
                    setCurrentChatId(null);
                  }}
                  className="btn-secondary text-sm"
                >
                  All Categories
                </button>
              )}
              <button 
                onClick={() => setAnalyticsOpen(true)}
                className="btn-secondary flex items-center space-x-2"
              >
                <BarChart3 className="w-4 h-4" />
                <span>Analytics</span>
              </button>
              <button 
                onClick={() => setExploreOpen(true)}
                className="btn-secondary flex items-center space-x-2"
              >
                <Brain className="w-4 h-4" />
                <span>Explore</span>
              </button>
            </div>
          </div>
        </div>

        {/* Messages Area */}
        <div className="flex-1 overflow-y-auto p-6">
          {messages.length === 0 ? (
            /* Welcome Screen */
            <div className="max-w-3xl mx-auto text-center py-12">
              {/* Avatar with Glowing Effect */}
              <div className="relative w-48 h-48 mx-auto mb-8">
                {/* Outer glow circles */}
                <div className="absolute inset-0 rounded-full border-2 border-primary/30 animate-pulse"></div>
                <div className="absolute inset-4 rounded-full border-2 border-primary/50"></div>
                <div className="absolute inset-8 rounded-full border-2 border-primary/70"></div>
                
                {/* Avatar container */}
                <div className="absolute inset-12 bg-gradient-to-br from-primary/20 to-primary-dark/20 rounded-full flex items-center justify-center backdrop-blur-sm">
                  {/* You can replace this with: <img src="/images/avatar.png" alt="Dunk AI" className="w-full h-full object-cover rounded-full" /> */}
                  <Brain className="w-16 h-16 text-primary" />
                </div>
                
                {/* Decorative elements */}
                <div className="absolute -top-2 left-1/4 w-3 h-3 bg-primary rounded-full animate-pulse"></div>
                <div className="absolute top-8 -right-2 w-2 h-2 bg-primary-light rounded-full animate-pulse delay-100"></div>
                <div className="absolute bottom-12 -left-3 w-2.5 h-2.5 bg-primary rounded-full animate-pulse delay-200"></div>
              </div>
              
              <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
                Hi {user?.name?.split(' ')[0]}, How can I help you?
              </h2>
              {currentCategory ? (
                <p className="text-gray-600 dark:text-gray-400 mb-8">
                  Ask me anything about {currentCategory.title.toLowerCase()}
                </p>
              ) : (
                <p className="text-gray-600 dark:text-gray-400 mb-8">
                  I can help you with portfolio management, expense tracking, loans, emergency funds, and investment advice.
                </p>
              )}
              
              {/* Quick Prompts */}
              {currentCategory ? (
                /* Category-specific prompts */
                <div className="grid md:grid-cols-2 gap-4 mt-8">
                  {featurePrompts[currentCategory.id]?.map((prompt, index) => (
                    <button
                      key={index}
                      onClick={() => handlePromptSelect(prompt)}
                      className="card text-left hover:shadow-lg transition-all group"
                    >
                      <div className="flex items-start justify-between">
                        <p className="text-sm text-gray-700 dark:text-gray-300 flex-1">
                          {prompt}
                        </p>
                        <ChevronRight className="w-5 h-5 text-gray-400 group-hover:text-primary transition-colors flex-shrink-0" />
                      </div>
                    </button>
                  ))}
                </div>
              ) : (
                /* General prompts */
                <div className="grid md:grid-cols-2 gap-4 mt-8">
                  {Object.entries(featurePrompts).slice(0, 4).map(([feature, prompts]) => (
                    <button
                      key={feature}
                      onClick={() => handlePromptSelect(prompts[0])}
                      className="card text-left hover:shadow-lg transition-all group"
                    >
                      <div className="flex items-start justify-between">
                        <div className="flex-1">
                          <h3 className="font-semibold text-gray-900 dark:text-white mb-2">
                            {feature.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ')}
                          </h3>
                          <p className="text-sm text-gray-600 dark:text-gray-400">
                            {prompts[0]}
                          </p>
                        </div>
                        <ChevronRight className="w-5 h-5 text-gray-400 group-hover:text-primary transition-colors" />
                      </div>
                    </button>
                  ))}
                </div>
              )}
            </div>
          ) : (
            /* Messages */
            <div className="max-w-3xl mx-auto space-y-6">
              {messages.map(message => (
                <div 
                  key={message.id}
                  className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                >
                  <div className={`flex space-x-3 max-w-[80%] ${message.role === 'user' ? 'flex-row-reverse space-x-reverse' : ''}`}>
                    <div className={`w-8 h-8 rounded-full flex items-center justify-center flex-shrink-0 ${
                      message.role === 'user' 
                        ? 'bg-primary' 
                        : 'bg-gradient-to-br from-primary to-primary-dark'
                    }`}>
                      {message.role === 'user' ? (
                        <User className="w-4 h-4 text-white" />
                      ) : (
                        <Brain className="w-4 h-4 text-white" />
                      )}
                    </div>
                    <div className={`rounded-2xl p-4 ${
                      message.role === 'user'
                        ? 'bg-primary text-white'
                        : 'bg-white dark:bg-dark-card border border-gray-200 dark:border-dark-border'
                    }`}>
                      <p className={`text-sm leading-relaxed ${
                        message.role === 'user' ? 'text-white' : 'text-gray-900 dark:text-gray-100'
                      }`}>
                        {message.content}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
              <div ref={messagesEndRef} />
            </div>
          )}
        </div>

        {/* Input Area */}
        <div className="bg-white dark:bg-dark-card border-t border-gray-200 dark:border-dark-border p-4">
          <div className="max-w-3xl mx-auto">
            <form onSubmit={(e) => { e.preventDefault(); handleSend(); }} className="flex items-end space-x-3">
              <div className="flex-1 relative">
                <textarea
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  onKeyDown={(e) => {
                    if (e.key === 'Enter' && !e.shiftKey) {
                      e.preventDefault();
                      handleSend();
                    }
                  }}
                  placeholder="Ask me anything about your finances..."
                  rows="1"
                  className="input resize-none pr-20"
                  style={{ minHeight: '48px', maxHeight: '120px' }}
                />
                <div className="absolute right-2 bottom-2 flex space-x-2">
                  <button 
                    type="button"
                    className="p-2 hover:bg-gray-100 dark:hover:bg-dark-bg rounded-lg transition-colors"
                  >
                    <Paperclip className="w-4 h-4 text-gray-400" />
                  </button>
                  <button 
                    type="button"
                    className="p-2 hover:bg-gray-100 dark:hover:bg-dark-bg rounded-lg transition-colors"
                  >
                    <Smile className="w-4 h-4 text-gray-400" />
                  </button>
                </div>
              </div>
              <button 
                type="submit"
                disabled={!input.trim()}
                className="btn-primary p-3 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                <Send className="w-5 h-5" />
              </button>
            </form>
            <p className="text-xs text-gray-500 dark:text-gray-400 text-center mt-2">
              Dunk can make mistakes. Please verify important information.
            </p>
          </div>
        </div>
      </div>

      {/* Category Selector Modal */}
      {categorySelector && (
        <CategorySelector 
          onClose={() => setCategorySelector(false)}
          onSelectCategory={handleCategorySelect}
        />
      )}

      {/* Analytics Dashboard Modal */}
      {analyticsOpen && (
        <AnalyticsDashboard onClose={() => setAnalyticsOpen(false)} />
      )}

      {/* Explore Sidebar */}
      {exploreOpen && (
        <ExploreSidebar 
          onClose={() => setExploreOpen(false)}
          onPromptSelect={handlePromptSelect}
        />
      )}
    </div>
  );
};

export default ChatPage;

