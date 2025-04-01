import sys
import click
from utils import console
from gitlab_api import GitLabAPI

api = GitLabAPI()


@click.command("create")
@click.argument("project_id", type=str)
@click.option("--title", "-t", prompt=True, help="Issue title")
@click.option("--description", "-d", help="Issue description (can be markdown)")
@click.option("--labels", "-l", help="Comma-separated labels")
@click.option("--assignees", "-a", help="Comma-separated assignee IDs")
@click.option("--milestone", "-m", help="Milestone ID")
@click.option("--due-date", help="Due date (YYYY-MM-DD)")
@click.option("--confidential", is_flag=True, help="Mark as confidential")
@click.option("--weight", type=int, help="Issue weight")
@click.option("--editor", is_flag=True, help="Open description in editor")
def create_issue(
    project_id,
    title,
    description,
    labels,
    assignees,
    milestone,
    due_date,
    confidential,
    weight,
    editor,
):
    """Create a new issue in a project."""
    try:
        if editor and not description:
            description = click.edit(
                "\n\n# Write issue description here (markdown supported)"
            )
            if description is None:  # User canceled the editor
                console.print("[yellow]Operation canceled[/yellow]")
                return

        # Process inputs
        labels_list = [l.strip() for l in labels.split(",")] if labels else None
        assignee_ids = (
            [int(a.strip()) for a in assignees.split(",")] if assignees else None
        )
        milestone_id = int(milestone) if milestone else None

        with console.status("Creating issue...", spinner="dots"):
            issue = api.create_project_issue(
                project_id=project_id,
                title=title,
                description=description,
                labels=labels_list,
                assignee_ids=assignee_ids,
                milestone_id=milestone_id,
                due_date=due_date,
                confidential=confidential,
                weight=weight,
            )

        console.print(
            f"[bold green]Success![/bold green] Issue #{issue['iid']} created"
        )
        console.print(f"[bold]Title:[/bold] {issue['title']}")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        sys.exit(1)
