# commitgpt

A Python CLI and Git hook that generates **conventional commit messages** from staged diffs using an LLM.

---

## Overview

Writing consistent commit messages is slow and error-prone.  
`commitgpt` automates this by converting staged changes into a validated, conventional commit message.

It integrates directly into your workflow via a CLI and optional Git hook.

---

## Features

- Generate commit messages from staged diffs (`git diff --cached`)
- Interactive CLI:
  - accept
  - edit
  - regenerate
- Git hook integration (`prepare-commit-msg`)
- Automatic commit message insertion (no copy/paste)
- Intelligent diff truncation (prioritizes added lines)
- Strict output validation (conventional commits format)

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

### CLI mode

```bash
git add .
commitgpt suggest
```

### Git hook (recommended)

Install the hook:

```bash
commitgpt install-hook
```

Now simply run:

```bash
git commit
```

A commit message will be generated automatically.

---

## Example

Input (diff):

```python
+ def add(a, b):
+     return a + b
```

Output:

```
feat: add basic addition function
```

---

## How it Works

### 1. Diff Processing

- Reads staged changes using `git diff --cached`
- Truncates large diffs to control token usage
- Prioritizes added lines over removed lines

### 2. Prompt Engineering

- Enforces a strict output contract:
  - single line only
  - conventional commits format
  - imperative, concise language
- Includes examples and banned patterns to reduce ambiguity

### 3. LLM Integration

- Sends prompt to OpenRouter
- Uses short, non-streaming responses for low latency

### 4. Output Validation

Ensures format matches:

```
^(feat|fix|docs|style|refactor|test|chore)(\(.+\))?: .+
```

Rejects invalid outputs.

### 5. Git Hook Integration

- Uses `prepare-commit-msg`
- Writes directly to Git's commit message file
- Skips overwrite if user already provided a message
- Runs safely without breaking commits on failure

---

## Design Considerations

**Determinism over creativity**  
Strict prompts and output validation ensure consistent, predictable results.

**Fail-safe behavior**  
The hook never blocks commits if the API fails.

**Minimal friction**  
Optional full automation via Git hook — zero extra steps once installed.

---

## Tech Stack

- Python 3.12
- Click (CLI)
- OpenRouter API
- pytest
- Ruff
- GitHub Actions

---

## License

MIT