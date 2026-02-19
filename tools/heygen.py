"""
HeyGen API (AI video generation). Use for candidate outreach videos, follow-up videos.
Docs: https://docs.heygen.com/
"""
import os
from typing import Any, Dict

try:
    import requests
except ImportError:
    requests = None

BASE_URL = "https://api.heygen.com/v2"
_API_KEY = os.environ.get("HEYGEN_API_KEY", "").strip()


def _headers() -> Dict[str, str]:
    return {"X-Api-Key": _API_KEY, "Content-Type": "application/json"}


def heygen_create_video(
    script: str,
    avatar_id: str | None = None,
    voice_id: str | None = None,
    title: str | None = None,
) -> Dict[str, Any]:
    """
    Create an avatar video from script text.
    Returns { ok, video_id?, status?, error? }. Poll video status for URL when ready.
    """
    if not _API_KEY or not requests:
        return {"ok": False, "error": "HEYGEN_API_KEY not set or requests not installed", "stub": True}
    url = f"{BASE_URL}/video/generate"
    payload = {
        "video_inputs": [{"character": {"type": "avatar", "avatar_id": avatar_id or "default"}, "voice": {"type": "text", "input_text": script[:5000], "voice_id": voice_id or "1bd001e7e50f421d891986aad7298c22"}}],
        "dimension": {"width": 1920, "height": 1080},
        "title": title or "Recruitment outreach",
    }
    try:
        r = requests.post(url, json=payload, headers=_headers(), timeout=60)
        data = r.json() if r.text else {}
        if r.status_code >= 400:
            return {"ok": False, "error": data.get("message", r.text), "status_code": r.status_code}
        return {"ok": True, "video_id": data.get("data", {}).get("video_id"), "status": data.get("data", {}).get("status")}
    except Exception as e:
        return {"ok": False, "error": str(e)}
