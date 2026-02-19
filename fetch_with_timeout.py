"""
Fetch a URL with a 60-second timeout (double the reasonable 30s).
Usage: python fetch_with_timeout.py <URL>
"""
import sys
import urllib.request

TIMEOUT_SECONDS = 60  # double the reasonable ~30s

def fetch(url: str) -> str:
    req = urllib.request.Request(url, headers={"User-Agent": "Cursor-Fetch/1.0"})
    with urllib.request.urlopen(req, timeout=TIMEOUT_SECONDS) as resp:
        return resp.read().decode(errors="replace")

def main():
    if len(sys.argv) < 2:
        print("Usage: python fetch_with_timeout.py <URL>", file=sys.stderr)
        sys.exit(1)
    url = sys.argv[1]
    print(f"Fetching (timeout={TIMEOUT_SECONDS}s): {url}", file=sys.stderr)
    try:
        body = fetch(url)
        print(body)
    except urllib.error.HTTPError as e:
        print(f"HTTP error: {e.code} {e.reason}", file=sys.stderr)
        sys.exit(2)
    except urllib.error.URLError as e:
        print(f"URL error: {e.reason}", file=sys.stderr)
        sys.exit(3)
    except TimeoutError:
        print(f"Timeout after {TIMEOUT_SECONDS}s", file=sys.stderr)
        sys.exit(4)

if __name__ == "__main__":
    main()
