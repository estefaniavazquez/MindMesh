"""
UI package for MindMesh application.

This package provides different user interface implementations
including GUI, CLI, and web-based interfaces.
"""

from .base import BaseUI
from .cli_ui import CLIUI
from .factory import UIFactory

try:
    from .tkinter_ui import TkinterUI
    __all__ = ["BaseUI", "TkinterUI", "CLIUI", "UIFactory"]
except ImportError:
    # Tkinter not available
    __all__ = ["BaseUI", "CLIUI", "UIFactory"]