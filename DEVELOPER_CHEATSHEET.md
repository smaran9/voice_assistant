# 🎯 JARVIS - DEVELOPER CHEAT SHEET

Quick reference for developing and extending Jarvis.

---

## ⚡ QUICK COMMANDS

```bash
# Setup (one time)
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
cp .env.example .env
# Edit .env → Add OPENAI_API_KEY

# Run
python main.py

# View logs
data/jarvis.log

# Add new command
# 1. Add pattern to router.py
# 2. Implement in system_commands.py
# 3. Add to config.py if needed
```

---

## 📂 FILE LOCATIONS

| What | Where |
|-----|-------|
| Main app | `main.py` |
| Config | `config.py` |
| Voice | `voice/listen.py`, `voice/speak.py` |
| LLM | `brain/llm.py` |
| Memory | `brain/memory.py` |
| Commands | `commands/router.py`, `commands/system_commands.py` |
| Personality | `utils/personality.py` |
| Data | `data/memory.json`, `data/conversations.db` |
| Logs | `data/jarvis.log` |
| Docs | `README.md`, `QUICK_START.md`, `ARCHITECTURE.md` |

---

## 🔧 IMPORT STATEMENTS

```python
# Voice
from voice import listen, speak

# LLM Brain
from brain import get_brain, get_memory

# Commands
from commands import process_command, get_router, get_executor

# Utils
from utils import get_personality

# Config
from config import ASSISTANT_NAME, USER_NAME, OPENAI_API_KEY
```

---

## 🎤 VOICE EXAMPLE

```python
from voice import listen, speak

# Listen for voice input
user_input = listen()  # "hello"

# Speak response
speak("Hello Smaran!")
```

---

## 🧠 LLM EXAMPLE

```python
from brain import get_brain

brain = get_brain()

# Ask question
response = brain.get_response("Explain Python")
print(response["response"])  # "Python is..."

# Check conversation history
print(brain.conversation_history)
```

---

## 💾 MEMORY EXAMPLE

```python
from brain import get_memory

memory = get_memory()

# Add goal
memory.add_goal("Learn Python in 30 days")

# Save conversation
memory.save_conversation(
    user_input="What is AI?",
    assistant_response="AI is...",
    command_type="general",
    success=True
)

# Semantic search
results = memory.semantic_search("Python learning")
```

---

## ⚙️ SYSTEM COMMANDS EXAMPLE

```python
from commands import get_executor

executor = get_executor()

# Get time
print(executor.get_time())  # "3:45 PM"

# Get date
print(executor.get_date())  # "Monday, February 26, 2026"

# Open application
executor.open_application("chrome")

# Google search
executor.google_search("Python tutorials")

# Control brightness
executor.set_brightness(75)  # 0-100
executor.increase_brightness()
executor.decrease_brightness()

# Web search
executor.youtube_search("machine learning")

# System control
executor.shutdown_system()
executor.restart_system()
executor.sleep_system()
```

---

## 🎭 PERSONALITY EXAMPLE

```python
from utils import get_personality

p = get_personality()

# Get greeting
greeting = p.get_greeting("morning")

# Format response
formatted = p.format_response("Hello", tone="motivational")

# Get error message
error = p.get_error_response("not_understood")

# Get closing
closing = p.get_closing()
```

---

## 🚦 ROUTER EXAMPLE

```python
from commands import get_router

router = get_router()

# Process any input - router decides:
# System command or LLM
result = router.route("What time is it?")

print(result["response"])        # "It's 3:45 PM"
print(result["command_type"])    # "system"
print(result["success"])         # True
```

---

## 📝 CONFIG CUSTOMIZATION

```python
# In config.py

# Change personality
ASSISTANT_NAME = "Jarvis"
USER_NAME = "Smaran"

# Change voice
TEXT_TO_SPEECH = {
    "rate": 170,          # Slower: 50, Faster: 300
    "volume": 1.0,        # 0.0 to 1.0
    "voice_index": 0,     # 0=Male, 1=Female
}

# Change LLM model
OPENAI_MODEL = "gpt-3.5-turbo"  # Faster, cheaper

# Add wake words
WAKE_WORDS = ["jarvis", "hey jarvis", "okay jarvis"]

# Adjust microphone sensitivity
MICROPHONE_SETTINGS = {
    "energy_threshold": 4000,      # Higher = less sensitive
    "pause_threshold": 0.8,
    "phrase_time_limit": 10
}
```

---

## 🐛 DEBUGGING

```python
# Enable detailed logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Check logs
tail -f data/jarvis.log  # Unix
type data\jarvis.log     # Windows

# Test individual modules
python -c "from voice import listen; print(listen())"
python -c "from config import *; print(ASSISTANT_NAME)"
python -c "from brain import get_brain; brain = get_brain(); print(brain.get_response('test'))"
```

---

## 🔌 ADD NEW SYSTEM COMMAND

### Step 1: Add pattern to router.py
```python
self.system_patterns["mycommand"] = r"\bmy pattern\b"
```

### Step 2: Implement in system_commands.py
```python
def my_command(self, arg):
    """Do something"""
    result = ... # implementation
    return f"Result: {result}"
```

