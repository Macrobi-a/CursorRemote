# Quick Start: Access from Any Computer

## 🎯 Fastest Path (5 minutes)

**Deploy Chainlit to Railway** — then access from any browser, anywhere.

### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin <your-github-repo-url>
git push -u origin main
```

### Step 2: Deploy to Railway
1. Go to https://railway.app → Sign up (free $5 credit)
2. Click **"New Project"** → **"Deploy from GitHub repo"**
3. Select your repo
4. Railway auto-detects `Dockerfile.chainlit`

### Step 3: Set Environment Variables
In Railway dashboard → your project → **Variables**:
- `GEMINI_API_KEY` = your key
- `ANTHROPIC_API_KEY` = your key
- (Optional) `INSTANTLY_API_KEY`, `HEYGEN_API_KEY`, `STRIPE_SECRET_KEY`

### Step 4: Get Your URL
Railway gives you: `https://your-app-name.up.railway.app`

**Done!** Open that URL from **any computer** — your Chainlit UI is there.

---

## 🔄 Alternative: GitHub Codespaces (Cloud Dev)

If you want to **edit code** from any computer:

1. Push to GitHub (same as above)
2. Go to your repo → **Code** → **Codespaces** → **Create codespace**
3. In Codespace terminal:
   ```bash
   pip install -r requirements.txt
   export GEMINI_API_KEY="your_key"
   export ANTHROPIC_API_KEY="your_key"
   chainlit run app.py -w
   ```
4. Click **"Forwarded Ports"** → open port 8000 in browser

**Note:** Codespaces sleeps after 30 min (free tier). Railway stays on 24/7.

---

## 📋 What You Get

- ✅ **Browser UI** (Chainlit) — no terminal needed
- ✅ **Step-by-step view** — see each agent run
- ✅ **Human steps in chat** — reply in browser, not terminal
- ✅ **Persistent state** — SQLite checkpoints survive reloads
- ✅ **Access from anywhere** — just open the URL

---

## 🆘 Troubleshooting

**Railway deployment fails?**
- Check `Dockerfile.chainlit` exists
- Verify env vars are set in Railway dashboard
- Check Railway logs: `railway logs`

**Can't access the URL?**
- Railway may take 2-3 minutes to deploy
- Check Railway dashboard → your service → "Deployments" for status

**Want to update code?**
- Push to GitHub → Railway auto-deploys (if connected)
- Or run `railway up` manually

---

**See `REMOTE_ACCESS.md` for detailed options (Railway, Codespaces, VPS).**
