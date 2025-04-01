import sys
import click
from rich.panel import Panel
from rich.table import Table
from rich.markdown import Markdown
from gitlab_cli.utils import console
from gitlab_cli.gitlab_api import GitLabAPI
from gitlab_cli.utils import get_logger

api = GitLabAPI()

logger = get_logger(__name__)


@click.command("show")
@click.argument("project_id", type=str)
@click.argument("issue_iid", type=str)
def show_issue(project_id, issue_iid):
    """Show detailed information about a specific issue."""
    try:
        with console.status(f"Fetching issue {issue_iid}...", spinner="dots"):
            issue = api.get_project_issue(project_id, issue_iid)
            if not issue:
                console.print("[bold red]Error:[/bold red] Issue not found")
                sys.exit(1)

            logger.info("Fetched issue data %s", issue)
            links = api.get_issue_links(project_id, issue_iid)

        # Create a rich panel with issue details
        state_color = "green" if issue.get("state") == "opened" else "red"

        # Handle potential missing fields with defensive coding
        author_name = issue.get("author", {}).get("name", "Unknown")
        assignees = ", ".join(
            [a.get("name", "Unknown") for a in issue.get("assignees", [])]
        )
        labels = ", ".join(issue.get("labels", []))
        due_date = issue.get("due_date") or "Not set"
        weight = issue.get("weight") or "Not set"

        # Format the panel with safe access to keys
        console.print(
            Panel(
                f"""
    [bold cyan]#{issue.get('iid', 'N/A')}[/bold cyan] [bold]{issue.get('title', 'No title')}[/bold]
    [bold]State:[/bold] [{state_color}]{issue.get('state', 'unknown')}[/{state_color}]
    [bold]Author:[/bold] {author_name}
    [bold]Assignees:[/bold] {assignees or 'None'}
    [bold]Labels:[/bold] {labels or 'None'}
    [bold]Created:[/bold] {issue.get('created_at', 'Unknown')}
    [bold]Updated:[/bold] {issue.get('updated_at', 'Unknown')}
    [bold]Due date:[/bold] {due_date}
    [bold]Weight:[/bold] {weight}
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
                if not isinstance(link, dict) or "issue" not in link:
                    continue

                related_issue = link["issue"]
                link_type = link.get("link_type", "Unknown")
                state = related_issue.get("state", "unknown")
                state_color = "green" if state == "opened" else "red"

                link_table.add_row(
                    f"{related_issue.get('iid', 'N/A')}",
                    link_type,
                    related_issue.get("title", "No title"),
                    f"[{state_color}]{state}[/{state_color}]",
                )
            console.print(link_table)

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        sys.exit(1)
