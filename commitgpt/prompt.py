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
- Use lowercase
- Use imperative verbs (add, fix, remove)
- Each bullet must start with "-"
- Each bullet must be non-empty and specific
- Use 2–4 bullet points (no empty bullets)
- No trailing "-" or blank bullets
- Keep bullets concise and technical
- Do NOT include explanations outside this format

GOOD EXAMPLE:

feat(config): add YAML-based site configuration system

- add sites.yaml for defining scraping targets
- implement loader to parse YAML into dictionary
- enable dynamic scraper configuration

enables scalable multi-site scraping without hardcoding

---

Git diff:
{diff}

Return ONLY the commit message.
""".strip()