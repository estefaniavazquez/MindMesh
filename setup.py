#!/usr/bin/env python3
"""
MindMesh setup script for alternative installation methods.

This provides a traditional setup.py interface for environments
that don't support pyproject.toml.
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="mindmesh",
    version="0.1.0",
    description="A standalone Python app with UI and LLM integration for personalized learning",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="MindMesh Team",
    author_email="",
    url="https://github.com/estefaniavazquez/MindMesh",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.25.0",
        "pydantic>=2.0.0",
        "python-dotenv>=0.19.0",
    ],
    extras_require={
        "llm": [
            "openai>=1.0.0",
            "anthropic>=0.7.0",
        ],
        "dev": [
            "pytest>=6.0",
            "black>=22.0",
            "flake8>=4.0",
            "mypy>=0.910",
        ],
    },
    entry_points={
        "console_scripts": [
            "mindmesh=mindmesh.main:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Education",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords="ai, education, learning, llm, gui, personalized-learning",
    project_urls={
        "Bug Reports": "https://github.com/estefaniavazquez/MindMesh/issues",
        "Source": "https://github.com/estefaniavazquez/MindMesh",
        "Documentation": "https://github.com/estefaniavazquez/MindMesh#readme",
    },
)