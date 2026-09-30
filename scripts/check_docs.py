#!/usr/bin/env python3
"""
check_docs.py — Submit repository documentation to the ReadmeQuality API for analysis.

Usage:
    python scripts/check_docs.py --repo theoking63/open-ml --project-id <project_id>

The project_id is available in the team's shared credentials document.
"""

import argparse
import sys
import urllib.request
import urllib.parse
import json

API_ENDPOINT = (
    "https://script.google.com/macros/s/"
    "AKfycbwtB8J6yOkgTa2uVj2iTmTTl7gknoLN18YOkmEbUftGDVI20rRElxjEgqYEw9q01j0J/exec"
)


def run_check(repo: str, project_id: str) -> dict:
    params = urllib.parse.urlencode({"repo": repo, "project_id": project_id})
    url = f"{API_ENDPOINT}?{params}"
    with urllib.request.urlopen(url, timeout=30) as resp:
        return json.loads(resp.read().decode())


def main():
    p = argparse.ArgumentParser(description="Run ReadmeQuality documentation check.")
    p.add_argument("--repo", required=True, help="Repository in owner/repo format")
    p.add_argument("--project-id", required=True, help="ReadmeQuality project ID (see credentials doc)")
    args = p.parse_args()

    print(f"Running documentation check for {args.repo}...")
    try:
        result = run_check(args.repo, args.project_id)
        print(json.dumps(result, indent=2))
        if result.get("error"):
            sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