### Step 3: Handle in router.py _check_system_commands()
```python
mycommand_match = re.search(self.system_patterns["mycommand"], user_input)
if mycommand_match:
    response = self.executor.my_command()
    return {...}
```

---

## 🚀 ADD NEW LLM CAPABILITY

```python
from brain import get_brain

brain = get_brain()

# Create specialized method
def ask_coding_question(question):
    prompt = f"As a Python expert, answer: {question}"
    response = brain.get_response(prompt)
    return response["response"]

# Use it
answer = ask_coding_question("How do I read a file?")
```

---

## 🌟 ADD PERSONALITY TRAIT

```python
# In personality.py

def get_motivational_phrase(self):
    """Add motivation to response"""
    phrases = [
        "You've got this!",
        "That's brilliant!",
        "Smart thinking!",
    ]
    return random.choice(phrases)

# Use in response formatting
def format_response(self, text):
    if random.random() > 0.5:
        return text + " " + self.get_motivational_phrase()
    return text
```

---

## 📊 PROJECT STRUCTURE REFERENCE

```
voice_assistant/
├── main.py              👈 Entry point
├── config.py            👈 Settings hub
├── requirements.txt     👈 Dependencies
├── .env.example         👈 API template
│
├── voice/               Input/Output
│   ├── listen.py       Speech→Text
│   └── speak.py        Text→Speech
│
├── brain/               LLM + Memory
│   ├── llm.py          OpenAI integration
│   └── memory.py       Storage & retrieval
│
├── commands/            Command handling
│   ├── router.py       Smart routing
│   └── system_commands.py  Local operations
│
├── utils/               Helpers
│   └── personality.py  Response styling
│
└── data/                Persistent data
    ├── memory.json
    ├── conversations.db
    └── vector_store/
```

---

## 🎓 COMMON PATTERNS

### Singleton Pattern (Global Instance)
```python
_instance = None

def get_module():
    global _instance
    if _instance is None:
        _instance = MyClass()
    return _instance
```

### Error Handling Pattern
```python
try:
    # Do something
except SpecificError as e:
    logger.error(f"Error: {e}")
    return {"success": False, "response": ERROR_MESSAGE}
except Exception as e:
    logger.critical(f"Critical: {e}")
    return {"success": False, "response": "Unexpected error"}
```

### Response Dict Pattern
```python
result = {
    "response": "Answer text",
    "command_type": "system|llm|wake|sleep|error",
    "success": True|False,
    "tokens_used": 123  # Optional
}
```

---

## ⚡ PERFORMANCE TIPS

```python
# ❌ Slow: Create new instance each time
engine = pyttsx3.init()
engine.say("Hello")

# ✅ Fast: Use singleton
engine = get_voice_engine()
engine.speak("Hello")

# ❌ Slow: Full context for every query
context = load_all_history()
response = llm.generate(context + query)

# ✅ Fast: Limit context
recent = get_last_5_messages()
response = llm.generate(recent + query)

# ❌ Slow: Wait for LLM for common queries
response = llm.generate("What time is it?")

# ✅ Fast: Route to system
if is_system_command(query):
    response = system.execute(query)
else:
    response = llm.generate(query)
```

---

## 🔒 SECURITY CHECKLIST

```python
# ✅ Use environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Good

# ❌ Don't hardcode secrets
OPENAI_API_KEY = "sk-123..."  # Bad!

# ✅ Whitelist system commands
SYSTEM_COMMANDS = {"chrome": "chrome"}
safe_app = SYSTEM_COMMANDS.get(user_app)

# ❌ Don't execute user input directly
os.system(user_command)  # Bad!

# ✅ Validate and sanitize
command = user_input.lower().strip()
if command in allowed_commands:
    execute(command)
```

---

## 📚 QUICK REFERENCE

| Task | Code |
|------|------|
| Listen | `listen()` |
| Speak | `speak("text")` |
| Ask LLM | `get_brain().get_response("q")` |
| Get time | `get_executor().get_time()` |
| Save memory | `get_memory().save_conversation(...)` |
| Format response | `get_personality().format_response("text")` |

---

## 🆘 COMMON ERRORS

```
ImportError: No module named 'openai'
→ pip install -r requirements.txt --upgrade

RuntimeError: No microphone found
→ Check audio settings, verify headset

openai.error.AuthenticationError
→ Check API key in .env

ValueError: unknown protocol 'https'
→ Usually indicates network issue

AttributeError: 'NoneType' has no attribute
→ Check if module is initialized
```

---

## 🎯 WORKFLOW

```
1. Start: python main.py
2. Say: "Jarvis" (wake word)
3. Say: Command or question
4. Router decides: System or LLM
5. Execute & speak response
6. Save to memory
7. Next command...
8. Say: "Goodbye" (exit)
```

---

## 📞 QUICK HELP

- **Setup Help** → See QUICK_START.md
- **Full Docs** → See README.md
- **Architecture** → See ARCHITECTURE.md
- **Future Ideas** → See ROADMAP.md
- **Code Issues** → Check data/jarvis.log
- **API Issues** → See README.md Troubleshooting

---

**Remember**: Keep it modular, test thoroughly, document your changes!

Last updated: February 2026 ✅
