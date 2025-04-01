import click
from user.login import verify_login
from repos.list import list_repos
from issue import issues


@click.group()
def cli():
    """CLI tool for GitLab API interactions"""
    pass


# Añadimos los comandos al CLI
cli.add_command(verify_login)
cli.add_command(list_repos)
cli.add_command(issues)

if __name__ == "__main__":
    cli()
