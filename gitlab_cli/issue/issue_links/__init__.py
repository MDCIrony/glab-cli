import click

# Importar todos los comandos de enlaces
from gitlab_cli.issue.issue_links.create_link import create_link
from gitlab_cli.issue.issue_links.list_links import list_links
from gitlab_cli.issue.issue_links.delete_link import delete_link


@click.group("link")
def issue_links():
    """Manage links between issues."""
    pass


# Registrar subcomandos
issue_links.add_command(create_link)
issue_links.add_command(list_links)
issue_links.add_command(delete_link)
