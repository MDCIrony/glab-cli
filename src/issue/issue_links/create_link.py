import sys
import click
from utils import console
from gitlab_api import GitLabAPI

api = GitLabAPI()


@click.command("create")
@click.argument("project_id", type=str)
@click.argument("issue_iid", type=str)
@click.argument("target_project_id", type=str)
@click.argument("target_issue_iid", type=str)
@click.option(
    "--link-type",
    type=click.Choice(
        ["relates_to", "blocks", "is_blocked_by", "duplicates", "is_duplicated_by"]
    ),
    default="relates_to",
    help="Relationship type",
)
def create_link(project_id, issue_iid, target_project_id, target_issue_iid, link_type):
    """Link an issue to another issue."""
    try:
        with console.status("Creating issue link...", spinner="dots"):
            result = api.create_issue_relationship(
                project_id, issue_iid, target_project_id, target_issue_iid, link_type
            )

        console.print(f"[bold green]Success![/bold green] Issues linked")
        console.print(f"Issue #{issue_iid} {link_type} Issue #{result['issue']['iid']}")

    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] {str(e)}")
        sys.exit(1)
