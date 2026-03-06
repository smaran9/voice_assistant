"""
⚙️  SYSTEM COMMANDS MODULE
===========================
Executes system-level tasks like opening applications, getting time/date,
controlling system settings, etc.
"""

import os
import subprocess
import webbrowser
import logging
from datetime import datetime
import json

try:
    import screen_brightness_control as sbc
    BRIGHTNESS_AVAILABLE = True
except ImportError:
    BRIGHTNESS_AVAILABLE = False

try:
    import pyautogui
    PYAUTOGUI_AVAILABLE = True
except ImportError:
    PYAUTOGUI_AVAILABLE = False

from config import SYSTEM_COMMANDS, USER_NAME, ASSISTANT_NAME

logger = logging.getLogger(__name__)


class SystemCommandExecutor:
    """
    Executes local system commands safely.
    Includes application launching, system control, and utilities.
    """
    
    def __init__(self):
        """Initialize system command executor."""
        self.available_apps = SYSTEM_COMMANDS
        self.running_sessions = []
    
    # ==================== APPLICATION LAUNCHING ====================
    def open_application(self, app_name):
        """
        Open an application by name.
        
        Args:
            app_name (str): Name of application (chrome, vscode, etc)
            
        Returns:
            str: Status message
        """
        app_name = app_name.lower().strip()
        
        if app_name not in self.available_apps:
            return f"Application '{app_name}' not found in safe list."
        
        try:
            command = self.available_apps[app_name]
            
            # Check if it's a URL
            if command.startswith("http"):
                webbrowser.open(command)
                return f"Opening {app_name} in browser."
            else:
                # Open as executable
                subprocess.Popen(command)
                return f"Opening {app_name}."
            
        except Exception as e:
            logger.error(f"Error opening {app_name}: {e}")
            return f"Failed to open {app_name}."
    
    # ==================== TIME & DATE ====================
    def get_time(self):
        """
        Get current time.
        
        Returns:
            str: Current time
        """
        return datetime.now().strftime("%I:%M %p")
    
    def get_date(self):
        """
        Get current date.
        
        Returns:
            str: Current date
        """
        return datetime.now().strftime("%A, %B %d, %Y")
    
    def get_day_of_week(self):
        """
        Get day of the week.
        
        Returns:
            str: Day name
        """
        return datetime.now().strftime("%A")
    
    # ==================== SYSTEM CONTROL ====================
    def shutdown_system(self):
        """
        Shutdown the computer.
        
        Returns:
            str: Status message
        """
        try:
            os.system("shutdown /s /t 60")
            return "Shutting down in 60 seconds."
        except Exception as e:
            logger.error(f"Shutdown error: {e}")
            return "Unable to execute shutdown."
    
    def restart_system(self):
        """
        Restart the computer.
        
        Returns:
            str: Status message
        """
        try:
            os.system("shutdown /r /t 60")
            return "Restarting in 60 seconds."
        except Exception as e:
            logger.error(f"Restart error: {e}")
            return "Unable to execute restart."
    
    def sleep_system(self):
        """
        Put system to sleep.
        
        Returns:
            str: Status message
        """
        try:
            os.system("rundll32.exe powrprof.dll,SetSuspendState 0,1,0")
            return "Going to sleep."
        except Exception as e:
            logger.error(f"Sleep error: {e}")
            return "Unable to sleep."
    
    # ==================== BRIGHTNESS CONTROL ====================
    def set_brightness(self, level):
        """
        Set screen brightness (0-100).
        
        Args:
            level (int): Brightness level
            
        Returns:
            str: Status message
        """
        if not BRIGHTNESS_AVAILABLE:
            return "Brightness control not available."
        
        try:
            level = max(0, min(100, int(level)))
            sbc.set_brightness(level)
            return f"Brightness set to {level} percent."
        except Exception as e:
            logger.error(f"Brightness error: {e}")
            return "Unable to control brightness."
    
    def increase_brightness(self, amount=10):
        """Increase brightness."""
        if not BRIGHTNESS_AVAILABLE:
            return "Brightness control not available."
        
        try:
            current = sbc.get_brightness()[0]
            new_level = min(100, current + amount)
            sbc.set_brightness(new_level)
            return f"Brightness increased to {new_level} percent."
        except Exception as e:
            logger.error(f"Error increasing brightness: {e}")
            return "Unable to adjust brightness."
    
    def decrease_brightness(self, amount=10):
        """Decrease brightness."""
        if not BRIGHTNESS_AVAILABLE:
            return "Brightness control not available."
        
        try:
            current = sbc.get_brightness()[0]
            new_level = max(0, current - amount)
            sbc.set_brightness(new_level)
            return f"Brightness decreased to {new_level} percent."
        except Exception as e:
            logger.error(f"Error decreasing brightness: {e}")
            return "Unable to adjust brightness."
    
    # ==================== FILE OPERATIONS ====================
    def open_file(self, file_path):
        """
        Open a file with default application.
        
        Args:
            file_path (str): Path to file
            
        Returns:
            str: Status message
        """
        try:
            if os.path.exists(file_path):
                os.startfile(file_path)
                return f"Opening {file_path}."
            else:
                return f"File not found: {file_path}"
        except Exception as e:
            logger.error(f"Error opening file: {e}")
            return "Unable to open file."
    
    def open_folder(self, folder_path):
        """
        Open a folder in file explorer.
        
        Args:
            folder_path (str): Path to folder
            
        Returns:
            str: Status message
        """
        try:
            if os.path.exists(folder_path):
                os.startfile(folder_path)
                return f"Opening {folder_path}."
            else:
                return f"Folder not found: {folder_path}"
        except Exception as e:
            logger.error(f"Error opening folder: {e}")
            return "Unable to open folder."
    
    # ==================== WEB SEARCH ====================
    def google_search(self, query):
        """
        Perform Google search.
        
        Args:
            query (str): Search query
            
        Returns:
            str: Status message
        """
        try:
            url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(url)
            return f"Searching for {query}."
        except Exception as e:
            logger.error(f"Search error: {e}")
            return "Unable to perform search."
    
    def youtube_search(self, query):
        """
        Search YouTube.
        
        Args:
            query (str): Search query
            
        Returns:
            str: Status message
        """
        try:
            url = f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}"
            webbrowser.open(url)
            return f"Searching YouTube for {query}."
        except Exception as e:
            logger.error(f"YouTube search error: {e}")
            return "Unable to search YouTube."
    
    # ==================== UTILITY ====================
    def get_system_info(self):
        """
        Get basic system information.
        
        Returns:
            str: System info
        """
        try:
            import platform
            system = platform.system()
            version = platform.version()
            return f"Running {system} {version}."
        except:
            return "System information unavailable."
    
    def execute_command(self, command):
        """
        Execute a safe system command.
        
        Args:
            command (str): Command to execute
            
        Returns:
            str: Command output
        """
        try:
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.stdout.strip() if result.stdout else "Command executed."
        except subprocess.TimeoutExpired:
            return "Command execution timeout."
        except Exception as e:
            logger.error(f"Command execution error: {e}")
            return "Unable to execute command."


# Global executor instance
_executor_instance = None


def get_executor():
    """Get or create global executor instance."""
    global _executor_instance
    if _executor_instance is None:
        _executor_instance = SystemCommandExecutor()
    return _executor_instance


def execute_system_command(command_name, **kwargs):
    """
    Simple function to execute system commands.
    
    Args:
        command_name (str): Name of command
        **kwargs: Additional arguments
        
    Returns:
        str: Result message
    """
    executor = get_executor()
    
    # Map command names to methods
    commands = {
        "time": executor.get_time,
        "date": executor.get_date,
        "day": executor.get_day_of_week,
        "open_app": lambda: executor.open_application(kwargs.get("app")),
        "shutdown": executor.shutdown_system,
        "restart": executor.restart_system,
        "sleep": executor.sleep_system,
        "brightness": lambda: executor.set_brightness(kwargs.get("level", 50)),
        "google": lambda: executor.google_search(kwargs.get("query", "")),
        "youtube": lambda: executor.youtube_search(kwargs.get("query", "")),
    }
    
    if command_name in commands:
        return commands[command_name]()
    
    return "Command not found."
