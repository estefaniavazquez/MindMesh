"""
Command-line interface implementation for MindMesh.

This module provides a text-based interface for the MindMesh application.
"""

import asyncio
import sys
from typing import Optional

from .base import BaseUI
from ..config import Config, LearningStyle
from ..llm.base import BaseLLMProvider, Message, LearningContext


class CLIUI(BaseUI):
    """Command-line interface for MindMesh application."""
    
    def __init__(self, config: Config, llm_provider: BaseLLMProvider):
        """Initialize CLI UI."""
        super().__init__(config, llm_provider)
        self.conversation_history = []
    
    def initialize(self) -> None:
        """Initialize the CLI interface."""
        self._print_welcome()
        self._print_help()
    
    def _print_welcome(self) -> None:
        """Print welcome message."""
        print("=" * 60)
        print("🧠 Welcome to MindMesh - AI-Powered Learning Assistant 🧠")
        print("=" * 60)
        print(f"Learning Style: {self.config.user_preferences.learning_style.value}")
        print(f"Difficulty Level: {self.config.user_preferences.difficulty_level}")
        print(f"LLM Provider: {self.config.llm.provider.value}")
        print("=" * 60)
    
    def _print_help(self) -> None:
        """Print help information."""
        print("\nAvailable commands:")
        print("  /help     - Show this help message")
        print("  /settings - Open settings")
        print("  /style    - Change learning style")
        print("  /clear    - Clear conversation history")
        print("  /quit     - Exit the application")
        print("\nJust type your question or topic to start learning!")
        print("-" * 60)
    
    def run(self) -> int:
        """Start the CLI main loop."""
        self.is_running = True
        
        try:
            while self.is_running:
                try:
                    # Get user input
                    user_input = input("\n💭 You: ").strip()
                    
                    if not user_input:
                        continue
                    
                    # Handle commands
                    if user_input.startswith('/'):
                        self._handle_command(user_input)
                        continue
                    
                    # Process regular message
                    print("🤖 AI Tutor: ", end="", flush=True)
                    self._process_message(user_input)
                    
                except EOFError:
                    print("\n\nGoodbye!")
                    break
                except KeyboardInterrupt:
                    print("\n\nSession interrupted. Type /quit to exit properly.")
                    continue
            
            return 0
            
        except Exception as e:
            print(f"\nError: {e}")
            return 1
        finally:
            self.is_running = False
    
    def _handle_command(self, command: str) -> None:
        """Handle CLI commands."""
        cmd = command.lower().strip()
        
        if cmd == '/help':
            self._print_help()
        elif cmd == '/settings':
            self.show_settings_dialog()
        elif cmd == '/style':
            self._change_learning_style()
        elif cmd == '/clear':
            self.conversation_history = []
            print("📝 Conversation history cleared!")
        elif cmd == '/quit':
            print("👋 Goodbye! Keep learning!")
            self.is_running = False
        else:
            print(f"❌ Unknown command: {command}")
            print("Type /help for available commands.")
    
    def _process_message(self, message: str) -> None:
        """Process a user message and get AI response."""
        try:
            # Create learning context
            learning_context = LearningContext(
                learning_style=self.config.user_preferences.learning_style,
                difficulty_level=self.config.user_preferences.difficulty_level,
                previous_topics=[],
                current_topic=message,
                session_duration=self.config.user_preferences.session_duration,
                user_progress={}
            )
            
            # Create message history
            messages = [Message(role="user", content=message)]
            
            # Get response from LLM
            response = asyncio.run(
                self.llm_provider.generate_response(messages, learning_context)
            )
            
            print(response)
            print("-" * 60)
            
            # Store in conversation history
            self.conversation_history.extend([
                {"role": "user", "content": message},
                {"role": "assistant", "content": response}
            ])
            
        except Exception as e:
            print(f"❌ Error processing message: {str(e)}")
    
    def _change_learning_style(self) -> None:
        """Change learning style interactively."""
        print("\nAvailable learning styles:")
        styles = list(LearningStyle)
        for i, style in enumerate(styles, 1):
            current = " (current)" if style == self.config.user_preferences.learning_style else ""
            print(f"  {i}. {style.value.replace('_', ' ').title()}{current}")
        
        try:
            choice = input("\nEnter your choice (1-{}): ".format(len(styles))).strip()
            if choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(styles):
                    self.config.user_preferences.learning_style = styles[index]
                    self.config.save()
                    print(f"✅ Learning style changed to: {styles[index].value}")
                else:
                    print("❌ Invalid choice!")
            else:
                print("❌ Please enter a number!")
        except ValueError:
            print("❌ Invalid input!")
    
    def shutdown(self) -> None:
        """Shutdown the CLI."""
        self.is_running = False
    
    def display_message(self, message: str, message_type: str = "info") -> None:
        """Display a message to the user."""
        icons = {
            "info": "ℹ️",
            "warning": "⚠️",
            "error": "❌",
            "success": "✅"
        }
        icon = icons.get(message_type, "ℹ️")
        print(f"{icon} {message}")
    
    def get_user_input(self, prompt: str, input_type: str = "text") -> str:
        """Get input from the user."""
        if input_type == "password":
            import getpass
            return getpass.getpass(prompt)
        elif input_type == "multiline":
            print(f"{prompt} (Press Ctrl+D or Ctrl+Z when done)")
            lines = []
            try:
                while True:
                    line = input()
                    lines.append(line)
            except EOFError:
                pass
            return '\n'.join(lines)
        else:
            return input(prompt)
    
    def show_settings_dialog(self) -> bool:
        """Show settings dialog."""
        print("\n" + "=" * 40)
        print("⚙️  SETTINGS")
        print("=" * 40)
        print(f"Learning Style: {self.config.user_preferences.learning_style.value}")
        print(f"Difficulty Level: {self.config.user_preferences.difficulty_level}")
        print(f"Session Duration: {self.config.user_preferences.session_duration} minutes")
        print(f"Font Size: {self.config.user_preferences.font_size}")
        print(f"LLM Provider: {self.config.llm.provider.value}")
        print(f"LLM Model: {self.config.llm.model}")
        print("=" * 40)
        
        while True:
            print("\nWhat would you like to change?")
            print("1. Learning Style")
            print("2. Difficulty Level")
            print("3. Session Duration")
            print("4. Back to chat")
            
            choice = input("Enter your choice (1-4): ").strip()
            
            if choice == "1":
                self._change_learning_style()
            elif choice == "2":
                self._change_difficulty_level()
            elif choice == "3":
                self._change_session_duration()
            elif choice == "4":
                break
            else:
                print("❌ Invalid choice!")
        
        return True
    
    def _change_difficulty_level(self) -> None:
        """Change difficulty level."""
        levels = ["beginner", "intermediate", "advanced"]
        print("\nDifficulty levels:")
        for i, level in enumerate(levels, 1):
            current = " (current)" if level == self.config.user_preferences.difficulty_level else ""
            print(f"  {i}. {level.title()}{current}")
        
        try:
            choice = input("Enter your choice (1-3): ").strip()
            if choice.isdigit():
                index = int(choice) - 1
                if 0 <= index < len(levels):
                    self.config.user_preferences.difficulty_level = levels[index]
                    self.config.save()
                    print(f"✅ Difficulty level changed to: {levels[index]}")
                else:
                    print("❌ Invalid choice!")
            else:
                print("❌ Please enter a number!")
        except ValueError:
            print("❌ Invalid input!")
    
    def _change_session_duration(self) -> None:
        """Change session duration."""
        try:
            duration = input(f"Enter session duration in minutes (current: {self.config.user_preferences.session_duration}): ").strip()
            if duration.isdigit():
                duration_int = int(duration)
                if 5 <= duration_int <= 180:  # 5 minutes to 3 hours
                    self.config.user_preferences.session_duration = duration_int
                    self.config.save()
                    print(f"✅ Session duration changed to: {duration_int} minutes")
                else:
                    print("❌ Duration must be between 5 and 180 minutes!")
            else:
                print("❌ Please enter a valid number!")
        except ValueError:
            print("❌ Invalid input!")
    
    def show_chat_interface(self) -> None:
        """Display the chat interface (already active in CLI)."""
        pass