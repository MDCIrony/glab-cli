from rich.console import Console
from gitlab_api import GitLabAPI
from utils.logging_config import get_logger, get_log_level, get_environment

# Instancias compartidas
console = Console()
gitlab = GitLabAPI()

# Exportar las funciones de logging
__all__ = ["console", "gitlab", "get_logger", "get_log_level", "get_environment"]
