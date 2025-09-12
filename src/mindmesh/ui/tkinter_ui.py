"""
Tkinter-based GUI implementation for MindMesh.

This module provides a graphical user interface using Python's built-in tkinter library.
"""

try:
    import tkinter as tk
    from tkinter import ttk, messagebox, scrolledtext, simpledialog
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False
    # Create dummy classes to prevent import errors
    tk = None
    ttk = None
    messagebox = None
    scrolledtext = None
    simpledialog = None

import asyncio
import threading
from typing import Optional

from .base import BaseUI, UIEvent
from ..config import Config, UITheme, LearningStyle
from ..llm.base import BaseLLMProvider, Message, LearningContext


class TkinterUI(BaseUI):
    """Tkinter-based GUI for MindMesh application."""
    
    def __init__(self, config: Config, llm_provider: BaseLLMProvider):
        """Initialize Tkinter UI."""
        super().__init__(config, llm_provider)
        """Initialize Tkinter UI."""
        super().__init__(config, llm_provider)
        self.root: Optional[tk.Tk] = None
        self.chat_display: Optional[scrolledtext.ScrolledText] = None
        self.input_entry: Optional[tk.Entry] = None
        self.send_button: Optional[tk.Button] = None
        self.status_bar: Optional[tk.Label] = None
        self.conversation_history = []
    
    def initialize(self) -> None:
        """Initialize the Tkinter GUI components."""
        self.root = tk.Tk()
        self.root.title("MindMesh - AI-Powered Learning Assistant")
        self.root.geometry("800x600")
        
        # Set up the main layout
        self._create_menu()
        self._create_main_interface()
        self._create_status_bar()
        
        # Apply theme and restore window state
        self.update_theme()
        self.restore_window_state()
        
        # Bind window close event
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
    
    def _create_menu(self) -> None:
        """Create the application menu bar."""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Session", command=self._new_session)
        file_menu.add_command(label="Save Session", command=self._save_session)
        file_menu.add_command(label="Load Session", command=self._load_session)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self._on_closing)
        
        # Settings menu
        settings_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Settings", menu=settings_menu)
        settings_menu.add_command(label="Preferences", command=self.show_settings_dialog)
        settings_menu.add_command(label="Learning Style", command=self._show_learning_style_dialog)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self._show_about_dialog)
    
    def _create_main_interface(self) -> None:
        """Create the main chat interface."""
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Chat display area
        chat_frame = ttk.LabelFrame(main_frame, text="Learning Chat")
        chat_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            wrap=tk.WORD,
            width=80,
            height=20,
            state=tk.DISABLED,
            font=("Consolas", self.config.user_preferences.font_size)
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Input area
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 5))
        
        # Input entry
        self.input_entry = ttk.Entry(input_frame, font=("Consolas", self.config.user_preferences.font_size))
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.input_entry.bind("<Return>", self._on_send_message)
        self.input_entry.bind("<Control-Return>", self._on_multiline_input)
        
        # Send button
        self.send_button = ttk.Button(input_frame, text="Send", command=self._on_send_message)
        self.send_button.pack(side=tk.RIGHT)
        
        # Focus on input
        self.input_entry.focus()
    
    def _create_status_bar(self) -> None:
        """Create the status bar."""
        self.status_bar = ttk.Label(
            self.root,
            text=f"Ready - Learning Style: {self.config.user_preferences.learning_style.value}",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def _on_send_message(self, event=None) -> None:
        """Handle sending a message."""
        message = self.input_entry.get().strip()
        if not message:
            return
        
        # Clear input
        self.input_entry.delete(0, tk.END)
        
        # Add user message to display
        self._add_message_to_chat("You", message, "user")
        
        # Start async message processing
        threading.Thread(target=self._process_message_async, args=(message,), daemon=True).start()
    
    def _process_message_async(self, message: str) -> None:
        """Process message asynchronously."""
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
            
            # Add AI response to display (thread-safe)
            self.root.after(0, self._add_message_to_chat, "AI Tutor", response, "assistant")
            
        except Exception as e:
            error_msg = f"Error processing message: {str(e)}"
            self.root.after(0, self._add_message_to_chat, "System", error_msg, "error")
    
    def _add_message_to_chat(self, sender: str, message: str, role: str) -> None:
        """Add a message to the chat display."""
        self.chat_display.config(state=tk.NORMAL)
        
        # Add timestamp and sender
        import datetime
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        
        # Color coding based on role
        if role == "user":
            color = "blue"
        elif role == "assistant":
            color = "green"
        elif role == "error":
            color = "red"
        else:
            color = "black"
        
        # Insert message
        self.chat_display.insert(tk.END, f"[{timestamp}] {sender}: ", "timestamp")
        self.chat_display.insert(tk.END, f"{message}\n\n", role)
        
        # Configure tags for styling
        self.chat_display.tag_config("timestamp", foreground="gray")
        self.chat_display.tag_config("user", foreground="blue")
        self.chat_display.tag_config("assistant", foreground="green")
        self.chat_display.tag_config("error", foreground="red")
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def _on_multiline_input(self, event=None) -> None:
        """Handle multiline input dialog."""
        dialog = MultilineInputDialog(self.root, "Multi-line Input", "Enter your message:")
        if dialog.result:
            self.input_entry.delete(0, tk.END)
            self.input_entry.insert(0, dialog.result.replace('\n', ' '))
            self._on_send_message()
    
    def _new_session(self) -> None:
        """Start a new learning session."""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state=tk.DISABLED)
        self.conversation_history = []
        self._add_message_to_chat("System", "New learning session started!", "system")
    
    def _save_session(self) -> None:
        """Save current session."""
        # Placeholder for session saving functionality
        messagebox.showinfo("Save Session", "Session saving functionality coming soon!")
    
    def _load_session(self) -> None:
        """Load a previous session."""
        # Placeholder for session loading functionality
        messagebox.showinfo("Load Session", "Session loading functionality coming soon!")
    
    def _show_learning_style_dialog(self) -> None:
        """Show learning style selection dialog."""
        dialog = LearningStyleDialog(self.root, self.config)
        if dialog.result:
            self.config.user_preferences.learning_style = dialog.result
            self.config.save()
            self._update_status_bar()
    
    def _show_about_dialog(self) -> None:
        """Show about dialog."""
        about_text = """MindMesh v0.1.0
        
AI-Powered Personalized Learning Assistant

Features:
• Adaptive learning based on your learning style
• Multiple LLM provider support
• Customizable UI themes
• Session management

Built with Python and tkinter."""
        messagebox.showinfo("About MindMesh", about_text)
    
    def _update_status_bar(self) -> None:
        """Update the status bar text."""
        if self.status_bar:
            self.status_bar.config(
                text=f"Ready - Learning Style: {self.config.user_preferences.learning_style.value}"
            )
    
    def _on_closing(self) -> None:
        """Handle application closing."""
        self.save_window_state()
        self.shutdown()
    
    def run(self) -> int:
        """Start the Tkinter main loop."""
        if not self.root:
            self.initialize()
        
        self.is_running = True
        try:
            self.root.mainloop()
            return 0
        except KeyboardInterrupt:
            return 130
        except Exception as e:
            self.display_message(f"UI Error: {e}", "error")
            return 1
        finally:
            self.is_running = False
    
    def shutdown(self) -> None:
        """Shutdown the UI."""
        self.is_running = False
        if self.root:
            self.root.quit()
            self.root.destroy()
    
    def display_message(self, message: str, message_type: str = "info") -> None:
        """Display a message to the user."""
        if message_type == "error":
            messagebox.showerror("Error", message)
        elif message_type == "warning":
            messagebox.showwarning("Warning", message)
        elif message_type == "success":
            messagebox.showinfo("Success", message)
        else:
            messagebox.showinfo("Information", message)
    
    def get_user_input(self, prompt: str, input_type: str = "text") -> str:
        """Get input from the user."""
        if input_type == "password":
            return simpledialog.askstring("Input", prompt, show='*') or ""
        elif input_type == "multiline":
            dialog = MultilineInputDialog(self.root, "Input", prompt)
            return dialog.result or ""
        else:
            return simpledialog.askstring("Input", prompt) or ""
    
    def show_settings_dialog(self) -> bool:
        """Show settings dialog."""
        dialog = SettingsDialog(self.root, self.config)
        if dialog.result:
            self.config.save()
            self.update_theme()
            return True
        return False
    
    def show_chat_interface(self) -> None:
        """Display the main chat interface (already shown)."""
        pass
    
    def update_theme(self) -> None:
        """Update UI theme."""
        theme = self.config.user_preferences.ui_theme
        if theme == UITheme.DARK:
            # Simple dark theme implementation
            style = ttk.Style()
            style.theme_use('clam')
            # More sophisticated theming would go here
    
    def save_window_state(self) -> None:
        """Save window state to configuration."""
        if self.root:
            self.config.user_preferences.window_geometry = self.root.geometry()
            self.config.save()
    
    def restore_window_state(self) -> None:
        """Restore window state from configuration."""
        if self.root and self.config.user_preferences.window_geometry:
            try:
                self.root.geometry(self.config.user_preferences.window_geometry)
            except tk.TclError:
                pass  # Invalid geometry string


