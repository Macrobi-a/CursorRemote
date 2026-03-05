# Steps to See the Chainlit Chat UI

Follow these in order. Use **Option A** if your app is on Railway, or **Option B** to run it on your computer.

---

## Option A: See Chainlit on Railway (browser, no install)

### Step 1: Open Railway
1. Go to **https://railway.app**
2. Log in
3. Click your project (e.g. **zestful-nourishment** or the one with CursorRemote)

### Step 2: Open your service
1. Click the **CursorRemote** service card (the one that shows "Online" or your repo name)

### Step 3: Get your app URL
1. Click the **Settings** tab (or the **Variables** tab and look for a link to your app)
2. If you see **Networking** or **Public Networking**: click **Generate domain** if there’s no URL yet, then **copy the URL** (e.g. `https://cursorremote-production-xxxx.up.railway.app`)
3. If you don’t see that: try the **Deployments** tab → click the latest deployment → look for a **"View"** or **"Open"** link that opens your app, and copy that URL

### Step 4: Open the URL in your browser
1. Paste the URL into your browser’s address bar (Chrome, Edge, etc.)
2. Press **Enter**

### Step 5: You should see the Chainlit UI
- A chat window with a welcome message
- A text box at the bottom to type messages
- Text like “Recruitment workflow is active” or “Type **Start** to run the pipeline”

### Step 6: Run the workflow
1. Type **Start** (or any message) in the chat box
2. Press **Enter** or click Send
3. You should see steps appear (e.g. agent_lead_generation, agent_contact_info_lookup, etc.)

**If you see plain text instead of a chat window:** Your app might be running the API instead of Chainlit. Add variable `RAILWAY_DOCKERFILE_PATH` = `Dockerfile.chainlit` in Railway → Variables, then redeploy and open the URL again.

---

## Option B: See Chainlit on your computer (local)

### Step 1: Open the project in Cursor
1. Open **Cursor**
2. **File** → **Open Folder**
3. Select your project folder (e.g. `money curs proj` or `CursorRemote`) → **Select Folder**

### Step 2: Open a terminal in Cursor
1. **Terminal** → **New Terminal** (or press `` Ctrl+` ``)

### Step 3: Create a virtual environment (first time only)
In the terminal, run:
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
(If you already have `.venv` but get **"chainlit is not recognized"**, run the **Activate** and **pip install** lines again, then try Step 5.)

### Step 4: Set your API keys (first time only)
1. Copy `.env.example` to `.env` (or create `.env`)
2. Open `.env` and add your keys:
   ```
   GEMINI_API_KEY=your_key_here
   ANTHROPIC_API_KEY=your_key_here
   ```

### Step 5: Install dependencies (if you see "chainlit is not recognized")
Run these two lines **one after the other** in the same terminal:
```powershell
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```
Wait until `pip` finishes. Then run Step 6.

### Step 6: Run Chainlit
In the same terminal (with venv activated), run:
```powershell
chainlit run app.py -w
```

### Step 7: Open the UI in your browser
1. When you see “Your app is available at …” in the terminal, **click that link** (e.g. http://localhost:8000)
2. Or open your browser and go to: **http://localhost:8000**

### Step 8: You should see the Chainlit UI
- Chat window and welcome message
- Type **Start** and press Enter to run the workflow

---

## Quick checklist

- [ ] I’m on Railway (Option A) or in Cursor with the project open (Option B)
- [ ] I have the app URL (Railway) or ran `chainlit run app.py -w` (local)
- [ ] I opened that URL in my browser
- [ ] I see a chat box and welcome message (not plain text)
- [ ] I typed **Start** and see workflow steps

If something doesn’t match (e.g. no chat box, or “can’t connect”), say which step you’re on and what you see, and we can fix it.
