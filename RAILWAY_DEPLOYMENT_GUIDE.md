# 🚀 Railway Deployment Guide for Nutrition Chatbot

This guide will walk you through deploying your Telegram nutrition chatbot to Railway platform.

## 📋 Prerequisites

1. **Telegram Bot Token** - Get from @BotFather on Telegram
2. **Railway Account** - Sign up at [railway.app](https://railway.app)
3. **GitHub Account** - For code repository
4. **Git installed** - For version control

## 🎯 Quick Deployment (10 minutes)

### Step 1: Prepare Your Telegram Bot

1. Open Telegram and search for `@BotFather`
2. Create a new bot with `/newbot`
3. Choose bot name: "Your Nutrition Assistant"
4. Choose username: "your_nutrition_bot" (must end with 'bot')
5. **Copy and save your bot token** - you'll need it for Railway!

### Step 2: Set Up Git Repository

```bash
# Navigate to your project
cd /Users/uditrai88/Desktop/nutrition-chatbot

# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit files
git commit -m "Initial nutrition chatbot deployment"

# Create GitHub repository and push (or use Railway GitHub integration)
```

### Step 3: Deploy to Railway

#### Option A: GitHub Integration (Recommended)

1. **Push to GitHub first:**
   ```bash
   # Create repository on GitHub, then:
   git remote add origin https://github.com/YOUR_USERNAME/nutrition-chatbot.git
   git branch -M main
   git push -u origin main
   ```

2. **Deploy on Railway:**
   - Go to [railway.app](https://railway.app)
   - Click "Start a New Project"
   - Select "Deploy from GitHub repo"
   - Connect your GitHub account
   - Select your nutrition-chatbot repository
   - Railway will auto-detect Python and start deployment

#### Option B: Railway CLI (Alternative)

1. **Install Railway CLI:**
   ```bash
   # macOS
   brew install railway
   
   # Or download from: https://railway.app/cli
   ```

2. **Login and deploy:**
   ```bash
   railway login
   railway link  # Link to existing project or create new one
   railway up    # Deploy your code
   ```

### Step 4: Configure Environment Variables

1. **In Railway Dashboard:**
   - Go to your project
   - Click on "Variables" tab
   - Add the following environment variable:

   ```
   TELEGRAM_BOT_TOKEN = your_actual_bot_token_here
   ```

2. **Optional variables:**
   ```
   LOG_LEVEL = INFO
   PORT = 8000
   ```

### Step 5: Verify Deployment

1. **Check Railway Logs:**
   - In Railway dashboard, go to "Deployments" tab
   - Click on latest deployment
   - Check logs for:
     ```
     🚀 Starting Integrated Telegram Nutrition Bot...
     ✅ This version includes full journey flows!
     📱 Users can now have complete interactive conversations
     ```

2. **Test Your Bot:**
   - Go to Telegram
   - Find your bot by username
   - Send `/start`
   - Try: "Find me a recipe" or "Track my food"

## 🔧 Deployment Files Included

Your project now includes these Railway-specific files:

### `requirements.txt`
```txt
python-telegram-bot>=20.7
python-dotenv>=1.0.0
typing-extensions>=4.0.0
```

### `Procfile`
```
web: python chatbot/telegram_bot_integrated.py
```

### `railway.json`
```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python chatbot/telegram_bot_integrated.py",
    "healthcheckPath": "/",
    "healthcheckTimeout": 100,
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

### `runtime.txt`
```
python-3.11.0
```

### `.env.example`
```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
LOG_LEVEL=INFO
```

## 🎛️ Railway Configuration Details

### Build Settings
- **Builder**: NIXPACKS (auto-detected)
- **Python Version**: 3.11.0
- **Start Command**: `python chatbot/telegram_bot_integrated.py`

### Environment Variables Required
| Variable | Description | Example |
|----------|-------------|---------|
| `TELEGRAM_BOT_TOKEN` | Your bot token from BotFather | `1234567890:ABC...` |

### Optional Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `LOG_LEVEL` | Logging verbosity | `INFO` |
| `PORT` | Port for health checks | `8000` |

## 🚨 Troubleshooting

### Common Issues & Solutions

#### ❌ "TELEGRAM_BOT_TOKEN not found!"
**Solution**: 
- Check Railway environment variables
- Ensure variable name is exactly `TELEGRAM_BOT_TOKEN`
- No extra spaces in the token value

#### ❌ Import errors during deployment
**Solution**:
- Check `requirements.txt` is in root directory
- Verify all dependencies are listed
- Check Railway build logs for specific missing packages

#### ❌ Bot not responding
**Solution**:
1. Check Railway deployment logs
2. Verify bot token is correct
3. Test bot locally first
4. Check Telegram webhook conflicts (use `/setwebhook` with empty URL)

#### ❌ "Module not found" errors
**Solution**:
- Ensure all Python files are committed to git
- Check that all required JSON data files are included
- Verify file paths are correct for Railway's file structure

### Debugging Steps

1. **Check Deployment Status:**
   ```bash
   railway status
   railway logs
   ```

2. **Test Locally First:**
   ```bash
   cd /Users/uditrai88/Desktop/nutrition-chatbot
   export TELEGRAM_BOT_TOKEN="your_token"
   python chatbot/telegram_bot_integrated.py
   ```

3. **Verify File Structure:**
   ```
   nutrition-chatbot/
   ├── requirements.txt
   ├── Procfile
   ├── railway.json
   ├── runtime.txt
   ├── chatbot/
   │   ├── telegram_bot_integrated.py
   │   └── (other Python files)
   └── raw_data/
       ├── recipes_raw.json
       ├── meal_suggestions_raw.json
       └── (other JSON files)
   ```

## 🔄 Updating Your Deployment

To update your bot after making changes:

### Via GitHub (Automatic)
```bash
git add .
git commit -m "Update nutrition chatbot features"
git push origin main
# Railway will auto-deploy the changes
```

### Via Railway CLI
```bash
railway up
```

## 📊 Monitoring & Maintenance

### Railway Dashboard Features
- **Real-time Logs**: Monitor bot activity and errors
- **Metrics**: CPU, memory usage, deployment stats
- **Environment Variables**: Update bot configuration
- **Deployments**: History and rollback options

### Bot Health Monitoring
Your bot logs will show:
- User interactions and journey flows
- Error messages and recovery actions
- Performance metrics and response times
- Database access and search results

### Recommended Monitoring
- Check logs daily for errors
- Monitor user engagement and feature usage
- Update bot token if compromised
- Keep dependencies updated

## 💰 Railway Pricing

### Free Tier (Hobby Plan)
- $5/month of usage included
- Perfect for personal nutrition bot
- Supports moderate user traffic
- No sleep/wake delays

### Usage Estimates
- **Light usage** (10-50 users/day): ~$2-5/month
- **Moderate usage** (100-200 users/day): ~$5-15/month
- **Heavy usage** (500+ users/day): ~$15+/month

## 🎯 Next Steps After Deployment

### Immediate Actions
1. ✅ Test all 6 journey flows
2. ✅ Verify database access works
3. ✅ Check error handling and recovery
4. ✅ Test cross-journey transitions

### Optional Enhancements
1. **Custom Domain**: Point your own domain to Railway
2. **Database Integration**: Add PostgreSQL for user persistence
3. **Analytics**: Add usage tracking and user metrics
4. **Monitoring**: Set up alerts for downtime or errors

### User Management
1. **Bot Discovery**: Submit to Telegram bot directories
2. **User Support**: Create /help command documentation
3. **Usage Analytics**: Monitor popular features and journeys
4. **Feedback System**: Implement user rating and feedback

## 🎉 Success!

Once deployed successfully, your nutrition chatbot will be available 24/7 on Telegram with:

✅ **All 6 Journey Flows**: Recipe Discovery, Food Tracking, Meal Planning, Grocery Assistance, Cooking Guidance, Calorie Meal Recommendations

✅ **Real Database Integration**: 8 recipes, 50+ meal suggestions, complete nutrition data

✅ **Advanced Features**: Step-by-step cooking, smart shopping lists, calorie-based meal matching

✅ **Cross-Journey Workflows**: Seamless transitions between planning, shopping, and cooking

✅ **Error Handling**: Graceful recovery from errors with user-friendly messages

✅ **Scalable Architecture**: Ready for multiple users and future enhancements

---

**🎊 Congratulations!** Your nutrition chatbot is now live on Railway and ready to help users worldwide with their nutrition goals!

## 📞 Support

If you need help:
1. Check Railway documentation: [docs.railway.app](https://docs.railway.app)
2. Review deployment logs in Railway dashboard
3. Test locally to isolate issues
4. Check Telegram Bot API documentation

**Happy deploying!** 🚀