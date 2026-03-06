"""
⚙️  JARVIS CONFIGURATION
========================
Central configuration for all assistant parameters.
Customizable personality, API keys, and behavior settings.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# ============================================
# ASSISTANT IDENTITY & PERSONALITY
# ============================================
ASSISTANT_NAME = "Mitra"
USER_NAME = "Smaran"

PERSONALITY = {
    "greeting": f"Good morning, {USER_NAME}. Ready to assist.",
    "tone": "Professional and motivational",
    "style": "Helpful, friendly, and intelligent",
    "prefix": "Command received",
    "closing": "Always here to help."
}

# ============================================
# API CONFIGURATION
# ============================================
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your-api-key-here")
OPENAI_MODEL = "gpt-4"  # or "gpt-3.5-turbo" for faster responses
OPENAI_TEMPERATURE = 0.7  # Balance between creativity (1.0) and consistency (0)
OPENAI_MAX_TOKENS = 500

# ============================================
# VOICE SETTINGS
# ============================================
MICROPHONE_SETTINGS = {
    "energy_threshold": 4000,  # Adjust based on ambient noise
    "pause_threshold": 0.8,    # Seconds of silence to detect speech end
    "phrase_time_limit": 10    # Max seconds per recognition
}

TEXT_TO_SPEECH = {
    "rate": 170,           # Speech rate (words per minute)
    "volume": 1.0,         # 0.0 to 1.0
    "voice_index": 0,      # 0 = Male (preferred), 1 = Female
    "engine": "sapi5"      # Windows SAPI5, macOS: nsss, Linux: espeak
}

# ============================================
# WAKE WORD & VOICE COMMANDS
# ============================================
WAKE_WORDS = ["mitra", "hey mitra", "okay mitra"]
SLEEP_COMMANDS = ["sleep", "quiet", "standby"]
EXIT_COMMANDS = ["exit", "quit", "goodbye", "bye", "shutdown"]

# ============================================
# MEMORY & DATABASE
# ============================================
DATA_DIR = "data"
MEMORY_FILE = os.path.join(DATA_DIR, "memory.json")
CONVERSATION_DB = os.path.join(DATA_DIR, "conversations.db")
VECTOR_DB_PATH = os.path.join(DATA_DIR, "vector_store")
BRAIN_FILE = os.path.join(DATA_DIR, "brain.json")

# Vector database backend: "faiss" or "chroma"
VECTOR_DB_TYPE = "faiss"
EMBEDDING_DIMENSION = 1536  # OpenAI embeddings dimension

# ============================================
# SYSTEM COMMANDS WHITELIST
# ============================================
SYSTEM_COMMANDS = {
    "chrome": "chrome",
    "vscode": "code",
    "notepad": "notepad",
    "youtube": "https://youtube.com",
    "spotify": "spotify",
    "gmail": "https://gmail.com",
    "github": "https://github.com",
}

# ============================================
# LOGGING
# ============================================
LOG_LEVEL = "INFO"  # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FILE = os.path.join(DATA_DIR, "jarvis.log")

# ============================================
# CONVERSATION CONTEXT
# ============================================
MAX_CONVERSATION_HISTORY = 10  # Keep last N interactions in context
CONTEXT_INJECTION_PROMPT = f"""
You are {ASSISTANT_NAME}, a professional AI assistant. 
You're speaking to {USER_NAME}.
Your personality: {PERSONALITY['style']}.
Keep responses concise (2-3 sentences max for voice).
Be helpful, logical, and slightly futuristic in tone.
"""

# ============================================
# FUTURE INTEGRATIONS (HOOKS)
# ============================================
FUTURE_FEATURES = {
    "face_recognition": False,
    "home_automation": False,
    "drone_control": False,
    "iot_integration": False,
    "calendar_sync": False,
    "email_integration": False,
    "health_tracking": False,
}

# ============================================
# ERROR MESSAGES
# ============================================
ERROR_MESSAGES = {
    "mic_not_found": "Microphone not detected. Please check your audio settings.",
    "api_failure": "Unable to reach OpenAI API. Falling back to local commands.",
    "no_recognition": "I didn't catch that. Please repeat.",
    "unknown_command": "I'm not sure how to help with that.",
    "permission_denied": "I don't have permission to execute that command.",
}

# ============================================
# HELPER: Create data directory
# ============================================
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)
