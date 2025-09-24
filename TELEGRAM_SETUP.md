# 🤖 Telegram Bot Setup Guide

This guide will help you deploy your Nutrition Chatbot to Telegram.

## 📋 Prerequisites

- Python 3.8 or higher
- Your existing nutrition chatbot code
- A Telegram account

## 🚀 Quick Setup (5 minutes)

### Step 1: Create Telegram Bot

1. Open Telegram and search for `@BotFather`
2. Start conversation with `/start`
3. Create new bot with `/newbot`
4. Choose bot name: "Your Nutrition Assistant" 
5. Choose username: "your_nutrition_bot" (must end with 'bot')
6. **Save the API token** - you'll need it!

### Step 2: Install Dependencies

```bash
cd /Users/uditrai88/Desktop/nutrition-chatbot/chatbot
pip install -r requirements_telegram.txt
```

### Step 3: Configure Bot Token

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` file and add your bot token:
```
TELEGRAM_BOT_TOKEN=your_actual_token_here
```

### Step 4: Start Your Bot

```bash
python start_telegram_bot.py
```

You should see:
```
🚀 Starting Telegram Nutrition Bot...
✅ Bot token found
🤖 Starting bot...
INFO - Started polling
```

### Step 5: Test Your Bot

1. Go to Telegram and find your bot
2. Send `/start` to begin
3. Try commands like:
   - "Find me a recipe"
   - "Track my food"
   - "Plan my meals"

## 🎯 Bot Features

Your Telegram bot includes:

### 📱 **Commands**
- `/start` - Welcome message and main menu
- `/help` - Detailed help and usage examples  
- `/menu` - Show main menu with quick actions
- `/status` - Check current session status
- `/reset` - Reset conversation and start fresh

### 🔘 **Quick Action Buttons**
- 🔍 Recipe Discovery
- 📋 Meal Planning  
- 📊 Food Calorie Tracking
- 🛒 Grocery Assistance
- 👩‍🍳 Cooking Guidance
- 🥗 Calorie-Based Meals

### 💬 **Natural Language**
Users can type naturally:
- "I want to log my breakfast"
- "Show me healthy recipes"
- "Create a grocery list"
- "Help me cook pasta"

## 🛠️ Advanced Configuration

### Environment Variables

Create a `.env` file with these options:

```env
# Required
TELEGRAM_BOT_TOKEN=your_bot_token_here

# Optional
LOG_LEVEL=INFO
```

### Running in Background

For production deployment:

```bash
# Install screen (if not available)
# On macOS: brew install screen
# On Linux: sudo apt-get install screen

# Start bot in background
screen -S nutrition_bot python start_telegram_bot.py

# Detach: Ctrl+A, then D
# Reattach: screen -r nutrition_bot
```

### Production Deployment Options

1. **Heroku** (Free tier available)
2. **Railway** (Simple deployment)  
3. **DigitalOcean App Platform**
4. **AWS Lambda** (for serverless)
5. **Google Cloud Run**
6. **Your own VPS**

## 🧪 Testing

Test all features:

1. **Recipe Discovery**: "Find me Italian recipes"
2. **Food Tracking**: "Log my lunch"  
3. **Meal Planning**: "Plan meals for this week"
4. **Grocery Lists**: "Create grocery list"
5. **Cooking Help**: "Guide me through cooking"
6. **Calorie Meals**: "Find 400 calorie meals"

## 📊 Bot Capabilities

✅ **Multi-user support** - Each user has their own session
✅ **Context awareness** - Remembers conversation flow
✅ **Journey continuity** - Can pause and resume conversations
✅ **Inline keyboards** - Quick action buttons
✅ **Long message handling** - Splits responses if too long
✅ **Error handling** - Graceful error recovery
✅ **Session management** - Reset and status commands

## 🔧 Troubleshooting

### Bot not responding?
1. Check if token is correct in `.env`
2. Verify bot is running (`python start_telegram_bot.py`)
3. Check console for error messages

### Import errors?
```bash
pip install --upgrade -r requirements_telegram.txt
```

### Bot stops working?
1. Check logs for errors
2. Use `/reset` command to clear session
3. Restart bot if needed

## 🚀 Next Steps

### Optional Enhancements:
1. **Database persistence** - Store user data permanently
2. **Image support** - Allow users to send food photos
3. **Voice messages** - Voice-to-text food logging
4. **Scheduled reminders** - Daily nutrition reminders
5. **Analytics dashboard** - Usage statistics
6. **Multi-language support** - International users

### Deployment:
1. Choose hosting platform
2. Set up environment variables
3. Configure domain (optional)
4. Set up monitoring
5. Launch! 🎉

## 📞 Support

If you encounter issues:
1. Check the logs for error messages
2. Verify all dependencies are installed
3. Test with a fresh bot token
4. Check Telegram Bot API status

---

🎉 **Congratulations!** Your nutrition chatbot is now available on Telegram!

Users can find it by searching for your bot username and start getting personalized nutrition assistance right away.