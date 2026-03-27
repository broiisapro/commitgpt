import os
import re
import requests


OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Use auto for now to ensure stability (we will optimize later)
MODEL = "openrouter/auto"

COMMIT_REGEX = re.compile(
    r"^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: .+"
)


def generate_commit_message(prompt: str) -> str:
    """
    Send prompt to OpenRouter and return a validated commit message.

    Args:
        prompt: Prompt string

    Returns:
        str: Valid conventional commit message

    Raises:
        RuntimeError: API or validation failure
    """
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("OPENROUTER_API_KEY not set")

    response = requests.post(
        OPENROUTER_URL,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        json={
            "model": MODEL,
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": 100,
        },
        timeout=30,
    )

    if response.status_code != 200:
        raise RuntimeError(f"OpenRouter API error: {response.text}")

    data = response.json()

    try:
        text = data["choices"][0]["message"]["content"]
    except (KeyError, IndexError):
        raise RuntimeError(f"Unexpected API response: {data}")

    # --- SANITIZATION ---
    text = text.strip()

    # Remove code block formatting if present
    if text.startswith("```"):
        text = text.strip("`").strip()

    # Keep only first line
    if "\n" in text:
        text = text.split("\n")[0].strip()

    # Remove surrounding quotes
    text = text.strip('"').strip("'")

    # --- VALIDATION ---
    if not COMMIT_REGEX.match(text):
        raise RuntimeError(f"Invalid commit message format: {text}")

    return text