# 📊 Dunk.ai Project Overview

## 🏗️ Architecture

### Component Hierarchy

```
App (Router + Providers)
├── ThemeProvider
│   └── AuthProvider
│       └── Routes
│           ├── / (LandingPage)
│           │   └── LoginModal
│           └── /chat (ChatPage - Protected)
│               ├── ExploreSidebar
│               └── ProfileSettings
```

## 📂 File Structure Explained

### `/src/contexts/`
**Purpose**: Global state management using React Context API

- **ThemeContext.jsx**
  - Manages light/dark theme
  - Persists theme to localStorage
  - Provides `theme`, `toggleTheme`, `isDark`

- **AuthContext.jsx**
  - Manages user authentication
  - Handles dummy login/logout
  - Stores user data in localStorage
  - Provides `user`, `isAuthenticated`, `login`, `logout`, `updateProfile`

### `/src/pages/`
**Purpose**: Main page components

- **LandingPage.jsx**
  - Hero section with branding
  - Feature showcase
  - Call-to-action buttons
  - Login modal trigger

- **ChatPage.jsx**
  - Main chat interface
  - Sidebar with chat history
  - Message display area
  - Input field with send functionality
  - AI response simulation
  - Chat history management

### `/src/components/`
**Purpose**: Reusable UI components

- **LoginModal.jsx**
  - Phone number input
  - Verification code input
  - Dummy authentication flow
  - Redirects to chat after login

- **ExploreSidebar.jsx**
  - Lists all 6 financial features
  - Shows feature-specific prompts
  - Sidebar overlay design
  - Prompt selection handler

- **ProfileSettings.jsx**
  - User profile form
  - Theme toggle
  - Avatar display
  - Save profile changes

### `/src/utils/`
**Purpose**: Utility functions and constants

- **featurePrompts.js**
  - Object containing all feature prompts
  - 5 prompts per feature
  - Used by Explore sidebar and Chat page

### Configuration Files

- **tailwind.config.js**
  - Custom color palette
  - Dark mode configuration
  - Theme extensions

- **postcss.config.js**
  - Tailwind CSS processing
  - Autoprefixer setup

- **vite.config.js**
  - React plugin configuration
  - Build settings

## 🎨 Design System

### Color Palette

