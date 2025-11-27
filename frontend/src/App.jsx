import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './contexts/AuthContext';
import { ThemeProvider } from './contexts/ThemeContext';
import LandingPage from './pages/LandingPage';
import ChatPage from './pages/ChatPage';
import ProfilePage from './pages/ProfilePage';
import PortfolioManagerPage from './pages/PortfolioManagerPage';
import SmartExpenseCoachPage from './pages/SmartExpenseCoachPage';
import LoanClarityEnginePage from './pages/LoanClarityEnginePage';
import EmergencyFundAssistancePage from './pages/EmergencyFundAssistancePage';
import AnomalyWatchdogPage from './pages/AnomalyWatchdogPage';
import InvestmentNavigatorPage from './pages/InvestmentNavigatorPage';

// Protected Route Component
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? children : <Navigate to="/" />;
};

function App() {
  return (
    <ThemeProvider>
      <AuthProvider>
        <Router>
          <Routes>
            <Route path="/" element={<LandingPage />} />
            <Route 
              path="/chat" 
              element={
                <ProtectedRoute>
                  <ChatPage />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/profile" 
              element={
                <ProtectedRoute>
                  <ProfilePage />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/chat/portfolio-manager" 
              element={
                <ProtectedRoute>
                  <PortfolioManagerPage />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/chat/smart-expense-coach" 
              element={
                <ProtectedRoute>
                  <SmartExpenseCoachPage />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/chat/loan-clarity-engine" 
              element={
                <ProtectedRoute>
                  <LoanClarityEnginePage />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/chat/emergency-fund-assistance" 
              element={
                <ProtectedRoute>
                  <EmergencyFundAssistancePage />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/chat/anomaly-watchdog" 
              element={
                <ProtectedRoute>
                  <AnomalyWatchdogPage />
                </ProtectedRoute>
              } 
            />
            <Route 
              path="/chat/investment-navigator" 
              element={
                <ProtectedRoute>
                  <InvestmentNavigatorPage />
                </ProtectedRoute>
              } 
            />
          </Routes>
        </Router>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;
