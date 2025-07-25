"""
Auth Manager for managing authentication and permissions.
"""

import logging
import hashlib
import secrets
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

class AuthManager:
    """
    Manages authentication and permissions.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize the Auth Manager.
        
        Args:
            config: Configuration dictionary
        """
        self.config = config or {}
        self.users = {}
        self.sessions = {}
        self.permissions = {}
        self._load_initial_users()
        logger.info("AuthManager initialized")
    
    def _load_initial_users(self) -> None:
        """Load initial users from configuration."""
        # In a real implementation, this would load users from a database
        # For demonstration, we'll use a hardcoded set of users
        
        initial_users = self.config.get("initial_users", [
            {
                "username": "admin",
                "password_hash": self._hash_password("admin123"),
                "role": "admin"
            },
            {
                "username": "user",
                "password_hash": self._hash_password("user123"),
                "role": "user"
            }
        ])
        
        for user in initial_users:
            self.users[user["username"]] = user
        
        # Set up role permissions
        self.permissions = {
            "admin": ["read", "write", "execute", "manage_users"],
            "user": ["read", "write"],
            "guest": ["read"]
        }
    
    def authenticate(self, username: str, password: str) -> Optional[str]:
        """
        Authenticate a user and return a session token.
        
        Args:
            username: Username
            password: Password
            
        Returns:
            Session token or None if authentication fails
        """
        logger.info("Authenticating user: %s", username)
        
        # Check if user exists
        if username not in self.users:
            logger.warning("Authentication failed: User %s not found", username)
            return None
        
        # Check password
        user = self.users[username]
        password_hash = self._hash_password(password)
        
        if password_hash != user["password_hash"]:
            logger.warning("Authentication failed: Invalid password for user %s", username)
            return None
        
        # Generate session token
        token = self._generate_token()
        
        # Store session
        self.sessions[token] = {
            "username": username,
            "role": user["role"],
            "created_at": self._get_timestamp()
        }
        
        logger.info("User %s authenticated successfully", username)
        return token
    
    def validate_session(self, token: str) -> bool:
        """
        Validate a session token.
        
        Args:
            token: Session token
            
        Returns:
            True if the session is valid, False otherwise
        """
        return token in self.sessions
    
    def get_user_from_token(self, token: str) -> Optional[Dict[str, Any]]:
        """
        Get user information from a session token.
        
        Args:
            token: Session token
            
        Returns:
            User information or None if the token is invalid
        """
        if token not in self.sessions:
            return None
        
        session = self.sessions[token]
        username = session["username"]
        
        if username not in self.users:
            return None
        
        return self.users[username]
    
    def check_permission(self, token: str, permission: str) -> bool:
        """
        Check if a user has a specific permission.
        
        Args:
            token: Session token
            permission: Permission to check
            
        Returns:
            True if the user has the permission, False otherwise
        """
        if token not in self.sessions:
            return False
        
        session = self.sessions[token]
        role = session["role"]
        
        if role not in self.permissions:
            return False
        
        return permission in self.permissions[role]
    
    def invalidate_session(self, token: str) -> None:
        """
        Invalidate a session token.
        
        Args:
            token: Session token
        """
        if token in self.sessions:
            username = self.sessions[token]["username"]
            del self.sessions[token]
            logger.info("Session invalidated for user %s", username)
    
    def create_user(
        self, 
        username: str, 
        password: str, 
        role: str, 
        admin_token: str
    ) -> bool:
        """
        Create a new user.
        
        Args:
            username: Username
            password: Password
            role: User role
            admin_token: Admin session token
            
        Returns:
            True if the user was created, False otherwise
        """
        # Check admin permission
        if not self.check_permission(admin_token, "manage_users"):
            logger.warning("User creation failed: Insufficient permissions")
            return False
        
        # Check if user already exists
        if username in self.users:
            logger.warning("User creation failed: User %s already exists", username)
            return False
        
        # Check if role is valid
        if role not in self.permissions:
            logger.warning("User creation failed: Invalid role %s", role)
            return False
        
        # Create user
        self.users[username] = {
            "username": username,
            "password_hash": self._hash_password(password),
            "role": role,
            "created_at": self._get_timestamp()
        }
        
        logger.info("User %s created with role %s", username, role)
        return True
    
    def update_user(
        self, 
        username: str, 
        updates: Dict[str, Any], 
        admin_token: str
    ) -> bool:
        """
        Update a user.
        
        Args:
            username: Username
            updates: Updates to apply
            admin_token: Admin session token
            
        Returns:
            True if the user was updated, False otherwise
        """
        # Check admin permission
        if not self.check_permission(admin_token, "manage_users"):
            logger.warning("User update failed: Insufficient permissions")
            return False
        
        # Check if user exists
        if username not in self.users:
            logger.warning("User update failed: User %s not found", username)
            return False
        
        # Apply updates
        user = self.users[username]
        
        for key, value in updates.items():
            if key == "password":
                user["password_hash"] = self._hash_password(value)
            elif key == "role":
                if value not in self.permissions:
                    logger.warning("User update failed: Invalid role %s", value)
                    return False
                user["role"] = value
            else:
                user[key] = value
        
        logger.info("User %s updated", username)
        return True
    
    def delete_user(self, username: str, admin_token: str) -> bool:
        """
        Delete a user.
        
        Args:
            username: Username
            admin_token: Admin session token
            
        Returns:
            True if the user was deleted, False otherwise
        """
        # Check admin permission
        if not self.check_permission(admin_token, "manage_users"):
            logger.warning("User deletion failed: Insufficient permissions")
            return False
        
        # Check if user exists
        if username not in self.users:
            logger.warning("User deletion failed: User %s not found", username)
            return False
        
        # Delete user
        del self.users[username]
        
        # Invalidate any active sessions for this user
        tokens_to_invalidate = []
        for token, session in self.sessions.items():
            if session["username"] == username:
                tokens_to_invalidate.append(token)
        
        for token in tokens_to_invalidate:
            del self.sessions[token]
        
        logger.info("User %s deleted", username)
        return True
    
    def _hash_password(self, password: str) -> str:
        """
        Hash a password.
        
        Args:
            password: Password to hash
            
        Returns:
            Password hash
        """
        # In a real implementation, this would use a proper password hashing algorithm
        # For demonstration, we'll use a simple SHA-256 hash
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _generate_token(self) -> str:
        """
        Generate a random session token.
        
        Returns:
            Session token
        """
        return secrets.token_hex(16)
    
    def _get_timestamp(self) -> str:
        """
        Get the current timestamp as a string.
        
        Returns:
            Current timestamp string
        """
        from datetime import datetime
        return datetime.now().isoformat()