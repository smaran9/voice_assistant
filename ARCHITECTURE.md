# 🏗️ JARVIS ARCHITECTURE & DESIGN GUIDE

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     USER INTERFACE                           │
│            (Voice Console or Web Browser)                    │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   VOICE MODULE                               │
│  ┌─────────────┐          ┌──────────────┐                 │
│  │  listen()   │          │   speak()    │                 │
│  │ (speech2txt)│◄────────►│   (txt2speech)                 │
│  └─────────────┘          └──────────────┘                 │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                   COMMAND ROUTER                             │
│              (Decision Engine)                               │
│  ┌─────────────────────────────────────────────────┐        │
│  │ 1. Check special commands (wake, sleep, exit)   │        │
│  │ 2. Pattern match system commands                │        │
│  │ 3. Route to LLM if no match                     │        │
│  └─────────────────────────────────────────────────┘        │
└──────────┬──────────────────────────────────┬────────────────┘
           │                                  │
           ▼                                  ▼
  ┌──────────────────┐           ┌─────────────────────┐
  │ SYSTEM MODULE    │           │  LLM BRAIN          │
  │ (Fast, Local)    │           │ (Intelligent)       │
  │ ┌──────────────┐ │           │ ┌─────────────────┐ │
  │ │ Time/Date    │ │           │ │ OpenAI GPT      │ │
  │ │ Open Apps    │ │           │ │ Conversation    │ │
  │ │ Brightness   │ │           │ │ Context Aware   │ │
  │ │ Google       │ │           │ │ Multi-turn      │ │
  │ │ YouTube      │ │           │ └─────────────────┘ │
  │ │ Shutdown etc │ │           │                     │
  │ └──────────────┘ │           │ ┌─────────────────┐ │
  │ <10ms response   │           │ │ MEMORY SYSTEM   │ │
  └──────────────────┘           │ │ ┌─────────────┐ │ │
                                 │ │ │ JSON Memory │ │ │
                                 │ │ │ Preferences │ │ │
                                 │ │ │ Goals       │ │ │
                                 │ │ └─────────────┘ │ │
                                 │ │ ┌─────────────┐ │ │
                                 │ │ │ SQLite DB   │ │ │
                                 │ │ │ History     │ │ │
                                 │ │ │ Context     │ │ │
                                 │ │ └─────────────┘ │ │
                                 │ │ ┌─────────────┐ │ │
                                 │ │ │ Vector DB   │ │ │
                                 │ │ │ (FAISS)     │ │ │
                                 │ │ │ Embeddings  │ │ │
                                 │ │ │ Search      │ │ │
                                 │ │ └─────────────┘ │ │
                                 │ └─────────────────┘ │
                                 └─────────────────────┘
                                          │
                                          ▼
                                 ┌─────────────────────┐
                                 │ PERSONALITY ENGINE  │
                                 │ (Response Styling)  │
                                 │ ┌─────────────────┐ │
                                 │ │ Add personality │ │
                                 │ │ Truncate for   │ │
                                 │ │ voice output   │ │
                                 │ └─────────────────┘ │
                                 └─────────────────────┘
                                          │
                                          ▼
                       ┌─────────────────────────────┐
                       │   OUTPUT FORMATTING         │
                       │   Display + Speak Response  │
                       └─────────────────────────────┘
```

---

## Module Breakdown

### 1. **Voice Module** (`voice/`)
**Purpose**: Handle audio I/O (input & output)

**Files:**
- `listen.py`: Speech-to-text via Google API
- `speak.py`: Text-to-speech via pyttsx3 (offline)

**Design Decisions:**
- ✅ Use Google Speech Recognition (free, accurate)
- ✅ Use pyttsx3 (offline, no API calls needed)
- ✅ Error handling for missing microphone
- ✅ Noise adjustment for robustness

**Flow:**
```
Microphone → Audio→Text → Route to Router
Response → Format → Text→Speech → Speaker
```

---

### 2. **Brain Module** (`brain/`)
**Purpose**: Intelligence and memory

**Files:**
- `llm.py`: OpenAI GPT integration
- `memory.py`: Semantic storage & retrieval

**Design Decisions:**
- ✅ Multi-turn conversations (context aware)
- ✅ Conversation history tracking
- ✅ JSON for user preferences (lightweight)
- ✅ SQLite for conversations (queryable)
- ✅ FAISS for vector embeddings (fast semantic search)
- ✅ Context injection for relevant responses

**Data Flow:**
```
User Input 
    ↓