**Light Mode:**
- Background: White (#FFFFFF)
- Cards: White with subtle borders
- Text: Dark gray (#111827)
- Primary: Teal (#14B8A6)
- Accent: Light teal (#5EEAD4)

**Dark Mode:**
- Background: Dark teal (#0A1E1E)
- Cards: Darker teal (#0F2626)
- Text: Light gray (#F3F4F6)
- Primary: Teal (#14B8A6)
- Accent: Light teal (#5EEAD4)

### Typography
- Font Family: System fonts (San Francisco, Segoe UI, Roboto)
- Headings: Bold, varying sizes (text-xl to text-6xl)
- Body: Regular weight, text-sm to text-base

### Spacing
- Padding: Consistent 4px increments (p-2, p-4, p-6, p-8)
- Margins: Similar scale
- Gap: Space-x and space-y utilities

### Components

**Buttons:**
- `.btn-primary`: Teal background, white text, rounded-full
- `.btn-secondary`: Gray background, rounded-full

**Cards:**
- `.card`: White/dark background, border, rounded-2xl, shadow

**Inputs:**
- `.input`: Full width, padding, border, focus ring

## 🔄 Data Flow

### Authentication Flow
```
User clicks "Sign In"
  → LoginModal opens
  → User enters phone number
  → Shows verification code input
  → User enters code
  → AuthContext.login() called
  → User data saved to localStorage
  → Navigate to /chat
```

### Chat Flow
```
User types message
  → handleSend() triggered
  → User message added to state
  → Message displayed in UI
  → AI response generated (after 1s delay)
  → AI message added to state
  → Chat history updated
  → History saved to localStorage
```

### Theme Flow
```
User clicks theme toggle
  → ThemeContext.toggleTheme() called
  → Theme state updated
  → 'dark' class added/removed from <html>
  → Theme saved to localStorage
```

## 💾 Data Persistence

### LocalStorage Keys

1. **`dunk-theme`**
   - Value: 'light' or 'dark'
   - Updated: When theme is toggled

2. **`dunk-user`**
   - Value: JSON object `{ phone, name, email }`
   - Updated: On login and profile update

3. **`dunk-chat-history`**
   - Value: Array of chat objects
   - Each chat: `{ id, title, messages, timestamp }`
   - Updated: After each conversation

## 🎯 Feature Implementation

### 1. Portfolio Manager
- Shows SIP amounts
- Investment breakdown
- Returns analysis
- Rebalancing suggestions

### 2. Smart Expense Coach
- Spending patterns
- Category breakdown
- Month-over-month comparison
- Budget alerts

### 3. Emergency Fund Assistance
- Liquid assets check
- Source recommendations
- PPF/FD advice
- Fund building tips

### 4. Loan Clarity Engine
- Affordability calculation
- EMI range suggestions
- Tenure comparison
- Interest calculations

### 5. Anomaly Watchdog
- Unusual transaction detection
- Duplicate charge finder
- Subscription review
- Fraud alerts

### 6. Investment Navigator
- Risk-based suggestions
- SIP vs lump sum advice
- Fund recommendations
- Allocation strategies

## 🧪 Testing Checklist

### Authentication
- [ ] Login with valid phone number
- [ ] Login with different phone numbers
- [ ] Verification code acceptance
- [ ] Redirect to chat after login
- [ ] Logout functionality
- [ ] Protected route (try accessing /chat without login)

### Chat Interface
- [ ] Send messages
- [ ] Receive AI responses
- [ ] Start new chat
- [ ] Load chat from history
- [ ] Chat history persistence (refresh page)
- [ ] Message scrolling

### Theme
- [ ] Toggle to dark mode
- [ ] Toggle to light mode
- [ ] Theme persists after refresh
- [ ] All components render correctly in both themes

### Explore Features
- [ ] Open explore sidebar
- [ ] Click each feature
- [ ] Select prompts
- [ ] Prompts populate input field
- [ ] Close sidebar

### Profile Settings
- [ ] Open settings
- [ ] Update name
- [ ] Update email
- [ ] Theme toggle in settings
- [ ] Save changes
- [ ] Changes persist

### Responsive Design
- [ ] Mobile view (< 768px)
- [ ] Tablet view (768px - 1024px)
- [ ] Desktop view (> 1024px)
- [ ] Sidebar collapse on mobile

## 🚀 Future Enhancements

### Possible Additions
1. **Real API Integration**
   - Connect to actual financial APIs
   - Real-time data fetching
   - Secure authentication

2. **Advanced Features**
   - Voice input
   - File attachments
   - Export chat history
   - Share conversations

3. **Personalization**
   - Custom avatars
   - Multiple color themes
   - Font size adjustments
   - Language preferences

4. **Analytics**
   - Usage tracking
   - Feature popularity
   - User behavior insights

5. **Enhanced AI**
   - Real AI model integration (Gemini API)
   - Context awareness
   - Multi-turn conversations
   - Personalized recommendations

## 📚 Code Comments

The codebase includes extensive comments explaining:
- Component purpose
- Function logic
- State management
- Complex operations
- Best practices

Perfect for beginners to learn from!

## 🎓 Learning Path

**For React Beginners:**

1. Start here:
   - `src/main.jsx` - Entry point
   - `src/App.jsx` - Routing setup

2. Then explore:
   - `src/contexts/ThemeContext.jsx` - Simple context
   - `src/components/LoginModal.jsx` - Form handling

3. Advanced concepts:
   - `src/pages/ChatPage.jsx` - Complex state management
   - `src/contexts/AuthContext.jsx` - Authentication patterns

## 🛠️ Development Tips

1. **Use React DevTools**
   - Install browser extension
   - Inspect component tree
   - Monitor state changes

2. **Hot Module Replacement**
   - Changes reflect instantly
   - No page refresh needed
   - State preserved

3. **Console Logging**
   - Add console.logs to track data flow
   - Useful for debugging

4. **Tailwind IntelliSense**
   - Install VS Code extension
   - Get class name autocomplete
   - See color previews

---

**Built with ❤️ and attention to detail for the best learning experience!**

