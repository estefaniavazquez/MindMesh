"""
Anthropic provider implementation for MindMesh.

This module provides integration with Anthropic's Claude API for LLM functionality.
"""

import asyncio
from typing import List, Dict, Any, Optional, AsyncGenerator

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

from .base import BaseLLMProvider, Message, LearningContext


class AnthropicProvider(BaseLLMProvider):
    """Anthropic Claude LLM provider implementation."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize Anthropic provider with configuration."""
        super().__init__(config)
        
        if not ANTHROPIC_AVAILABLE:
            raise ImportError("Anthropic package not installed. Install with: pip install anthropic")
        
        api_key = config.get("api_key")
        if not api_key:
            raise ValueError("Anthropic API key not provided")
        
        self.client = anthropic.Anthropic(
            api_key=api_key,
            base_url=config.get("base_url"),
            timeout=self.timeout
        )
        
        # Default to Claude-3 if no model specified
        if not self.model or self.model == "default":
            self.model = "claude-3-sonnet-20240229"
    
    async def generate_response(
        self,
        messages: List[Message],
        learning_context: Optional[LearningContext] = None
    ) -> str:
        """Generate a response using Anthropic's API."""
        # Convert internal messages to Anthropic format
        anthropic_messages = []
        system_message = None
        
        for msg in messages:
            if msg.role == "system":
                system_message = msg.content
            else:
                anthropic_messages.append({
                    "role": msg.role,
                    "content": msg.content
                })
        
        # Add learning context to system message if provided
        if learning_context:
            context_prompt = self.create_learning_prompt("", learning_context)
            if system_message:
                system_message = f"{system_message}\n\n{context_prompt}"
            else:
                system_message = context_prompt
        
        try:
            # Prepare parameters
            params = {
                "model": self.model,
                "messages": anthropic_messages,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature
            }
            
            if system_message:
                params["system"] = system_message
            
            # Run the synchronous API call in a thread to make it async
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.messages.create(**params)
            )
            
            return response.content[0].text if response.content else ""
            
        except Exception as e:
            raise RuntimeError(f"Anthropic API error: {str(e)}")
    
    async def generate_streaming_response(
        self,
        messages: List[Message],
        learning_context: Optional[LearningContext] = None
    ) -> AsyncGenerator[str, None]:
        """Generate a streaming response using Anthropic's API."""
        # Convert internal messages to Anthropic format
        anthropic_messages = []
        system_message = None
        
        for msg in messages:
            if msg.role == "system":
                system_message = msg.content
            else:
                anthropic_messages.append({
                    "role": msg.role,
                    "content": msg.content
                })
        
        # Add learning context to system message if provided
        if learning_context:
            context_prompt = self.create_learning_prompt("", learning_context)
            if system_message:
                system_message = f"{system_message}\n\n{context_prompt}"
            else:
                system_message = context_prompt
        
        try:
            # Prepare parameters
            params = {
                "model": self.model,
                "messages": anthropic_messages,
                "max_tokens": self.max_tokens,
                "temperature": self.temperature,
                "stream": True
            }
            
            if system_message:
                params["system"] = system_message
            
            # Create streaming response
            stream = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.messages.create(**params)
            )
            
            for chunk in stream:
                if hasattr(chunk, 'delta') and hasattr(chunk.delta, 'text'):
                    yield chunk.delta.text
                    
        except Exception as e:
            raise RuntimeError(f"Anthropic streaming API error: {str(e)}")
    
    def test_connection(self) -> bool:
        """Test connection to Anthropic API."""
        try:
            # Simple test with minimal request
            response = self.client.messages.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )
            return response.content[0].text is not None
        except Exception:
            return False
    
    def get_available_models(self) -> List[str]:
        """Get list of available Anthropic models."""
        # Anthropic doesn't have a models endpoint, return known models
        return [
            "claude-3-opus-20240229",
            "claude-3-sonnet-20240229",
            "claude-3-haiku-20240307",
            "claude-2.1",
            "claude-2.0",
            "claude-instant-1.2"
        ]