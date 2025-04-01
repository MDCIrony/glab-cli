import click
from gitlab_cli.user.login import verify_login
from gitlab_cli.repos.list import list_repos
from gitlab_cli.issue import issues


@click.group()
def cli():
    """CLI tool for GitLab API interactions"""
    pass


# Añadimos los comandos al CLI
cli.add_command(verify_login)
cli.add_command(list_repos)
cli.add_command(issues)


def main():
    """Entry point for the application defined in setup.py"""
    cli()


if __name__ == "__main__":
    cli()
