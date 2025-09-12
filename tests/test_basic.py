"""
Basic tests for MindMesh application.

This module contains basic functionality tests to ensure
the core components work correctly.
"""

import asyncio
import tempfile
import os
from pathlib import Path

from mindmesh import MindMeshApp, Config, UserPreferences
from mindmesh.config import LearningStyle, LLMProvider, UITheme
from mindmesh.llm.factory import LLMFactory
from mindmesh.llm.base import Message, LearningContext
from mindmesh.ui.factory import UIFactory


class TestConfig:
    """Test configuration management."""
    
    def test_config_creation(self):
        """Test creating a new configuration."""
        config = Config()
        assert config.debug is False
        assert config.log_level == "INFO"
        assert config.llm.provider == LLMProvider.OPENAI
        assert config.user_preferences.learning_style == LearningStyle.MULTIMODAL
    
    def test_config_save_load(self):
        """Test saving and loading configuration."""
        with tempfile.TemporaryDirectory() as temp_dir:
            config_path = os.path.join(temp_dir, "test_config.json")
            
            # Create and save config
            config = Config()
            config.debug = True
            config.user_preferences.learning_style = LearningStyle.VISUAL
            config.save(config_path)
            
            # Load config
            loaded_config = Config.load(config_path)
            assert loaded_config.debug is True
            assert loaded_config.user_preferences.learning_style == LearningStyle.VISUAL
    
    def test_user_preferences_update(self):
        """Test updating user preferences."""
        config = Config()
        config.update_user_preferences(
            learning_style=LearningStyle.AUDITORY,
            difficulty_level="advanced"
        )
        
        assert config.user_preferences.learning_style == LearningStyle.AUDITORY
        assert config.user_preferences.difficulty_level == "advanced"


class TestLLMFactory:
    """Test LLM factory and providers."""
    
    def test_create_mock_provider(self):
        """Test creating mock LLM provider."""
        from mindmesh.config import LLMConfig
        
        config = LLMConfig(provider=LLMProvider.LOCAL)
        provider = LLMFactory.create_provider(config, fallback_to_mock=True)
        
        assert provider is not None
        assert provider.test_connection() is True
    
    async def test_mock_provider_response(self):
        """Test mock provider response generation."""
        from mindmesh.config import LLMConfig
        
        config = LLMConfig(provider=LLMProvider.LOCAL)
        provider = LLMFactory.create_provider(config, fallback_to_mock=True)
        
        messages = [Message(role="user", content="Hello")]
        response = await provider.generate_response(messages)
        
        assert "Hello" in response
        assert len(response) > 0
    
    def test_available_providers(self):
        """Test getting available providers."""
        providers = LLMFactory.get_available_providers()
        assert isinstance(providers, dict)
        assert len(providers) > 0


class TestUIFactory:
    """Test UI factory."""
    
    def test_available_ui_types(self):
        """Test getting available UI types."""
        ui_types = UIFactory.get_available_ui_types()
        assert isinstance(ui_types, list)
        assert "cli" in ui_types
        assert "tkinter" in ui_types
    
    def test_create_cli_ui(self):
        """Test creating CLI UI."""
        config = Config()
        provider = LLMFactory.create_provider(config.llm, fallback_to_mock=True)
        
        ui = UIFactory.create_ui("cli", config, provider)
        assert ui is not None
        assert hasattr(ui, 'run')
        assert hasattr(ui, 'initialize')


class TestMindMeshApp:
    """Test main application class."""
    
    def test_app_creation(self):
        """Test creating MindMesh application."""
        app = MindMeshApp()
        assert app.config is not None
        assert app.ui_type in ["cli", "tkinter"]
    
    def test_app_initialization(self):
        """Test application initialization."""
        config = Config()
        app = MindMeshApp(config=config, ui_type="cli")
        
        success = app.initialize()
        assert success is True
        assert app.llm_provider is not None
        assert app.ui is not None
        
        app.shutdown()
    
    def test_app_status(self):
        """Test getting application status."""
        app = MindMeshApp(ui_type="cli")
        app.initialize()
        
        status = app.get_status()
        assert isinstance(status, dict)
        assert "ui_type" in status
        assert "llm_provider" in status
        assert status["ui_type"] == "cli"
        
        app.shutdown()
    
    def test_config_update(self):
        """Test updating application configuration."""
        app = MindMeshApp()
        app.initialize()
        
        original_style = app.config.user_preferences.learning_style
        app.update_config(learning_style=LearningStyle.KINESTHETIC)
        
        assert app.config.user_preferences.learning_style == LearningStyle.KINESTHETIC
        assert app.config.user_preferences.learning_style != original_style
        
        app.shutdown()


class TestLearningContext:
    """Test learning context functionality."""
    
    def test_learning_context_creation(self):
        """Test creating learning context."""
        context = LearningContext(
            learning_style=LearningStyle.VISUAL,
            difficulty_level="beginner",
            previous_topics=["python", "variables"],
            current_topic="functions",
            session_duration=30,
            user_progress={"python": 0.8}
        )
        
        assert context.learning_style == LearningStyle.VISUAL
        assert context.difficulty_level == "beginner"
        assert "python" in context.previous_topics
        assert context.current_topic == "functions"
    
    def test_learning_prompt_creation(self):
        """Test creating learning prompts."""
        from mindmesh.config import LLMConfig
        
        config = LLMConfig()
        provider = LLMFactory.create_provider(config, fallback_to_mock=True)
        
        context = LearningContext(
            learning_style=LearningStyle.KINESTHETIC,
            difficulty_level="intermediate",
            previous_topics=[],
            current_topic="Python loops",
            session_duration=45,
            user_progress={}
        )
        
        prompt = provider.create_learning_prompt("Python loops", context)
        assert "kinesthetic" in prompt.lower()
        assert "intermediate" in prompt.lower()
        assert "Python loops" in prompt


def test_import_structure():
    """Test that all modules can be imported correctly."""
    # Test main imports
    from mindmesh import MindMeshApp, Config, UserPreferences
    
    # Test config imports
    from mindmesh.config import LearningStyle, LLMProvider, UITheme, LLMConfig
    
    # Test LLM imports
    from mindmesh.llm import BaseLLMProvider, LLMFactory
    
    # Test UI imports
    from mindmesh.ui import BaseUI, UIFactory
    
    # Test that classes are properly defined
    assert MindMeshApp is not None
    assert Config is not None
    assert BaseLLMProvider is not None
    assert BaseUI is not None


if __name__ == "__main__":
    # Run basic tests without pytest
    print("Running basic MindMesh tests...")
    
    # Test configuration
    print("✓ Testing configuration...")
    test_config = TestConfig()
    test_config.test_config_creation()
    
    # Test LLM factory
    print("✓ Testing LLM factory...")
    test_llm = TestLLMFactory()
    test_llm.test_create_mock_provider()
    
    # Test UI factory
    print("✓ Testing UI factory...")
    test_ui = TestUIFactory()
    test_ui.test_available_ui_types()
    
    # Test app
    print("✓ Testing application...")
    test_app = TestMindMeshApp()
    test_app.test_app_creation()
    
    # Test imports
    print("✓ Testing imports...")
    test_import_structure()
    
    print("🎉 All basic tests passed!")