import sys
import click
from rich.table import Table
from utils import console
from gitlab_api import GitLabAPI

api = GitLabAPI()


@click.command("list")
@click.argument("project_id", type=str)
@click.option(
    "--state",
    type=click.Choice(["opened", "closed", "all"]),
    default="opened",
    help="Filter issues by state",
)
@click.option("--labels", help="Filter issues by labels (comma separated)")
@click.option("--assignee", help="Filter issues by assignee username")
@click.option("--milestone", help="Filter issues by milestone")
@click.option(
    "--sort",
    type=click.Choice(["created_at", "updated_at", "priority"]),
    default="created_at",
    help="Sort issues by field",
)
@click.option(
    "--order",
    type=click.Choice(["asc", "desc"]),
    default="desc",
    help="Sort order (ascending or descending)",
)
@click.option("--limit", type=int, default=20, help="Maximum number of issues to show")
def list_issues(project_id, state, labels, assignee, milestone, sort, order, limit):
    """List issues for a specific project in a beautiful table."""
    try:
        params = {
            "state": state,
            "order_by": sort,  # Parámetro para especificar el campo a ordenar
            "sort": order,  # Parámetro para especificar la dirección (asc/desc)
            "per_page": limit,
        }

        if labels:
            params["labels"] = labels
        if assignee:
            params["assignee_username"] = assignee
        if milestone:
            params["milestone"] = milestone

        with console.status(
            f"Fetching issues for project {project_id}...", spinner="dots"
        ):
            issues = api.get_project_issues(project_id, params=params)

        if not issues:
            console.print(
                "[yellow]No issues found with the specified criteria[/yellow]"
            )
            return

        table = Table(title=f"Issues for Project {project_id}")

        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Title", style="green")
        table.add_column("State", style="magenta")
        table.add_column("Assignees", style="blue")
        table.add_column("Labels", style="yellow")
        table.add_column("Created", style="white")

        for issue in issues:
            state_color = "green" if issue["state"] == "opened" else "red"
            assignees = ", ".join(
                [a.get("name", "") for a in issue.get("assignees", [])]
            )
            labels = ", ".join(issue.get("labels", []))

            table.add_row(
                str(issue["iid"]),
                issue["title"],
                f"[{state_color}]{issue['state']}[/{state_color}]",
                assignees or "-",
                labels or "-",
                issue["created_at"].split("T")[0] if "created_at" in issue else "-",
            )

        console.print(table)
        console.print(f"\nShowing {len(issues)} issues. Use --limit to see more.")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        sys.exit(1)
