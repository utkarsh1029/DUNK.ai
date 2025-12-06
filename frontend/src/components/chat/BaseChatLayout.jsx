import { useState, useEffect, useRef } from 'react';
import { 
  Menu, X, Send, User, Brain, ChevronRight, Paperclip, Smile
} from 'lucide-react';

const BaseChatLayout = ({ 
  category, 
  prompts, 
  generateResponse, 
  sidebarOpen, 
  setSidebarOpen,
  user,
  children 
}) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [currentChatId, setCurrentChatId] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Auto scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Handle sending message
  const handleSend = async (messageOverride) => {
    const content = (messageOverride ?? input).trim();
    if (!content || isLoading) return;
    
    const userMessage = {
      id: Date.now(),
      role: 'user',
      content,
      timestamp: new Date().toISOString()
    };

    const placeholderMessage = {
      id: Date.now() + 1,
      role: 'assistant',
      content: 'Analyzing your request...',
      timestamp: new Date().toISOString()
    };

    const optimisticMessages = [...messages, userMessage, placeholderMessage];
    setMessages(optimisticMessages);
    if (!messageOverride) {
      setInput('');
    }
    setIsLoading(true);

    try {
      const aiResponse = await generateResponse(content, optimisticMessages);
      const finalMessages = optimisticMessages.map((message) =>
        message.id === placeholderMessage.id
          ? typeof aiResponse === 'object'
            ? {
                ...message,
                content: aiResponse.caption || 'Chart generated.',
                attachment: aiResponse.url
              }
            : { ...message, content: aiResponse || 'I could not generate a response.' }
          : message
      );
      setMessages(finalMessages);
      saveChatHistory(finalMessages);
    } catch (error) {
      const errorMessage = optimisticMessages.map((message) =>
        message.id === placeholderMessage.id
          ? { ...message, content: `⚠️ ${error.message || 'Something went wrong.'}` }
          : message
      );
      setMessages(errorMessage);
      saveChatHistory(errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  // Save chat history
  const saveChatHistory = (currentMessages) => {
    if (currentMessages.length === 0) return;

    const chatTitle = currentMessages[0].content.slice(0, 50) + '...';
    const chatData = {
      id: currentChatId || Date.now(),
      title: chatTitle,
      messages: currentMessages,
      category: category,
      timestamp: new Date().toISOString()
    };

    const savedHistory = localStorage.getItem('dunk-chat-history');
    const history = savedHistory ? JSON.parse(savedHistory) : [];
    
    const existingIndex = history.findIndex(chat => chat.id === chatData.id);
    if (existingIndex >= 0) {
      history[existingIndex] = chatData;
    } else {
      history.unshift(chatData);
    }
    
    localStorage.setItem('dunk-chat-history', JSON.stringify(history));

    if (!currentChatId) {
      setCurrentChatId(chatData.id);
    }
  };

  // Handle prompt selection
  const handlePromptSelect = (prompt) => {
    setInput(prompt);
    handleSend(prompt);
  };

  return (
    <div className="flex-1 flex flex-col">
      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-6">
        {messages.length === 0 ? (
          /* Welcome Screen */
          <div className="max-w-3xl mx-auto text-center py-12">
            {/* Avatar with Glowing Effect */}
            <div className="relative w-48 h-48 mx-auto mb-8">
              <div className="absolute inset-0 rounded-full border-2 border-primary/30 animate-pulse"></div>
              <div className="absolute inset-4 rounded-full border-2 border-primary/50"></div>
              <div className="absolute inset-8 rounded-full border-2 border-primary/70"></div>
              
              <div className="absolute inset-12 bg-gradient-to-br from-primary/20 to-primary-dark/20 rounded-full flex items-center justify-center backdrop-blur-sm">
                <Brain className="w-16 h-16 text-primary" />
              </div>
              
              <div className="absolute -top-2 left-1/4 w-3 h-3 bg-primary rounded-full animate-pulse"></div>
              <div className="absolute top-8 -right-2 w-2 h-2 bg-primary-light rounded-full animate-pulse delay-100"></div>
              <div className="absolute bottom-12 -left-3 w-2.5 h-2.5 bg-primary rounded-full animate-pulse delay-200"></div>
            </div>
            
            <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">
              Hi {user?.name?.split(' ')[0] || 'there'}, How can I help you?
            </h2>
            <p className="text-gray-600 dark:text-gray-400 mb-8">
              Ask me anything about {category?.title?.toLowerCase() || 'your finances'}
            </p>
            
            {/* Category-specific prompts */}
            <div className="grid md:grid-cols-2 gap-4 mt-8">
              {prompts.map((prompt, index) => (
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
                    {message.attachment && (
                      <div className="mt-3">
                        <img
                          src={message.attachment}
                          alt="Generated chart"
                          className="rounded-xl border border-gray-200 dark:border-dark-border"
                        />
                      </div>
                    )}
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
                placeholder={`Ask me anything about ${category?.title?.toLowerCase() || 'your finances'}...`}
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
              disabled={!input.trim() || isLoading}
              className="btn-primary p-3 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Send className={`w-5 h-5 ${isLoading ? 'animate-pulse' : ''}`} />
            </button>
          </form>
          <p className="text-xs text-gray-500 dark:text-gray-400 text-center mt-2">
            {isLoading ? 'Fetching real data from the backend...' : 'Dunk can make mistakes. Please verify important information.'}
          </p>
        </div>
      </div>
    </div>
  );
};

export default BaseChatLayout;

