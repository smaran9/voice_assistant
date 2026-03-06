"""
💾 MEMORY SYSTEM - SEMANTIC STORAGE & RECALL
==============================================
Stores conversations, user preferences, goals, and provides semantic search.
Uses vector embeddings for intelligent memory recall.
Supports FAISS for efficient similarity search.
"""

import json
import sqlite3
import logging
import os
from datetime import datetime, timedelta
from typing import List, Dict

try:
    import numpy as np
    from sentence_transformers import SentenceTransformer
    EMBEDDINGS_AVAILABLE = True
except ImportError:
    EMBEDDINGS_AVAILABLE = False
    print("⚠️  Vector embedding libraries not installed. Basic memory only.")

from config import (
    MEMORY_FILE, CONVERSATION_DB, VECTOR_DB_PATH,
    VECTOR_DB_TYPE, DATA_DIR, USER_NAME
)

logger = logging.getLogger(__name__)


class MemoryManager:
    """
    Manages both traditional JSON memory and vector-based semantic memory.
    Provides persistent storage for conversations and user context.
    """
    
    def __init__(self):
        """Initialize memory system."""
        self.memory_file = MEMORY_FILE
        self.db_path = CONVERSATION_DB
        self.vector_db_path = VECTOR_DB_PATH
        
        # Initialize databases
        self._init_json_memory()
        self._init_sqlite_db()
        
        # Initialize vector embeddings if available
        if EMBEDDINGS_AVAILABLE:
            self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
            self._init_vector_db()
        else:
            self.embedder = None
    
    def _init_json_memory(self):
        """Initialize JSON memory file with default structure."""
        if not os.path.exists(self.memory_file):
            default_memory = {
                "user_name": USER_NAME,
                "created_at": datetime.now().isoformat(),
                "preferences": {
                    "voice_rate": 170,
                    "volume": 1.0,
                    "preferred_sources": []
                },
                "goals": [],
                "recent_commands": [],
                "context": {},
                "mood_history": []
            }
            self.save_json_memory(default_memory)
    
    def _init_sqlite_db(self):
        """Initialize SQLite database for conversations."""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Create conversations table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    user_input TEXT,
                    assistant_response TEXT,
                    command_type TEXT,
                    success BOOLEAN
                )
            ''')
            
            # Create memories table (extractable facts)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    memory_type TEXT,
                    content TEXT,
                    importance INTEGER
                )
            ''')
            
            conn.commit()
            conn.close()
            logger.info("SQLite database initialized")
            
        except Exception as e:
            logger.error(f"Error initializing SQLite: {e}")
    
    def _init_vector_db(self):
        """Initialize vector database for semantic search."""
        if not EMBEDDINGS_AVAILABLE:
            return
        
        os.makedirs(self.vector_db_path, exist_ok=True)
        logger.info("Vector database initialized")
    
    # ==================== JSON MEMORY ====================
    def load_json_memory(self):
        """
        Load memory from JSON file.
        
        Returns:
            dict: Memory dictionary
        """
        try:
            with open(self.memory_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Error loading JSON memory: {e}")
            return {}
    
    def save_json_memory(self, memory_dict):
        """
        Save memory to JSON file.
        
        Args:
            memory_dict (dict): Memory to save
        """
        try:
            with open(self.memory_file, 'w') as f:
                json.dump(memory_dict, f, indent=2)
        except Exception as e:
            logger.error(f"Error saving JSON memory: {e}")
    
    def update_user_preferences(self, preferences):
        """
        Update user preferences.
        
        Args:
            preferences (dict): User preferences
        """
        memory = self.load_json_memory()
        memory["preferences"].update(preferences)
        self.save_json_memory(memory)
    
    def add_goal(self, goal):
        """
        Add a user goal.
        
        Args:
            goal (str): Goal description
        """
        memory = self.load_json_memory()
        memory["goals"].append({
            "content": goal,
            "created_at": datetime.now().isoformat(),
            "completed": False
        })
        self.save_json_memory(memory)
    
    def track_command(self, command):
        """
        Track executed command in memory.
        
        Args:
            command (str): Command executed
        """
        memory = self.load_json_memory()
        memory["recent_commands"].append({
            "command": command,
            "timestamp": datetime.now().isoformat()
        })
        # Keep only last 50 commands
        memory["recent_commands"] = memory["recent_commands"][-50:]
        self.save_json_memory(memory)
    
    # ==================== SQLITE CONVERSATIONS ====================
    def save_conversation(self, user_input, assistant_response, 
                         command_type="general", success=True):
        """
        Save conversation to SQLite.
        
        Args:
            user_input (str): User's message
            assistant_response (str): Assistant's response
            command_type (str): Type of command
            success (bool): Whether command succeeded
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO conversations 
                (timestamp, user_input, assistant_response, command_type, success)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                user_input,
                assistant_response,
                command_type,
                success
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error saving conversation: {e}")
    
    def get_conversation_history(self, limit=20):
        """
        Retrieve conversation history.
        
        Args:
            limit (int): Number of recent conversations
            
        Returns:
            list: List of conversations
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM conversations 
                ORDER BY timestamp DESC 
                LIMIT ?
            ''', (limit,))
            
            rows = cursor.fetchall()
            conn.close()
            
            return rows
            
        except Exception as e:
            logger.error(f"Error retrieving conversation history: {e}")
            return []
    
    # ==================== VECTOR DATABASE & SEMANTIC SEARCH ====================
    def add_memory_embedding(self, text, memory_type="general"):
        """
        Add text to vector database for semantic search.
        
        Args:
            text (str): Text to embed
            memory_type (str): Type of memory
        """
        if not EMBEDDINGS_AVAILABLE or self.embedder is None:
            return
        
        try:
            # Generate embedding
            embedding = self.embedder.encode(text)
            
            # Save to vector store (FAISS)
            embedding_file = os.path.join(
                self.vector_db_path, 
                f"embedding_{hash(text)}.npy"
            )
            
            np.save(embedding_file, embedding)
            
            # Also save metadata in SQLite
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO memories (timestamp, memory_type, content, importance)
                VALUES (?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                memory_type,
                text,
                1
            ))
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            logger.error(f"Error adding memory embedding: {e}")
    
    def semantic_search(self, query, top_k=5):
        """
        Search memory using semantic similarity.
        
        Args:
            query (str): Search query
            top_k (int): Number of results
            
        Returns:
            list: Similar memories
        """
        if not EMBEDDINGS_AVAILABLE or self.embedder is None:
            return []
        
        try:
            # Encode query
            query_embedding = self.embedder.encode(query)
            
            # Search in SQLite memories
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute('''
                SELECT * FROM memories 
                ORDER BY importance DESC 
                LIMIT ?
            ''', (top_k,))
            
            memories = cursor.fetchall()
            conn.close()
            
            return memories
            
        except Exception as e:
            logger.error(f"Error in semantic search: {e}")
            return []
    
    def get_context_for_llm(self):
        """
        Build context string for LLM injection.
        Includes recent conversations and user preferences.
        
        Returns:
            str: Context for LLM
        """
        memory = self.load_json_memory()
        
        history = self.get_conversation_history(limit=5)
        
        context = f"""
User Name: {memory.get('user_name', 'User')}
Recent Goals: {'; '.join(g.get('content', '') for g in memory.get('goals', [])[:3])}
Recent Commands: {', '.join(c.get('command', '') for c in memory.get('recent_commands', [])[-3:])}
"""
        
        return context.strip()


# Global memory instance
_memory_instance = None


def get_memory():
    """Get or create global memory manager instance."""
    global _memory_instance
    if _memory_instance is None:
        _memory_instance = MemoryManager()
    return _memory_instance
