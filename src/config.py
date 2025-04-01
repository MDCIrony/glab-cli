from dotenv import load_dotenv
import os
from pathlib import Path

# Determinar la ubicación del directorio raíz del proyecto
# independientemente de dónde se ejecute el script
project_root = Path(__file__).parent.parent.absolute()
dotenv_path = project_root / '.env'

# Load environment variables from .env file with explicit path
load_dotenv(dotenv_path)

# GitLab API configuration with better defaults and error handling
GITLAB_URL = os.getenv('GITLAB_URL')
if not GITLAB_URL:
    GITLAB_URL = 'https://gitlab.com'
    print(f"Warning: GITLAB_URL not found in environment. Using default: {GITLAB_URL}")

GITLAB_TOKEN = os.getenv('GITLAB_TOKEN')
API_VERSION = 'v4'
BASE_URL = f"{GITLAB_URL}/api/{API_VERSION}"

# API endpoints
PROJECTS_ENDPOINT = f"{BASE_URL}/projects"
USERS_ENDPOINT = f"{BASE_URL}/users"
GROUPS_ENDPOINT = f"{BASE_URL}/groups"
CURRENT_USER_ENDPOINT = f"{BASE_URL}/user"  # Endpoint para el usuario autenticado

# Request headers
HEADERS = {
    'Private-Token': GITLAB_TOKEN,
    'Content-Type': 'application/json'
}

# Error messages
ERROR_MISSING_TOKEN = "GitLab API token not found. Please set GITLAB_TOKEN in .env file"
ERROR_REQUEST_FAILED = "Request to GitLab API failed: {}"

# Verify token exists
if not GITLAB_TOKEN:
    raise ValueError(ERROR_MISSING_TOKEN)

# Debug information to help diagnose environment issues
print(f"Using GitLab URL: {GITLAB_URL}")
print(f"API Base URL: {BASE_URL}")
print(f"Loaded .env from: {dotenv_path}")
