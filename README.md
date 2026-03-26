# commitgpt

A Python CLI tool that generates conventional commit messages from staged git diffs using an LLM via OpenRouter.

## Why this exists

Writing good commit messages is slow and inconsistent.  
This tool automates that process by:

- Reading your staged changes (`git diff --cached`)
- Sending a structured prompt to an LLM
- Returning a clean, valid conventional commit message

The goal is speed, consistency, and correctness.

---

## Features (current)

- CLI command: `commitgpt suggest`
- Reads staged git diff
- Truncates large diffs intelligently (prioritizes added lines)
- Uses OpenRouter (auto model selection) for generation
- Enforces conventional commit format via validation

---

## Planned (Day 2)

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

Set your API key:

export OPENROUTER_API_KEY=your_key_here


⸻

Usage

Stage your changes:

git add .

Generate a commit message:

commitgpt suggest


⸻

Example

Input (diff):

+ def add(a, b):
+     return a + b

Output:

feat: add basic addition function


⸻

Design Decisions

Diff Truncation Strategy

Large diffs are reduced by:
	•	Keeping added lines (most informative)
	•	Sampling removed lines
	•	Limiting total size to control token usage

Prompt Engineering

The model is instructed to:
	•	Return exactly one commit message
	•	Follow Conventional Commits strictly
	•	Avoid explanations or formatting

Output Validation

Responses are validated against this pattern:

^(feat|fix|docs|style|refactor|test|chore)($begin:math:text$\.\+$end:math:text$)?: .+

Invalid outputs are rejected.

⸻

Tech Stack
	•	Python 3.12
	•	Click (CLI)
	•	OpenRouter API (LLM access)
	•	pytest
	•	Ruff
	•	GitHub Actions (CI)

⸻

Why this project matters

This project demonstrates:
	•	LLM integration in real workflows
	•	Prompt engineering for structured outputs
	•	Handling unbounded input (git diffs)
	•	Building developer tooling

⸻

License

MIT

---