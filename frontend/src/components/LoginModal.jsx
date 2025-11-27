import { useState } from 'react';
import { X, Phone } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';
import { useNavigate } from 'react-router-dom';

const LoginModal = ({ onClose }) => {
  const [phone, setPhone] = useState('');
  const [showCodeInput, setShowCodeInput] = useState(false);
  const [code, setCode] = useState('');
  const { login } = useAuth();
  const navigate = useNavigate();

  const handlePhoneSubmit = (e) => {
    e.preventDefault();
    if (phone.length >= 10) {
      setShowCodeInput(true);
    }
  };

  const handleCodeSubmit = (e) => {
    e.preventDefault();
    // For demo purposes, any code works
    if (code.length > 0) {
      login(phone);
      navigate('/chat');
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4">
      <div className="bg-white dark:bg-dark-card rounded-2xl max-w-md w-full p-8 relative shadow-2xl">
        {/* Close button */}
        <button 
          onClick={onClose}
          className="absolute top-4 right-4 p-2 hover:bg-gray-100 dark:hover:bg-dark-bg rounded-lg transition-colors"
        >
          <X className="w-5 h-5" />
        </button>

        {/* Logo & Title */}
        <div className="text-center mb-8">
          <div className="w-16 h-16 bg-primary rounded-2xl flex items-center justify-center mx-auto mb-4">
            <span className="text-white font-bold text-2xl">D</span>
          </div>
          <h2 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">
            Login
          </h2>
          <p className="text-gray-600 dark:text-gray-400">
            {showCodeInput 
              ? 'Enter the verification code'
              : 'Enter your mobile number registered with Fi Money'
            }
          </p>
        </div>

        {!showCodeInput ? (
          /* Phone Number Form */
          <form onSubmit={handlePhoneSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Phone Number
              </label>
              <div className="relative">
                <Phone className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
                <input
                  type="tel"
                  value={phone}
                  onChange={(e) => setPhone(e.target.value)}
                  placeholder="9876543210"
                  className="input pl-11"
                  maxLength="10"
                  required
                />
              </div>
              <p className="mt-2 text-xs text-gray-500 dark:text-gray-400">
                Try: 9876543210 or 1234567890 for demo
              </p>
            </div>

            <button 
              type="submit"
              className="w-full btn-primary text-lg py-3"
            >
              Enter code
            </button>
          </form>
        ) : (
          /* Verification Code Form */
          <form onSubmit={handleCodeSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                Verification Code
              </label>
              <input
                type="text"
                value={code}
                onChange={(e) => setCode(e.target.value)}
                placeholder="Enter 6-digit code"
                className="input text-center text-2xl tracking-widest"
                maxLength="6"
                required
              />
              <p className="mt-2 text-xs text-gray-500 dark:text-gray-400">
                For demo: Enter any code (e.g., 123456)
              </p>
            </div>

            <div className="space-y-3">
              <button 
                type="submit"
                className="w-full btn-primary text-lg py-3"
              >
                Verify & Login
              </button>
              
              <button 
                type="button"
                onClick={() => {
                  setShowCodeInput(false);
                  setCode('');
                }}
                className="w-full btn-secondary py-3"
              >
                Back
              </button>
            </div>

            <div className="text-center">
              <button 
                type="button" 
                className="text-sm text-primary hover:underline"
              >
                Resend code
              </button>
            </div>
          </form>
        )}

        {/* Additional Info */}
        <div className="mt-6 pt-6 border-t border-gray-200 dark:border-dark-border">
          <p className="text-xs text-gray-500 dark:text-gray-400 text-center">
            By continuing, you agree to our Terms of Service and Privacy Policy
          </p>
        </div>
      </div>
    </div>
  );
};

export default LoginModal;

