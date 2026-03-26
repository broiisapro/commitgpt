import subprocess


MAX_DIFF_CHARS = 12000


def get_staged_diff() -> str:
    """
    Retrieve the staged git diff.

    Returns:
        str: Raw diff output.

    Raises:
        RuntimeError: If git command fails.
    """
    result = subprocess.run(
        ["git", "diff", "--cached"],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        raise RuntimeError("Failed to get staged git diff")

    return result.stdout


def truncate_diff(diff: str) -> str:
    """
    Truncate a diff to stay within token limits while preserving intent.

    Strategy:
    - Keep all added lines (+) — highest signal
    - Keep a small sample of removed lines (-)
    - Keep limited context lines
    - Enforce a hard character cap

    Args:
        diff: Raw git diff string

    Returns:
        str: Truncated diff
    """
    if len(diff) <= MAX_DIFF_CHARS:
        return diff

    lines = diff.splitlines()

    added_lines = []
    removed_lines = []
    context_lines = []

    for line in lines:
        if line.startswith("+") and not line.startswith("+++"):
            added_lines.append(line)
        elif line.startswith("-") and not line.startswith("---"):
            removed_lines.append(line)
        else:
            context_lines.append(line)

    # Limit less important categories
    removed_sample = removed_lines[:50]
    context_sample = context_lines[:200]

    combined = context_sample + removed_sample + added_lines

    truncated = "\n".join(combined)

    return truncated[:MAX_DIFF_CHARS]