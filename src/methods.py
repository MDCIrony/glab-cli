# gitlab_utils.py
from gitlab_api import GitLabAPI
from rich.console import Console
from rich.table import Table

console = Console()
gitlab = GitLabAPI()


def list_my_repositories(page=1, per_page=10):
    """Lists your GitLab repositories with pagination."""
    try:
        projects = gitlab.get_projects({
            "page": page,
            "per_page": per_page,
            "order_by": "name"
        })

        table = Table(title="Your GitLab Repositories")
        table.add_column("ID", justify="right", style="cyan")
        table.add_column("Name", style="green")
        table.add_column("Description")
        table.add_column("URL", style="blue")

        for project in projects:
            table.add_row(
                str(project['id']),
                project['name'],
                project.get('description', ''),
                project['web_url']
            )

        console.print(table)
    except Exception as e:
        console.print(f"[red]Error listing repositories: {str(e)}[/red]")


def list_project_issues(project_id, state='opened', page=1, per_page=10):
    """Lists issues for a specific project with pagination and state filtering."""
    try:
        issues = gitlab.get_project_issues(
            project_id,
            {
                "state": state,
                "page": page,
                "per_page": per_page,
                "order_by": "created_at"
            }
        )

        table = Table(title=f"Issues for Project {project_id}")
        table.add_column("ID", justify="right", style="cyan")
        table.add_column("Title", style="green")
        table.add_column("State", style="yellow")
        table.add_column("Created At", style="blue")

        for issue in issues:
            table.add_row(
                str(issue['iid']),
                issue['title'],
                issue['state'],
                issue['created_at']
            )

        console.print(table)
    except Exception as e:
        console.print(f"[red]Error listing issues: {str(e)}[/red]")

def list_project_merge_requests(project_id, state='opened', page=1, per_page=10):
    """Lists merge requests for a specific project with pagination and state filtering."""
    try:
        merge_requests = gitlab.get_project_merge_requests(
            project_id,
            {
                "state": state,
                "page": page,
                "per_page": per_page,
                "order_by": "created_at"
            }
        )

        table = Table(title=f"Merge Requests for Project {project_id}")
        table.add_column("ID", justify="right", style="cyan")
        table.add_column("Title", style="green")
        table.add_column("State", style="yellow")
        table.add_column("Source Branch", style="blue")
        table.add_column("Target Branch", style="blue")
        table.add_column("Created At", style="blue")

        for mr in merge_requests:
            table.add_row(
                str(mr['iid']),
                mr['title'],
                mr['state'],
                mr['source_branch'],
                mr['target_branch'],
                mr['created_at']
            )

        console.print(table)
    except Exception as e:
        console.print(f"[red]Error listing merge requests: {str(e)}[/red]")

def list_project_branches(project_id):
    """Lists branches for a specific project."""
    try:
        branches = gitlab.get_project_branches(project_id)

        table = Table(title=f"Branches for Project {project_id}")
        table.add_column("Name", style="green")
        table.add_column("Commit", style="cyan")
        table.add_column("Protected", style="yellow")

        for branch in branches:
            table.add_row(
                branch['name'],
                branch['commit']['id'][:8],  # Short commit ID
                str(branch['protected'])
            )

        console.print(table)
    except Exception as e:
        console.print(f"[red]Error listing branches: {str(e)}[/red]")

if __name__ == '__main__':
    # Example usage:
    # list_my_repositories()
    # list_project_issues(12345)  # Replace with a valid project ID
    # list_project_merge_requests(12345)  # Replace with a valid project ID
    # list_project_branches(12345)  # Replace with a valid project ID
    pass
