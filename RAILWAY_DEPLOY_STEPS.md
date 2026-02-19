# Railway Deployment: Step-by-Step Guide

Deploy your Chainlit recruitment workflow to Railway so you can access it from any computer via browser.

---

## Prerequisites

- ✅ GitHub account (free)
- ✅ Railway account (free $5 credit to start)
- ✅ Your project code ready (with `Dockerfile.chainlit`)

---

## Step 1: Push Code to GitHub

**If you haven't already:**

1. **Open terminal/PowerShell in your project folder:**
   ```powershell
   cd "c:\Users\Hafid\money curs proj"
   ```

2. **Initialize git (if not already done):**
   ```powershell
   git init
   ```

3. **Create `.gitignore`** (already created, but verify it exists):
   - Should include: `.env`, `.venv/`, `__pycache__/`, `data/`

4. **Add all files:**
   ```powershell
   git add .
   ```

5. **Commit:**
   ```powershell
   git commit -m "Initial commit - ready for Railway deployment"
   ```

6. **Create GitHub repo:**
   - Go to https://github.com/new
   - Repository name: `recruitment-workflow` (or any name)
   - **Don't** initialize with README (you already have files)
   - Click "Create repository"

7. **Link and push:**
   ```powershell
   git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
   git branch -M main
   git push -u origin main
   ```
   Replace `YOUR_USERNAME` and `YOUR_REPO_NAME` with your actual GitHub username and repo name.

**✅ Done when:** You can see your code at `https://github.com/YOUR_USERNAME/YOUR_REPO_NAME`

---

## Step 2: Sign Up for Railway

1. **Go to:** https://railway.app
2. **Click:** "Start a New Project" or "Login"
3. **Sign up with:**
   - GitHub (recommended - easiest)
   - Or email
4. **Verify email** if needed
5. **You'll see:** Railway dashboard

**✅ Done when:** You're logged into Railway dashboard

---

## Step 3: Create New Project from GitHub

1. **In Railway dashboard, click:** "New Project"
2. **Select:** "Deploy from GitHub repo"
3. **Authorize Railway** (if first time) - allows Railway to access your GitHub repos
4. **Select your repository:** `YOUR_USERNAME/YOUR_REPO_NAME`
5. **Click:** "Deploy Now"

