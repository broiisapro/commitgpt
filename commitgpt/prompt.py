def build_prompt(diff: str, detailed: bool = False) -> str:
    """
    Build prompt for commit message generation.
    """

    if not detailed:
        return f"""
You generate a conventional commit message.

RULES:
- Output EXACTLY one line
- No explanations
- Use lowercase
- Use imperative verbs (add, fix, remove)
- Do NOT use: implement, update, improve

FORMAT:
<type>(optional scope): <description>

ALLOWED TYPES:
feat, fix, docs, style, refactor, test, chore

---

Git diff:
{diff}

Return ONLY the commit message.
""".strip()

    # --- DETAILED MODE ---
    return f"""
You generate a detailed conventional commit message from a git diff.

OUTPUT FORMAT:

<type>(optional scope): <short summary>

- bullet describing key change
- bullet describing key change
- bullet describing key change

(optional) final line describing purpose or impact

RULES:
- First line max 72 characters
- Use imperative verbs (add, fix, remove)
- Be specific and technical
- Bullet points must reflect actual changes
- Do NOT include explanations outside this format

---

Git diff:
{diff}

Return ONLY the commit message.
""".strip()