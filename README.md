# Course-to-Agents Pipeline

Turn a business course (MP4 videos) into a **System Design** (agents + human nodes) and then into **runnable Python agents** wired with **LangGraph** and **human-in-the-loop**.

## Flow

1. **You**: Put MP4 course videos in a folder (e.g. `course_videos/`).
2. **Gemini**: Watches/processes the folder, analyzes the videos, and outputs `output/system_design.json` with:
   - **Agents** – one per automatable task (e.g. outreach, content, scheduling).
   - **Tools** – what each agent uses.
   - **Human nodes** – tasks best done by a human (e.g. client meetings); the JSON tells you what you need to do.
3. **Claude**: Reads the JSON and generates:
   - One Python file per agent under `output/agents/`.
   - `output/master_graph.py` – a LangGraph graph that connects agents and a **human-in-the-loop** node for oversight and actions only humans can do.

## Setup

**Option A – One-time setup (PowerShell, run in project folder):**

```powershell
cd "c:\Users\Hafid\money curs proj"
# Create venv first (required before activation)
python -m venv .venv
# Activate it (if you get "cannot be loaded" run: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser)
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
# Edit .env and set GEMINI_API_KEY and ANTHROPIC_API_KEY
```

**Option B – Use the setup script:**

```powershell
cd "c:\Users\Hafid\money curs proj"
.\setup.ps1
# Then edit .env with your API keys
```

- **Error:** If `.\.venv\Scripts\Activate.ps1` is not recognized, the venv doesn’t exist yet. Run `python -m venv .venv` first, then run the activate command again.
- **Warning about `dotenv.exe` not on PATH:** You can ignore it. The pipeline uses the `python-dotenv` library from Python, not the `dotenv` CLI.
- **Gemini API key**: https://aistudio.google.com/apikey  
- **Anthropic API key**: https://console.anthropic.com/

## Usage

- **Full pipeline** (videos → JSON → code):

  ```bash
  python run_pipeline.py "C:\path\to\folder\with\mp4\videos"
  ```

  If you omit the path, it uses `COURSE_VIDEOS_PATH` from `.env` (default: `./course_videos`).

- **Step 1 only** (videos → `output/system_design.json`):

  ```bash
  python video_to_system_design.py "C:\path\to\video\folder"
  ```

- **Step 2 only** (JSON → agents + master graph; run after Step 1):

  ```bash
  python generate_agents_from_design.py
  ```

After Step 2, run the generated graph (e.g. from your app or):

```bash
python output/master_graph.py
```

(If Claude generates a different entry point, use that instead.)

## What Gets Generated

- **`output/system_design.json`** – Course summary, agents, human nodes, edges. Use this to see what’s automated and what the human must do.
- **`output/agents/<agent_id>.py`** – One file per agent; each can be used as a node in the graph.
- **`output/master_graph.py`** – LangGraph `StateGraph` with agent nodes, a `human_in_the_loop` node, and edges so data flows between agents and to/from the human.

## Human-in-the-loop

The design separates:

- **Agents** – Automatable steps (outreach, research, content, etc.).
- **Human nodes** – Steps that require a human (meetings, decisions, signatures). The JSON describes when they run and what inputs/outputs they use.

The generated `master_graph.py` includes a `human_in_the_loop` node that:

- Receives state when the workflow needs a human (e.g. after “meeting requested”).
- Returns updated state after the human provides input (e.g. meeting notes, next steps).

You can implement the human step with `input()`, a UI, or a callback.

## Models

- **Gemini**: Script uses `gemini-2.5-flash` for video analysis. You can change `MODEL` in `video_to_system_design.py` (e.g. to a “Pro” variant if available).
- **Claude**: Script uses `claude-sonnet-4-20250514` for code generation. Change `MODEL` in `generate_agents_from_design.py` if you use a different model (e.g. Opus).

## Optional: Fetch timeout

For URL fetching with a 60s timeout (e.g. in other scripts):

```bash
python fetch_with_timeout.py "https://example.com"
```
