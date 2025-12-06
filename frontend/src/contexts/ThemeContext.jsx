import { createContext, useContext, useEffect, useState } from 'react';

// Create the Theme Context
const ThemeContext = createContext();

// Custom hook to use the Theme Context
export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme must be used within a ThemeProvider');
  }
  return context;
};

// Theme Provider Component
export const ThemeProvider = ({ children }) => {
  // Check if user has a saved theme preference, otherwise use 'dark' as default
  const [theme, setTheme] = useState(() => {
    try {
      const savedTheme = localStorage.getItem('dunk-theme');
      return savedTheme || 'dark';
    } catch (error) {
      return 'dark';
    }
  });

  // Apply theme to document and save to localStorage
  useEffect(() => {
    try {
      const root = window.document.documentElement;
      
      // Remove both classes first
      root.classList.remove('light', 'dark');
      
      // Add the current theme class
      root.classList.add(theme);
      
      // Save to localStorage
      localStorage.setItem('dunk-theme', theme);
    } catch (error) {
      // Silently fail if localStorage is unavailable
    }
  }, [theme]);

  // Toggle between light and dark theme
  const toggleTheme = () => {
    setTheme(prevTheme => prevTheme === 'light' ? 'dark' : 'light');
  };

  const value = {
    theme,
    toggleTheme,
    isDark: theme === 'dark'
  };

  return (
    <ThemeContext.Provider value={value}>
      {children}
    </ThemeContext.Provider>
  );
};

