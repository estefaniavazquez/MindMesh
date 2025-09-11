"""
Factory for creating LLM providers in MindMesh.

This module provides a factory pattern for creating different LLM providers
based on configuration settings.
"""

from typing import Dict, Any, Optional

from ..config import LLMProvider, LLMConfig
from .base import BaseLLMProvider
from .openai_provider import OpenAIProvider
from .anthropic_provider import AnthropicProvider


class MockLLMProvider(BaseLLMProvider):
    """Mock LLM provider for testing and development."""
    
    async def generate_response(self, messages, learning_context=None):
        """Generate a mock response."""
        return f"Mock response to: {messages[-1].content if messages else 'empty message'}"
    
    async def generate_streaming_response(self, messages, learning_context=None):
        """Generate a mock streaming response."""
        response = f"Mock streaming response to: {messages[-1].content if messages else 'empty message'}"
        for word in response.split():
            yield word + " "
    
    def test_connection(self):
        """Always return True for mock provider."""
        return True


class LLMFactory:
    """Factory for creating LLM providers."""
    
    _providers = {
        LLMProvider.OPENAI: OpenAIProvider,
        LLMProvider.ANTHROPIC: AnthropicProvider,
        LLMProvider.LOCAL: MockLLMProvider,  # Placeholder for local providers
        LLMProvider.CUSTOM: MockLLMProvider,  # Placeholder for custom providers
    }
    
    @classmethod
    def create_provider(
        self,
        config: LLMConfig,
        fallback_to_mock: bool = True
    ) -> BaseLLMProvider:
        """
        Create an LLM provider based on configuration.
        
        Args:
            config: LLM configuration object
            fallback_to_mock: Whether to fallback to mock provider on errors
            
        Returns:
            BaseLLMProvider instance
            
        Raises:
            ValueError: If provider is not supported and fallback is disabled
            ImportError: If required dependencies are not installed and fallback is disabled
        """
        provider_class = self._providers.get(config.provider)
        
        if not provider_class:
            if fallback_to_mock:
                print(f"Warning: Provider {config.provider} not supported, using mock provider")
                return MockLLMProvider(config.dict())
            else:
                raise ValueError(f"Unsupported LLM provider: {config.provider}")
        
        try:
            return provider_class(config.dict())
        except ImportError as e:
            if fallback_to_mock:
                print(f"Warning: {str(e)}, using mock provider")
                return MockLLMProvider(config.dict())
            else:
                raise
        except Exception as e:
            if fallback_to_mock:
                print(f"Warning: Failed to initialize {config.provider}: {str(e)}, using mock provider")
                return MockLLMProvider(config.dict())
            else:
                raise
    
    @classmethod
    def get_available_providers(self) -> Dict[str, bool]:
        """
        Get list of available providers and their availability status.
        
        Returns:
            Dictionary mapping provider names to availability status
        """
        availability = {}
        
        for provider_name in LLMProvider:
            try:
                # Try to create a mock config and provider
                mock_config = LLMConfig(provider=provider_name, api_key="test")
                self.create_provider(mock_config, fallback_to_mock=False)
                availability[provider_name.value] = True
            except (ImportError, ValueError):
                availability[provider_name.value] = False
        
        return availability
    
    @classmethod
    def register_provider(
        self,
        provider_name: str,
        provider_class: type
    ) -> None:
        """
        Register a custom LLM provider.
        
        Args:
            provider_name: Name of the provider
            provider_class: Provider class that inherits from BaseLLMProvider
        """
        if not issubclass(provider_class, BaseLLMProvider):
            raise ValueError("Provider class must inherit from BaseLLMProvider")
        
        # Create a custom enum value if needed
        if provider_name not in [p.value for p in LLMProvider]:
            # For simplicity, we'll just add it to the providers dict
            # In a more sophisticated implementation, you might want to extend the enum
            pass
        
        self._providers[provider_name] = provider_class