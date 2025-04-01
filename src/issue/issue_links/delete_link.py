import sys
import click
from rich.prompt import Confirm
from utils import console
from gitlab_api import GitLabAPI

api = GitLabAPI()


@click.command("delete")
@click.argument("project_id", type=str)
@click.argument("issue_iid", type=str)
@click.argument("link_id", type=str)
@click.option("--force", "-f", is_flag=True, help="Skip confirmation")
def delete_link(project_id, issue_iid, link_id, force):
    """Remove a link between issues."""
    try:
        if not force and not Confirm.ask(
            f"Are you sure you want to delete link {link_id}?"
        ):
            console.print("[yellow]Operation canceled[/yellow]")
            return

        with console.status("Removing issue link...", spinner="dots"):
            api.remove_issue_link(project_id, issue_iid, link_id)

        console.print(f"[bold green]Success![/bold green] Link {link_id} removed")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        sys.exit(1)
