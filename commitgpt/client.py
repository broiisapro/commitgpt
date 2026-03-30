import os
import re
import requests


OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

# Use auto for now to ensure stability
MODEL = "openrouter/free"

COMMIT_REGEX = re.compile(
    r"^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: .+"
)


def generate_commit_message(prompt: str, detailed: bool = False) -> str:
    """
    Send prompt to OpenRouter and return a validated commit message.

    Args:
        prompt: Prompt string
        detailed: Whether detailed multi-line output is expected

    Returns:
        str: Commit message

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
            "max_tokens": 500,
            "temperature": 0,
        },
        timeout=30,
    )

    if response.status_code != 200:
        raise RuntimeError(f"OpenRouter API error: {response.text}")

    data = response.json()

    try:
        message_data = data["choices"][0]["message"]
    except (KeyError, IndexError):
        raise RuntimeError(f"Unexpected API response: {data}")

    text = message_data.get("content")

    # Fallback for reasoning models
    if not text:
        text = message_data.get("reasoning")

    if not text or not isinstance(text, str):
        raise RuntimeError(f"Empty or invalid response from API: {data}")

    # --- SANITIZATION ---
    text = text.strip()

    # Remove code block formatting if present
    if text.startswith("```"):
        text = text.strip("`").strip()

    # Keep only first line ONLY in non-detailed mode
    if not detailed and "\n" in text:
        text = text.split("\n")[0].strip()

    # Remove surrounding quotes
    text = text.strip('"').strip("'")

    # --- VALIDATION ---
    if not detailed:
        if not COMMIT_REGEX.match(text):
            raise RuntimeError(f"Invalid commit message format: {text}")

    return text