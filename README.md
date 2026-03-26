# commitgpt

A Python CLI tool that generates conventional commit messages from staged git diffs using an LLM via OpenRouter.

## Why this exists

Writing good commit messages is slow and inconsistent. This tool automates it by:

- Reading your staged changes (`git diff --cached`)
- Sending a structured prompt to an LLM
- Returning a clean, valid conventional commit message

---

## Features

- CLI command: `commitgpt suggest`
- Reads staged git diff
- Truncates large diffs intelligently (prioritizes added lines)
- Uses OpenRouter for LLM generation
- Validates output against conventional commit format

---

## Planned

- Interactive mode (accept / edit / regenerate)
- Git hook integration (`prepare-commit-msg`)
- Automatic commit message insertion
- Expanded test coverage

---

## Installation
```bash
git clone <your-repo-url>
cd commitgpt

python3.12 -m venv venv
source venv/bin/activate

pip install -e .
```

Set your API key:
```bash
export OPENROUTER_API_KEY=your_key_here
```

---

## Usage

Stage your changes:
```bash
git add .
```

Generate a commit message:
```bash
commitgpt suggest
```

---

## Example

Input (diff):
```diff
+ def add(a, b):
+     return a + b
```

Output:
```
feat: add basic addition function
```

---

## Design Decisions

**Diff truncation** — Large diffs are reduced by keeping added lines (most informative), sampling removed lines, and capping total size to control token usage.

**Prompt engineering** — The model is told to return exactly one commit message, follow Conventional Commits strictly, and skip explanations or extra formatting.

**Output validation** — Responses are validated against:
```
^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: .+
```

Invalid outputs are rejected.

---

## Tech Stack

- Python 3.12
- Click (CLI)
- OpenRouter API (LLM access)
- pytest
- Ruff
- GitHub Actions (CI)

---

## License

MIT