class MultilineInputDialog:
    """Simple multiline input dialog."""
    
    def __init__(self, parent, title, prompt):
        self.result = None
        
        self.top = tk.Toplevel(parent)
        self.top.title(title)
        self.top.geometry("400x300")
        self.top.transient(parent)
        self.top.grab_set()
        
        # Prompt label
        tk.Label(self.top, text=prompt).pack(pady=10)
        
        # Text area
        self.text_area = scrolledtext.ScrolledText(self.top, width=50, height=15)
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Buttons
        button_frame = tk.Frame(self.top)
        button_frame.pack(pady=5)
        
        tk.Button(button_frame, text="OK", command=self.ok_clicked).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cancel", command=self.cancel_clicked).pack(side=tk.LEFT, padx=5)
        
        self.text_area.focus()
        self.top.wait_window()
    
    def ok_clicked(self):
        self.result = self.text_area.get(1.0, tk.END).strip()
        self.top.destroy()
    
    def cancel_clicked(self):
        self.top.destroy()


class LearningStyleDialog:
    """Learning style selection dialog."""
    
    def __init__(self, parent, config):
        self.result = None
        self.config = config
        
        self.top = tk.Toplevel(parent)
        self.top.title("Learning Style")
        self.top.geometry("300x250")
        self.top.transient(parent)
        self.top.grab_set()
        
        tk.Label(self.top, text="Select your preferred learning style:").pack(pady=10)
        
        self.style_var = tk.StringVar(value=config.user_preferences.learning_style.value)
        
        for style in LearningStyle:
            tk.Radiobutton(
                self.top,
                text=style.value.replace('_', ' ').title(),
                variable=self.style_var,
                value=style.value
            ).pack(anchor=tk.W, padx=20)
        
        button_frame = tk.Frame(self.top)
        button_frame.pack(pady=20)
        
        tk.Button(button_frame, text="OK", command=self.ok_clicked).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cancel", command=self.cancel_clicked).pack(side=tk.LEFT, padx=5)
        
        self.top.wait_window()
    
    def ok_clicked(self):
        self.result = LearningStyle(self.style_var.get())
        self.top.destroy()
    
    def cancel_clicked(self):
        self.top.destroy()


