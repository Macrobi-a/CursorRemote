# Railway Deployment Troubleshooting

## Current Issue: Build Succeeds, Deploy Fails

If your deployment shows:
- ✅ Build: Success
- ❌ Deploy: Failed (not started)

## Fix Steps

### Step 1: Verify Dockerfile Settings in Railway

Railway might be using the wrong Dockerfile. Check:

1. **In Railway dashboard:**
   - Click your service **"CursorRemote"**
   - Go to **"Settings"** tab
   - Scroll to **"Build"** section
   - Check **"Dockerfile Path"**:
     - Should be: `Dockerfile` (default) OR `Dockerfile.chainlit`
     - Both are now fixed to use Railway's PORT env var

2. **If Railway is using `Dockerfile.chainlit`:**
   - Make sure it's set correctly in Settings → Build → Dockerfile Path
   - Or change it to `Dockerfile` (which is also fixed)

### Step 2: Check Deployment Logs

**Critical:** Click **"View logs"** on the failed deployment to see the actual error.

Common errors:

**Error: "ModuleNotFoundError: No module named 'agents'"**
- **Fix:** The `output/agents/` folder might not be in your repo
- **Solution:** Run locally: `python run_pipeline.py` (generates agents), then commit and push:
  ```powershell
  git add output/
  git commit -m "Add generated agents"
  git push origin main
  ```

**Error: "Port already in use" or "Cannot bind to port"**
- **Fix:** Railway sets PORT automatically - Dockerfile should use `${PORT:-8000}`
- **Status:** ✅ Already fixed in both Dockerfiles

**Error: "chainlit: command not found"**
- **Fix:** Chainlit not installed
- **Solution:** Check `requirements.txt` includes `chainlit>=1.0.0` ✅ Already included

**Error: "Import error" or "No module named 'master_graph'"**
- **Fix:** `output/master_graph.py` missing
- **Solution:** Run `python run_pipeline.py` locally, commit `output/` folder

### Step 3: Verify Required Files Are Committed

Run this locally to check:
```powershell
git ls-files output/master_graph.py
git ls-files output/agents/agent_*.py | Select-Object -First 3
```

If these don't show files, you need to:
1. Run `python run_pipeline.py` (generates agents + master_graph)
2. Commit: `git add output/` → `git commit -m "Add generated code"` → `git push`

### Step 4: Set Environment Variables

**In Railway dashboard:**
- Service → **"Variables"** tab
- Add:
  - `GEMINI_API_KEY` = your key
  - `ANTHROPIC_API_KEY` = your key

### Step 5: Manual Redeploy

After fixing issues:
1. Click **"Deployments"** tab
2. Click **"Deploy the repo Macrobi-a/CursorRemote"** button
3. Watch logs for errors

---

## Quick Checklist

- [ ] Railway Settings → Build → Dockerfile Path is set (either `Dockerfile` or `Dockerfile.chainlit`)
- [ ] `output/master_graph.py` exists in GitHub repo
- [ ] `output/agents/` folder exists in GitHub repo (at least a few agent files)
- [ ] `requirements.txt` includes `chainlit`
- [ ] Environment variables set in Railway (GEMINI_API_KEY, ANTHROPIC_API_KEY)
- [ ] Checked deployment logs for specific error message

---

## Most Likely Issue

**Missing `output/` folder in repo:**
- The generated agents and master_graph might not be committed
- Railway can't import them → deployment fails

**Quick fix:**
```powershell
# Generate agents locally (if not done)
python run_pipeline.py

# Commit and push
git add output/
git commit -m "Add generated agents and master graph"
git push origin main
```

Then Railway will redeploy automatically.
