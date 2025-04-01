import click

# Importar todos los comandos
from .list_issues import list_issues
from .show_issue import show_issue
from .create_issue import create_issue
from .update_issue import update_issue
from .delete_issue import delete_issue
from .issue_links import issue_links


@click.group()
def issues():
    """GitLab Issues CLI - Manage your GitLab issues with style!"""
    pass


# Registrar todos los comandos
issues.add_command(list_issues)
issues.add_command(show_issue)
issues.add_command(create_issue)
issues.add_command(update_issue)
issues.add_command(delete_issue)
issues.add_command(issue_links)

# # Para poder ejecutar directamente este módulo
# if __name__ == "__main__":
#     issues()
