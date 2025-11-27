import { useState } from 'react';
import { X, User, Mail, Phone, Moon, Sun, Save } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { useTheme } from '../contexts/ThemeContext';

const ProfileSettings = ({ onClose }) => {
  const { user, updateProfile } = useAuth();
  const { theme, toggleTheme } = useTheme();
  
  const [formData, setFormData] = useState({
    name: user?.name || '',
    email: user?.email || '',
    phone: user?.phone || ''
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    updateProfile(formData);
    onClose();
  };

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-white dark:bg-dark-card rounded-2xl max-w-md w-full shadow-2xl">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200 dark:border-dark-border">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
            Profile Settings
          </h2>
          <button 
            onClick={onClose}
            className="p-2 hover:bg-gray-100 dark:hover:bg-dark-bg rounded-lg transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Content */}
        <div className="p-6 space-y-6">
          {/* Profile Picture */}
          <div className="flex flex-col items-center">
            <div className="w-24 h-24 bg-gradient-to-br from-primary to-primary-dark rounded-full flex items-center justify-center mb-3">
              <User className="w-12 h-12 text-white" />
            </div>
            <button className="text-sm text-primary hover:underline">
              Change Avatar
            </button>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Full Name
              </label>
              <div className="relative">
                <User className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                  type="text"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  className="input pl-11"
                  placeholder="Enter your name"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Email
              </label>
              <div className="relative">
                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  onChange={handleChange}
                  className="input pl-11"
                  placeholder="Enter your email"
                />
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Phone Number
              </label>
              <div className="relative">
                <Phone className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                  type="tel"
                  name="phone"
                  value={formData.phone}
                  onChange={handleChange}
                  className="input pl-11"
                  placeholder="Enter your phone"
                  disabled
                />
              </div>
              <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                Phone number cannot be changed
              </p>
            </div>

            {/* Theme Toggle */}
            <div className="pt-4 border-t border-gray-200 dark:border-dark-border">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="font-medium text-gray-900 dark:text-white">
                    Appearance
                  </h3>
                  <p className="text-sm text-gray-600 dark:text-gray-400">
                    Choose your preferred theme
                  </p>
                </div>
                <button 
                  type="button"
                  onClick={toggleTheme}
                  className="p-3 rounded-lg bg-gray-100 dark:bg-dark-bg hover:bg-gray-200 dark:hover:bg-gray-700 transition-colors"
                >
                  {theme === 'dark' ? (
                    <Sun className="w-5 h-5 text-yellow-500" />
                  ) : (
                    <Moon className="w-5 h-5 text-gray-600" />
                  )}
                </button>
              </div>
              <div className="grid grid-cols-2 gap-3 mt-3">
                <button
                  type="button"
                  onClick={() => theme === 'dark' && toggleTheme()}
                  className={`p-3 rounded-lg border-2 transition-all ${
                    theme === 'light'
                      ? 'border-primary bg-primary/5'
                      : 'border-gray-200 dark:border-dark-border'
                  }`}
                >
                  <Sun className="w-5 h-5 mx-auto mb-1" />
                  <span className="text-sm font-medium">Light</span>
                </button>
                <button
                  type="button"
                  onClick={() => theme === 'light' && toggleTheme()}
                  className={`p-3 rounded-lg border-2 transition-all ${
                    theme === 'dark'
                      ? 'border-primary bg-primary/5'
                      : 'border-gray-200'
                  }`}
                >
                  <Moon className="w-5 h-5 mx-auto mb-1" />
                  <span className="text-sm font-medium">Dark</span>
                </button>
              </div>
            </div>

            {/* Buttons */}
            <div className="flex space-x-3 pt-4">
              <button
                type="button"
                onClick={onClose}
                className="flex-1 btn-secondary"
              >
                Cancel
              </button>
              <button
                type="submit"
                className="flex-1 btn-primary flex items-center justify-center space-x-2"
              >
                <Save className="w-4 h-4" />
                <span>Save Changes</span>
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default ProfileSettings;

