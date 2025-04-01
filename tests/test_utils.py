"""
Tests para el módulo utils de GitLab CLI
"""

import logging
import pytest
from unittest.mock import patch

from gitlab_cli.utils import get_logger, get_log_level, get_environment
from gitlab_cli.utils import console, gitlab


def test_get_environment():
    """Verifica que get_environment devuelve el ambiente correcto"""
    # Debería ser 'testing' porque lo configuramos en conftest.py
    assert get_environment() == "testing"


def test_get_log_level():
    """Verifica que get_log_level devuelve el nivel correcto para testing"""
    assert get_log_level() == logging.INFO


def test_get_logger():
    """Verifica que get_logger devuelve un logger configurado correctamente"""
    logger = get_logger("test_logger")
    # Verificar que el logger tiene el nivel correcto
    assert logger.level == logging.INFO
    # Verificar que el logger tiene el nombre correcto
    assert logger.name == "test_logger"


def test_console_instance():
    """Verifica que la instancia de console está disponible"""
    assert console is not None
    # Verificar que es una instancia de Console de rich
    from rich.console import Console

    assert isinstance(console, Console)


def test_gitlab_instance():
    """Verifica que la instancia de gitlab está disponible"""
    assert gitlab is not None
    # Verificar que es una instancia de GitLabAPI
    from gitlab_cli.gitlab_api import GitLabAPI

    assert isinstance(gitlab, GitLabAPI)
