#!/usr/bin/env python3
"""
Management script for running administrative commands.

Usage:
    python manage.py <command> [arguments]

Available commands:
    create-admin    Create an admin user
    
Examples:
    python manage.py create-admin --email admin@example.com --name "Admin User" --password "SecurePass123!"
    python manage.py create-admin --email joao@gmail.com --name "João Silva" --password "MyPassword123" --force
"""

import argparse
import sys
from typing import Dict, Type

from app.commands.base import BaseCommand
from app.commands.create_admin import CreateAdminCommand


# Registry of available commands
COMMANDS: Dict[str, Type[BaseCommand]] = {
    'create-admin': CreateAdminCommand,
}


def main():
    """Main entry point for the management script."""
    parser = argparse.ArgumentParser(
        description="Management script for FastAPI application",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        'command',
        choices=COMMANDS.keys(),
        help='Command to run'
    )
    
    # Parse known args to get the command
    args, remaining = parser.parse_known_args()
    
    # Get the command class
    command_class = COMMANDS[args.command]
    command = command_class()
    
    # Create a new parser for the specific command
    command_parser = argparse.ArgumentParser(
        description=command.help,
        prog=f'manage.py {args.command}'
    )
    
    # Add command-specific arguments
    command.add_arguments(command_parser)
    
    # Parse the remaining arguments
    command_args = command_parser.parse_args(remaining)
    
    try:
        # Execute the command
        result = command.execute(**vars(command_args))
        if result:
            print(f"\n🎉 Command completed: {result}")
        sys.exit(0)
    except Exception as e:
        print(f"\n💥 Command failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()