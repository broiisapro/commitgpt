import click

from commitgpt.diff import get_staged_diff, truncate_diff
from commitgpt.prompt import build_prompt
from commitgpt.client import generate_commit_message


@click.group()
def cli() -> None:
    """commitgpt CLI"""
    pass


@cli.command()
def suggest() -> None:
    """
    Generate a commit message from staged changes.
    """
    try:
        diff = get_staged_diff()
    except Exception as e:
        click.echo(f"Error getting git diff: {e}")
        return

    if not diff.strip():
        click.echo("No staged changes found.")
        return

    truncated = truncate_diff(diff)
    prompt = build_prompt(truncated)

    try:
        message = generate_commit_message(prompt)
    except Exception as e:
        click.echo(f"Error generating commit message: {e}")
        return

    click.echo("\nSuggested commit message:\n")
    click.echo(message)