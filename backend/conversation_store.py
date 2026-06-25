"""
Conversation Store Module
Persists short-term conversation history in SQLite so it is shared across all
gunicorn workers and survives restarts.

Previously history lived in an in-process dict on the RAG engine. With multiple
workers that meant a user's follow-up could land on a worker with no memory of
the prior turn (context silently lost ~half the time), and every restart wiped
all conversations. This store fixes both by keeping history in one SQLite file
(WAL mode) that every worker reads and writes.
"""

import os
import json
import sqlite3
import logging
import threading
from datetime import datetime

logger = logging.getLogger(__name__)

# Keep only the most recent N messages (user/assistant) per conversation,
# matching the previous in-memory behaviour (10 exchanges = 20 messages).
_MAX_MESSAGES = 20


class ConversationStore:
    """Thread-safe, multi-worker-safe conversation history store."""

    def __init__(self, db_path: str = './data/conversations.db', max_messages: int = _MAX_MESSAGES):
        self.db_path = db_path
        self.max_messages = max_messages
        self._lock = threading.Lock()
        self._init_db()
        logger.info(f"Conversation store ready at {db_path}")

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path, timeout=5)
        # WAL allows concurrent readers/writer across gunicorn workers.
        conn.execute('PRAGMA journal_mode=WAL')
        return conn

    def _init_db(self):
        os.makedirs(os.path.dirname(self.db_path) or '.', exist_ok=True)
        with self._lock, self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS messages (
                    id              INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id TEXT NOT NULL,
                    role            TEXT NOT NULL,
                    content         TEXT NOT NULL,
                    created_at      TEXT NOT NULL
                )
                """
            )
            conn.execute(
                'CREATE INDEX IF NOT EXISTS idx_conv ON messages(conversation_id, id)'
            )
            conn.commit()

    def get_history(self, conversation_id: str):
        """Return the conversation's messages as [{'role','content'}, ...] (oldest first)."""
        if not conversation_id:
            return []
        try:
            with self._lock, self._connect() as conn:
                rows = conn.execute(
                    """
                    SELECT role, content FROM messages
                    WHERE conversation_id = ?
                    ORDER BY id ASC
                    """,
                    (conversation_id,),
                ).fetchall()
            return [{'role': r[0], 'content': r[1]} for r in rows]
        except Exception as e:
            logger.warning(f"Conversation history read failed (non-fatal): {e}")
            return []

    def append(self, conversation_id: str, user_message: str, assistant_message: str):
        """Append a user/assistant exchange, then trim to the most recent messages."""
        if not conversation_id:
            return
        try:
            now = datetime.utcnow().isoformat()
            with self._lock, self._connect() as conn:
                conn.execute(
                    'INSERT INTO messages (conversation_id, role, content, created_at) VALUES (?,?,?,?)',
                    (conversation_id, 'user', user_message, now),
                )
                conn.execute(
                    'INSERT INTO messages (conversation_id, role, content, created_at) VALUES (?,?,?,?)',
                    (conversation_id, 'assistant', assistant_message, now),
                )
                # Trim: keep only the newest self.max_messages rows for this conversation.
                conn.execute(
                    """
                    DELETE FROM messages
                    WHERE conversation_id = ? AND id NOT IN (
                        SELECT id FROM messages
                        WHERE conversation_id = ?
                        ORDER BY id DESC LIMIT ?
                    )
                    """,
                    (conversation_id, conversation_id, self.max_messages),
                )
                conn.commit()
        except Exception as e:
            logger.warning(f"Conversation append failed (non-fatal): {e}")

    def clear(self, conversation_id: str):
        """Delete all messages for a conversation."""
        if not conversation_id:
            return
        try:
            with self._lock, self._connect() as conn:
                conn.execute('DELETE FROM messages WHERE conversation_id = ?', (conversation_id,))
                conn.commit()
            logger.info(f"Cleared conversation: {conversation_id}")
        except Exception as e:
            logger.warning(f"Conversation clear failed (non-fatal): {e}")

    def active_count(self) -> int:
        """Number of distinct conversations currently stored."""
        try:
            with self._lock, self._connect() as conn:
                return conn.execute(
                    'SELECT COUNT(DISTINCT conversation_id) FROM messages'
                ).fetchone()[0]
        except Exception:
            return 0