**✅ Done when:** Railway starts building your project (you'll see "Building..." status)

---

## Step 4: Configure Railway Settings

Railway should auto-detect `Dockerfile.chainlit`. If not:

1. **Click on your service** (the deployment)
2. **Go to:** "Settings" tab
3. **Check:**
   - **Root Directory:** `/` (default)
   - **Dockerfile Path:** `Dockerfile.chainlit` (should auto-detect)
   - **Start Command:** Leave empty (Dockerfile has CMD)

**If Dockerfile not detected:**
- Go to "Settings" → "Build"
- Set **Dockerfile Path:** `Dockerfile.chainlit`

**✅ Done when:** Settings show `Dockerfile.chainlit` as the build file

---

## Step 5: Set Environment Variables

**Critical:** Your API keys must be set here, not in `.env` (Railway doesn't use local `.env`).

1. **In Railway dashboard, click your service**
2. **Go to:** "Variables" tab
3. **Click:** "New Variable" for each:

   **Required:**
   - **Name:** `GEMINI_API_KEY`
     **Value:** `your_actual_gemini_key_here`
   
   - **Name:** `ANTHROPIC_API_KEY`
     **Value:** `your_actual_anthropic_key_here`

   **Optional (for tool bindings):**
   - **Name:** `INSTANTLY_API_KEY`
     **Value:** `your_instantly_key` (if you have one)
   
   - **Name:** `HEYGEN_API_KEY`
     **Value:** `your_heygen_key` (if you have one)
   
   - **Name:** `STRIPE_SECRET_KEY`
     **Value:** `your_stripe_key` (if you have one)

4. **Click:** "Add" after each variable
5. **Verify:** All variables show in the list

**✅ Done when:** All required env vars are set (green checkmarks)

---

## Step 6: Wait for Deployment

1. **Watch the build logs:**
   - Click your service → "Deployments" tab
   - Click the latest deployment → "View Logs"
   - You'll see: "Installing dependencies...", "Building...", etc.

2. **Wait for:** "Build successful" or "Deployment successful"
   - Usually takes 2-5 minutes

3. **If build fails:**
   - Check logs for errors
   - Common issues:
     - Missing `Dockerfile.chainlit` → verify it's in repo
     - Missing `requirements.txt` → verify it's in repo
     - Env var issues → check Step 5

**✅ Done when:** Deployment shows "Active" status (green)

---

## Step 7: Get Your Public URL

1. **In Railway dashboard, click your service**
2. **Go to:** "Settings" tab
3. **Scroll to:** "Networking" section
4. **Click:** "Generate Domain" (if no domain exists)
5. **Copy the URL:** Something like `https://your-app-name.up.railway.app`

**Or:**
- Click "Settings" → "Networking" → "Public Domain"
- Railway auto-generates one

**✅ Done when:** You have a URL like `https://your-app-name.up.railway.app`

---

## Step 8: Test Your Deployment

1. **Open the URL** in any browser
2. **You should see:**
   - Chainlit welcome screen
   - Or: "Recruitment workflow is active. Type Start..."

3. **Test the workflow:**
   - Type "Start" in the chat
   - You should see steps appearing (agent nodes running)
   - When a human step appears, reply in chat

**✅ Done when:** Chainlit UI loads and you can interact with it

---

## Step 9: (Optional) Custom Domain

If you want a custom domain:

1. **In Railway:** Settings → Networking → "Custom Domain"
2. **Add domain:** `your-domain.com`
3. **Follow DNS instructions** Railway provides
4. **Wait for DNS propagation** (5-30 minutes)

**✅ Done when:** Your custom domain works

---

## Troubleshooting

### Build Fails

**Error: "Dockerfile not found"**
- ✅ Verify `Dockerfile.chainlit` is in your GitHub repo
- ✅ Check Settings → Build → Dockerfile Path is `Dockerfile.chainlit`

**Error: "Module not found" or "Import error"**
- ✅ Check `requirements.txt` includes all dependencies
- ✅ Check build logs for missing packages

**Error: "Port already in use"**
- ✅ Railway sets `PORT` env var automatically - don't override it
- ✅ Dockerfile should use `$PORT` or `8000`

### App Doesn't Load

**"Connection refused" or blank page**
- ✅ Wait 2-3 minutes after deployment completes
- ✅ Check deployment logs for errors
- ✅ Verify env vars are set (Step 5)

**"Internal Server Error"**
- ✅ Check Railway logs: Service → Deployments → View Logs
- ✅ Common: Missing `GEMINI_API_KEY` or `ANTHROPIC_API_KEY`
- ✅ Verify `output/agents/` files exist (if not, run pipeline locally first and push)

### Human Steps Don't Work

**Graph pauses but no prompt appears**
- ✅ Check Railway logs for errors
- ✅ Verify `output/master_graph.py` exists in repo
- ✅ Check that `get_graph_for_chainlit()` function exists

---

## Updating Your Deployment

**When you change code:**

1. **Push to GitHub:**
   ```powershell
   git add .
   git commit -m "Update code"
   git push origin main
   ```

2. **Railway auto-deploys** (if connected to GitHub)
   - Or manually: Railway dashboard → "Redeploy"

3. **Wait 2-3 minutes** for new deployment

**✅ Done when:** New deployment shows "Active"

---

## Cost Estimate

- **Free tier:** $5 credit (enough for ~1 month of light usage)
- **After free credit:** ~$5-20/month depending on:
  - CPU/RAM usage
  - Bandwidth
  - Uptime

**Tip:** Railway charges per hour of usage. If you only use it occasionally, costs stay low.

---

## Quick Reference

| Step | Action | Time |
|------|--------|------|
| 1 | Push to GitHub | 5 min |
| 2 | Sign up Railway | 2 min |
| 3 | Deploy from GitHub | 1 min |
| 4 | Configure settings | 2 min |
| 5 | Set env vars | 3 min |
| 6 | Wait for build | 3-5 min |
| 7 | Get URL | 1 min |
| 8 | Test | 2 min |
| **Total** | | **~20 minutes** |

---

## Success Checklist

- [ ] Code pushed to GitHub
- [ ] Railway account created
- [ ] Project deployed from GitHub
- [ ] `Dockerfile.chainlit` detected
- [ ] `GEMINI_API_KEY` set in Railway
- [ ] `ANTHROPIC_API_KEY` set in Railway
- [ ] Deployment shows "Active"
- [ ] Public URL works in browser
- [ ] Chainlit UI loads
- [ ] Can type "Start" and see steps

**✅ All checked?** You're done! Access your app from any computer via the Railway URL.

---

## Next Steps

- **Bookmark your Railway URL** for easy access
- **Share the URL** with team members (if needed)
- **Monitor usage** in Railway dashboard → "Usage" tab
- **Set up alerts** if you want notifications

**Need help?** Check Railway docs: https://docs.railway.app
