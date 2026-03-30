import sys
from pathlib import Path

from commitgpt.diff import get_staged_diff, truncate_diff
from commitgpt.prompt import build_prompt
from commitgpt.client import generate_commit_message


def run_hook(commit_msg_file: str) -> None:
    """
    Generate and write a commit message into the given file.

    Args:
        commit_msg_file: Path to the commit message file provided by git hook
    """
    path = Path(commit_msg_file)

    # --- Check if a real message already exists (ignore comments) ---
    if path.exists():
        content = path.read_text()

        non_comment_lines = [
            line for line in content.splitlines()
            if not line.strip().startswith("#")
        ]

        if any(line.strip() for line in non_comment_lines):
            return

    # --- Get staged diff ---
    try:
        diff = get_staged_diff()
    except Exception:
        return

    if not diff.strip():
        return

    # --- Generate commit message ---
    try:
        truncated = truncate_diff(diff)
        prompt = build_prompt(truncated)
        message = generate_commit_message(prompt)
    except Exception as e:
        print("HOOK ERROR:", e)
        return

    # --- Write message ---
    path.write_text(message + "\n")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(0)

    commit_msg_file = sys.argv[1]
    run_hook(commit_msg_file)