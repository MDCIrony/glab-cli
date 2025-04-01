import sys
import click
from rich.prompt import Confirm
from utils import console
from gitlab_api import GitLabAPI

api = GitLabAPI()


@click.command("update")
@click.argument("project_id", type=str)
@click.argument("issue_iid", type=str)
@click.option("--title", "-t", help="New title")
@click.option("--description", "-d", help="New description")
@click.option(
    "--state-event", type=click.Choice(["close", "reopen"]), help="Change state"
)
@click.option("--labels", "-l", help="Comma-separated labels")
@click.option("--assignees", "-a", help="Comma-separated assignee IDs")
@click.option("--milestone", "-m", help="Milestone ID (0 to clear)")
@click.option("--due-date", help="Due date (YYYY-MM-DD) (remove with --clear-due-date)")
@click.option("--clear-due-date", is_flag=True, help="Remove due date")
@click.option("--confidential/--non-confidential", help="Mark as confidential or not")
@click.option("--weight", type=int, help="Issue weight (0 to clear)")
@click.option("--editor", is_flag=True, help="Open description in editor")
def update_issue(
    project_id,
    issue_iid,
    title,
    description,
    state_event,
    labels,
    assignees,
    milestone,
    due_date,
    clear_due_date,
    confidential,
    weight,
    editor,
):
    """Update an existing issue."""
    try:
        # First get the current issue so we can show what we're updating
        with console.status(f"Fetching issue {issue_iid}...", spinner="dots"):
            current = api.get_project_issue(project_id, issue_iid)

        # Prepare update data
        update_data = {}

        if title:
            update_data["title"] = title

        if editor:
            if description is None:
                # Pre-fill with current description
                current_desc = current.get("description", "")
                description = click.edit(
                    current_desc + "\n\n# Edit issue description (markdown supported)"
                )
                if description is None:  # User canceled the editor
                    console.print("[yellow]Description not updated[/yellow]")
                else:
                    update_data["description"] = description
        elif description is not None:
            update_data["description"] = description

        if state_event:
            update_data["state_event"] = state_event

        if labels:
            update_data["labels"] = [l.strip() for l in labels.split(",")]

        if assignees:
            update_data["assignee_ids"] = [int(a.strip()) for a in assignees.split(",")]

        if milestone is not None:
            update_data["milestone_id"] = int(milestone)

        if clear_due_date:
            update_data["due_date"] = None
        elif due_date:
            update_data["due_date"] = due_date

        if confidential is not None:
            update_data["confidential"] = confidential

        if weight is not None:
            update_data["weight"] = weight

        # Only proceed if we have something to update
        if not update_data:
            console.print("[yellow]No update parameters provided[/yellow]")
            return

        # Confirmation
        console.print("[cyan]Updating issue with the following changes:[/cyan]")
        for key, value in update_data.items():
            console.print(f"  [bold]{key}:[/bold] {value}")

        if not Confirm.ask("\nProceed with update?"):
            console.print("[yellow]Update canceled[/yellow]")
            return

        # Perform update
        with console.status("Updating issue...", spinner="dots"):
            result = api.update_project_issue(project_id, issue_iid, **update_data)

        console.print(
            f"[bold green]Success![/bold green] Issue #{result['iid']} updated"
        )

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        sys.exit(1)
