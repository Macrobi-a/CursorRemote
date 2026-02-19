# Remote Access: Run from Any Computer

Access your recruitment workflow from any computer via browser. Three options:

## Option 1: Deploy Chainlit to Railway (Recommended)

**Best for:** Always-on browser access, no setup on new computers.

### Steps

1. **Push code to GitHub** (if not already):
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Deploy to Railway**:
   - Go to https://railway.app
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repo
   - Railway auto-detects the Dockerfile

3. **Set environment variables** in Railway dashboard:
   - `GEMINI_API_KEY`
   - `ANTHROPIC_API_KEY`
   - `INSTANTLY_API_KEY` (optional)
   - `HEYGEN_API_KEY` (optional)
   - `STRIPE_SECRET_KEY` (optional)
   - `PORT=8000` (Railway sets this automatically)

4. **Update Dockerfile for Chainlit** (see below)

5. **Get your URL**: Railway gives you a URL like `https://your-app.up.railway.app`

6. **Access from any computer**: Open that URL in any browser, anywhere.

### Update Dockerfile for Chainlit

The current Dockerfile runs `server.py` (FastAPI). To run Chainlit instead, create `Dockerfile.chainlit`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .
RUN rm -rf .venv __pycache__ output/__pycache__ output/agents/__pycache__ 2>/dev/null; true

ENV PYTHONUNBUFFERED=1
EXPOSE 8000

# Run Chainlit (browser UI) instead of FastAPI server
CMD ["chainlit", "run", "app.py", "--host", "0.0.0.0", "--port", "8000"]
```

Then in Railway, set the Dockerfile path to `Dockerfile.chainlit` (or rename it to `Dockerfile`).

---

## Option 2: GitHub Codespaces (Cloud Dev Environment)

**Best for:** Full development environment accessible from any computer, edit code and run Chainlit.

### Steps

1. **Push code to GitHub** (if not already)

2. **Create Codespace**:
   - Go to your repo on GitHub
   - Click "Code" → "Codespaces" → "Create codespace on main"
   - Wait ~2 minutes for setup

3. **In Codespace terminal**:
   ```bash
   # Install deps
   pip install -r requirements.txt
   
   # Set env vars (or use Codespace secrets)
   export GEMINI_API_KEY="your_key"
   export ANTHROPIC_API_KEY="your_key"
   
   # Run Chainlit
   chainlit run app.py -w
   ```

4. **Access Chainlit**:
   - Codespace shows a popup: "Forwarded Ports" → click "Open in Browser" for port 8000
   - Or use the URL shown in the terminal

5. **From any computer**: Open the Codespace URL, then access Chainlit via the forwarded port.

**Note:** Codespaces auto-sleeps after 30 min inactivity (free tier). Paid tier stays on longer.

---

## Option 3: Persistent VPS (DigitalOcean, AWS EC2, etc.)

**Best for:** Full control, always-on, SSH access.

### Steps

1. **Create VPS** (e.g. DigitalOcean Droplet, AWS EC2 t2.micro)

2. **SSH in**:
   ```bash
   ssh root@your-server-ip
   ```

3. **Install dependencies**:
   ```bash
   apt update && apt install -y python3.11 python3-pip git
   git clone <your-repo-url>
   cd money-curs-proj
   pip3 install -r requirements.txt
   ```

4. **Set env vars** (use `export` or `.env` file)

5. **Run Chainlit with screen/tmux** (so it stays running after SSH disconnect):
   ```bash
   screen -S chainlit
   chainlit run app.py --host 0.0.0.0 --port 8000
   # Press Ctrl+A then D to detach
   ```

6. **Access from any computer**: `http://your-server-ip:8000`

**Security:** Use a firewall (UFW) and only open port 8000, or use a reverse proxy (nginx) with HTTPS.

---

## Quick Comparison

| Option | Cost | Setup Time | Always On | Edit Code | Best For |
|--------|------|------------|-----------|-----------|----------|
| **Railway** | $5-20/mo | 5 min | ✅ Yes | Via GitHub | Production use |
| **Codespaces** | Free/$4+/mo | 2 min | ⚠️ Sleeps | ✅ Full IDE | Development |
| **VPS** | $5-10/mo | 15 min | ✅ Yes | ✅ SSH + editor | Full control |

---

## Recommended: Railway for Chainlit

1. Use `Dockerfile.chainlit` (see above)
2. Deploy to Railway
3. Access from any browser: `https://your-app.up.railway.app`
4. No setup needed on new computers — just open the URL

**Pro tip:** Railway gives you a free $5 credit to start. After that it's pay-as-you-go (~$5-20/mo depending on usage).
