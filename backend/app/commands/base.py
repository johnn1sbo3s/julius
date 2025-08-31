"""
Base command class for management commands.
"""

import abc
from typing import Any, Dict, List, Optional


class BaseCommand(abc.ABC):
    """Base class for management commands."""
    
    help = "Description of the command"
    
    def __init__(self):
        self.verbosity = 1
    
    def add_arguments(self, parser) -> None:
        """
        Add command-specific arguments to the parser.
        Override this method in subcommands to add custom arguments.
        """
        pass
    
    @abc.abstractmethod
    def handle(self, *args: Any, **kwargs: Any) -> Optional[str]:
        """
        The actual logic of the command. Subclasses must implement this method.
        """
        pass
    
    def print_success(self, message: str) -> None:
        """Print a success message."""
        print(f"✅ {message}")
    
    def print_error(self, message: str) -> None:
        """Print an error message."""
        print(f"❌ {message}")
    
    def print_warning(self, message: str) -> None:
        """Print a warning message."""
        print(f"⚠️  {message}")
    
    def print_info(self, message: str) -> None:
        """Print an info message."""
        print(f"ℹ️  {message}")
    
    def execute(self, *args: Any, **kwargs: Any) -> Optional[str]:
        """Execute the command."""
        try:
            return self.handle(*args, **kwargs)
        except Exception as e:
            self.print_error(f"Command failed: {e}")
            raise