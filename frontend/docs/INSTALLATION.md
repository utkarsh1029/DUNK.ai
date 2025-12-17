# 🔧 Installation & Setup Guide

## Prerequisites Check

Before starting, ensure you have:

- **Node.js**: Version 16.x or higher
  ```bash
  node --version
  ```

- **npm**: Version 7.x or higher
  ```bash
  npm --version
  ```

If you don't have Node.js installed:
- Visit https://nodejs.org/
- Download the LTS version
- Follow installation instructions for your OS

## Installation Steps

### Step 1: Navigate to Project Directory

```bash
cd /home/Documents/Frontend-dunk.ai
```

### Step 2: Install Dependencies

This will install all required packages including:
- React and React DOM
- React Router DOM (for navigation)
- Lucide React (for icons)
- Tailwind CSS (for styling)
- And all dev dependencies

```bash
npm install
```

**Expected output:**
```
added XXX packages, and audited XXX packages in XXs

XX packages are looking for funding
  run `npm fund` for details

found 0 vulnerabilities
```

### Step 3: Verify Installation

Check if all key packages are installed:

```bash
npm list react react-router-dom lucide-react tailwindcss
```

You should see:
```
dunk-ai@0.0.0 /path/to/project
├── lucide-react@0.400.0
├── react-router-dom@6.26.0
├── react@19.1.1
└── tailwindcss@3.4.4
```

## Running the Application

### Development Mode

Start the development server with hot-reload:

```bash
npm run dev
```

**You should see:**
```
  VITE v7.1.7  ready in 500 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

### Access the Application

Open your browser and navigate to:
```
http://localhost:5173
```

## Testing the Installation

### Quick Feature Test

1. **Landing Page Load**
   - ✅ Page loads without errors
   - ✅ Theme toggle works
   - ✅ "Sign In" button visible

2. **Login Flow**
   - ✅ Click "Sign In"
   - ✅ Enter phone: `9876543210`
   - ✅ Enter code: `123456`
   - ✅ Redirect to chat page

3. **Chat Interface**
   - ✅ Chat interface loads
   - ✅ Can type and send messages
   - ✅ AI responds
   - ✅ Explore button works

4. **Theme Toggle**
   - ✅ Dark mode works
   - ✅ Light mode works
   - ✅ Theme persists on refresh

## Troubleshooting

### Issue: Port 5173 Already in Use

**Error:**
```
Port 5173 is in use, trying another one...
```

**Solution 1: Use the suggested port**
- Vite will automatically try another port
- Use the new port shown in the terminal

**Solution 2: Kill the existing process**
```bash
# Find the process
lsof -ti:5173

# Kill it
kill -9 $(lsof -ti:5173)

# Restart
npm run dev
```

### Issue: Module Not Found

**Error:**
```
Error: Cannot find module 'react-router-dom'
```

**Solution:**
```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

### Issue: Tailwind Styles Not Applying

**Symptoms:**
- No colors or styling
- Plain HTML appearance

**Solution 1: Restart dev server**
```bash
# Press Ctrl+C to stop
npm run dev
```

**Solution 2: Clear cache**
```bash
# Clear Vite cache
rm -rf node_modules/.vite
npm run dev
```

### Issue: Cannot Read Property of Undefined

**Error:**
```
TypeError: Cannot read property 'X' of undefined
```

**Solution:**
- Clear browser cache
- Clear localStorage:
  ```javascript
  // In browser console (F12)
  localStorage.clear()
  location.reload()
  ```

### Issue: Blank Page / White Screen

**Solution:**
1. Open browser console (F12)
2. Check for errors
3. Common fixes:
   ```bash
   # Clear everything and restart
   rm -rf node_modules package-lock.json .vite
   npm install
   npm run dev
   ```

### Issue: ESLint Errors

**Note:** ESLint warnings don't prevent the app from running.

To check for issues:
```bash
npm run lint
```

To auto-fix some issues:
```bash
npx eslint . --fix
```

## Environment Verification

### Check if Everything Works

Run this command to verify all critical imports:

```bash
node -e "
console.log('Checking installations...');
try {
  require('react');
  console.log('✅ React installed');
  require('react-router-dom');
  console.log('✅ React Router installed');
  require('lucide-react');
  console.log('✅ Lucide React installed');
  console.log('✅ All critical packages installed!');
} catch(e) {
  console.log('❌ Error:', e.message);
}
"
```

## Build for Production

When ready to deploy:

```bash
# Create optimized build
npm run build

# Preview the build
npm run preview
```

The build will be in the `dist/` folder.

## Next Steps

After successful installation:

1. ✅ Read `QUICK_START.md` for usage guide
2. ✅ Check `README.md` for feature overview
3. ✅ Review `PROJECT_OVERVIEW.md` for architecture
4. ✅ Start coding and customizing!

## Package Versions

Current versions in this project:

| Package | Version |
|---------|---------|
| React | 19.1.1 |
| React DOM | 19.1.1 |
| React Router DOM | 6.26.0 |
| Lucide React | 0.400.0 |
| Tailwind CSS | 3.4.4 |
| Vite | 7.1.7 |

## Support

If you encounter issues not covered here:

1. Check the browser console for errors
2. Review the component code comments
3. Ensure all dependencies are installed
4. Try clearing caches and rebuilding

---

**Happy Building! 🚀**

