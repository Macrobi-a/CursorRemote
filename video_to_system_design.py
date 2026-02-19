"""
Step 1: Watch a folder of MP4 course videos, send to Gemini, get System Design JSON.
Output: output/system_design.json (agents, tools, human_nodes, edges).
"""
import json
import sys
import time
from pathlib import Path

from google import genai
from google.genai import types

from config import GEMINI_API_KEY, OUTPUT_DIR, SYSTEM_DESIGN_JSON

# Default when no CLI arg (must match run_pipeline.py or pass folder explicitly)
DEFAULT_VIDEO_FOLDER = r"C:\Users\Hafid\Downloads\rest abu musa pt 2"

# Max videos per Gemini request (limit to stay under 1M token context; ~300 tokens/sec per video)
MAX_VIDEOS_PER_REQUEST = 2
MODEL = "gemini-2.5-flash"

SYSTEM_DESIGN_PROMPT = """You are analyzing a business course delivered as video(s). Your job is to produce a single System Design as valid JSON.

Identify every task the course teaches (e.g. outreach, content creation, booking meetings, follow-ups, reporting). For each task that can be automated, define an AGENT. For each task that is best done by a human (e.g. live client meetings, negotiations, in-person events), define a HUMAN NODE. Be exhaustive: the goal is to automate as much as possible and clearly list what the human must do.

Output ONLY valid JSON with this exact structure (no markdown, no code block wrapper):
{
  "course_summary": "One-paragraph summary of the business course.",
  "agents": [
    {
      "id": "agent_<snake_case>",
      "name": "Human-readable name",
      "role": "What this agent does.",
      "tools": ["tool1", "tool2"],
      "inputs": ["input1", "input2"],
      "outputs": ["output1", "output2"],
      "depends_on": ["agent_id_or_empty"]
    }
  ],
  "human_nodes": [
    {
      "id": "human_<snake_case>",
      "description": "What the human does.",
      "trigger_condition": "When this is needed.",
      "inputs_from_agents": ["output_from_agent"],
      "outputs_for_agents": ["what_human_produces_for_agents"]
    }
  ],
  "edges": [
    { "from": "start", "to": "agent_id" },
    { "from": "agent_id", "to": "human_id", "condition": "optional_condition" },
    { "from": "human_id", "to": "agent_id", "condition": "optional_condition" }
  ]
}

Rules:
- Use only the keys above. Agent ids must be in edges (from/to) and match agent id or "start". Human node ids must match human_nodes[].id.
- List every automatable task as an agent (outreach, research, content, scheduling, CRM, reporting, etc.).
- List every human-only task as a human_node (meetings, calls, signatures, in-person).
- Edges define flow: start -> agents -> human_nodes -> agents as needed."""


def get_mp4_paths(folder: str) -> list[Path]:
    folder_path = Path(folder)
    if not folder_path.is_dir():
        return []
    return sorted(folder_path.glob("*.mp4"))


def upload_videos(client: genai.Client, paths: list[Path]) -> list:
    """Upload videos via Files API; return list of file references for generate_content."""
    refs = []
    for p in paths:
        try:
            f = client.files.upload(file=str(p))
            refs.append(f)
            print(f"  Uploaded: {p.name}", flush=True)
        except Exception as e:
            print(f"  Skip {p.name}: {e}", flush=True)
    return refs


def wait_for_processing(client: genai.Client, file_refs: list) -> None:
    """Poll until all files are in ACTIVE state (required before generate_content)."""
    for f in file_refs:
        name = getattr(f, "name", None)
        if not name:
            continue
        while True:
            current = client.files.get(name=name)
            state = getattr(current, "state", None)
            state_str = (getattr(state, "name", None) or str(state) or "").upper()
            if state == types.FileState.ACTIVE or state_str == "ACTIVE":
                break
            if state == types.FileState.FAILED or state_str == "FAILED":
                raise RuntimeError(f"File {name} processing failed (state={state})")
            time.sleep(5)
            print(f"  Waiting for file to be ready... ({state})", flush=True)


