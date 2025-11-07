"""
Max-Code CLI - Setup Configuration

Constitutional AI Framework with Multi-Agent System
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

# Read requirements
requirements_file = Path(__file__).parent / "requirements.txt"
requirements = []
if requirements_file.exists():
    with open(requirements_file, "r", encoding="utf-8") as f:
        requirements = [
            line.strip()
            for line in f
            if line.strip() and not line.startswith("#")
        ]

setup(
    name="max-code-cli",
    version="3.0.0",
    description="AI-Powered Development Assistant with Constitutional AI Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Juan Carlos",
    author_email="juan@maximus.ai",
    url="https://github.com/juan/max-code-cli",
    license="MIT",

    # Package discovery
    packages=find_packages(exclude=["tests", "tests.*", "docs", "scripts"]),
    include_package_data=True,

    # Dependencies
    install_requires=requirements,
    python_requires=">=3.8",

    # Entry points for CLI commands
    entry_points={
        "console_scripts": [
            "max-code=cli.main:cli",
        ],
    },

    # Package data
    package_data={
        "": ["*.txt", "*.md", "*.yml", "*.yaml", "*.json"],
        "ui": ["*.tcss"],  # Textual CSS files
    },

    # Classifiers
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Code Generators",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],

    # Keywords
    keywords="ai cli assistant code-generation constitutional-ai claude anthropic",

    # Project URLs
    project_urls={
        "Documentation": "https://max-code.readthedocs.io",
        "Source": "https://github.com/juan/max-code-cli",
        "Bug Reports": "https://github.com/juan/max-code-cli/issues",
    },
)
