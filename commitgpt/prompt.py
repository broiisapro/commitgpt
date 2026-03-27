def build_prompt(diff: str) -> str:
    """
    Build a strict prompt for generating a conventional commit message.

    Args:
        diff: Truncated git diff

    Returns:
        str: Prompt string
    """
    return f"""
You are a tool that generates a single conventional commit message from a git diff.

STRICT RULES (MUST FOLLOW):
- Output EXACTLY one line
- Do NOT include explanations
- Do NOT include quotes or markdown
- Use lowercase type and description
- Use imperative mood (e.g., "add", "fix", "remove")
- Do NOT use words like: "implement", "update", "improve", "fix up"
- Keep message concise and specific

FORMAT:
<type>(optional scope): <description>

ALLOWED TYPES:
feat, fix, docs, style, refactor, test, chore

SCOPE RULES:
- Use scope when clear (e.g., cli, hook, diff, prompt, client)
- Omit scope if unclear

DESCRIPTION RULES:
- Max 72 characters
- No period at end
- Describe WHAT changed, not HOW

GOOD EXAMPLES:
feat(cli): add suggest command
fix(hook): handle existing commit messages
docs: update README installation section

BAD EXAMPLES:
feat: implement feature
fix: update stuff
feat(cli): improve logic

---

Git diff:
{diff}

Return ONLY the commit message.
""".strip()