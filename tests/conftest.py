"""
Configuración y fixtures compartidos para las pruebas de GitLab CLI
"""

import os
import pytest
from unittest.mock import MagicMock, patch


# Asegurarse de que estamos en ambiente de testing
@pytest.fixture(autouse=True)
def setup_test_environment():
    """Configura el entorno de testing para todas las pruebas"""
    original_env = os.environ.get("ENVIRONMENT", None)
    os.environ["ENVIRONMENT"] = "testing"
    yield
    if original_env:
        os.environ["ENVIRONMENT"] = original_env
    else:
        os.environ.pop("ENVIRONMENT", None)


@pytest.fixture
def mock_gitlab_api():
    """Mock para el cliente de GitLab API"""
    with patch("gitlab_cli.gitlab_api.GitLabAPI") as mock_api:
        # Configurar comportamientos comunes del mock aquí
        instance = mock_api.return_value
        instance.get_user.return_value = {"username": "test_user", "id": 123}
        instance.get_projects.return_value = [
            {"id": 1, "name": "test-project-1"},
            {"id": 2, "name": "test-project-2"},
        ]
        yield instance
