# 🚀 MITRA - YOUR QUICK SETUP (WITHOUT API KEY YET)

## You can test RIGHT NOW without API key! ⚡

**System commands work offline** - no API needed:
- ✅ Time & Date
- ✅ Open Chrome, VS Code
- ✅ Google/YouTube search
- ✅ Brightness control
- ✅ Shutdown/Sleep

---

## 5-MINUTE SETUP

### Step 1: Install Packages
```bash
pip install -r requirements.txt
```

### Step 2: Create .env File (No key needed yet!)
```bash
cp .env.example .env
```

**That's it!** Leave `OPENAI_API_KEY=your-api-key-here` as is for now.

### Step 3: Run Mitra
```bash
python main.py
```

Choose option **1** (Voice Interface)

---

## 🎤 TEST IT NOW!

```
🎤 Say: "Mitra"
↓
🔊 Mitra: Hello Smaran. Ready to assist.

Say: "What time is it?"
↓
✅ Works! (System command = instant)

Say: "Tell me a joke"
↓
❌ Won't work (needs API key)
```

---

## 💰 GET FREE API KEY (Takes 5 minutes)

### Quick Steps:
1. Go to: https://platform.openai.com/signup
2. Sign up (FREE - includes $5 credits)
3. Go to: https://platform.openai.com/api-keys
4. Click "Create new secret key"
5. Copy the key

### Add to .env File:
```bash
# Edit .env
OPENAI_API_KEY=sk-your-actual-key-here
```

Save file → **Done!** ✅

---

## 🎤 VOICE COMMANDS TO TEST

```
OFFLINE (No API Key Needed):
  "Mitra"                    → Wakes up
  "What time is it?"         → Time
  "What's the date?"         → Date
  "Open Chrome"              → Opens browser
  "Google Python"            → Web search
  "Set brightness to 80"     → Controls display
  "Sleep"                    → Standby mode
  "Goodbye"                  → Exit

ONLINE (Needs API Key):
  "Tell me a joke"           → LLM response
  "Help me code"             → Coding assistance
  "Explain AI"               → Smart explanation
  "What are my goals?"       → Memory recall
```

---

## 📊 QUICK REFERENCE

| Action | Time | Cost |
|--------|------|------|
| Setup (no API) | 2 min | FREE |
| Get API key | 5 min | FREE ($5 credits) |
| Add to .env | 1 min | FREE |
| Full setup | 5 min total | FREE |

---

## ✅ VERIFY SETUP

```bash
# Check Python imports
python -c "from config import *; print('✓ Config loaded')"

# Check voice + commands work
python -c "from commands import process_command; print(process_command('what time'))"
```

---

## 🆘 ISSUES?

### "What if I can't speak?"
→ Use web mode: Option 2 in main.py (type instead)

### "Package not found?"
→ Run: `pip install -r requirements.txt --upgrade`

### "Microphone error?"
→ Check Windows Settings → Sound

### "Want full power?"
→ Get API key (see above) → Takes 5 minutes

---

## 🎁 WHAT YOU CAN DO NOW

✅ Test voice input
✅ Get current time/date
✅ Open applications
✅ Search web
✅ Control brightness
✅ Full assistant feel without LLM

---

**Next**: Say "Mitra" to wake up! 🤖

**After APIs ready**: Full AI conversations + memory! 🧠

---

Questions? See [API_SETUP.md](API_SETUP.md) for detailed API key guide.
