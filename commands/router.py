"""
🚦 COMMAND ROUTER
==================
Intelligent router that decides whether to execute system commands
or send to LLM for processing.
Hybrid architecture for optimal performance.
"""

import logging
import re
from typing import Dict, Tuple

from config import (
    SYSTEM_COMMANDS, WAKE_WORDS, SLEEP_COMMANDS, EXIT_COMMANDS,
    ERROR_MESSAGES
)
from commands.system_commands import get_executor
from brain.llm import get_brain
from brain.memory import get_memory
from utils.personality import get_personality

logger = logging.getLogger(__name__)


class CommandRouter:
    """
    Routes user input to appropriate handler:
    - Local system commands
    - LLM queries
    - Special commands (wake, sleep, exit)
    """
    
    def __init__(self):
        """Initialize router with command patterns."""
        self.executor = get_executor()
        self.brain = get_brain()
        self.memory = get_memory()
        self.personality = get_personality()
        
        # Pattern matching for quick command detection
        self.system_patterns = {
            "time": r"\b(what time|what\'s the time|current time|tell me the time)\b",
            "date": r"\b(what date|what\'s the date|today\'s date|current date|what day)\b",
            "weather": r"\bweather\b",
            "open": r"\b(open|launch|start)\s+(\w+)",
            "google": r"\b(google|search for|search)\s+(.+)",
            "youtube": r"\b(youtube|video)\s+(.+)",
            "brightness": r"\b(brightness|bright)\b",
            "shutdown": r"\b(shutdown|power off|turn off)\b",
            "restart": r"\brestart\b",
            "sleep": r"\b(sleep|rest)\b",
        }
    
    def route(self, user_input: str) -> Dict:
        """
        Route user input to appropriate handler.
        
        Args:
            user_input (str): User's command or query
            
        Returns:
            dict: {
                "response": str,
                "command_type": str,
                "success": bool
            }
        """
        if not user_input or not isinstance(user_input, str):
            return {
                "response": ERROR_MESSAGES["no_recognition"],
                "command_type": "error",
                "success": False
            }
        
        user_input = user_input.lower().strip()
        
        # ==== 1. Check for special commands ====
        special_result = self._check_special_commands(user_input)
        if special_result:
            return special_result
        
        # ==== 2. Check for system commands ====
        system_result = self._check_system_commands(user_input)
        if system_result:
            self.memory.save_conversation(
                user_input,
                system_result["response"],
                "system_command",
                True
            )
            return system_result
        
        # ==== 3. Send to LLM for conversation ====
        llm_result = self._route_to_llm(user_input)
        
        self.memory.save_conversation(
            user_input,
            llm_result["response"],
            "llm_query",
            llm_result["success"]
        )
        
        # Track command in memory
        self.memory.track_command(user_input)
        
        return llm_result
    
    def _check_special_commands(self, user_input: str):
        """
        Check for wake, sleep, exit commands.
        
        Args:
            user_input (str): User input
            
        Returns:
            dict or None: Response if special command found
        """
        # Wake word detection
        if any(wake_word in user_input for wake_word in WAKE_WORDS):
            return {
                "response": self.personality.format_wake_response(),
                "command_type": "wake",
                "success": True
            }
        
        # Sleep command
        if any(cmd in user_input for cmd in SLEEP_COMMANDS):
            return {
                "response": self.personality.format_sleep_response(),
                "command_type": "sleep",
                "success": True
            }
        
        # Exit command
        if any(cmd in user_input for cmd in EXIT_COMMANDS):
            return {
                "response": self.personality.get_closing(),
                "command_type": "exit",
                "success": True
            }
        
        return None
    
    def _check_system_commands(self, user_input: str):
        """
        Check if input matches system command patterns.
        
        Args:
            user_input (str): User input
            
        Returns:
            dict or None: Result if system command matched
        """
        # Time check
        if re.search(self.system_patterns["time"], user_input):
            return {
                "response": f"It's {self.executor.get_time()}.",
                "command_type": "system",
                "success": True
            }
        
        # Date check
        if re.search(self.system_patterns["date"], user_input):
            return {
                "response": self.executor.get_date(),
                "command_type": "system",
                "success": True
            }
        
        # Open application
        open_match = re.search(self.system_patterns["open"], user_input)
        if open_match:
            app_name = open_match.group(2)
            response = self.executor.open_application(app_name)
            return {
                "response": response,
                "command_type": "system",
                "success": True
            }
        
        # Google search
        google_match = re.search(self.system_patterns["google"], user_input)
        if google_match:
            query = google_match.group(2)
            response = self.executor.google_search(query)
            return {
                "response": response,
                "command_type": "system",
                "success": True
            }
        
        # YouTube search
        youtube_match = re.search(self.system_patterns["youtube"], user_input)
        if youtube_match:
            query = youtube_match.group(2)
            response = self.executor.youtube_search(query)
            return {
                "response": response,
                "command_type": "system",
                "success": True
            }
        
        # Brightness
        if re.search(self.system_patterns["brightness"], user_input):
            if "increase" in user_input or "brighter" in user_input:
                response = self.executor.increase_brightness()
            elif "decrease" in user_input or "darker" in user_input:
                response = self.executor.decrease_brightness()
            else:
                response = self.executor.set_brightness(50)
            
            return {
                "response": response,
                "command_type": "system",
                "success": True
            }
        
        # Shutdown
        if re.search(self.system_patterns["shutdown"], user_input):
            return {
                "response": self.executor.shutdown_system(),
                "command_type": "system",
                "success": True
            }
        
        # Restart
        if re.search(self.system_patterns["restart"], user_input):
            return {
                "response": self.executor.restart_system(),
                "command_type": "system",
                "success": True
            }
        
        return None
    
    def _route_to_llm(self, user_input: str):
        """
        Send input to LLM for processing.
        
        Args:
            user_input (str): User input
            
        Returns:
            dict: LLM response and metadata
        """
        try:
            # Get relevant context from memory
            context = self.memory.get_context_for_llm()
            
            # Build prompt with context
            enhanced_input = f"{context}\n\nUser: {user_input}"
            
            # Get LLM response
            llm_result = self.brain.get_response(enhanced_input)
            
            # Format with personality
            response = self.personality.add_personality_to_llm_response(
                llm_result["response"]
            )
            
            return {
                "response": response,
                "command_type": "llm",
                "success": llm_result["success"],
                "tokens": llm_result.get("tokens_used", 0)
            }
            
        except Exception as e:
            logger.error(f"Error routing to LLM: {e}")
            return {
                "response": ERROR_MESSAGES["api_failure"],
                "command_type": "error",
                "success": False
            }


# Global router instance
_router_instance = None


def get_router():
    """Get or create global router instance."""
    global _router_instance
    if _router_instance is None:
        _router_instance = CommandRouter()
    return _router_instance


def process_command(user_input: str):
    """
    Process user input and return response.
    
    Args:
        user_input (str): User's input
        
    Returns:
        dict or str: Response from router
    """
    router = get_router()
    return router.route(user_input)
