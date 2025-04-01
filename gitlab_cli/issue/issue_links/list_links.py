import sys
import click
from rich.table import Table
from gitlab_cli.utils import console
from gitlab_cli.gitlab_api import GitLabAPI

api = GitLabAPI()


@click.command("list")
@click.argument("project_id", type=str)
@click.argument("issue_iid", type=str)
def list_links(project_id, issue_iid):
    """List all links for an issue."""
    try:
        with console.status(f"Fetching links for issue {issue_iid}...", spinner="dots"):
            links = api.get_issue_links(project_id, issue_iid)

        if not links:
            console.print("[yellow]No linked issues found[/yellow]")
            return

        table = Table(title=f"Links for Issue #{issue_iid}")
        table.add_column("Link ID", style="cyan")
        table.add_column("Issue ID", style="green")
        table.add_column("Link Type", style="magenta")
        table.add_column("Title", style="blue")
        table.add_column("State", style="yellow")

        for link in links:
            related_issue = link["issue"]
            state_color = "green" if related_issue["state"] == "opened" else "red"

            table.add_row(
                str(link.get("id", "N/A")),
                str(related_issue["iid"]),
                link["link_type"],
                related_issue["title"],
                f"[{state_color}]{related_issue['state']}[/{state_color}]",
            )

        console.print(table)

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        sys.exit(1)
