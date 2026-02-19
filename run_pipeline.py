"""
Run the full pipeline: (1) videos -> Gemini -> system_design.json, (2) JSON -> Claude -> agent code + master graph.
Usage:
  python run_pipeline.py [path_to_video_folder]
If folder is omitted, uses DEFAULT_VIDEO_FOLDER below.
"""
import subprocess
import sys
from pathlib import Path

from config import SYSTEM_DESIGN_JSON

# Default folder for course videos (used when no CLI arg)
DEFAULT_VIDEO_FOLDER = r"C:\Users\Hafid\Downloads\rest abu musa pt 2"


def main() -> None:
    folder = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_VIDEO_FOLDER
    root = Path(__file__).resolve().parent

    # Step 1: Video folder -> system_design.json (skip if already present and user wants to only run step 2)
    if not SYSTEM_DESIGN_JSON.exists():
        print("--- Step 1: Video -> System Design JSON (Gemini) ---")
        r = subprocess.run([sys.executable, str(root / "video_to_system_design.py"), folder], cwd=root)
        if r.returncode != 0:
            sys.exit(r.returncode)
    else:
        print("system_design.json already exists. Skipping Step 1. Delete it to re-run from videos.")

    # Step 2: system_design.json -> agent files + master_graph.py (Claude)
    print("--- Step 2: System Design JSON -> Agents + Master Graph (Claude) ---")
    r = subprocess.run([sys.executable, str(root / "generate_agents_from_design.py")], cwd=root)
    sys.exit(r.returncode if r.returncode != 0 else 0)


if __name__ == "__main__":
    main()
