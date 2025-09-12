"""
Base UI interface for MindMesh application.

This module defines the interface that all UI implementations must follow.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Callable, Optional
from dataclasses import dataclass

from ..config import Config
from ..llm.base import BaseLLMProvider


@dataclass
class UIEvent:
    """Represents a UI event."""
    event_type: str
    data: Dict[str, Any]
    source: str


class BaseUI(ABC):
    """Abstract base class for all UI implementations."""
    
    def __init__(self, config: Config, llm_provider: BaseLLMProvider):
        """
        Initialize the UI with configuration and LLM provider.
        
        Args:
            config: Application configuration
            llm_provider: LLM provider instance
        """
        self.config = config
        self.llm_provider = llm_provider
        self.event_handlers: Dict[str, Callable] = {}
        self.is_running = False
    
    @abstractmethod
    def initialize(self) -> None:
        """Initialize the UI components."""
        pass
    
    @abstractmethod
    def run(self) -> int:
        """
        Start the UI main loop.
        
        Returns:
            Exit code (0 for success)
        """
        pass
    
    @abstractmethod
    def shutdown(self) -> None:
        """Shutdown the UI and cleanup resources."""
        pass
    
    @abstractmethod
    def display_message(self, message: str, message_type: str = "info") -> None:
        """
        Display a message to the user.
        
        Args:
            message: Message to display
            message_type: Type of message ("info", "warning", "error", "success")
        """
        pass
    
    @abstractmethod
    def get_user_input(self, prompt: str, input_type: str = "text") -> str:
        """
        Get input from the user.
        
        Args:
            prompt: Prompt to display
            input_type: Type of input ("text", "password", "multiline")
            
        Returns:
            User input as string
        """
        pass
    
    @abstractmethod
    def show_settings_dialog(self) -> bool:
        """
        Show settings/preferences dialog.
        
        Returns:
            True if settings were modified, False otherwise
        """
        pass
    
    @abstractmethod
    def show_chat_interface(self) -> None:
        """Display the main chat/learning interface."""
        pass
    
    def register_event_handler(self, event_type: str, handler: Callable) -> None:
        """
        Register an event handler.
        
        Args:
            event_type: Type of event to handle
            handler: Function to call when event occurs
        """
        self.event_handlers[event_type] = handler
    
    def emit_event(self, event: UIEvent) -> None:
        """
        Emit an event to registered handlers.
        
        Args:
            event: Event to emit
        """
        handler = self.event_handlers.get(event.event_type)
        if handler:
            try:
                handler(event)
            except Exception as e:
                self.display_message(f"Error handling event {event.event_type}: {e}", "error")
    
    def update_theme(self) -> None:
        """Update UI theme based on configuration."""
        # Base implementation - override in subclasses
        pass
    
    def save_window_state(self) -> None:
        """Save current window state to configuration."""
        # Base implementation - override in subclasses
        pass
    
    def restore_window_state(self) -> None:
        """Restore window state from configuration."""
        # Base implementation - override in subclasses
        pass