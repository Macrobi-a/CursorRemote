"""Load env vars for the pipeline. Create .env from .env.example."""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "").strip()
_DEFAULT_VIDEOS_PATH = r"C:\Users\Hafid\Downloads\rest abu musa pt 2"
COURSE_VIDEOS_PATH = os.getenv("COURSE_VIDEOS_PATH", "").strip() or _DEFAULT_VIDEOS_PATH
OUTPUT_DIR = Path(__file__).resolve().parent / "output"
SYSTEM_DESIGN_JSON = OUTPUT_DIR / "system_design.json"
AGENTS_DIR = OUTPUT_DIR / "agents"
