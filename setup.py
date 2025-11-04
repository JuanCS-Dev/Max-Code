"""
Max-Code CLI Setup
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="max-code-cli",
    version="1.0.0-alpha",
    description="Constitutional Code Generation CLI powered by DETER-AGENT framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Max-Code Team",
    author_email="",  # TODO
    url="https://github.com/your-org/max-code-cli",  # TODO
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=[
        "requests>=2.31.0",
        "urllib3>=2.0.0",
        "click>=8.1.7",
        "rich>=13.7.0",
        "typer>=0.9.0",
        "pyyaml>=6.0.1",
        "python-dotenv>=1.0.0",
        "aiohttp>=3.9.0",
        "anthropic>=0.18.0",
        "pydantic>=2.5.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.12.0",
            "black>=23.12.0",
            "ruff>=0.1.0",
            "mypy>=1.7.0",
            "ipython>=8.18.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "max-code=cli.main:cli",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Code Generators",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="code-generation claude ai llm constitutional governance deter-agent",
)
