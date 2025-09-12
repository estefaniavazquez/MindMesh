"""
MindMesh - A standalone Python app with UI and LLM integration for personalized learning.

This package provides a modular framework for creating educational applications
that can adapt to users' preferred learning methods using AI/LLM integration.
"""

__version__ = "0.1.0"
__author__ = "MindMesh Team"
__description__ = "A standalone Python app with UI and LLM integration for personalized learning"

from .app import MindMeshApp
from .config import Config, UserPreferences

__all__ = ["MindMeshApp", "Config", "UserPreferences"]