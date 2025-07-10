import sqlite3
import datetime
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class Database:
    def __init__(self, db_path: str = "bot_database.db"):
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize the database with required tables."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Users table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY,
                        username TEXT,
                        first_name TEXT,
                        last_name TEXT,
                        joined_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        last_activity TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        is_member BOOLEAN DEFAULT 0
                    )
                ''')
                
                # Feedback table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS feedback (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        username TEXT,
                        feedback_text TEXT,
                        submitted_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users (user_id)
                    )
                ''')
                
                # Bot stats table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS bot_stats (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        stat_date DATE DEFAULT CURRENT_DATE,
                        total_users INTEGER DEFAULT 0,
                        active_users_today INTEGER DEFAULT 0,
                        total_feedback INTEGER DEFAULT 0
                    )
                ''')
                
                conn.commit()
                logger.info("Database initialized successfully")
                
        except Exception as e:
            logger.error(f"Database initialization error: {e}")
    
    def add_user(self, user_id: int, username: str = None, first_name: str = None, last_name: str = None, is_member: bool = False):
        """Add or update user information."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                cursor.execute('''
                    INSERT OR REPLACE INTO users 
                    (user_id, username, first_name, last_name, joined_date, last_activity, is_member)
                    VALUES (?, ?, ?, ?, 
                            COALESCE((SELECT joined_date FROM users WHERE user_id = ?), CURRENT_TIMESTAMP),
                            CURRENT_TIMESTAMP, ?)
                ''', (user_id, username, first_name, last_name, user_id, is_member))
                
                conn.commit()
                
        except Exception as e:
            logger.error(f"Error adding user {user_id}: {e}")
    
    def update_user_activity(self, user_id: int):
        """Update user's last activity timestamp."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE users SET last_activity = CURRENT_TIMESTAMP WHERE user_id = ?
                ''', (user_id,))
                conn.commit()
                
        except Exception as e:
            logger.error(f"Error updating activity for user {user_id}: {e}")
    
    def add_feedback(self, user_id: int, username: str, feedback_text: str):
        """Add user feedback to database."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO feedback (user_id, username, feedback_text)
                    VALUES (?, ?, ?)
                ''', (user_id, username, feedback_text))
                conn.commit()
                return True
                
        except Exception as e:
            logger.error(f"Error adding feedback from user {user_id}: {e}")
            return False
    
    def get_user_stats(self) -> Dict:
        """Get comprehensive user statistics."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Total users
                cursor.execute('SELECT COUNT(*) FROM users')
                total_users = cursor.fetchone()[0]
                
                # Active users today
                cursor.execute('''
                    SELECT COUNT(*) FROM users 
                    WHERE DATE(last_activity) = DATE('now')
                ''')
                active_today = cursor.fetchone()[0]
                
                # Active users this week
                cursor.execute('''
                    SELECT COUNT(*) FROM users 
                    WHERE DATE(last_activity) >= DATE('now', '-7 days')
                ''')
                active_week = cursor.fetchone()[0]
                
                # Total feedback
                cursor.execute('SELECT COUNT(*) FROM feedback')
                total_feedback = cursor.fetchone()[0]
                
                # Members vs non-members
                cursor.execute('SELECT COUNT(*) FROM users WHERE is_member = 1')
                members = cursor.fetchone()[0]
                
                return {
                    'total_users': total_users,
                    'active_today': active_today,
                    'active_week': active_week,
                    'total_feedback': total_feedback,
                    'members': members,
                    'non_members': total_users - members
                }
                
        except Exception as e:
            logger.error(f"Error getting user stats: {e}")
            return {}
    
    def get_all_user_ids(self) -> List[int]:
        """Get all user IDs for broadcasting."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT user_id FROM users')
                return [row[0] for row in cursor.fetchall()]
                
        except Exception as e:
            logger.error(f"Error getting user IDs: {e}")
            return []
    
    def get_recent_feedback(self, limit: int = 10) -> List[Dict]:
        """Get recent feedback for admin review."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT username, feedback_text, submitted_date 
                    FROM feedback 
                    ORDER BY submitted_date DESC 
                    LIMIT ?
                ''', (limit,))
                
                feedback_list = []
                for row in cursor.fetchall():
                    feedback_list.append({
                        'username': row[0],
                        'text': row[1],
                        'date': row[2]
                    })
                
                return feedback_list
                
        except Exception as e:
            logger.error(f"Error getting recent feedback: {e}")
            return []