# 🦖 RAMPAGE REFACTOR - Code City Apocalypse

> **Turn boring debugging into an epic 3D battle!**  
> Your codebase becomes a city. Bugs become monsters. Deploy agents to hunt them down.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-MVP-orange)

---

## 🎮 What Is This?

**Rampage Refactor** is a gamified code visualization and debugging tool that:

- 🏙️ **Visualizes your codebase** as a beautiful 3D city
- 🐛 **Turns bugs into monsters** that attack your code buildings
- 🤖 **Lets you deploy AI agents** to hunt down and fix bugs
- 🎯 **Makes refactoring fun** with game mechanics and rewards

**1 File = 1 Building**  
Building height = lines of code  
Building size = file complexity  
Building color = file type (Python, JavaScript, etc.)

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Node.js 16+
- Modern web browser (Chrome, Firefox, Safari)

### Installation

```bash
# 1. Clone or download this repository
cd rampage-refactor

# 2. Install backend dependencies
cd backend
pip install -r requirements.txt

# 3. Install frontend dependencies
cd ../frontend
npm install
# OR if you prefer yarn:
yarn install

# 4. Start the backend server
cd ../backend
python server.py
# Backend will run on http://localhost:8765

# 5. In a new terminal, start the frontend
cd ../frontend
npm start
# Frontend will open at http://localhost:3000
```

---

## 📖 How To Use

### Step 1: Point at Your Codebase
1. Open the app in your browser (http://localhost:3000)
2. Click **"📁 SELECT FOLDER"**
3. Enter the path to your code folder (e.g., `/home/user/my-project`)

### Step 2: Scan & Generate City
1. Click **"🔍 SCAN CODEBASE"**
2. Watch as your code transforms into a 3D city!
3. Buildings appear based on your files
4. Monsters spawn where bugs are detected

### Step 3: Hunt Bugs
1. Click on any **monster** to see bug details
2. Click **"Open in Editor"** to jump to the buggy line
3. Fix the bug manually in your code editor
4. Click **"Re-scan"** to see the monster disappear!

### Step 4: Deploy Agents (Optional)
1. Click **"🤖 DEPLOY AGENT"**
2. Watch agents hunt down monsters with laser effects
3. Agents show suggested fixes (read-only)
4. You decide whether to apply them

---

## 🗂️ Project Structure

```
rampage-refactor/
├── README.md           ← You are here!
├── docs/
│   ├── SETUP.md       ← Detailed setup guide
│   ├── API.md         ← Backend API documentation
│   └── TROUBLESHOOTING.md
├── backend/
│   ├── server.py      ← Main FastAPI server
│   ├── scanner.py     ← Code analysis engine
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── package.json
│   ├── public/
│   └── src/
│       ├── App.js     ← Main React component
│       ├── City3D.js  ← Three.js city renderer
│       └── components/
└── tests/
```

---

## 🎨 Features

### ✅ Phase 1 (MVP - Current)
- [x] 3D city visualization with Three.js
- [x] Real filesystem scanning
- [x] Python & JavaScript bug detection
- [x] Manual fix workflow
- [x] Dynamic monster animations
- [x] Building damage effects
- [x] Points & gamification
- [x] File watching (auto re-scan)

### 🚧 Phase 2 (Coming Soon)
- [ ] AI-powered fix suggestions (optional API key)
- [ ] Multiplayer mode (collaborate with team)
- [ ] Code metrics dashboard
- [ ] Export city as image/video
- [ ] Support for more languages (Java, C++, Go, Rust)
- [ ] Desktop app (Electron)

---

## 🛠️ Configuration

### Backend Configuration

Edit `backend/.env`:

```env
# Backend settings
PORT=8765
HOST=localhost

# Code scanning
MAX_FILE_SIZE=1048576  # 1MB max per file
SUPPORTED_EXTENSIONS=.py,.js,.ts,.jsx,.tsx,.java,.cpp,.c,.go,.rs

# Optional: AI integration (Phase 2)
# OPENAI_API_KEY=your-key-here
# ANTHROPIC_API_KEY=your-key-here
```

### Frontend Configuration

Edit `frontend/.env`:

```env
REACT_APP_BACKEND_URL=http://localhost:8765
REACT_APP_ENABLE_AI=false
```

---

## 🐛 Supported Bug Types

| Bug Type | Language | Monster Shape | Color |
|----------|----------|---------------|-------|
| Syntax Error | Python, JS | Spiky Cone | 🔴 Red |
| Undefined Variable | Python, JS | Sphere | 🟠 Orange |
| Console.log | JavaScript | Sphere | 🟡 Yellow |
| Unused Import | Python | Cube | 🟣 Purple |
| Line Too Long | All | Small Cube | 🔵 Blue |
| Type Error | Python, TS | Octahedron | 🔴 Red |

---

## 📝 File Extensions Reference

**When saving/renaming files:**

```
Backend files:
  server.py          ← Python script
  scanner.py         ← Python script
  requirements.txt   ← Text file
  .env               ← Environment file (no extension)

Frontend files:
  App.js             ← JavaScript React component
  City3D.js          ← JavaScript Three.js code
  package.json       ← JSON config file
  index.html         ← HTML file
  styles.css         ← CSS stylesheet

Documentation:
  README.md          ← Markdown file
  SETUP.md           ← Markdown file
```

---

## 🚢 Deployment

### Deploy Anywhere (No Vendor Lock-in!)

**Backend options:**
- DigitalOcean Droplet
- AWS EC2
- Google Cloud Run
- Any VPS with Python
- Docker container

**Frontend options:**
- Vercel (free tier)
- Netlify (free tier)
- GitHub Pages
- AWS S3 + CloudFront
- Any static hosting

### Docker Deployment (Coming Soon)

```bash
docker-compose up
```

---

## 🤝 Contributing

This is an open-source project! Contributions welcome:

1. Fork the repo
2. Create a feature branch: `git checkout -b feature/awesome-feature`
3. Commit changes: `git commit -m 'Add awesome feature'`
4. Push to branch: `git push origin feature/awesome-feature`
5. Open a Pull Request

---

## 📄 License

MIT License - Use it however you want!

---

## 🆘 Troubleshooting

### Backend won't start
```bash
# Check Python version
python --version  # Should be 3.8+

# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend won't connect
```bash
# Check if backend is running
curl http://localhost:8765/health

# Check frontend .env file
cat frontend/.env
# Should have: REACT_APP_BACKEND_URL=http://localhost:8765
```

### No monsters appearing
- Make sure your code folder actually has bugs!
- Check backend logs for scanning errors
- Try scanning a different folder

### "WebSocket connection failed"
- Backend server might not be running
- Check firewall settings
- Try restarting both backend and frontend

**More help:** See `docs/TROUBLESHOOTING.md`

---

## 💰 Support Development

If this tool helps you, consider:
- ⭐ Star this repo
- 🐦 Share on Twitter
- ☕ Buy me a coffee (link coming soon)
- 💼 Hire me for custom features

---

## 🎯 Roadmap

- **Q1 2025**: MVP release
- **Q2 2025**: AI integration, multiplayer
- **Q3 2025**: Desktop app, VS Code extension
- **Q4 2025**: Enterprise features, analytics

---

**Made with 🔥 by [Your Name]**  
**Questions?** Open an issue or email: your@email.com

---

> *"Debugging is like monster hunting - except the monsters are invisible and made of semicolons."*
