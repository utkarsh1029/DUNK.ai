import { createContext, useContext, useState, useEffect } from 'react';

// Create the Auth Context
const AuthContext = createContext();

// Custom hook to use the Auth Context
export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

// Auth Provider Component
export const AuthProvider = ({ children }) => {
  // Check if user is already logged in (from localStorage)
  const [user, setUser] = useState(() => {
    const savedUser = localStorage.getItem('dunk-user');
    return savedUser ? JSON.parse(savedUser) : null;
  });

  const [isAuthenticated, setIsAuthenticated] = useState(!!user);

  // Dummy user credentials for demo
  const DUMMY_USERS = [
    { phone: '9876543210', name: 'Disha Kumar', email: 'disha@example.com', netWorth: '25,00,000' },
    { phone: '1234567890', name: 'Demo User', email: 'demo@example.com', netWorth: '' },
  ];

  // Save user to localStorage whenever it changes
  useEffect(() => {
    try {
      if (user) {
        localStorage.setItem('dunk-user', JSON.stringify(user));
      } else {
        localStorage.removeItem('dunk-user');
      }
    } catch (error) {
      // Silently fail if localStorage is unavailable
    }
  }, [user]);

  // Login function - accepts phone number
  const login = (phone) => {
    // Find user by phone or create a new dummy user
    let foundUser = DUMMY_USERS.find(u => u.phone === phone);
    
    if (!foundUser) {
      foundUser = {
        phone: phone,
        name: 'Demo User',
        email: 'user@example.com',
        netWorth: ''
      };
    }

    setUser(foundUser);
    setIsAuthenticated(true);
    return true;
  };

  // Logout function
  const logout = () => {
    setUser(null);
    setIsAuthenticated(false);
    try {
      localStorage.removeItem('dunk-user');
      localStorage.removeItem('dunk-chat-history');
    } catch (error) {
      // Silently fail if localStorage is unavailable
    }
  };

  // Update user profile
  const updateProfile = (updatedData) => {
    const updatedUser = { ...user, ...updatedData };
    setUser(updatedUser);
  };

  const value = {
    user,
    isAuthenticated,
    login,
    logout,
    updateProfile
  };

  return (
    <AuthContext.Provider value={value}>
      {children}
    </AuthContext.Provider>
  );
};