class SettingsDialog:
    """Settings/preferences dialog."""
    
    def __init__(self, parent, config):
        self.result = False
        self.config = config
        
        self.top = tk.Toplevel(parent)
        self.top.title("Settings")
        self.top.geometry("400x300")
        self.top.transient(parent)
        self.top.grab_set()
        
        # Create notebook for tabs
        notebook = ttk.Notebook(self.top)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # General tab
        general_frame = ttk.Frame(notebook)
        notebook.add(general_frame, text="General")
        
        # Theme selection
        tk.Label(general_frame, text="Theme:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.theme_var = tk.StringVar(value=config.user_preferences.ui_theme.value)
        theme_combo = ttk.Combobox(general_frame, textvariable=self.theme_var, state="readonly")
        theme_combo['values'] = [theme.value for theme in UITheme]
        theme_combo.grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Font size
        tk.Label(general_frame, text="Font Size:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.font_size_var = tk.IntVar(value=config.user_preferences.font_size)
        font_size_spin = tk.Spinbox(general_frame, from_=8, to=24, textvariable=self.font_size_var)
        font_size_spin.grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Buttons
        button_frame = tk.Frame(self.top)
        button_frame.pack(pady=10)
        
        tk.Button(button_frame, text="OK", command=self.ok_clicked).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Cancel", command=self.cancel_clicked).pack(side=tk.LEFT, padx=5)
        
        self.top.wait_window()
    
    def ok_clicked(self):
        # Apply changes
        self.config.user_preferences.ui_theme = UITheme(self.theme_var.get())
        self.config.user_preferences.font_size = self.font_size_var.get()
        self.result = True
        self.top.destroy()
    
    def cancel_clicked(self):
        self.top.destroy()