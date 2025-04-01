from setuptools import setup, find_packages

setup(
    name="gitlab-cli",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click",
        "requests",
        "rich",
    ],
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
