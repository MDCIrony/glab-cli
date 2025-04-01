import sys
import click
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from utils import console
from gitlab_api import GitLabAPI

api = GitLabAPI()


@click.command("show")
@click.argument("project_id", type=str)
@click.argument("issue_iid", type=str)
def show_issue(project_id, issue_iid):
    """Show detailed information about a specific issue."""
    try:
        with console.status(f"Fetching issue {issue_iid}...", spinner="dots"):
            issue = api.get_project_issue(project_id, issue_iid)
            links = api.get_issue_links(project_id, issue_iid)

        # Create a rich panel with issue details
        state_color = "green" if issue["state"] == "opened" else "red"
        assignees = ", ".join([a.get("name", "") for a in issue.get("assignees", [])])
        labels = ", ".join(issue.get("labels", []))

        console.print(
            Panel(
                f"""
    [bold cyan]#{issue['iid']}[/bold cyan] [bold]{issue['title']}[/bold]

    [bold]State:[/bold] [{state_color}]{issue['state']}[/{state_color}]
    [bold]Author:[/bold] {issue['author']['name']}
    [bold]Assignees:[/bold] {assignees or 'None'}
    [bold]Labels:[/bold] {labels or 'None'}
    [bold]Created:[/bold] {issue['created_at']}
    [bold]Updated:[/bold] {issue['updated_at']}
    {f"[bold]Due date:[/bold] {issue.get('due_date')}" if issue.get('due_date') else ''}
    {f"[bold]Weight:[/bold] {issue.get('weight')}" if issue.get('weight') is not None else ''}
            """,
                title="Issue Details",
                width=100,
            )
        )

        if issue.get("description"):
            console.print(
                Panel(Markdown(issue["description"]), title="Description", width=100)
            )

        # Show related issues if any
        if links:
            link_table = Table(title="Related Issues")
            link_table.add_column("ID", style="cyan")
            link_table.add_column("Link Type", style="magenta")
            link_table.add_column("Title", style="green")
            link_table.add_column("State", style="yellow")

            for link in links:
                related_issue = link["issue"]
                state_color = "green" if related_issue["state"] == "opened" else "red"
                link_table.add_row(
                    f"{related_issue['iid']}",
                    link["link_type"],
                    related_issue["title"],
                    f"[{state_color}]{related_issue['state']}[/{state_color}]",
                )
            console.print(link_table)

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        sys.exit(1)
