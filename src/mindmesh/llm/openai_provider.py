"""
OpenAI provider implementation for MindMesh.

This module provides integration with OpenAI's API for LLM functionality.
"""

import asyncio
from typing import List, Dict, Any, Optional, AsyncGenerator

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

from .base import BaseLLMProvider, Message, LearningContext


class OpenAIProvider(BaseLLMProvider):
    """OpenAI LLM provider implementation."""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize OpenAI provider with configuration."""
        super().__init__(config)
        
        if not OPENAI_AVAILABLE:
            raise ImportError("OpenAI package not installed. Install with: pip install openai")
        
        api_key = config.get("api_key")
        if not api_key:
            raise ValueError("OpenAI API key not provided")
        
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url=config.get("base_url"),
            timeout=self.timeout
        )
        
        # Default to GPT-3.5-turbo if no model specified
        if not self.model or self.model == "default":
            self.model = "gpt-3.5-turbo"
    
    async def generate_response(
        self,
        messages: List[Message],
        learning_context: Optional[LearningContext] = None
    ) -> str:
        """Generate a response using OpenAI's API."""
        # Convert internal messages to OpenAI format
        openai_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]
        
        # Add learning context as system message if provided
        if learning_context:
            system_prompt = self.create_learning_prompt("", learning_context)
            openai_messages.insert(0, {"role": "system", "content": system_prompt})
        
        try:
            # Run the synchronous API call in a thread to make it async
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model=self.model,
                    messages=openai_messages,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature
                )
            )
            
            return response.choices[0].message.content or ""
            
        except Exception as e:
            raise RuntimeError(f"OpenAI API error: {str(e)}")
    
    async def generate_streaming_response(
        self,
        messages: List[Message],
        learning_context: Optional[LearningContext] = None
    ) -> AsyncGenerator[str, None]:
        """Generate a streaming response using OpenAI's API."""
        # Convert internal messages to OpenAI format
        openai_messages = [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]
        
        # Add learning context as system message if provided
        if learning_context:
            system_prompt = self.create_learning_prompt("", learning_context)
            openai_messages.insert(0, {"role": "system", "content": system_prompt})
        
        try:
            # Create streaming response
            stream = await asyncio.get_event_loop().run_in_executor(
                None,
                lambda: self.client.chat.completions.create(
                    model=self.model,
                    messages=openai_messages,
                    max_tokens=self.max_tokens,
                    temperature=self.temperature,
                    stream=True
                )
            )
            
            for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
                    
        except Exception as e:
            raise RuntimeError(f"OpenAI streaming API error: {str(e)}")
    
    def test_connection(self) -> bool:
        """Test connection to OpenAI API."""
        try:
            # Simple test with minimal request
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": "Hello"}],
                max_tokens=5
            )
            return response.choices[0].message.content is not None
        except Exception:
            return False
    
    def get_available_models(self) -> List[str]:
        """Get list of available OpenAI models."""
        try:
            models = self.client.models.list()
            return [model.id for model in models.data if "gpt" in model.id]
        except Exception:
            return ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"]