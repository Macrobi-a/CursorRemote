"""
View the recruitment workflow as a diagram (all agents and how they're connected).
Run: python view_workflow_diagram.py
Opens workflow_diagram.html in your browser, or prints Mermaid to the console.
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "output"))

from langgraph.checkpoint.memory import MemorySaver
from master_graph import get_graph_for_chainlit


def get_mermaid_diagram() -> str:
    """Generate Mermaid flowchart source for the recruitment workflow graph."""
    graph = get_graph_for_chainlit(MemorySaver())
    return graph.get_graph().draw_mermaid()


def main():
    mermaid = get_mermaid_diagram()
    out_file = ROOT / "workflow_diagram.html"

    html = f"""<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Recruitment workflow – agent diagram</title>
  <script type="module">
    import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
    mermaid.initialize({{ startOnLoad: true, theme: 'dark', flowchart: {{ curve: 'linear' }} }});
  </script>
  <style>
    body {{ font-family: system-ui, sans-serif; background: #1a1a1a; color: #e0e0e0; margin: 1rem; }}
    h1 {{ margin-bottom: 0.5rem; }}
    p {{ color: #888; margin-bottom: 1rem; }}
    .mermaid {{ background: #252525; padding: 1rem; border-radius: 8px; }}
  </style>
</head>
<body>
  <h1>Recruitment workflow</h1>
  <p>All agents and human-in-the-loop, and how they are connected.</p>
  <div class="mermaid">
{mermaid}
  </div>
</body>
</html>
"""

    out_file.write_text(html, encoding="utf-8")
    print(f"Diagram saved to: {out_file.resolve()}")
    print("Open this file in your browser to view the workflow.")
    try:
        import webbrowser
        webbrowser.open(out_file.as_uri())
    except Exception:
        pass
    return mermaid


if __name__ == "__main__":
    main()
