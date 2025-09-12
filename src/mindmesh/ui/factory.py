"""
UI Factory for creating different user interface implementations.

This module provides a factory pattern for creating UI instances
based on configuration or user preference.
"""

from typing import Dict, Type

from ..config import Config
from ..llm.base import BaseLLMProvider
from .base import BaseUI
from .cli_ui import CLIUI

try:
    from .tkinter_ui import TkinterUI
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False


class UIFactory:
    """Factory for creating UI implementations."""
    
    _ui_classes: Dict[str, Type[BaseUI]] = {
        "cli": CLIUI,
        "terminal": CLIUI,  # Alias for CLI
        "console": CLIUI,  # Another alias for CLI
    }
    
    # Add tkinter classes if available
    if TKINTER_AVAILABLE:
        _ui_classes.update({
            "tkinter": TkinterUI,
            "gui": TkinterUI,  # Alias for tkinter
        })
    
    @classmethod
    def create_ui(
        cls,
        ui_type: str,
        config: Config,
        llm_provider: BaseLLMProvider
    ) -> BaseUI:
        """
        Create a UI instance based on type.
        
        Args:
            ui_type: Type of UI to create ("tkinter", "cli", etc.)
            config: Application configuration
            llm_provider: LLM provider instance
            
        Returns:
            BaseUI instance
            
        Raises:
            ValueError: If UI type is not supported
        """
        ui_type = ui_type.lower()
        
        if ui_type not in cls._ui_classes:
            available = ", ".join(cls._ui_classes.keys())
            raise ValueError(f"Unsupported UI type: {ui_type}. Available types: {available}")
        
        ui_class = cls._ui_classes[ui_type]
        return ui_class(config, llm_provider)
    
    @classmethod
    def get_available_ui_types(cls) -> list[str]:
        """
        Get list of available UI types.
        
        Returns:
            List of available UI type names
        """
        return list(cls._ui_classes.keys())
    
    @classmethod
    def register_ui_type(cls, ui_type: str, ui_class: Type[BaseUI]) -> None:
        """
        Register a custom UI implementation.
        
        Args:
            ui_type: Name for the UI type
            ui_class: UI class that inherits from BaseUI
            
        Raises:
            ValueError: If ui_class doesn't inherit from BaseUI
        """
        if not issubclass(ui_class, BaseUI):
            raise ValueError("UI class must inherit from BaseUI")
        
        cls._ui_classes[ui_type.lower()] = ui_class
    
    @classmethod
    def get_default_ui_type(cls) -> str:
        """
        Get the default UI type.
        
        Returns:
            Default UI type name
        """
        # Use CLI as default since tkinter may not be available in all environments
        return "cli"