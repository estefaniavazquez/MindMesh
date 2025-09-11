"""
Main MindMesh application class.

This module contains the main application logic that orchestrates
the UI, LLM providers, and configuration management.
"""

import logging
import sys
from typing import Optional

from .config import Config
from .llm.factory import LLMFactory
from .ui.factory import UIFactory
from .llm.base import BaseLLMProvider
from .ui.base import BaseUI


class MindMeshApp:
    """Main MindMesh application class."""
    
    def __init__(self, config: Optional[Config] = None, ui_type: Optional[str] = None):
        """
        Initialize the MindMesh application.
        
        Args:
            config: Application configuration (defaults to loading from file)
            ui_type: UI type to use (defaults to configuration or auto-detect)
        """
        self.config = config or Config.load()
        self.ui_type = ui_type or self._determine_ui_type()
        self.llm_provider: Optional[BaseLLMProvider] = None
        self.ui: Optional[BaseUI] = None
        
        # Set up logging
        self._setup_logging()
        
        logging.info(f"MindMesh application initialized with UI type: {self.ui_type}")
    
    def _determine_ui_type(self) -> str:
        """Determine the best UI type to use."""
        # Check if we're in a terminal environment
        if not sys.stdout.isatty():
            return "cli"
        
        # Try to get default from factory
        try:
            return UIFactory.get_default_ui_type()
        except Exception:
            return "cli"
    
    def _setup_logging(self) -> None:
        """Set up application logging."""
        log_level = getattr(logging, self.config.log_level.upper(), logging.INFO)
        
        logging.basicConfig(
            level=log_level,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(self.config.get_data_path('mindmesh.log')),
                logging.StreamHandler() if self.config.debug else logging.NullHandler()
            ]
        )
    
    def initialize(self) -> bool:
        """
        Initialize the application components.
        
        Returns:
            True if initialization was successful, False otherwise
        """
        try:
            # Initialize LLM provider
            logging.info("Initializing LLM provider...")
            self.llm_provider = LLMFactory.create_provider(
                self.config.llm,
                fallback_to_mock=True
            )
            
            # Test LLM connection
            if not self.llm_provider.test_connection():
                logging.warning("LLM provider connection test failed, but continuing with fallback")
            else:
                logging.info("LLM provider connection test successful")
            
            # Initialize UI
            logging.info(f"Initializing UI: {self.ui_type}")
            self.ui = UIFactory.create_ui(
                self.ui_type,
                self.config,
                self.llm_provider
            )
            
            # Initialize UI components
            self.ui.initialize()
            
            # Set up event handlers
            self._setup_event_handlers()
            
            logging.info("Application initialization complete")
            return True
            
        except Exception as e:
            logging.error(f"Failed to initialize application: {e}")
            if self.config.debug:
                import traceback
                traceback.print_exc()
            return False
    
    def _setup_event_handlers(self) -> None:
        """Set up event handlers for UI events."""
        if not self.ui:
            return
        
        # Register event handlers
        self.ui.register_event_handler("config_changed", self._on_config_changed)
        self.ui.register_event_handler("llm_provider_changed", self._on_llm_provider_changed)
        self.ui.register_event_handler("ui_theme_changed", self._on_ui_theme_changed)
    
    def _on_config_changed(self, event) -> None:
        """Handle configuration change events."""
        logging.info("Configuration changed, saving...")
        self.config.save()
    
    def _on_llm_provider_changed(self, event) -> None:
        """Handle LLM provider change events."""
        logging.info("LLM provider changed, reinitializing...")
        try:
            self.llm_provider = LLMFactory.create_provider(
                self.config.llm,
                fallback_to_mock=True
            )
        except Exception as e:
            logging.error(f"Failed to reinitialize LLM provider: {e}")
    
    def _on_ui_theme_changed(self, event) -> None:
        """Handle UI theme change events."""
        if self.ui:
            self.ui.update_theme()
    
    def run(self) -> int:
        """
        Run the application.
        
        Returns:
            Exit code (0 for success, non-zero for error)
        """
        # Initialize if not already done
        if not self.llm_provider or not self.ui:
            if not self.initialize():
                return 1
        
        try:
            logging.info("Starting MindMesh application")
            
            # Show welcome message
            self._show_welcome_message()
            
            # Run the UI main loop
            exit_code = self.ui.run()
            
            logging.info(f"Application exited with code: {exit_code}")
            return exit_code
            
        except KeyboardInterrupt:
            logging.info("Application interrupted by user")
            return 130
        except Exception as e:
            logging.error(f"Application error: {e}")
            if self.config.debug:
                import traceback
                traceback.print_exc()
            return 1
        finally:
            self.shutdown()
    
    def _show_welcome_message(self) -> None:
        """Show welcome message based on UI type."""
        if not self.ui:
            return
        
        welcome_msg = (
            "Welcome to MindMesh! 🧠\n"
            "I'm your AI-powered learning assistant, ready to adapt to your learning style.\n"
            f"Your current learning preference: {self.config.user_preferences.learning_style.value}\n"
            "Ask me anything or type a topic you'd like to learn about!"
        )
        
        if self.ui_type == "cli":
            # CLI will show its own welcome message
            pass
        else:
            # For GUI, we could show this in the chat area
            pass
    
    def shutdown(self) -> None:
        """Shutdown the application and cleanup resources."""
        logging.info("Shutting down MindMesh application")
        
        if self.ui:
            try:
                self.ui.shutdown()
            except Exception as e:
                logging.error(f"Error shutting down UI: {e}")
        
        # Save final configuration
        try:
            self.config.save()
        except Exception as e:
            logging.error(f"Error saving configuration: {e}")
        
        logging.info("Application shutdown complete")
    
    def get_status(self) -> dict:
        """
        Get application status information.
        
        Returns:
            Dictionary with status information
        """
        return {
            "ui_type": self.ui_type,
            "llm_provider": self.config.llm.provider.value if self.config else None,
            "llm_model": self.config.llm.model if self.config else None,
            "learning_style": self.config.user_preferences.learning_style.value if self.config else None,
            "is_running": self.ui.is_running if self.ui else False,
            "data_dir": self.config.data_dir if self.config else None
        }
    
    def update_config(self, **kwargs) -> None:
        """
        Update configuration with provided values.
        
        Args:
            **kwargs: Configuration values to update
        """
        for key, value in kwargs.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
            elif hasattr(self.config.user_preferences, key):
                setattr(self.config.user_preferences, key, value)
            elif hasattr(self.config.llm, key):
                setattr(self.config.llm, key, value)
        
        self.config.save()
    
    def switch_ui_type(self, new_ui_type: str) -> bool:
        """
        Switch to a different UI type.
        
        Args:
            new_ui_type: New UI type to switch to
            
        Returns:
            True if switch was successful, False otherwise
        """
        if new_ui_type == self.ui_type:
            return True
        
        try:
            # Shutdown current UI
            if self.ui:
                self.ui.shutdown()
            
            # Create new UI
            self.ui_type = new_ui_type
            self.ui = UIFactory.create_ui(
                self.ui_type,
                self.config,
                self.llm_provider
            )
            
            self.ui.initialize()
            self._setup_event_handlers()
            
            logging.info(f"Switched to UI type: {new_ui_type}")
            return True
            
        except Exception as e:
            logging.error(f"Failed to switch UI type: {e}")
            return False