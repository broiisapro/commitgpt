import click
from pathlib import Path
import os
import sys
import subprocess  # <-- REQUIRED

from commitgpt.diff import get_staged_diff, truncate_diff
from commitgpt.prompt import build_prompt
from commitgpt.client import generate_commit_message, COMMIT_REGEX


@click.group()
def cli() -> None:
    """commitgpt CLI"""
    pass


def generate(diff: str, detailed: bool = False) -> str:
    """
    Generate a commit message from diff.
    """
    truncated = truncate_diff(diff)
    prompt = build_prompt(truncated, detailed=detailed)
    return generate_commit_message(prompt, detailed=detailed)


@cli.command()
@click.option("--detailed", is_flag=True, help="Generate detailed commit message")
def suggest(detailed: bool) -> None:
    """
    Generate a commit message from staged changes with interaction.
    """
    try:
        diff = get_staged_diff()
    except Exception as e:
        click.echo(f"Error getting git diff: {e}")
        return

    if not diff.strip():
        click.echo("No staged changes found.")
        return

    while True:
        try:
            message = generate(diff, detailed=detailed)
        except Exception as e:
            click.echo(f"Error generating commit message: {e}")
            return

        click.echo("\nSuggested commit message:\n")
        click.echo(message)

        choice = click.prompt(
            "\n[y] accept  [e] edit  [r] regenerate  [q] quit",
            type=str,
            default="y"
        ).lower()

        if choice == "y":
            click.echo("\nFinal commit message:\n")
            click.echo(message)
            return

        elif choice == "e":
            edited = click.prompt("\nEdit commit message", default=message)
            edited = edited.strip()

            if not edited:
                click.echo("Empty message. Keeping original.")
                edited = message

            elif not detailed and not COMMIT_REGEX.match(edited):
                click.echo("Invalid commit format. Keeping original.")
                edited = message

            click.echo("\nFinal commit message:\n")
            click.echo(edited)
            return

        elif choice == "r":
            continue

        elif choice == "q":
            click.echo("Aborted.")
            return

        else:
            click.echo("Invalid choice. Please select y/e/r/q.")


@cli.command()
def install_hook() -> None:
    """
    Install the prepare-commit-msg git hook.
    """
    git_dir = Path(".git")

    if not git_dir.exists():
        click.echo("Error: not a git repository.")
        return

    hooks_dir = git_dir / "hooks"
    hooks_dir.mkdir(exist_ok=True)

    hook_path = hooks_dir / "prepare-commit-msg"

    python_path = sys.executable

    hook_content = f"""#!/bin/sh
# commitgpt hook

export OPENROUTER_API_KEY="{os.environ.get('OPENROUTER_API_KEY')}"
export GIT_EDITOR=:

"{python_path}" -m commitgpt.hook "$1"
"""

    # Idempotency check
    if hook_path.exists():
        existing = hook_path.read_text()
        if "commitgpt hook" in existing:
            click.echo("Hook already installed.")
            return

    hook_path.write_text(hook_content)
    os.chmod(hook_path, 0o755)

    click.echo("Hook installed at .git/hooks/prepare-commit-msg")


@cli.command()
@click.option("--detailed", is_flag=True, help="Generate detailed commit message")
def commit(detailed: bool) -> None:
    """
    Generate commit message and commit.
    """
    try:
        diff = get_staged_diff()
    except Exception as e:
        click.echo(f"Error getting git diff: {e}")
        return

    if not diff.strip():
        click.echo("No staged changes found.")
        return

    while True:
        try:
            message = generate(diff, detailed=detailed)
        except Exception as e:
            click.echo(f"Error generating commit message: {e}")
            return

        click.echo("\n--- Suggested Commit ---\n")
        click.echo(message)
        click.echo("\n------------------------")

        choice = click.prompt(
            "\n[y] commit  [e] edit  [r] regenerate  [q] cancel",
            default="y"
        ).lower()

        if choice == "y":
            try:
                subprocess.run(
                    ["git", "commit", "-m", message],
                    check=True
                )
                click.echo("Committed.")
            except subprocess.CalledProcessError as e:
                click.echo(f"Git commit failed: {e}")
            return

        elif choice == "e":
            edited = click.edit(message)

            if not edited:
                click.echo("Edit cancelled.")
                continue

            edited = edited.strip()

            try:
                subprocess.run(
                    ["git", "commit", "-m", edited],
                    check=True
                )
                click.echo("Committed.")
            except subprocess.CalledProcessError as e:
                click.echo(f"Git commit failed: {e}")
            return

        elif choice == "r":
            continue

        elif choice == "q":
            click.echo("Aborted.")
            return

        else:
            click.echo("Invalid choice.")