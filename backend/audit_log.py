"""
Audit Log Module
Records every chat interaction (and especially every safety interception) to a
local SQLite database for quality review and accountability — a baseline
requirement for a production medical tool.

Privacy note: user messages are stored for quality/safety review. Client IPs are
only ever stored as a short salted hash, never in plaintext. A real clinical
deployment would additionally require consent and HIPAA-grade controls.
"""

import os
import sqlite3
import hashlib
import logging
import threading
from datetime import datetime

logger = logging.getLogger(__name__)

# Per-process salt for IP hashing so stored hashes aren't trivially reversible.
_IP_SALT = os.getenv('AUDIT_IP_SALT', 'juniper-audit-salt')


class AuditLog:
    """Lightweight, thread-safe SQLite audit logger."""

    def __init__(self, db_path: str = './data/audit.db'):
        self.db_path = db_path
        self._lock = threading.Lock()
        self._init_db()
        logger.info(f"Audit log ready at {db_path}")

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
                CREATE TABLE IF NOT EXISTS interactions (
                    id               INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp        TEXT NOT NULL,
                    conversation_id  TEXT,
                    language         TEXT,
                    user_message     TEXT,
                    response_preview TEXT,
                    safety_flag      TEXT,
                    source_count     INTEGER,
                    ip_hash          TEXT
                )
                """
            )
            conn.execute(
                'CREATE INDEX IF NOT EXISTS idx_safety_flag ON interactions(safety_flag)'
            )
            conn.execute(
                'CREATE INDEX IF NOT EXISTS idx_timestamp ON interactions(timestamp)'
            )
            conn.commit()

    @staticmethod
    def _hash_ip(ip: str) -> str:
        return hashlib.sha256((_IP_SALT + ip).encode('utf-8')).hexdigest()[:16]

    def log(self, user_message: str, response: str = '', conversation_id: str = None,
            language: str = 'en', safety_flag: str = None, source_count: int = 0,
            ip: str = None):
        """Record one interaction. Never raises — logging must not break chat."""
        try:
            ip_hash = self._hash_ip(ip) if ip else None
            with self._lock, self._connect() as conn:
                conn.execute(
                    """
                    INSERT INTO interactions
                        (timestamp, conversation_id, language, user_message,
                         response_preview, safety_flag, source_count, ip_hash)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        datetime.utcnow().isoformat(),
                        conversation_id,
                        language,
                        (user_message or '')[:1000],
                        (response or '')[:500],
                        safety_flag,
                        source_count,
                        ip_hash,
                    ),
                )
                conn.commit()
            if safety_flag:
                logger.warning(f"AUDIT: safety event recorded (flag={safety_flag})")
        except Exception as e:
            logger.warning(f"Audit log write failed (non-fatal): {e}")

    def recent_safety_events(self, limit: int = 50):
        """Return recent safety interceptions (for review/reporting)."""
        try:
            with self._lock, self._connect() as conn:
                rows = conn.execute(
                    """
                    SELECT timestamp, safety_flag, language, user_message
                    FROM interactions
                    WHERE safety_flag IS NOT NULL
                    ORDER BY id DESC LIMIT ?
                    """,
                    (limit,),
                ).fetchall()
            return [
                {'timestamp': r[0], 'safety_flag': r[1], 'language': r[2], 'user_message': r[3]}
                for r in rows
            ]
        except Exception as e:
            logger.warning(f"Audit log read failed: {e}")
            return []

    def stats(self) -> dict:
        """Aggregate counts for quick reporting."""
        try:
            with self._lock, self._connect() as conn:
                total = conn.execute('SELECT COUNT(*) FROM interactions').fetchone()[0]
                safety = conn.execute(
                    'SELECT COUNT(*) FROM interactions WHERE safety_flag IS NOT NULL'
                ).fetchone()[0]
            return {'total_interactions': total, 'safety_events': safety}
        except Exception as e:
            logger.warning(f"Audit stats read failed: {e}")
            return {'total_interactions': 0, 'safety_events': 0}
