import click
from utils import console, gitlab


@click.command()
def verify_login():
    """Verify GitLab login by getting the authenticated user info"""
    try:
        # Obtener info del usuario autenticado actual (usando el token)
        user_info = gitlab.get_current_user()

        console.print("[green]✓ Login successful![/green]")
        console.print(f"User ID: {user_info['id']}")
        console.print(f"Username: {user_info['username']}")
        console.print(f"Name: {user_info['name']}")
        console.print(f"Email: {user_info.get('email', 'N/A')}")

    except Exception as e:
        console.print(f"[red]✗ Login failed: {str(e)}[/red]")