Load Memory Context
    ↓
Build Prompt with History
    ↓
Send to OpenAI API
    ↓
Get Response
    ↓
Save to Memory
    ↓
Return Formatted Response
```

---

### 3. **Commands Module** (`commands/`)
**Purpose**: Route commands intelligently

**Files:**
- `system_commands.py`: Local operations (time, open app, etc)
- `router.py`: Decision engine (system vs LLM)

**Routing Logic:**

```python
IF input.contains(["what time", "date", "open chrome"]):
    Execute Locally (System Module)
    Response Time: <10ms
    Cost: $0
ELSE:
    Send to LLM (Brain Module)
    Response Time: 2-5 seconds
    Cost: ~$0.0001 per request
```

**System Commands Supported:**
- Time/Date → Instant local
- Open apps → Execute desktop
- Google/YouTube → Web search
- Brightness → System control
- Shutdown/Sleep → Power management

**Design Benefits:**
- ⚡ Fast responses for common queries
- 💰 Lower API costs
- 📊 Reduced latency
- 🔒 More private (no API for system tasks)

---

### 4. **Utils Module** (`utils/`)
**Purpose**: Helper functions and personality

**Files:**
- `personality.py`: Response styling and tone

**Personality Engine Features:**
- Custom greeting based on time of day
- Adaptive tone (casual, formal, motivational)
- Error messages with empathy
- Wake/sleep/exit responses
- Post-processing for voice (truncate long responses)

---

### 5. **Configuration** (`config.py`)
**Purpose**: Central settings and constants

**Why separate?**
- ✅ Easy customization
- ✅ Environment variables support
- ✅ Centralized constants
- ✅ No hardcoded values
- ✅ Production-ready approach

---

## Data Flow Examples

### Example 1: System Command (Time Query)

```
[User] "What time is it?"
   ↓
[Voice.listen()] "what time is it"
   ↓
[Router.route()] Pattern match: SYSTEM
   ↓
[SystemCommands.get_time()] "3:45 PM"
   ↓
[Personality.format_response()] "It's 3:45 PM."
   ↓
[Voice.speak()] "It's 3:45 PM."
   ↓
[Memory.save_conversation()] Log to SQLite
   ↓
Total Time: <50ms
API Cost: $0
```

### Example 2: LLM Query

```
[User] "Tell me a joke"
   ↓
[Voice.listen()] "tell me a joke"
   ↓
[Router.route()] No pattern match → LLM
   ↓
[Memory.load_context()] Get recent history
   ↓
[Brain.get_response()] 
   - Load messages: [system, history, user_input]
   - Call OpenAI API
   - Get: "Why did the developer go broke?..."
   ↓
[Personality.add_personality()] Truncate to 2-3 sentences
   ↓
[Voice.speak()] "Why did the developer go broke..."
   ↓
[Memory.save_conversation()] Log conversation + embeddings
   ↓
Total Time: 2-5 seconds
API Cost: ~$0.0001
```

### Example 3: Smart Context Usage

```
[Conversation]
1. User: "I want to learn Python"
2. Jarvis: "Great goal! Python is versatile..."
3. Memory.add_goal("Learn Python")
4. Memory.add_memory_embedding("Learn Python")

[Later...]
5. User: "Tell me about my goals"
6. Router → LLM
7. Brain.get_context():
   - Recent goals: ["Learn Python"]
   - Recent commands: ["search python tutorials", "open github"]
   - User mood: "educational"
8. Brain.get_response() with injected context
9. Response: "You're focusing on learning Python. 
             Based on your recent searches..."
