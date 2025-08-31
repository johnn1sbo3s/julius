"""
Create admin user command.
"""

from datetime import datetime, timezone
from typing import Any, Optional

from app.commands.base import BaseCommand
from app.database import SessionLocal
from app.models.user import User
from app.models.enums import UserRole
from app.security import get_password_hash
from app.crud.user import get_user_by_email, _create_default_categories_and_expenses


class CreateAdminCommand(BaseCommand):
    """Command to create an admin user."""
    
    help = "Create an admin user for the system"
    
    def add_arguments(self, parser) -> None:
        """Add command arguments."""
        parser.add_argument(
            '--email',
            type=str,
            required=True,
            help='Admin user email (REQUIRED)'
        )
        parser.add_argument(
            '--name',
            type=str,
            required=True,
            help='Admin user name (REQUIRED)'
        )
        parser.add_argument(
            '--password',
            type=str,
            required=True,
            help='Admin user password (REQUIRED)'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force creation even if user exists (will upgrade to admin)'
        )
    
    def handle(self, *args: Any, **kwargs: Any) -> Optional[str]:
        """Handle the command execution."""
        email = kwargs.get('email')
        name = kwargs.get('name')
        password = kwargs.get('password')
        force = kwargs.get('force', False)
        
        # Validate that all required fields are present
        if not email or not name or not password:
            self.print_error("All fields are required: --email, --name, and --password")
            return "Missing required parameters"
        
        self.print_info(f"Creating admin user: {name} <{email}>")
        
        db = SessionLocal()
        
        try:
            # Check if admin user already exists
            existing_user = get_user_by_email(db, email)
            if existing_user:
                if not force:
                    if existing_user.is_admin():
                        self.print_warning(f"Admin user with email {email} already exists!")
                        self.print_info("Use --force to upgrade user or change role")
                        return f"Admin user already exists: {email}"
                    else:
                        self.print_warning(f"User with email {email} exists but is not admin!")
                        self.print_info("Use --force to upgrade to admin role")
                        return f"User exists but not admin: {email}"
                else:
                    # Force upgrade to admin
                    existing_user.role = UserRole.ADMIN
                    existing_user.is_active = True
                    existing_user.password_hash = get_password_hash(password)
                    db.commit()
                    db.refresh(existing_user)
                    self.print_success(f"Upgraded existing user {email} to admin role")
                    self.print_info("Password updated")
                    return f"User upgraded to admin: {email}"
            
            # Create new admin user
            password_hash = get_password_hash(password)
            
            # Create admin user
            admin_user = User(
                name=name,
                email=email,
                password_hash=password_hash,
                role=UserRole.ADMIN,
                is_active=True,
                created_at=datetime.now(timezone.utc)
            )
            
            db.add(admin_user)
            db.commit()
            db.refresh(admin_user)
            
            # Create default categories and expenses for the admin user
            _create_default_categories_and_expenses(db, admin_user.id)
            
            self.print_success("Admin user created successfully!")
            self.print_info(f"Email: {email}")
            self.print_info(f"Name: {name}")
            self.print_info(f"Role: {admin_user.role}")
            self.print_info(f"Password: {password}")
            
            return f"Admin user created: {email}"
            
        except Exception as e:
            db.rollback()
            self.print_error(f"Failed to create admin user: {e}")
            raise
        finally:
            db.close()