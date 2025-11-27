import { useState } from 'react';
import { ArrowLeft, User, Mail, Phone, Moon, Sun, Save, DollarSign } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { useTheme } from '../contexts/ThemeContext';
import { useNavigate } from 'react-router-dom';

const ProfilePage = () => {
  const { user, updateProfile } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();
  
  const [formData, setFormData] = useState({
    name: user?.name || '',
    email: user?.email || '',
    phone: user?.phone || '',
    netWorth: user?.netWorth || ''
  });

  const [saved, setSaved] = useState(false);

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    updateProfile(formData);
    setSaved(true);
    setTimeout(() => setSaved(false), 3000);
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-dark-bg">
      {/* Header */}
      <div className="bg-white dark:bg-dark-card border-b border-gray-200 dark:border-dark-border">
        <div className="max-w-4xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <button 
                onClick={() => navigate(-1)}
                className="p-2 hover:bg-gray-100 dark:hover:bg-dark-bg rounded-lg transition-colors"
              >
                <ArrowLeft className="w-5 h-5" />
              </button>
              <div>
                <h1 className="text-2xl font-bold text-gray-900 dark:text-white">
                  Profile Settings
                </h1>
                <p className="text-sm text-gray-600 dark:text-gray-400">
                  Manage your account and preferences
                </p>
              </div>
            </div>
            
            {saved && (
              <div className="px-4 py-2 bg-green-50 dark:bg-green-900/20 text-green-600 dark:text-green-400 rounded-lg text-sm font-medium">
                ✓ Profile saved
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Content */}
      <div className="max-w-4xl mx-auto px-6 py-8">
        <div className="grid lg:grid-cols-3 gap-6">
          {/* Profile Card */}
          <div className="lg:col-span-1">
            <div className="card sticky top-6">
              <div className="text-center">
                <div className="w-32 h-32 bg-gradient-to-br from-primary to-primary-dark rounded-full flex items-center justify-center mx-auto mb-4">
                  <User className="w-16 h-16 text-white" />
                </div>
                <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-1">
                  {formData.name || 'User'}
                </h2>
                <p className="text-sm text-gray-600 dark:text-gray-400 mb-4">
                  {formData.phone}
                </p>
                <button className="text-sm text-primary hover:underline">
                  Change Avatar
                </button>
              </div>

              {/* Quick Stats */}
              <div className="mt-6 pt-6 border-t border-gray-200 dark:border-dark-border space-y-3">
                <div className="flex items-center justify-between p-3 bg-gray-50 dark:bg-dark-bg rounded-lg">
                  <span className="text-sm text-gray-700 dark:text-gray-300">Member Since</span>
                  <span className="font-medium text-gray-900 dark:text-white">Oct 2025</span>
                </div>
             
              </div>
            </div>
          </div>

          {/* Settings Form */}
          <div className="lg:col-span-2 space-y-6">
            {/* Personal Information */}
            <div className="card">
              <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4">
                Personal Information
              </h3>
              
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
                    Email Address
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
                

                <button 
                  type="submit"
                  className="w-full btn-primary flex items-center justify-center space-x-2 py-3"
                >
                  <Save className="w-4 h-4" />
                  <span>Save Changes</span>
                </button>
              </form>
            </div>

            {/* Appearance Settings */}
            <div className="card">
              <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-4">
                Appearance
              </h3>
              
              <div className="flex items-center justify-between mb-4">
                <div>
                  <h4 className="font-medium text-gray-900 dark:text-white">
                    Theme Preference
                  </h4>
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
              
              <div className="grid grid-cols-2 gap-3">
                <button
                  type="button"
                  onClick={() => theme === 'dark' && toggleTheme()}
                  className={`p-4 rounded-lg border-2 transition-all ${
                    theme === 'light'
                      ? 'border-primary bg-primary/5'
                      : 'border-gray-200 dark:border-dark-border hover:border-gray-300'
                  }`}
                >
                  <Sun className="w-6 h-6 mx-auto mb-2" />
                  <span className="text-sm font-medium">Light</span>
                </button>
                <button
                  type="button"
                  onClick={() => theme === 'light' && toggleTheme()}
                  className={`p-4 rounded-lg border-2 transition-all ${
                    theme === 'dark'
                      ? 'border-primary bg-primary/5'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <Moon className="w-6 h-6 mx-auto mb-2" />
                  <span className="text-sm font-medium">Dark</span>
                </button>
              </div>
            </div>


            {/* Danger Zone */}
            <div className="card border-red-200 dark:border-red-900/50">
              <h3 className="text-lg font-bold text-red-600 dark:text-red-400 mb-4">
                Danger Zone
              </h3>
              
              <div className="space-y-3">
                <button className="w-full p-4 text-left rounded-lg border border-red-200 dark:border-red-900/50 hover:bg-red-50 dark:hover:bg-red-900/10 transition-colors">
                  <div className="flex items-center justify-between">
                    <div>
                      <h4 className="font-medium text-gray-900 dark:text-white">
                        Delete Account
                      </h4>
                      <p className="text-sm text-gray-600 dark:text-gray-400">
                        Permanently delete your account and data
                      </p>
                    </div>
                    <span className="text-sm text-red-600">Delete</span>
                  </div>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ProfilePage;

