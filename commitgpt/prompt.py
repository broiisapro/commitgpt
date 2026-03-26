def build_prompt(diff: str) -> str:
    """
    Build a strict prompt for generating a conventional commit message.

    Args:
        diff: Truncated git diff

    Returns:
        str: Prompt to send to LLM
    """

    conventional_commits_spec = """
The commit message must follow the Conventional Commits specification:

<type>[optional scope]: <description>

Allowed types:
feat: A new feature
fix: A bug fix
docs: Documentation only changes
style: Changes that do not affect the meaning of the code
refactor: Code change that neither fixes a bug nor adds a feature
test: Adding or correcting tests
chore: Maintenance work

Rules:
- Use imperative mood (e.g., "add", not "added")
- Keep the description under 72 characters
- Do not end the description with a period
"""

    instructions = """
You are a tool that generates a single conventional commit message from a git diff.

Strict requirements:
- Return EXACTLY one line
- Follow the Conventional Commits format
- Do not include explanations
- Do not include markdown
- Do not include quotes
- Do not include multiple options
"""

    prompt = f"""
{instructions}

{conventional_commits_spec}

Git diff:
{diff}

Return ONLY the commit message.
"""

    return prompt.strip()