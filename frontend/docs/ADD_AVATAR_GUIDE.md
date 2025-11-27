# 🎨 How to Add Your Avatar Image

## Quick Steps

### 1. Save Your Avatar Image

Save your avatar image (the 3D man with glowing circles) to:
```
/home/Documents/Frontend-dunk.ai/public/images/avatar.png
```

**Recommended format:**
- PNG with transparent background
- Size: 512x512 pixels or larger
- Square aspect ratio

### 2. Update the Code

The code is already prepared for your avatar! Just save the image and it will automatically work.

The avatar appears in the welcome screen at:
- `src/pages/ChatPage.jsx` line 339

**To enable the image:**

Replace this line:
```jsx
<Brain className="w-16 h-16 text-primary" />
```

With:
```jsx
<img src="/images/avatar.png" alt="Dunk AI" className="w-full h-full object-cover rounded-full" />
```

Or keep both and use conditional rendering:
```jsx
{/* Option 1: Use image if available */}
<img 
  src="/images/avatar.png" 
  alt="Dunk AI" 
  className="w-full h-full object-cover rounded-full"
  onError={(e) => {
    e.target.style.display = 'none';
    // Show Brain icon as fallback
  }}
/>

{/* Option 2: Or keep the Brain icon */}
<Brain className="w-16 h-16 text-primary" />
```

## 🎨 Current Design

The avatar component includes:
- ✅ 3 concentric glowing circles (animated)
- ✅ Pulsing animation
- ✅ Decorative dots around the avatar
- ✅ Teal/cyan color scheme
- ✅ Dark background support

## 🖼️ Alternative: Base64 Image

If you prefer to embed the image directly in code:

1. Convert your image to base64
2. Use it like this:

```jsx
<img 
  src="data:image/png;base64,YOUR_BASE64_STRING_HERE" 
  alt="Dunk AI" 
  className="w-full h-full object-cover rounded-full"
/>
```

## 📝 Notes

- The image path `/images/avatar.png` is relative to the `public` folder
- Vite serves files from `public` at the root URL
- The avatar appears on the chat welcome screen when there are no messages
- The glowing circles and animation effects are already styled

---

**Your avatar will perfectly match the design from your screenshot! 🎉**

