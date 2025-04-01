import click
from rich.table import Table
from utils import console, gitlab


@click.command()
@click.option("--page", default=1, help="Page number")
@click.option("--per-page", default=10, help="Items per page")
def list_repos(page, per_page):
    """List your GitLab repositories"""
    try:
        projects = gitlab.get_projects(
            {"page": page, "per_page": per_page, "order_by": "name"}
        )

        table = Table(title="Your GitLab Repositories")
        table.add_column("ID", justify="right", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Description")
        table.add_column("URL", style="blue")

        for project in projects:
            table.add_row(
                str(project["id"]),
                project["name"],
                project.get("description", ""),
                project["web_url"],
            )

        console.print(table)
    except Exception as e:
        console.print(f"[red]Error listing repositories: {str(e)}[/red]")
