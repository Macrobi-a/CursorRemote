# Chainlit browser UI

Run the recruitment workflow in the browser instead of the terminal (Lovable-style step-by-step view).

## Quick start

```bash
# From project root (with venv activated)
pip install chainlit langgraph-checkpoint-sqlite
chainlit run app.py -w
```

Then open the URL (e.g. http://localhost:8000) in your browser.

- **`-w`** = watch mode: when you save code in Cursor, Chainlit reloads so you see changes without restarting by hand.

## What you get

- **Steps view** — Each graph node (agent or human) appears as a collapsible step. Click into a step to see that node’s output (agentic debugging).
- **Chat** — When the graph pauses at a human step, the UI asks for your input. Reply in the chat; your message is fed back into the graph as `pending_human_input`.
- **Persistence** — State is stored in `data/recruitment_checkpoints.sqlite`. If Chainlit reloads (e.g. after a code change), the run resumes from the last checkpoint so you don’t lose progress.

## Side-by-side (Lovable-style)

1. Cursor on one side (code).
2. Browser with Chainlit on the other.
3. Edit the graph or an agent in Cursor and save.
4. With `-w`, Chainlit reloads and the UI reflects the new code; next run uses the updated logic.

## Human steps

When the graph hits **human_in_the_loop** (e.g. outbound caller, client job intake), it **interrupts** and the UI shows a “Human step” message. Type your reply in the chat and send. That reply is injected into the graph and the run continues until the next human step or end.

Type **done** or **exit** in chat when asked for input to end the workflow.

## If you lose chat session on reload

Checkpoints (graph state) are in SQLite, but the **Chainlit chat session** (which thread_id we use) is in memory. For a single user, one thread per browser tab is usually enough. For “stickier” sessions across reloads you can persist the Chainlit session (see Chainlit docs) or reuse a fixed `thread_id` from a cookie/database.
