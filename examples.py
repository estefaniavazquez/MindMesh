#!/usr/bin/env python3
"""
Example usage of MindMesh application.

This script demonstrates how to use the MindMesh framework
for creating AI-powered learning applications.
"""

import asyncio
from mindmesh import MindMeshApp, Config, UserPreferences
from mindmesh.config import LearningStyle, LLMProvider
from mindmesh.llm.base import Message, LearningContext


def example_basic_usage():
    """Example: Basic usage with default configuration."""
    print("=== Example 1: Basic Usage ===")
    
    # Create and run app with defaults
    app = MindMeshApp()
    
    # Show status
    status = app.get_status()
    print(f"App Status: {status}")
    
    # Note: app.run() would start the interactive UI
    # For this example, we'll just show initialization
    app.initialize()
    print("✅ App initialized successfully!")
    app.shutdown()


def example_custom_config():
    """Example: Custom configuration setup."""
    print("\n=== Example 2: Custom Configuration ===")
    
    # Create custom configuration
    config = Config()
    config.user_preferences.learning_style = LearningStyle.VISUAL
    config.user_preferences.difficulty_level = "advanced"
    config.llm.provider = LLMProvider.OPENAI
    config.llm.model = "gpt-4"
    config.debug = True
    
    # Create app with custom config
    app = MindMeshApp(config=config, ui_type="cli")
    
    print(f"Learning Style: {config.user_preferences.learning_style.value}")
    print(f"LLM Provider: {config.llm.provider.value}")
    print(f"UI Type: {app.ui_type}")
    
    app.initialize()
    print("✅ App with custom config initialized!")
    app.shutdown()


async def example_direct_llm_usage():
    """Example: Direct LLM provider usage."""
    print("\n=== Example 3: Direct LLM Usage ===")
    
    from mindmesh.llm.factory import LLMFactory
    from mindmesh.config import LLMConfig
    
    # Create LLM config (will use mock provider without API keys)
    llm_config = LLMConfig(
        provider=LLMProvider.OPENAI,
        model="gpt-3.5-turbo",
        max_tokens=100
    )
    
    # Create provider (will fallback to mock)
    provider = LLMFactory.create_provider(llm_config, fallback_to_mock=True)
    
    # Create learning context
    context = LearningContext(
        learning_style=LearningStyle.KINESTHETIC,
        difficulty_level="beginner",
        previous_topics=[],
        current_topic="Python basics",
        session_duration=30,
        user_progress={}
    )
    
    # Create messages
    messages = [
        Message(role="user", content="Explain Python variables")
    ]
    
    # Get response
    response = await provider.generate_response(messages, context)
    print(f"LLM Response: {response}")
    
    print("✅ Direct LLM usage completed!")


def example_ui_types():
    """Example: Different UI types."""
    print("\n=== Example 4: UI Types ===")
    
    from mindmesh.ui.factory import UIFactory
    
    # Show available UI types
    available_ui = UIFactory.get_available_ui_types()
    print(f"Available UI types: {available_ui}")
    
    # Create app with CLI interface
    app_cli = MindMeshApp(ui_type="cli")
    print(f"CLI App UI Type: {app_cli.ui_type}")
    
    # Create app with GUI interface
    try:
        app_gui = MindMeshApp(ui_type="tkinter")
        print(f"GUI App UI Type: {app_gui.ui_type}")
    except Exception as e:
        print(f"GUI not available: {e}")
    
    print("✅ UI types example completed!")


def example_configuration_management():
    """Example: Configuration management."""
    print("\n=== Example 5: Configuration Management ===")
    
    # Load default config
    config = Config.load()
    print(f"Default data directory: {config.data_dir}")
    
    # Update user preferences
    config.update_user_preferences(
        learning_style=LearningStyle.MULTIMODAL,
        difficulty_level="intermediate",
        session_duration=45
    )
    
    # Get LLM config
    llm_config = config.get_llm_config()
    print(f"LLM Config: {llm_config}")
    
    # Save configuration
    config.save()
    print("✅ Configuration saved!")
    
    # Load configuration
    reloaded_config = Config.load()
    print(f"Reloaded learning style: {reloaded_config.user_preferences.learning_style.value}")
    
    print("✅ Configuration management completed!")


def example_extensibility():
    """Example: Extending MindMesh with custom components."""
    print("\n=== Example 6: Extensibility ===")
    
    from mindmesh.llm.base import BaseLLMProvider
    from mindmesh.ui.base import BaseUI
    
    # Custom LLM Provider
    class CustomLLMProvider(BaseLLMProvider):
        async def generate_response(self, messages, learning_context=None):
            return f"Custom LLM response to: {messages[-1].content if messages else 'N/A'}"
        
        async def generate_streaming_response(self, messages, learning_context=None):
            response = await self.generate_response(messages, learning_context)
            for word in response.split():
                yield word + " "
        
        def test_connection(self):
            return True
    
    # Register custom provider
    from mindmesh.llm.factory import LLMFactory
    LLMFactory.register_provider("custom", CustomLLMProvider)
    
    print("✅ Custom LLM provider registered!")
    
    # Show available providers
    providers = LLMFactory.get_available_providers()
    print(f"Available providers: {providers}")
    
    print("✅ Extensibility example completed!")


def main():
    """Run all examples."""
    print("🧠 MindMesh Examples")
    print("=" * 50)
    
    # Run synchronous examples
    example_basic_usage()
    example_custom_config()
    example_ui_types()
    example_configuration_management()
    example_extensibility()
    
    # Run async example
    asyncio.run(example_direct_llm_usage())
    
    print("\n🎉 All examples completed!")
    print("\nTo run the actual MindMesh application:")
    print("  python -m mindmesh.main")
    print("  python -m mindmesh.main --ui cli")
    print("  python -m mindmesh.main --config myconfig.json")


if __name__ == "__main__":
    main()