# Railway Deployment: Quick Checklist

## ✅ Pre-Deployment Checklist

- [ ] Project has `Dockerfile.chainlit`
- [ ] Project has `requirements.txt`
- [ ] Project has `app.py` (Chainlit app)
- [ ] `.env` file exists (for reference - you'll copy keys to Railway)
- [ ] GitHub account ready
- [ ] Railway account ready (or will create)

---

## 🚀 Deployment Steps (20 minutes)

### Step 1: Push to GitHub (5 min)
```powershell
git init                                    # If not already a git repo
git add .
git commit -m "Ready for Railway"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```
**✅ Check:** Code visible at `github.com/YOUR_USERNAME/YOUR_REPO`

---

### Step 2: Railway Setup (2 min)
1. Go to https://railway.app
2. Click "Start a New Project"
3. Sign up with GitHub (or email)
4. Authorize Railway to access GitHub

**✅ Check:** Logged into Railway dashboard

---

### Step 3: Deploy from GitHub (1 min)
1. Click "New Project"
2. Select "Deploy from GitHub repo"
3. Choose your repository
4. Click "Deploy Now"

**✅ Check:** Railway shows "Building..." status

---

### Step 4: Verify Dockerfile (2 min)
1. Click your service
2. Go to "Settings" → "Build"
3. Verify: **Dockerfile Path** = `Dockerfile.chainlit`
4. If wrong, change it and save

**✅ Check:** Dockerfile path is `Dockerfile.chainlit`

---

### Step 5: Set Environment Variables (3 min)
1. Click your service → "Variables" tab
2. Click "New Variable" for each:

   **Required:**
   ```
   GEMINI_API_KEY = your_gemini_key
   ANTHROPIC_API_KEY = your_anthropic_key
   ```

   **Optional:**
   ```
   INSTANTLY_API_KEY = your_key (if you have)
   HEYGEN_API_KEY = your_key (if you have)
   STRIPE_SECRET_KEY = your_key (if you have)
   ```

3. Click "Add" after each

**✅ Check:** All variables show in list with green checkmarks

---

### Step 6: Wait for Build (3-5 min)
1. Watch "Deployments" tab
2. Click latest deployment → "View Logs"
3. Wait for "Build successful"

**✅ Check:** Status shows "Active" (green)

---

### Step 7: Get Your URL (1 min)
1. Click service → "Settings" → "Networking"
2. Click "Generate Domain" (if needed)
3. Copy URL: `https://your-app-name.up.railway.app`

**✅ Check:** You have a URL

---

### Step 8: Test (2 min)
1. Open URL in browser
2. Should see Chainlit welcome screen
3. Type "Start" in chat
4. Should see workflow steps

**✅ Check:** Chainlit UI works and you can interact

---

## 🎉 Success!

**Your app is now accessible at:** `https://your-app-name.up.railway.app`

**Access from any computer:** Just open the URL in any browser!

---

## 🔧 Common Issues

| Problem | Solution |
|---------|----------|
| **Healthcheck failed** | Healthcheck is disabled in repo so deploy can succeed. Open your app URL; if it loads, you're good. To re-enable: Railway → Settings → Deploy → set Healthcheck Path to `/`. |
| Build fails | Check logs → verify `Dockerfile.chainlit` exists in repo |
| "Dockerfile not found" | Settings → Build → set Dockerfile Path to `Dockerfile.chainlit` |
| App doesn't load | Open **Deploy Logs** (not Build Logs) to see Chainlit startup and any Python errors |
| "Internal Server Error" | Check logs → likely missing `GEMINI_API_KEY` or `ANTHROPIC_API_KEY` |
| Blank page | Check **Deploy Logs** for Python/import errors |

---

## 📝 Notes

- **Cost:** Free $5 credit, then ~$5-20/month
- **Updates:** Push to GitHub → Railway auto-deploys
- **Logs:** Service → Deployments → View Logs
- **Env vars:** Set in Railway dashboard, NOT in `.env` file

---

**Full guide:** See `RAILWAY_DEPLOY_STEPS.md` for detailed instructions.
