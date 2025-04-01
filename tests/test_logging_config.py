"""
Tests para el módulo logging_config de GitLab CLI
"""

import os
import logging
import pytest
from pathlib import Path

from gitlab_cli.utils.logging_config import (
    get_logger,
    get_log_level,
    get_environment,
    LOGS_DIR,
    LOG_LEVELS,
    PROJECT_ROOT,
)


def test_logs_dir_exists():
    """Verificar que el directorio de logs exista"""
    assert LOGS_DIR.exists()
    assert LOGS_DIR.is_dir()


def test_project_root():
    """Verificar que PROJECT_ROOT sea válido"""
    assert PROJECT_ROOT.exists()
    assert PROJECT_ROOT.is_dir()
    # Comprobar que contiene archivos principales del proyecto
    assert (PROJECT_ROOT / "pyproject.toml").exists()


def test_log_levels_dict():
    """Verificar que el diccionario LOG_LEVELS está configurado correctamente"""
    assert "development" in LOG_LEVELS
    assert "testing" in LOG_LEVELS
    assert "production" in LOG_LEVELS

    assert LOG_LEVELS["development"] == logging.DEBUG
    assert LOG_LEVELS["testing"] == logging.INFO
    assert LOG_LEVELS["production"] == logging.WARNING


def test_environment_default():
    """Verificar el valor predeterminado de ENVIRONMENT"""
    # Guardamos el valor actual
    original = os.environ.get("ENVIRONMENT", None)

    try:
        # Eliminamos la variable si existe
        if "ENVIRONMENT" in os.environ:
            del os.environ["ENVIRONMENT"]

        # Importamos de nuevo para que use el valor por defecto
        from importlib import reload
        import gitlab_cli.utils.logging_config

        reload(gitlab_cli.utils.logging_config)

        # Verificamos que el valor predeterminado sea "development"
        assert gitlab_cli.utils.logging_config.ENVIRONMENT == "development"

    finally:
        # Restauramos el valor original
        if original:
            os.environ["ENVIRONMENT"] = original
