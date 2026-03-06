# 🔑 HOW TO GET A FREE OPENAI API KEY

## ⭐ OPTION 1: FREE OpenAI API Credits (Recommended!)

### Step 1: Create Account
1. Go to: https://platform.openai.com/signup
2. Sign up with email or Google/Microsoft account
3. Verify your email

### Step 2: Get Free $5 Credits
✅ **New accounts get $5 free credits automatically!**
- Good for ~200 API calls
- Valid for 3 months
- NO credit card needed initially

### Step 3: Get API Key
1. Go to: https://platform.openai.com/api-keys
2. Click **"Create new secret key"**
3. **Copy the key** (you'll only see it once!)
4. Paste it in your `.env` file:

```bash
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
```

### Step 4: Verify Setup
```bash
python -c "import openai; print('✅ API Key is valid!')"
```

---

## 💰 PRICING (After Free Credits)

**GPT-3.5-turbo** (Fast, Cheap)
- Input: $0.50 per 1M tokens
- Output: $1.50 per 1M tokens
- **Example**: 1000 requests ≈ $0.10

**GPT-4** (Powerful, Higher Cost)
- Input: $30 per 1M tokens
- Output: $60 per 1M tokens
- **Use for complex tasks only**

---

## 📊 COST ESTIMATION

| Scenario | API Calls | Cost |
|----------|-----------|------|
| 10 conversations/day | 300/month | ~$0.05 |
| 30 conversations/day | 900/month | ~$0.15 |
| 100 conversations/day | 3000/month | ~$0.50 |

**Mitra uses GPT-3.5-turbo** (fast + cheap) by default.

---

## 🔒 KEEPING YOUR KEY SAFE

✅ **DO THIS:**
- Keep `.env` file private (never commit to GitHub)
- Add `.env` to `.gitignore`
- Rotate keys if exposed

❌ **DON'T DO THIS:**
- Hardcode API key in code
- Share API key in messages
- Commit `.env` to public repos

---

## ⚡ TEST YOUR KEY

```bash
# Activate virtual environment first:
venv\Scripts\activate  # Windows

# Then test:
python -c "
from config import OPENAI_API_KEY
from brain import get_brain
brain = get_brain()
response = brain.get_response('Say hello!')
print('✅ SUCCESS:', response['response'])
"
```

**Expected output:**
```
✅ SUCCESS: Hello! How can I help?
```

---

## 🆘 TROUBLESHOOTING

### "Invalid API Key"
→ Check `.env` file has correct key
→ Regenerate key at https://platform.openai.com/api-keys
→ Make sure to `cp .env.example .env`

### "Rate limit exceeded"
→ Wait 1 minute before next request
→ Or upgrade to paid plan

### "Quota exceeded"
→ Your $5 free credits are used up
→ Add payment method to continue
→ Or wait for monthly reset

### Still not working?
```bash
# Check if key is loaded
python -c "from config import OPENAI_API_KEY; print(OPENAI_API_KEY)"
```

---

## 🎯 NEXT STEPS

1. ✅ Create account at https://platform.openai.com/signup
2. ✅ Copy API key from https://platform.openai.com/api-keys
3. ✅ Edit `.env` file and paste key
4. ✅ Run: `python main.py`
5. ✅ Say "Mitra" to wake up!

---

## 📞 NEED HELP?

- **OpenAI Status**: https://status.openai.com
- **API Docs**: https://platform.openai.com/docs
- **Billing**: https://platform.openai.com/account/billing/overview

---

**Total time**: 5 minutes ⚡
**Cost**: FREE (with $5 credits)
**Result**: Full voice assistant ready to use! 🤖