```

---

## Key Design Patterns Used

### 1. **Singleton Pattern** (Global Instances)
```python
# Ensures only one instance of each major module
_brain_instance = None

def get_brain():
    global _brain_instance
    if _brain_instance is None:
        _brain_instance = JarvisBrain()
    return _brain_instance

# Usage:
brain = get_brain()  # Always returns same instance
```

**Why?** Consistent state, memory management, resource efficiency.

---

### 2. **Strategy Pattern** (Routing)
```python
# Different strategies based on input type

if is_system_command(input):
    strategy = SystemCommandStrategy()
elif is_wake_word(input):
    strategy = WakeStrategy()
else:
    strategy = LLMStrategy()

response = strategy.execute(input)
```

---

### 3. **Factory Pattern** (Voice Engine)
```python
# Abstracts voice engine creation
class VoiceAssistant:
    def __init__(self):
        self.engine = pyttsx3.init(TEXT_TO_SPEECH["engine"])
        self._configure_voice()
```

---

### 4. **Dependency Injection** (Module Loading)
```python
# Modules don't create dependencies; they receive them
class Router:
    def __init__(self):
        self.executor = get_executor()
        self.brain = get_brain()
        self.memory = get_memory()
```

---

## Performance Optimizations

### 1. **Local First**
```
System Commands: <10ms (local execution)
LLM Queries: 2-5s (network dependent)
```

### 2. **Lazy Loading**
Modules instantiate only when needed.

### 3. **Memory Caching**
Recent conversations cached in memory.

### 4. **Vector Database**
Fast semantic search (<10ms) for similar memories.

### 5. **Conversation History Truncation**
Keeps only last N interactions to reduce token usage.

---

## Scalability Considerations

### Current Design Supports:

1. **Multi-User**: Each user gets their own memory file
   - Extension: Database with user IDs

2. **Multiple Commands**: Extensible system commands
   - Add new patterns to `system_patterns`
   - Or add new handler in router

3. **Different LLMs**: Abstract LLM interface
   - Easy to swap OpenAI for Llama, Claude, etc.

4. **Deployment Options**:
   - ✅ Console application
   - ✅ Web interface (Flask)
   - 🚀 Docker container (future)
   - 🚀 AWS Lambda (future)

---

## Security Considerations

1. **API Keys**: Using .env file (not in code)
2. **System Commands**: Whitelist-only execution
3. **Audio Privacy**: Local speech recognition fallback
4. **Data Isolation**: User data in `data/` directory
5. **Logging**: Configurable log levels

---

## Future Architecture Evolution

### Phase 1 (Current)
- Single-threaded console app
- Local execution + API calls
- File-based memory

### Phase 2 (Scalable)
- Multi-threaded background tasks
- Database backend
- REST API

### Phase 3 (Distributed)
- Microservices architecture
- Docker containerization
- Cloud deployment

### Phase 4 (Enterprise)
- High-availability setup
- Load balancing
- Real-time monitoring
- Advanced analytics

---

## Testing Strategy

### Unit Tests (Recommended)
```python
# Test individual modules
def test_listen():
    assert listen() returns string

def test_system_time():
    assert get_time() returns valid time

def test_router():
    assert route("what time") → system command
    assert route("joke") → llm
```

### Integration Tests
```python
# Test module interactions
def test_full_flow():
    input = listen()
    result = process_command(input)
    speak(result["response"])
```

---

## Extension Points

### Adding New System Commands
```python
# In commands/router.py
self.system_patterns["my_command"] = r"\bpattern\b"

# In commands/system_commands.py
def my_command(self):
    return "result"
```

### Adding New LLM Capabilities
```python
# In brain/llm.py
def ask_specialized_question(self, question):
    return self.get_response(question)
```

### Customizing Personality
```python
# In config.py
PERSONALITY = {
    "greeting": "Your custom greeting",
    "tone": "Your tone"
}
```

---

**This architecture is production-ready, scalable, and maintainable.** ✅
