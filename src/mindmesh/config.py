"""
Configuration management for MindMesh application.

This module handles application configuration, user preferences,
and settings for LLM providers and UI customization.
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional, List
from enum import Enum

from pydantic import BaseModel, Field, validator
from dotenv import load_dotenv


class LearningStyle(str, Enum):
    """Enumeration of supported learning styles."""
    VISUAL = "visual"
    AUDITORY = "auditory"
    KINESTHETIC = "kinesthetic"
    READING_WRITING = "reading_writing"
    MULTIMODAL = "multimodal"


class UITheme(str, Enum):
    """Enumeration of supported UI themes."""
    LIGHT = "light"
    DARK = "dark"
    SYSTEM = "system"


class LLMProvider(str, Enum):
    """Enumeration of supported LLM providers."""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    LOCAL = "local"
    CUSTOM = "custom"


class LLMConfig(BaseModel):
    """Configuration for LLM providers."""
    provider: LLMProvider = LLMProvider.OPENAI
    api_key: Optional[str] = None
    base_url: Optional[str] = None
    model: str = "gpt-3.5-turbo"
    max_tokens: int = 1000
    temperature: float = 0.7
    timeout: int = 30
    
    @validator('api_key', pre=True, always=True)
    def load_api_key_from_env(cls, v: Optional[str], values: Dict[str, Any]) -> Optional[str]:
        """Load API key from environment if not provided."""
        if v:
            return v
        
        provider = values.get('provider', LLMProvider.OPENAI)
        if provider == LLMProvider.OPENAI:
            return os.getenv('OPENAI_API_KEY')
        elif provider == LLMProvider.ANTHROPIC:
            return os.getenv('ANTHROPIC_API_KEY')
        
        return None


class UserPreferences(BaseModel):
    """User preferences and learning configuration."""
    learning_style: LearningStyle = LearningStyle.MULTIMODAL
    preferred_languages: List[str] = Field(default_factory=lambda: ["en"])
    difficulty_level: str = "intermediate"  # beginner, intermediate, advanced
    session_duration: int = 30  # minutes
    daily_goal: int = 60  # minutes
    enable_notifications: bool = True
    auto_save: bool = True
    
    # UI preferences
    ui_theme: UITheme = UITheme.SYSTEM
    font_size: int = 12
    window_geometry: Optional[str] = None  # "800x600+100+100"


class Config(BaseModel):
    """Main application configuration."""
    # Application settings
    debug: bool = False
    log_level: str = "INFO"
    data_dir: str = Field(default_factory=lambda: str(Path.home() / ".mindmesh"))
    
    # LLM configuration
    llm: LLMConfig = Field(default_factory=LLMConfig)
    
    # User preferences
    user_preferences: UserPreferences = Field(default_factory=UserPreferences)
    
    # Custom settings
    custom_settings: Dict[str, Any] = Field(default_factory=dict)
    
    def __init__(self, **data):
        super().__init__(**data)
        # Ensure data directory exists
        Path(self.data_dir).mkdir(parents=True, exist_ok=True)
    
    @classmethod
    def load(cls, config_path: Optional[str] = None) -> "Config":
        """
        Load configuration from file.
        
        Args:
            config_path: Path to configuration file. If None, uses default location.
            
        Returns:
            Config instance
        """
        # Load environment variables
        load_dotenv()
        
        # Determine config file path
        if config_path is None:
            config_path = str(Path.home() / ".mindmesh" / "config.json")
        
        # Create default config if file doesn't exist
        if not Path(config_path).exists():
            config = cls()
            config.save(config_path)
            return config
        
        # Load from file
        try:
            with open(config_path, 'r') as f:
                data = json.load(f)
            return cls(**data)
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Warning: Could not load config from {config_path}: {e}")
            print("Using default configuration")
            return cls()
    
    def save(self, config_path: Optional[str] = None) -> None:
        """
        Save configuration to file.
        
        Args:
            config_path: Path to save configuration. If None, uses default location.
        """
        if config_path is None:
            config_path = str(Path(self.data_dir) / "config.json")
        
        # Ensure directory exists
        Path(config_path).parent.mkdir(parents=True, exist_ok=True)
        
        with open(config_path, 'w') as f:
            json.dump(self.dict(), f, indent=2)
    
    def update_user_preferences(self, **kwargs) -> None:
        """Update user preferences with provided values."""
        for key, value in kwargs.items():
            if hasattr(self.user_preferences, key):
                setattr(self.user_preferences, key, value)
    
    def get_llm_config(self) -> Dict[str, Any]:
        """Get LLM configuration as dictionary for easy API usage."""
        return self.llm.dict()
    
    def get_data_path(self, filename: str) -> str:
        """Get full path for a data file."""
        return str(Path(self.data_dir) / filename)