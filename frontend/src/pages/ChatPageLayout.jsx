import { useState } from 'react';
import { 
  Menu, X, Plus, Moon, Sun, User, LogOut, 
  Settings, Brain, History, BarChart3
} from 'lucide-react';
import { useTheme } from '../contexts/ThemeContext';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';
import CategorySelector from '../components/CategorySelector';
import AnalyticsDashboard from '../components/AnalyticsDashboard';
import ExploreSidebar from '../components/ExploreSidebar';

const ChatPageLayout = ({ children, category }) => {
  const { theme, toggleTheme } = useTheme();
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [exploreOpen, setExploreOpen] = useState(false);
  const [analyticsOpen, setAnalyticsOpen] = useState(false);
  const [categorySelector, setCategorySelector] = useState(false);
  const [chatHistory, setChatHistory] = useState([]);

  // Load chat history
  const loadChatHistory = () => {
    const savedHistory = localStorage.getItem('dunk-chat-history');
    if (savedHistory) {
      const history = JSON.parse(savedHistory);
      // Filter by current category
      const filtered = category 
        ? history.filter(chat => chat.category?.id === category.id)
        : history;
      setChatHistory(filtered);
    }
  };

  // Start new chat
  const startNewChat = () => {
    setCategorySelector(true);
  };

  // Handle logout
  const handleLogout = () => {
    logout();
    navigate('/');
  };

  // Handle prompt selection
  const handlePromptSelect = (prompt) => {
    // This will be passed to child component
    setExploreOpen(false);
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
            {category ? `${category.title} Chats` : 'Recent Chats'}
          </div>
          {chatHistory.length === 0 && (
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
                  {category ? category.title : 'Hi, I\'m Dunk, your financial AI agent'}
                </h1>
                {category && (
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    {category.description}
                  </p>
                )}
              </div>
            </div>
            
            <div className="flex items-center space-x-2">
              {category && (
                <button 
                  onClick={() => navigate('/chat')}
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

        {/* Chat Content - Rendered by children */}
        {children({ sidebarOpen, setSidebarOpen, user })}
      </div>

      {/* Category Selector Modal */}
      {categorySelector && (
        <CategorySelector 
          onClose={() => setCategorySelector(false)}
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

export default ChatPageLayout;

