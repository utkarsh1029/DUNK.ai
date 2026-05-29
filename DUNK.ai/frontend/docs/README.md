# Dunk.ai - Your Financial AI Agent 💰

A beautiful, modern financial AI chatbot application built with React, Tailwind CSS, and inspired by the best UX practices from ChatGPT and Google Gemini.

![Dunk.ai](https://img.shields.io/badge/React-19.1.1-blue)
![Tailwind](https://img.shields.io/badge/Tailwind-3.4.4-teal)
![License](https://img.shields.io/badge/license-MIT-green)

## 🌟 Features

### Core Functionality
- 🎨 **Beautiful Light & Dark Themes** - Toggle between themes seamlessly
- 🔐 **Dummy Authentication System** - Phone-based login for demos
- 💬 **ChatGPT-like Interface** - Intuitive chat experience
- 📱 **Fully Responsive** - Works on all devices
- 💾 **Chat History** - Your conversations are saved locally
- 👤 **Profile Management** - Customize your profile and preferences

### Financial Features
1. **Portfolio Manager** - Track and optimize your investments
2. **Smart Expense Coach** - Get insights on spending patterns
3. **Emergency Fund Assistance** - Plan for unexpected expenses
4. **Loan Clarity Engine** - Understand loan affordability
5. **Anomaly Watchdog** - Detect unusual transactions
6. **Investment Navigator** - Discover investment opportunities

## 🚀 Getting Started

### Prerequisites
- Node.js (v16 or higher)
- npm or yarn

### Installation

1. **Clone the repository** (if not already done)
   ```bash
   cd /home/Documents/Frontend-dunk.ai
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm run dev
   ```

4. **Open your browser**
   Navigate to `http://localhost:5173` (or the URL shown in your terminal)

## 🎯 How to Use

### For Demo/Testing

1. **Landing Page**: 
   - Click the "Sign In" button in the header or "Get Started" button

2. **Login**:
   - Enter any 10-digit phone number (try: `9876543210` or `1234567890`)
   - Click "Enter code"
   - Enter any verification code (e.g., `123456`)
   - Click "Verify & Login"

3. **Chat Interface**:
   - You'll be redirected to the chat page
   - Click "Explore" to see all financial features
   - Click on any prompt to start chatting
   - Or type your own financial questions

4. **Features**:
   - **New Chat**: Start a fresh conversation
   - **History**: View and reload past conversations
   - **Profile Settings**: Update your name, email, and toggle theme
   - **Theme Toggle**: Switch between light and dark mode
   - **Logout**: Sign out of the application

## 📁 Project Structure

```
Frontend-dunk.ai/
├── src/
│   ├── components/
│   │   ├── ExploreSidebar.jsx      # Financial features sidebar
│   │   ├── LoginModal.jsx          # Authentication modal
│   │   └── ProfileSettings.jsx     # User settings
│   ├── contexts/
│   │   ├── AuthContext.jsx         # Authentication state
│   │   └── ThemeContext.jsx        # Theme management
│   ├── pages/
│   │   ├── ChatPage.jsx            # Main chat interface
│   │   └── LandingPage.jsx         # Landing/home page
│   ├── utils/
│   │   └── featurePrompts.js       # Dummy prompts for features
│   ├── App.jsx                     # Main app with routing
│   ├── main.jsx                    # App entry point
│   └── index.css                   # Tailwind styles
├── tailwind.config.js              # Tailwind configuration
├── package.json                    # Dependencies
└── README.md                       # This file
```

## 🎨 Customization

### Colors
Edit `tailwind.config.js` to change the color scheme:
```javascript
colors: {
  primary: {
    light: '#5EEAD4',
    DEFAULT: '#14B8A6',
    dark: '#0D9488',
  },
  // ... more colors
}
```

### Dummy Users
Edit `src/contexts/AuthContext.jsx` to add more demo users:
```javascript
const DUMMY_USERS = [
  { phone: '9876543210', name: 'Disha Kumar', email: 'disha@example.com' },
  // Add more users here
];
```

### Feature Prompts
Edit `src/utils/featurePrompts.js` to customize prompts for each feature.

## 🛠️ Technologies Used

- **React 19.1.1** - UI framework
- **React Router DOM 6** - Routing
- **Tailwind CSS 3** - Styling
- **Lucide React** - Beautiful icons
- **Vite** - Build tool

## 📝 Code Quality

This project follows React best practices:
- ✅ Functional components with hooks
- ✅ Context API for state management
- ✅ Clean, beginner-friendly code
- ✅ Proper component separation
- ✅ LocalStorage for persistence
- ✅ Responsive design patterns

## 🎓 For Beginners

### Key Concepts Used

1. **React Hooks**:
   - `useState` - Managing component state
   - `useEffect` - Side effects (localStorage, scrolling)
   - `useContext` - Global state (theme, auth)
   - `useRef` - DOM references

2. **React Router**:
   - Navigation between pages
   - Protected routes for authenticated users

3. **Context API**:
   - Theme management (light/dark mode)
   - Authentication state
   - User profile data

4. **LocalStorage**:
   - Persisting chat history
   - Saving user preferences
   - Theme preference

## 🚢 Building for Production

```bash
npm run build
```

This creates an optimized build in the `dist/` folder.

## 📄 License

This project is created for demonstration purposes.

## 🤝 Contributing

This is a demo project. Feel free to fork and customize it for your needs!

## 📧 Support

For questions or issues, please check the code comments or reach out to your development team.

---

**Made with ❤️ for Financial Empowerment**

*"Your Money, Our Responsibility"* - Dunk.ai
