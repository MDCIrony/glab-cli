"""
Tests para el módulo gitlab_api de GitLab CLI
"""

import pytest
from unittest.mock import patch

from gitlab_cli.gitlab_api import GitLabAPI


@pytest.fixture
def gitlab_instance():
    """Crea una instancia de GitLabAPI para pruebas"""
    return GitLabAPI()


def test_gitlab_api_init(gitlab_instance):
    """Verifica que se puede inicializar GitLabAPI"""
    assert gitlab_instance is not None
    assert isinstance(gitlab_instance, GitLabAPI)


@patch("gitlab_cli.gitlab_api.GitLabAPI.get_user")
def test_get_user_method(mock_get_user):
    """Prueba el método get_user de GitLabAPI"""
    # Configurar el mock
    expected_user = {"id": 123, "username": "test_user"}
    mock_get_user.return_value = expected_user

    # Crear instancia y llamar al método
    api = GitLabAPI()
    user = api.get_user()

    # Verificaciones
    assert user == expected_user
    mock_get_user.assert_called_once()
