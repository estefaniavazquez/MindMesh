"""
Base class for LLM providers in MindMesh.

This module defines the interface that all LLM providers must implement
to ensure consistent behavior across different AI services.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional, AsyncGenerator
from dataclasses import dataclass

from ..config import LearningStyle


@dataclass
class Message:
    """Represents a message in a conversation."""
    role: str  # "user", "assistant", "system"
    content: str
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class LearningContext:
    """Context information for personalized learning responses."""
    learning_style: LearningStyle
    difficulty_level: str
    previous_topics: List[str]
    current_topic: str
    session_duration: int
    user_progress: Dict[str, Any]


class BaseLLMProvider(ABC):
    """Abstract base class for all LLM providers."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Initialize the LLM provider with configuration.
        
        Args:
            config: Configuration dictionary containing API keys, model settings, etc.
        """
        self.config = config
        self.model = config.get("model", "default")
        self.max_tokens = config.get("max_tokens", 1000)
        self.temperature = config.get("temperature", 0.7)
        self.timeout = config.get("timeout", 30)
    
    @abstractmethod
    async def generate_response(
        self,
        messages: List[Message],
        learning_context: Optional[LearningContext] = None
    ) -> str:
        """
        Generate a response from the LLM.
        
        Args:
            messages: List of conversation messages
            learning_context: Context for personalized learning
            
        Returns:
            Generated response string
        """
        pass
    
    @abstractmethod
    async def generate_streaming_response(
        self,
        messages: List[Message],
        learning_context: Optional[LearningContext] = None
    ) -> AsyncGenerator[str, None]:
        """
        Generate a streaming response from the LLM.
        
        Args:
            messages: List of conversation messages
            learning_context: Context for personalized learning
            
        Yields:
            Chunks of the generated response
        """
        pass
    
    def create_learning_prompt(
        self,
        topic: str,
        learning_context: LearningContext
    ) -> str:
        """
        Create a personalized learning prompt based on context.
        
        Args:
            topic: The topic to teach/explain
            learning_context: User's learning preferences and context
            
        Returns:
            Formatted prompt for the LLM
        """
        style_instructions = {
            LearningStyle.VISUAL: "Use visual descriptions, diagrams, and examples that can be easily visualized.",
            LearningStyle.AUDITORY: "Use explanations that work well when spoken aloud, with rhythm and verbal mnemonics.",
            LearningStyle.KINESTHETIC: "Include hands-on activities, practical examples, and interactive elements.",
            LearningStyle.READING_WRITING: "Provide detailed written explanations with lists, notes, and text-based examples.",
            LearningStyle.MULTIMODAL: "Combine multiple approaches: visual, auditory, kinesthetic, and reading/writing elements."
        }
        
        difficulty_instructions = {
            "beginner": "Explain concepts in simple terms, avoid jargon, provide basic examples.",
            "intermediate": "Use moderate complexity, some technical terms with explanations, practical examples.",
            "advanced": "Use technical language, complex examples, assume prior knowledge."
        }
        
        base_prompt = f"""You are an AI tutor specializing in personalized education. Your task is to explain the topic "{topic}" to a learner.

Learning Style: {learning_context.learning_style.value}
Difficulty Level: {learning_context.difficulty_level}
Session Duration: {learning_context.session_duration} minutes
Current Topic: {learning_context.current_topic}

Instructions for this learning style:
{style_instructions.get(learning_context.learning_style, '')}

Instructions for this difficulty level:
{difficulty_instructions.get(learning_context.difficulty_level, '')}

Previous topics covered: {', '.join(learning_context.previous_topics) if learning_context.previous_topics else 'None'}

Please provide an engaging and personalized explanation of "{topic}" that matches the learner's style and level."""
        
        return base_prompt
    
    @abstractmethod
    def test_connection(self) -> bool:
        """
        Test if the connection to the LLM service is working.
        
        Returns:
            True if connection is successful, False otherwise
        """
        pass
    
    def get_model_info(self) -> Dict[str, Any]:
        """
        Get information about the current model.
        
        Returns:
            Dictionary with model information
        """
        return {
            "provider": self.__class__.__name__,
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature
        }