# 🚀 JARVIS - QUICK START GUIDE

Get your Jarvis assistant running in **5 minutes**.

---

## ⚡ TL;DR (Super Quick)

```bash
# 1. Setup environment
python -m venv venv
venv\Scripts\activate  # Windows
# or: source venv/bin/activate  # macOS/Linux

# 2. Install packages
pip install -r requirements.txt

# 3. Setup API key
cp .env.example .env
# Edit .env → Add OPENAI_API_KEY

# 4. Run!
python main.py

# 5. Say "Jarvis" to wake up assistant
```

---

## 📋 PREREQUISITES

- ✅ Python 3.10+
- ✅ Microphone + Speakers
- ✅ OpenAI API Key (free credits available)
- ✅ Internet connection

---

## 📥 INSTALLATION (Step by Step)

### Step 1: Open Terminal/PowerShell

```bash
# Windows: Press Win+R, type "cmd"
# macOS/Linux: Open Terminal
```

### Step 2: Navigate to Project

```bash
cd path/to/voice_assistant
```

### Step 3: Create Virtual Environment

```bash
python -m venv venv
```

### Step 4: Activate Virtual Environment

**Windows:**
```bash
venv\Scripts\activate
```

**macOS/Linux:**
```bash
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 5: Install Dependencies

```bash
pip install -r requirements.txt
```

⏳ This takes 2-3 minutes...

### Step 6: Get API Key

1. Go to: https://platform.openai.com/api-keys
2. Create new API key
3. Copy the key

### Step 7: Setup .env File

```bash
# Copy template
cp .env.example .env

# Edit file (Windows):
notepad .env

# Or macOS/Linux:
nano .env
```

**Add your API key:**
```
OPENAI_API_KEY=sk-your-actual-key-here
```

Save and close.

### Step 8: Test Installation

```bash
python -c "from config import *; print('✓ Ready to go!')"
```

---

## 🎮 RUN JARVIS

```bash
python main.py
```

You'll see:
```
50
Select mode:
1. Voice Interface (Console)
2. Web Interface (Browser)  
3. Exit

Enter choice (1-3): 1
```

Choose **1** for voice.

---

## 🎤 USE JARVIS

```
🎤 Listening for wake word: 'Jarvis'...

Say: "Jarvis"
↓
🔊 Jarvis: Hello Smaran. I'm ready.

Say: "What time is it?"
↓
🔊 Jarvis: It's 3:45 PM.

Say: "Open Chrome"
↓
🔊 Jarvis: Opening chrome.
(Chrome opens)

Say: "Tell me a joke"
↓
🔊 Jarvis: Command received. Why did the Math book look sad? 
Because of all the problems...

Say: "Goodbye"
↓
🔊 Jarvis: At your service, Smaran.
(Assistant exits)
```

---

## 🔧 CUSTOMIZATION

Edit `config.py` to customize:

```python
# Personality
ASSISTANT_NAME = "Jarvis"
USER_NAME = "Smaran"

# Voice
TEXT_TO_SPEECH = {
    "rate": 170,          # Faster (300) or slower (50)
    "volume": 1.0,        # 0.0 to 1.0
    "voice_index": 0,     # 0=Male, 1=Female
}

# LLM
OPENAI_MODEL = "gpt-4"    # or "gpt-3.5-turbo" (faster, cheaper)
OPENAI_TEMPERATURE = 0.7  # 0=consistent, 1=creative

# Wake words
WAKE_WORDS = ["jarvis", "hey jarvis", "okay jarvis"]
```

---

## 🔍 COMMON COMMANDS

```
Time & Date:
  "What time is it?"
  "What's today's date?"

Open Apps:
  "Open Chrome"
  "Launch VS Code"
  "Start YouTube"

Search:
  "Google Python tutorials"
  "Search for machine learning"
  "YouTube how to cook"

System:
  "Set brightness to 50"
  "Increase brightness"
  "Go to sleep"
  "Shutdown"

Conversation:
  "Tell me a joke"
  "Explain quantum computing"
  "Help me code Python"
  "What's the weather?"
```

---

## ⚠️ TROUBLESHOOTING

### **Microphone Error**
```bash
# Check if microphone is connected
# Windows: Settings → Sound
# macOS: System Preferences → Sound

# If PyAudio fails:
pip install pipwin
pipwin install pyaudio
```

### **API Key Error**
```
Make sure .env file has:
OPENAI_API_KEY=sk-...
```

Check at: https://platform.openai.com/api-keys

### **"No module named 'X'"**
```bash
pip install -r requirements.txt --upgrade
```

### **Still Stuck?**
- Check `data/jarvis.log` for detailed errors
- Review main `README.md` for full troubleshooting

---

## 📁 PROJECT STRUCTURE

```
voice_assistant/
├── main.py              👈 Run this!
├── config.py            ⚙️ Customize here
├── requirements.txt     📦 Dependencies
├── .env.example         🔑 Copy to .env
├── README.md            📚 Full docs
│
├── voice/               🎤 Voice I/O
├── brain/               🧠 LLM + Memory
├── commands/            ⚙️ System commands
└── data/                💾 Stored data
```

---

## 💡 TIPS

1. **First time slow?** LLM needs ~5 seconds. System commands are instant.
2. **Save money**: Use `gpt-3.5-turbo` instead of `gpt-4`
3. **Privacy**: All voice processing uses Google API only for recognition
4. **Offline**: System commands work without internet!

---

## 🎓 NEXT STEPS

1. Explore `config.py` - understand all settings
2. Read `README.md` - full feature documentation
3. Check `brain/llm.py` - LLM capabilities
4. Review `commands/router.py` - command logic

---

## 🆘 Need Help?

1. Check the logs: `data/jarvis.log`
2. Review **README.md** Troubleshooting section
3. Check each module's docstrings (detailed comments)

---

**Status**: ✅ Ready to Code! | 🚀 Production Grade | 💎 Enterprise Quality

Enjoy your AI assistant! 🤖