def run_gemini(client: genai.Client, file_refs: list, prompt: str) -> str:
    """Send video refs + prompt to Gemini; return response text. Text after files per API docs."""
    contents = [*file_refs, prompt]
    response = client.models.generate_content(model=MODEL, contents=contents)
    return response.text if hasattr(response, "text") else (response.candidates[0].content.parts[0].text if response.candidates else "")


def extract_json(text: str) -> dict:
    """Strip markdown code block if present and parse JSON."""
    s = text.strip()
    if s.startswith("```"):
        lines = s.split("\n")
        if lines[0].startswith("```"):
            lines = lines[1:]
        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]
        s = "\n".join(lines)
    return json.loads(s)


def main() -> None:
    folder = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_VIDEO_FOLDER
    if not GEMINI_API_KEY:
        print("Set GEMINI_API_KEY in .env", file=sys.stderr)
        sys.exit(1)

    paths = get_mp4_paths(folder)
    if not paths:
        print(f"No .mp4 files in {folder}. Add videos and run again.", file=sys.stderr)
        sys.exit(2)

    n_batches = (len(paths) + MAX_VIDEOS_PER_REQUEST - 1) // MAX_VIDEOS_PER_REQUEST
    print(f"Found {len(paths)} video(s). Processing in {n_batches} batch(es) of up to {MAX_VIDEOS_PER_REQUEST} video(s) each.", flush=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    client = genai.Client(api_key=GEMINI_API_KEY)

    # Process in batches of MAX_VIDEOS_PER_REQUEST
    all_designs = []
    for i in range(0, len(paths), MAX_VIDEOS_PER_REQUEST):
        batch = paths[i : i + MAX_VIDEOS_PER_REQUEST]
        print(f"Uploading batch {i // MAX_VIDEOS_PER_REQUEST + 1} ({len(batch)} videos)...", flush=True)
        refs = upload_videos(client, batch)
        if not refs:
            print("No files uploaded in this batch.", flush=True)
            continue
        print("Waiting for videos to be processed (ACTIVE)...", flush=True)
        wait_for_processing(client, refs)
        print("Calling Gemini...", flush=True)
        raw = run_gemini(client, refs, SYSTEM_DESIGN_PROMPT)
        try:
            design = extract_json(raw)
            all_designs.append(design)
        except json.JSONDecodeError as e:
            print(f"Gemini returned invalid JSON: {e}. Saving raw response.", flush=True)
            (OUTPUT_DIR / "gemini_raw_response.txt").write_text(raw, encoding="utf-8")
            sys.exit(3)

    if not all_designs:
        print("No videos were uploaded successfully. Check your GEMINI_API_KEY in .env (get a key at https://aistudio.google.com/apikey).", file=sys.stderr)
        sys.exit(4)

    # If multiple batches, merge into one design (simple merge: take first and merge agents/human_nodes/edges)
    if len(all_designs) == 1:
        final = all_designs[0]
    else:
        final = {
            "course_summary": all_designs[0].get("course_summary", "") + " [Merged from multiple video batches.]",
            "agents": [],
            "human_nodes": [],
            "edges": [],
        }
        seen_agent_ids = set()
        seen_human_ids = set()
        for d in all_designs:
            for a in d.get("agents", []):
                if a.get("id") and a["id"] not in seen_agent_ids:
                    seen_agent_ids.add(a["id"])
                    final["agents"].append(a)
            for h in d.get("human_nodes", []):
                if h.get("id") and h["id"] not in seen_human_ids:
                    seen_human_ids.add(h["id"])
                    final["human_nodes"].append(h)
            for e in d.get("edges", []):
                final["edges"].append(e)

    SYSTEM_DESIGN_JSON.write_text(json.dumps(final, indent=2), encoding="utf-8")
    print(f"Saved: {SYSTEM_DESIGN_JSON}", flush=True)


if __name__ == "__main__":
    main()
