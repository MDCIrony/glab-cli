import sys
import click
from rich.prompt import Confirm
from utils import console
from gitlab_api import GitLabAPI

api = GitLabAPI()


@click.command("delete")
@click.argument("project_id", type=str)
@click.argument("issue_iid", type=str)
@click.option("--force", "-f", is_flag=True, help="Skip confirmation")
def delete_issue(project_id, issue_iid, force):
    """Delete an issue (closes it, as GitLab doesn't allow true deletion via API)."""
    try:
        # Get issue details first
        with console.status(f"Fetching issue {issue_iid}...", spinner="dots"):
            issue = api.get_project_issue(project_id, issue_iid)

        console.print(f"Issue: [bold]#{issue['iid']}[/bold] - {issue['title']}")
        console.print(
            "[yellow]Note: This will close the issue, as GitLab doesn't allow true deletion via API[/yellow]"
        )

        if not force and not Confirm.ask(
            "\nAre you sure you want to close this issue?"
        ):
            console.print("[yellow]Operation canceled[/yellow]")
            return

        with console.status("Closing issue...", spinner="dots"):
            api.delete_project_issue(project_id, issue_iid)

        console.print(f"[bold green]Success![/bold green] Issue #{issue_iid} closed")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        sys.exit(1)
