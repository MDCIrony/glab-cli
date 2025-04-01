import click
from rich.table import Table
from gitlab_cli.utils import console, gitlab, get_logger

# Inicializar el logger para este módulo
logger = get_logger(__name__)


@click.command()
@click.option("--page", default=1, help="Page number")
@click.option("--per-page", default=10, help="Items per page")
def list_repos(page, per_page):
    """List your GitLab repositories"""
    try:
        logger.info(f"Listing repositories (page={page}, per_page={per_page})")
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
        logger.debug(f"Found {len(projects)} repositories")
    except Exception as e:
        error_msg = f"Error listing repositories: {str(e)}"
        console.print(f"[red]{error_msg}[/red]")
        logger.error(error_msg, exc_info=True)
