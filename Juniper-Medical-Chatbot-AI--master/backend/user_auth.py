"""
User Authentication Module
Handles user registration, login, and session management
"""

import sqlite3
import hashlib
import secrets
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class UserAuth:
    """
    User authentication service with SQLite backend
    """

    def __init__(self, db_path: str = "./data/users.db"):
        """
        Initialize user authentication service

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.init_database()
        logger.info(f"User authentication initialized with database: {db_path}")

    def init_database(self):
        """Initialize database tables"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Users table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                username TEXT NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        ''')

        # Sessions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS sessions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                session_token TEXT UNIQUE NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                expires_at TIMESTAMP NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

        # User conversations table (for cloud sync)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS user_conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                conversation_id TEXT NOT NULL,
                conversation_data TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')

        conn.commit()
        conn.close()
        logger.info("Database tables initialized")

    def hash_password(self, password: str) -> str:
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def generate_session_token(self) -> str:
        """Generate a secure session token"""
        return secrets.token_urlsafe(32)

    def register_user(self, email: str, username: str, password: str) -> Dict[str, Any]:
        """
        Register a new user

        Args:
            email: User's email
            username: User's username
            password: User's password

        Returns:
            Dictionary with success status and message
        """
        try:
            # Validate inputs
            if not email or not username or not password:
                return {'success': False, 'message': 'All fields are required'}

            if len(password) < 6:
                return {'success': False, 'message': 'Password must be at least 6 characters'}

            # Hash password
            password_hash = self.hash_password(password)

            # Insert user
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                INSERT INTO users (email, username, password_hash)
                VALUES (?, ?, ?)
            ''', (email.lower(), username, password_hash))

            conn.commit()
            user_id = cursor.lastrowid
            conn.close()

            logger.info(f"User registered successfully: {email}")
            return {
                'success': True,
                'message': 'Registration successful',
                'user_id': user_id
            }

        except sqlite3.IntegrityError:
            return {'success': False, 'message': 'Email already exists'}
        except Exception as e:
            logger.error(f"Registration error: {e}")
            return {'success': False, 'message': 'Registration failed'}

    def login_user(self, email: str, password: str) -> Dict[str, Any]:
        """
        Login user and create session

        Args:
            email: User's email
            password: User's password

        Returns:
            Dictionary with session token and user info
        """
        try:
            password_hash = self.hash_password(password)

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            # Check credentials
            cursor.execute('''
                SELECT id, username, email
                FROM users
                WHERE email = ? AND password_hash = ?
            ''', (email.lower(), password_hash))

            user = cursor.fetchone()

            if not user:
                conn.close()
                return {'success': False, 'message': 'Invalid email or password'}

            user_id, username, email = user

            # Create session
            session_token = self.generate_session_token()
            expires_at = datetime.now() + timedelta(days=30)

            cursor.execute('''
                INSERT INTO sessions (user_id, session_token, expires_at)
                VALUES (?, ?, ?)
            ''', (user_id, session_token, expires_at))

            # Update last login
            cursor.execute('''
                UPDATE users SET last_login = CURRENT_TIMESTAMP
                WHERE id = ?
            ''', (user_id,))

            conn.commit()
            conn.close()

            logger.info(f"User logged in: {email}")
            return {
                'success': True,
                'message': 'Login successful',
                'session_token': session_token,
                'user': {
                    'id': user_id,
                    'username': username,
                    'email': email
                }
            }

        except Exception as e:
            logger.error(f"Login error: {e}")
            return {'success': False, 'message': 'Login failed'}

    def validate_session(self, session_token: str) -> Optional[Dict[str, Any]]:
        """
        Validate session token

        Args:
            session_token: Session token to validate

        Returns:
            User info if valid, None otherwise
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('''
                SELECT u.id, u.username, u.email, s.expires_at
                FROM sessions s
                JOIN users u ON s.user_id = u.id
                WHERE s.session_token = ?
            ''', (session_token,))

            result = cursor.fetchone()
            conn.close()

            if not result:
                return None

            user_id, username, email, expires_at = result
            expires_at = datetime.fromisoformat(expires_at)

            # Check if session expired
            if datetime.now() > expires_at:
                self.logout_user(session_token)
                return None

            return {
                'id': user_id,
                'username': username,
                'email': email
            }

        except Exception as e:
            logger.error(f"Session validation error: {e}")
            return None

    def logout_user(self, session_token: str) -> bool:
        """
        Logout user by deleting session

        Args:
            session_token: Session token to delete

        Returns:
            True if successful
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            cursor.execute('DELETE FROM sessions WHERE session_token = ?', (session_token,))

            conn.commit()
            conn.close()

            logger.info("User logged out")
            return True

        except Exception as e:
            logger.error(f"Logout error: {e}")
            return False
