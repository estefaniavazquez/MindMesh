#!/usr/bin/env python3
"""
Main entry point for the MindMesh application.

This module provides the main function to start the MindMesh application
with UI and LLM integration capabilities.
"""

import sys
import argparse
from typing import List, Optional

from .app import MindMeshApp
from .config import Config


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="MindMesh - AI-powered personalized learning application",
        epilog="Example: mindmesh --config myconfig.json --ui tkinter"
    )
    
    parser.add_argument(
        "--config",
        type=str,
        default=None,
        help="Path to configuration file (default: ~/.mindmesh/config.json)"
    )
    
    parser.add_argument(
        "--ui",
        type=str,
        choices=["tkinter", "cli", "web"],
        default="tkinter",
        help="User interface type to use (default: tkinter)"
    )
    
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug mode with verbose logging"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"MindMesh {__import__('mindmesh').__version__}"
    )
    
    return parser


def main(args: Optional[List[str]] = None) -> int:
    """
    Main entry point for the MindMesh application.
    
    Args:
        args: Command line arguments (defaults to sys.argv[1:])
        
    Returns:
        Exit code (0 for success, non-zero for error)
    """
    parser = create_parser()
    parsed_args = parser.parse_args(args)
    
    try:
        # Load configuration
        config = Config.load(parsed_args.config)
        
        # Enable debug mode if requested
        if parsed_args.debug:
            config.debug = True
        
        # Create and run the application
        app = MindMeshApp(config=config, ui_type=parsed_args.ui)
        return app.run()
        
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
        return 130
    except Exception as e:
        if parsed_args.debug:
            import traceback
            traceback.print_exc()
        else:
            print(f"Error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())