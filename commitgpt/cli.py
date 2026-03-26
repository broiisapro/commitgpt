import click

from commitgpt.diff import get_staged_diff, truncate_diff
from commitgpt.prompt import build_prompt
from commitgpt.client import generate_commit_message, COMMIT_REGEX


@click.group()
def cli() -> None:
    """commitgpt CLI"""
    pass


def generate(diff: str) -> str:
    """
    Generate a commit message from diff.
    """
    truncated = truncate_diff(diff)
    prompt = build_prompt(truncated)
    return generate_commit_message(prompt)


@cli.command()
def suggest() -> None:
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
            message = generate(diff)
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

            elif not COMMIT_REGEX.match(edited):
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