# Running from Any Computer with Cursor

## ⚠️ What Cursor Can and Can't Do

**Cursor syncs:**
- ✅ Your Cursor settings (themes, extensions, AI preferences)
- ✅ Your Cursor account/login
- ❌ **NOT your project files** (code, `.env`, dependencies)

**So:** Downloading Cursor and logging in on a new computer gives you the editor, but **not your project**.

---

## ✅ Best Approach: Cursor + GitHub

**How it works:**
1. **On Computer A** (current):
   - Push project to GitHub
   - Cursor settings sync automatically

2. **On Computer B** (new):
   - Download Cursor → log in (settings sync)
   - Clone your GitHub repo: `git clone <your-repo-url>`
   - Open folder in Cursor
   - Set up Python + dependencies (see below)

**Setup on new computer:**
```bash
# 1. Clone repo
git clone <your-repo-url>
cd money-curs-proj

# 2. Create venv and install deps
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt

# 3. Copy .env.example to .env and fill in keys
copy .env.example .env
# Edit .env with your API keys

# 4. Run Chainlit
chainlit run app.py -w
```

**Time:** ~5-10 minutes per new computer.

---

## 🚀 Even Better: Cursor + Railway Deployment

**Why:** You don't need to "run" locally on each computer — just access the browser URL.

**Setup once:**
1. Push to GitHub
2. Deploy to Railway (see `QUICK_START_REMOTE.md`)
3. Get your URL: `https://your-app.up.railway.app`

**On any new computer:**
1. Download Cursor → log in
2. Clone repo (if you want to edit code)
3. **Or just open the Railway URL in any browser** — no setup needed!

**Benefits:**
- ✅ No Python/dependency setup on new computers
- ✅ No `.env` file management
- ✅ Always running (24/7)
- ✅ Access from phone/tablet too

---

## 📋 Comparison

| Method | Setup Time | Need Python? | Need .env? | Always On? |
|--------|------------|--------------|------------|------------|
| **Cursor + GitHub** | 5-10 min | ✅ Yes | ✅ Yes | ❌ No |
| **Cursor + Railway** | 5 min (once) | ❌ No | ❌ No* | ✅ Yes |
| **Just Railway URL** | 0 min | ❌ No | ❌ No | ✅ Yes |

*Env vars set in Railway dashboard, not local `.env`

---

## 🎯 Recommended Workflow

**For development (editing code):**
- Use **Cursor + GitHub** on each computer
- Clone, setup venv, run locally

**For using the app (running workflows):**
- Deploy to **Railway** once
- Access from any browser (any computer, phone, tablet)
- No setup needed

**Best of both worlds:**
- Deploy to Railway → use browser URL from anywhere
- Keep GitHub repo → clone on computers where you want to edit code in Cursor

---

## 🔧 Quick Setup Script for New Computer

Create `setup_new_computer.ps1`:

```powershell
# Setup project on a new computer
Write-Host "Setting up recruitment workflow..." -ForegroundColor Cyan

# Clone if not exists
if (-not (Test-Path "money-curs-proj")) {
    git clone <your-repo-url> money-curs-proj
    cd money-curs-proj
} else {
    cd money-curs-proj
    git pull
}

# Create venv
python -m venv .venv
.venv\Scripts\activate

# Install deps
pip install -r requirements.txt

# Setup .env
if (-not (Test-Path ".env")) {
    Copy-Item .env.example .env
    Write-Host "⚠️  Edit .env and add your API keys!" -ForegroundColor Yellow
}

Write-Host "✅ Setup complete! Run: chainlit run app.py -w" -ForegroundColor Green
```

---

## 💡 Pro Tip

**Use Railway for the app, GitHub for code:**

1. **Railway URL** = Use the app from anywhere (browser)
2. **GitHub repo** = Edit code in Cursor on any computer

This way:
- You can use the app from any device (no setup)
- You can edit code when needed (clone + setup once per computer)
- Best of both worlds!
