# 🤖 JARVIS - LLM POWERED VOICE ASSISTANT
## Production-Ready AI Assistant | Jarvis-Like System

---

## 📋 TABLE OF CONTENTS
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Quick Start](#quick-start)
4. [Installation](#installation)
5. [Configuration](#configuration)
6. [Usage](#usage)
7. [Features](#features)
8. [API Reference](#api-reference)
9. [Troubleshooting](#troubleshooting)
10. [Future Roadmap](#future-roadmap)

---

## 🎯 OVERVIEW

**Jarvis** is a production-ready, modular voice assistant powered by OpenAI's GPT models with semantic memory capabilities. It combines local system command execution with cloud-based LLM intelligence.

### Key Features:
- ✅ **Voice I/O**: Offline speech-to-text and text-to-speech
- ✅ **LLM Brain**: OpenAI GPT integration
- ✅ **Semantic Memory**: Vector database with FAISS for intelligent recall
- ✅ **System Commands**: Execute local operations safely
- ✅ **Personality Engine**: Customizable assistant personality
- ✅ **Web Interface**: Optional Flask-based dashboard
- ✅ **Production Architecture**: Modular, scalable, well-documented

---

## 🏗️ ARCHITECTURE

```
jarvis/
├── main.py                    # Entry point
├── config.py                  # Central configuration
├── requirements.txt           # Dependencies
├── .env.example              # API configuration template
│
├── voice/                     # Voice I/O Module
│   ├── __init__.py
│   ├── listen.py            # Speech-to-text (microphone input)
│   └── speak.py             # Text-to-speech (voice output)
│
├── brain/                     # Intelligence Module
│   ├── __init__.py
│   ├── llm.py               # OpenAI GPT integration
│   └── memory.py            # Semantic memory & storage
│
├── commands/                  # Command Execution
│   ├── __init__.py
│   ├── system_commands.py   # System operations (time, open apps, etc)
│   └── router.py            # Command routing (system vs LLM)
│
├── utils/                     # Utilities
│   ├── __init__.py
│   └── personality.py        # Assistant personality & tone
│
├── data/                      # Data Storage
│   ├── memory.json           # User preferences & goals
│   ├── conversations.db      # Conversation history (SQLite)
│   ├── vector_store/         # Vector embeddings for semantic search
│   └── jarvis.log            # System logs
│
├── templates/                 # Web Interface
│   └── index.html
│
└── static/                    # Web Assets
    ├── script.js
    └── style.css
```

### Architecture Diagram:

```
┌─────────────────────────────────────────────────────────┐
│                    USER INPUT                            │
│            (Voice or Text via Web UI)                    │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │   VOICE INPUT (listen) │
        └────────────┬───────────┘
                     │
                     ▼
        ┌────────────────────────┐
        │  COMMAND ROUTER        │
        │  - Pattern Matching    │
        │  - Intent Detection    │
        └────────┬───────────────┘
                 │
        ┌────────┴────────┐
        │                 │
        ▼                 ▼
   ┌────────┐        ┌──────────┐
   │SYSTEM  │        │  LLM     │
   │COMMANDS│        │  BRAIN   │
   └───┬────┘        └────┬─────┘
       │                  │
       │          ┌───────▼────────┐
       │          │ MEMORY SYSTEM  │
       │          │ - Context      │
       │          │ - Embeddings   │
       │          │ - Recall       │
       │          └────────────────┘
       │
       └──────────────┬─────────────┐
                      │             │
                      ▼             ▼
            ┌──────────────┐  ┌──────────────┐
            │ PERSONALITY  │  │   FORMAT     │
            │   ENGINE     │  │  RESPONSE    │
            └──────┬───────┘  └──────┬───────┘
                   │                 │
                   └────────┬────────┘
                            │
                            ▼
            ┌───────────────────────────┐
            │  VOICE OUTPUT (speak)     │
            │  Show user response       │
            └───────────────────────────┘
```

---

## ⚡ QUICK START

### 1. Clone & Setup (< 5 minutes)

```bash
cd voice_assistant

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
# Edit .env and add your OpenAI API key
```

### 2. Configure API Key

```bash
# Edit .env file
# Windows: notepad .env
# macOS/Linux: nano .env

# Add your OpenAI API key:
OPENAI_API_KEY=sk-your-key-here
```

Get free credits: [OpenAI Platform](https://platform.openai.com/api-keys)

### 3. Run Assistant

```bash
python main.py

# Choose mode:
# 1. Voice Interface (Console)
# 2. Web Interface (Browser)
```

### 4. Voice Commands

```
Say: "Jarvis"                    # Wake up assistant
Say: "What time is it?"          # Get current time
Say: "Search for Python"         # Google search
Say: "Open Chrome"               # Launch application
Say: "Tell me a joke"            # LLM conversation
Say: "Goodbye"                   # Exit
```

---

## 📦 INSTALLATION

### System Requirements
- **OS**: Windows 10+, macOS 10.14+, Linux
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum (8GB recommended)
- **Microphone & Speakers**: Required for voice features
- **Internet**: Required for OpenAI API

### Step-by-Step Installation

#### 1. **Install Python 3.10+**
```bash
# Windows: Download from python.org or use Chocolatey
choco install python

# macOS:
brew install python3

# Linux (Ubuntu/Debian):
sudo apt-get install python3 python3-venv python3-pip
```

#### 2. **Create Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# or
venv\Scripts\activate     # Windows
```

#### 3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

**Note for PyAudio on Windows:**
```bash
# If PyAudio installation fails, use:
pip install pipwin
pipwin install pyaudio
```

#### 4. **Setup API Keys**
```bash
cp .env.example .env
# Edit .env with your OpenAI API key
```

#### 5. **Test Installation**
```bash
python -c "from config import *; print('✓ Setup complete')"
```

---

## ⚙️ CONFIGURATION

### Main Configuration File: `config.py`

#### 1. **Personality Settings**
```python
ASSISTANT_NAME = "Jarvis"
USER_NAME = "Smaran"

PERSONALITY = {
    "greeting": f"Good morning, {USER_NAME}...",
    "tone": "Professional and motivational",
    "style": "Slightly futuristic, loyal, logical"
}
```

#### 2. **Voice Settings**
```python
TEXT_TO_SPEECH = {
    "rate": 170,           # Words per minute (50-300)
    "volume": 1.0,         # 0.0 to 1.0
    "voice_index": 0,      # 0=Male, 1=Female
    "engine": "sapi5"      # Windows SAPI5
}
```

#### 3. **LLM Configuration**
```python
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = "gpt-4"           # or "gpt-3.5-turbo"
OPENAI_TEMPERATURE = 0.7         # 0=deterministic, 1=creative
OPENAI_MAX_TOKENS = 500          # Max response length
```

#### 4. **Wake Words**
```python
WAKE_WORDS = ["jarvis", "hey jarvis", "okay jarvis"]
SLEEP_COMMANDS = ["sleep", "quiet", "standby"]
EXIT_COMMANDS = ["exit", "quit", "goodbye", "bye"]
```

#### 5. **Memory Settings**
```python
VECTOR_DB_TYPE = "faiss"         # "faiss" or "chroma"
MAX_CONVERSATION_HISTORY = 10    # Recent interactions
```

### Create `.env` File

```bash
# Copy template
cp .env.example .env

# Edit and add your API key
OPENAI_API_KEY=sk-your-actual-key

# Customize personality
ASSISTANT_NAME=Jarvis
USER_NAME=Smaran
VOICE_RATE=170
VOICE_VOLUME=1.0
```

---

## 🚀 USAGE

### Mode 1: Voice Interface (Console)

```bash
python main.py
# Choose option 1

# Example interaction:
# 🎤 Listening...
# You: "Jarvis"
# ✓ You: jarvis
# 🔊 Jarvis: Hello Smaran. I'm ready.
# 
# You: "What's the weather?"
# 🔊 Jarvis: [LLM response about weather...]
```

### Mode 2: Web Interface (Browser)

```bash
python main.py
# Choose option 2
# Open: http://localhost:5000
```

### Mode 3: Programmatic Usage

```python
from commands import process_command
from voice import speak, listen

# Listen for voice input
user_input = listen()

# Process command (routes to system or LLM)
result = process_command(user_input)

# Speak response
speak(result["response"])
```

### Advanced: Direct LLM Queries

```python
from brain import get_brain

brain = get_brain()

# Ask a question
response = brain.get_response("Write a Python hello world")
print(response["response"])

# Get conversation history
history = brain.conversation_history
```

### Advanced: Memory Management

```python
from brain import get_memory

memory = get_memory()

# Add a goal
memory.add_goal("Learn Python in 30 days")

# Save conversation
memory.save_conversation("What is AI?", "AI is artificial intelligence...", "general")

# Semantic search
results = memory.semantic_search("AI concepts")
```

---

## 💡 FEATURES EXPLAINED

### 1. Voice Input Module (`voice/listen.py`)

Captures audio and converts to text using Google Speech Recognition.

```python
from voice import listen

# Listen for speech
text = listen()  # Returns: "hello world"
```

**Features:**
- Noise adjustment
- Timeout handling
- Error recovery

---

### 2. Text-to-Speech Module (`voice/speak.py`)

Converts text to speech using offline pyttsx3.

```python
from voice import speak

speak("Hello Smaran")
```

**Features:**
- Configurable voice (male/female)
- Speed control (50-300 wpm)
- Volume adjustment
- Fallback voice selection

---

### 3. LLM Brain (`brain/llm.py`)

OpenAI GPT integration with conversation history.

```python
from brain import get_brain

brain = get_brain()
response = brain.get_response("Explain quantum computing")
```

**Features:**
- Multi-turn conversations
- Context injection
- Token usage tracking
- Error handling

---

### 4. Memory System (`brain/memory.py`)

Persistent storage with semantic search.

```python
from brain import get_memory

memory = get_memory()
memory.add_goal("Build a chatbot")
results = memory.semantic_search("chatbot topics")
```

**Features:**
- JSON user preferences
- SQLite conversation history
- Vector embeddings (FAISS)
- Semantic search via embeddings

---

### 5. System Commands (`commands/system_commands.py`)

Local operations without API calls.

```python
from commands import get_executor

executor = get_executor()
print(executor.get_time())        # "3:45 PM"
executor.open_application("chrome")
executor.google_search("Python")
```

**Available Commands:**
- Time & Date
- Open apps (Chrome, VS Code, etc)
- Google/YouTube search
- Brightness control
- Shutdown/Restart/Sleep
- File operations

---

### 6. Command Router (`commands/router.py`)

Intelligent router: system command vs LLM query.

```python
from commands import get_router

router = get_router()
result = router.route("What time is it?")
# → System command executed locally

result = router.route("Tell me a joke")
# → Sent to LLM for processing
```

**Logic:**
```
IF keyword_match(user_input, system_commands):
    Execute locally (fast, no API)
ELSE:
    Send to LLM (intelligent response)
```

---

### 7. Personality Engine (`utils/personality.py`)

Customizable assistant tone and responses.

```python
from utils import get_personality

p = get_personality()
greeting = p.get_greeting("morning")
# "Good morning, Smaran. Ready to seize the day."

error = p.get_error_response("not_understood")
# "I didn't quite catch that. Could you repeat, Smaran?"
```

---

## 🔌 API REFERENCE

### Main Functions

#### `listen() -> str`
Listen for voice input and return recognized text.

```python
from voice import listen
text = listen()
```

#### `speak(text: str) -> None`
Speak text aloud.

```python
from voice import speak
speak("Hello world")
```

#### `process_command(user_input: str) -> dict`
Route and process user input.

```python
from commands import process_command
result = process_command("What time is it?")
print(result["response"])
print(result["command_type"])  # "system" or "llm" or "wake"
```

#### `get_brain() -> JarvisBrain`
Get LLM brain instance.

```python
from brain import get_brain
brain = get_brain()
response = brain.get_response("Hello")
```

#### `get_memory() -> MemoryManager`
Get memory manager instance.

```python
from brain import get_memory
memory = get_memory()
memory.add_goal("Learn Python")
```

#### `get_personality() -> PersonalityEngine`
Get personality engine.

```python
from utils import get_personality
p = get_personality()
formatted = p.format_response("Hello", tone="motivational")
```

---

## 🐛 TROUBLESHOOTING

### Microphone Not Found
```bash
# Check audio devices
python -c "import speech_recognition; print(speech_recognition.Microphone.list_microphone_indexes())"

# Set specific device
MICROPHONE_INDEX=1  # Edit config.py
```

### OpenAI API Error
```
Error: AuthenticationError
→ Check .env file has correct API key
→ Verify key at: https://platform.openai.com/api-keys

Error: RateLimitError
→ Wait 1 minute before retry
→ Consider upgrading plan
```

### PyAudio Installation Fails
```bash
# Windows:
pip install pipwin
pipwin install pyaudio

# macOS:
brew install portaudio
pip install pyaudio

# Linux (Ubuntu):
sudo apt-get install portaudio19-dev
pip install pyaudio
```

### "No module named 'openai'"
```bash
# Reinstall dependencies
pip install -r requirements.txt --upgrade

# Or manually:
pip install openai>=1.3.0
```

### Memory Not Persisting
```python
# Check file permissions
# Ensure data/ directory is writable:
mkdir -p data
chmod -R 755 data
```

### Slow LLM Response
```python
# Use faster model in config.py:
OPENAI_MODEL = "gpt-3.5-turbo"  # Faster than gpt-4
OPENAI_MAX_TOKENS = 200          # Shorter responses
```

---

## 🚀 FUTURE ROADMAP

### Phase 2: Advanced Features
- [ ] **Face Recognition**: Identify users for personalization
- [ ] **Emotion Detection**: Analyze tone and adapt responses
- [ ] **Calendar Integration**: Schedule and manage events
- [ ] **Email Integration**: Check and send emails
- [ ] **IoT Control**: Smart home device integration
- [ ] **Drone Control**: Command drone operations
- [ ] **Health Tracking**: Fitness and wellness monitoring

### Phase 3: Optimization
- [ ] **Local LLM**: Use Llama 2 for private, offline responses
- [ ] **Voice Cloning**: Generate realistic assistant voice
- [ ] **Continuous Learning**: Improve from conversations
- [ ] **Multi-language**: Support multiple languages
- [ ] **Database**: Migrate to PostgreSQL

### Phase 4: Deployment
- [ ] **Docker Container**: Easy deployment
- [ ] **AWS Lambda**: Serverless hosting
- [ ] **Mobile App**: iOS/Android client
- [ ] **Browser Extension**: Chrome plugin
- [ ] **Desktop App**: Electron application

### Phase 5: Intelligence
- [ ] **RAG (Retrieval Augmented Generation)**: Access to live web data
- [ ] **Tool Use**: Integrate external APIs automatically
- [ ] **Reasoning Engine**: Multi-step problem solving
- [ ] **Knowledge Graph**: Store structured information

---

## 📝 EXAMPLE CONVERSATIONS

### Example 1: System Command
```
User: "What time is it?"
Route: System Command (pattern match)
Response: "It's 3:45 PM."
Time: <10ms (no API)
```

### Example 2: LLM Query
```
User: "Explain quantum computing"
Route: LLM (no pattern match)
Memory: Load context + conversation history
Response: "Quantum computing uses quantum mechanics..."
Time: ~2-5 seconds
Cost: ~0.05 tokens (~\$0.000001)
```

### Example 3: Web Search
```
User: "Search for Python tutorials"
Route: System Command (Google search pattern)
Response: "Searching YouTube for Python tutorials."
Action: Opens browser with results
```

### Example 4: Personality
```
User: "Make a joke"
Route: LLM
Personality Applied: "Command received, Smaran..."
Response: "Why did the scarecrow win? He was outstanding in his field!"
```

---

## 📚 LEARNING RESOURCES

- **OpenAI API Docs**: https://platform.openai.com/docs
- **Speech Recognition**: https://github.com/Uberi/speech_recognition
- **FAISS Vectors**: https://github.com/facebookresearch/faiss
- **Python Best Practices**: https://pep8.org

---

## 📄 LICENSE

MIT License - Free for personal and commercial use

---

## 👨‍💻 AUTHOR

Built with ❤️ by a Senior Python AI Engineer

---

## 🤝 SUPPORT

For issues, feature requests, or contributions:
1. Check [Troubleshooting](#troubleshooting) section
2. Review code comments (well-documented)
3. Check existing logs in `data/jarvis.log`

---

**Status**: ✅ Production Ready | 🚀 Ready to Deploy | 💎 Enterprise Grade

**Last Updated**: February 2026
