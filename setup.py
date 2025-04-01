from setuptools import setup, find_packages

setup(
    name="gitlab-cli",
    use_scm_version=True,  # Usa setuptools-scm para gestionar versiones
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "requests",
        "rich",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.3",  # Asegúrate de que pytest esté aquí
            "pytest-cov",
            "black",
            "flake8",
            "mypy",
            "build",
            "twine",
            "setuptools-scm",
        ],
    },
    entry_points={
        "console_scripts": [
            "gitlab-cli=gitlab_cli.cli:main",
        ],
    },
    author="Miguel Diaz Castillo",
    author_email="miguel.acastillodiaz@gmail.com",
    description="CLI tool for GitLab API",
    keywords="gitlab, cli, api",
    url="https://github.com/MDCIrony/glab-cli",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires=">=3.7",
)
