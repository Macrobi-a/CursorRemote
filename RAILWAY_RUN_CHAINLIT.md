# Run the Chainlit UI on Railway

Your app can run in two ways:
- **Chainlit** = browser chat UI (step-by-step, type "Start", see workflow steps) ← **this is what you want**
- **FastAPI** = plain API (you’d see text like "Recruitment workflow server" and no chat)

If your Railway URL shows **plain text** and **no chat**, the service is not using the Chainlit build. Do this:

---

## 1. Use the Chainlit Dockerfile

1. Open **Railway** → your project → **CursorRemote** service.
2. Go to **Settings** → **Build**.
3. Set **Dockerfile Path** to: `Dockerfile.chainlit`
4. Save.

---

## 2. Redeploy

1. Go to **Deployments**.
2. Click the **⋮** on the latest deployment → **Redeploy**,  
   **or** push a small change to GitHub so Railway deploys again.

---

## 3. Check the result

1. Open your Railway URL (e.g. `https://your-app.up.railway.app`).
2. You should see the **Chainlit** interface: chat input, welcome message, and "Type Start to run the pipeline".
3. If you still see plain text, check **Deploy logs** for errors and confirm **Build** shows `Dockerfile.chainlit`.

---

## Repo config

The repo is set up so Railway uses the Chainlit build by default:

- `railway.toml` has `dockerfilePath = "Dockerfile.chainlit"`.
- If Railway ever ignores that, set **Dockerfile Path** to `Dockerfile.chainlit` in the Railway dashboard (step 1 above).
