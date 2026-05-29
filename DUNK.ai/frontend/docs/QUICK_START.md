# 🚀 Quick Start Guide - Dunk.ai

## Step 1: Install Dependencies

Open your terminal in this directory and run:

```bash
npm install
```

This will install all required packages:
- react & react-dom (v19.1.1)
- react-router-dom (v6.26.0)
- lucide-react (v0.400.0)
- tailwindcss (v3.4.4)
- And other dependencies

## Step 2: Start Development Server

```bash
npm run dev
```

You should see output like:
```
  VITE v7.1.7  ready in XXX ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
  ➜  press h + enter to show help
```

## Step 3: Open in Browser

1. Open your browser
2. Go to `http://localhost:5173`
3. You should see the Dunk.ai landing page!

## Step 4: Test the Application

### Login:
1. Click "Sign In" button
2. Enter phone: `9876543210` (or any 10-digit number)
3. Click "Enter code"
4. Enter any code: `123456`
5. Click "Verify & Login"

### Use Features:
1. Click "Explore" to see all financial features
2. Select any feature to see prompts
3. Click a prompt or type your own question
4. Chat with the AI!

### Test Theme Toggle:
- Click the sun/moon icon to switch themes
- Theme preference is saved automatically

### Check Profile Settings:
- Click the Settings icon in sidebar
- Update your name and email
- Change theme preferences

## 🎯 Demo Credentials

**Phone Numbers** (any 10-digit number works, but these have profiles):
- `9876543210` - Disha Kumar
- `1234567890` - Demo User

**Verification Code**: Any code works (e.g., `123456`)

## 📱 Features to Test

1. **Portfolio Manager**: Ask "What is my current SIP amount?"
2. **Smart Expense Coach**: Ask "Show my spending pattern"
3. **Emergency Fund**: Ask "I need ₹2L urgently. Where can I get it?"
4. **Loan Clarity**: Ask "Can I afford a ₹50L home loan?"
5. **Anomaly Watchdog**: Ask "Have there been any unusual transactions?"
6. **Investment Navigator**: Ask "Suggest investment opportunities"

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Kill the process using port 5173
npx kill-port 5173

# Then restart
npm run dev
```

### Dependencies Not Installing
```bash
# Clear npm cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Tailwind Not Working
```bash
# Restart the dev server
# Press Ctrl+C to stop
npm run dev
```

## 🎨 Customization Tips

1. **Change Colors**: Edit `tailwind.config.js`
2. **Add More Prompts**: Edit `src/utils/featurePrompts.js`
3. **Modify AI Responses**: Edit `generateAIResponse` function in `src/pages/ChatPage.jsx`
4. **Add More Users**: Edit `DUMMY_USERS` in `src/contexts/AuthContext.jsx`

## 📦 Build for Production

```bash
npm run build
```

This creates an optimized production build in the `dist/` folder.

To preview the production build:
```bash
npm run preview
```

## 🎓 Learning Resources

If you're new to React:
1. Start with `src/App.jsx` - See how routing works
2. Check `src/contexts/` - Learn about Context API
3. Explore `src/pages/` - Understand page components
4. Review `src/components/` - Reusable UI components

---

**Happy Coding! 🚀**

