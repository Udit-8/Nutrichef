#!/usr/bin/env python3
"""
Telegram Bot Launcher - Simple version to avoid import issues
"""

import os
import sys
import asyncio
import logging
from typing import Dict, Any

# Load environment variables first
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("Warning: python-dotenv not installed")

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def check_dependencies():
    """Check if all required packages are installed"""
    try:
        from telegram import Update
        from telegram.ext import Application
        print("✅ python-telegram-bot is installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install: pip install python-telegram-bot python-dotenv")
        return False

def check_token():
    """Check if bot token is configured"""
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        print("❌ TELEGRAM_BOT_TOKEN not found!")
        print("Please set your bot token in .env file")
        return None
    print("✅ Bot token found")
    return token

def create_simple_bot(token: str):
    """Create a simple bot that can respond to messages"""
    from telegram import Update
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
    
    # Simple response function
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        welcome_text = """
🍎 **Welcome to your Nutrition Assistant!**

I'm your AI-powered nutrition helper, ready to assist you with:

🔍 **Recipe Discovery** - Find delicious recipes
📋 **Meal Planning** - Plan your weekly meals  
📊 **Food Tracking** - Log and track your nutrition
🛒 **Grocery Lists** - Create smart shopping lists
👩‍🍳 **Cooking Help** - Step-by-step cooking guidance
🥗 **Healthy Meals** - Find meals by calories and nutrition

**How to use me:**
Just type naturally what you want to do:
• "Find me a healthy recipe"
• "Track my breakfast" 
• "Plan meals for this week"
• "Create a grocery list"
• "Help me cook pasta"

Let's start! What would you like to do? 🌟
        """
        await update.message.reply_text(welcome_text, parse_mode='Markdown')
    
    async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
        help_text = """
🆘 **Nutrition Assistant Help**

**Available Commands:**
/start - Welcome message and introduction
/help - Show this help message
/features - List all available features

**How to interact:**
Just type what you want in natural language:

**Examples:**
• "I want a chicken recipe"
• "Log my lunch - grilled chicken and rice" 
• "Plan healthy meals for the week"
• "Create a grocery list for pasta dishes"
• "Guide me through cooking lasagna"
• "Find me 400 calorie meals"

**Features:**
🔍 Recipe Discovery
📋 Meal Planning
📊 Food & Calorie Tracking  
🛒 Grocery Assistance
👩‍🍳 Interactive Cooking
🥗 Calorie-based Recommendations

Type your request and I'll help you! 😊
        """
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def features(update: Update, context: ContextTypes.DEFAULT_TYPE):
        features_text = """
🌟 **All Available Features**

**🔍 Recipe Discovery**
Find recipes by ingredients, cuisine, dietary restrictions, or cooking time.
*Try: "Find me Italian vegetarian recipes"*

**📋 Meal Planning** 
Create personalized weekly meal plans based on your preferences.
*Try: "Plan healthy meals for this week"*

**📊 Food & Calorie Tracking**
Log your food intake and track nutrition goals.
*Try: "Log my breakfast - oatmeal and banana"*

**🛒 Grocery Assistance**
Generate smart shopping lists from your meal plans.
*Try: "Create grocery list for my meal plan"*

**👩‍🍳 Interactive Cooking**
Get step-by-step cooking guidance with timers.
*Try: "Guide me through cooking chicken stir-fry"*

**🥗 Calorie-Based Meals**
Find meals that match your calorie targets.
*Try: "Find me 300-400 calorie lunch options"*

Just type what you want naturally - I understand context! 🤖✨
        """
        await update.message.reply_text(features_text, parse_mode='Markdown')
    
    async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_input = update.message.text.lower()
        
        # Simple intent detection
        if any(word in user_input for word in ['recipe', 'cook', 'dish', 'meal']):
            response = """
🔍 **Recipe Discovery Mode**

I can help you find amazing recipes! Here's what I can do:

**Search by:**
• Ingredients: "recipes with chicken and broccoli"
• Cuisine: "Italian pasta recipes"  
• Diet: "vegetarian high-protein meals"
• Time: "quick 30-minute dinner recipes"

**Popular requests:**
• "Healthy chicken recipes"
• "Easy pasta dishes" 
• "Low-carb dinner ideas"
• "Breakfast recipes under 300 calories"

What type of recipe are you looking for? 🍳
            """
        
        elif any(word in user_input for word in ['track', 'log', 'food', 'calorie', 'ate', 'nutrition']):
            response = """
📊 **Food Tracking Mode**

Let me help you track your nutrition! Here's how:

**Log foods:**
• "Log breakfast: oatmeal with berries"
• "Track lunch: grilled chicken salad" 
• "Add snack: apple and peanut butter"

**Check progress:**
• "Show my food diary"
• "How many calories today?"
• "My nutrition summary"

**Set goals:**
• "Set daily calorie goal to 1800"
• "Track protein intake"

What would you like to log or check? 📝
            """
        
        elif any(word in user_input for word in ['plan', 'meal plan', 'weekly', 'week']):
            response = """
📋 **Meal Planning Mode**

I'll help you plan nutritious meals! Here's what I can do:

**Create plans:**
• "Plan meals for this week"
• "Healthy meal plan for weight loss"
• "High-protein meal plan"
• "Vegetarian weekly plan"

**Customize by:**
• Dietary preferences
• Calorie targets
• Cooking time available
• Number of people

**Get organized:**
• Daily meal schedules
• Shopping lists
• Prep instructions

What kind of meal plan do you need? 📅
            """
        
        elif any(word in user_input for word in ['grocery', 'shopping', 'list', 'buy', 'store']):
            response = """
🛒 **Grocery Assistance Mode**

Let me create smart shopping lists for you!

**Generate lists from:**
• Your meal plans
• Specific recipes
• Weekly menus
• Dietary goals

**Smart features:**
• Organized by store sections
• Ingredient consolidation
• Substitution suggestions
• Budget-friendly options

**Try saying:**
• "Create grocery list for pasta week"
• "Shopping list for healthy meals"
• "What ingredients do I need for meal prep?"

What groceries do you need help with? 🛍️
            """
        
        elif any(word in user_input for word in ['cooking', 'guide', 'help cook', 'how to cook']):
            response = """
👩‍🍳 **Cooking Guidance Mode**

I'll guide you through cooking step-by-step!

**Get help with:**
• Interactive cooking instructions
• Timer management
• Technique tips
• Troubleshooting

**Popular requests:**
• "Guide me through cooking pasta"
• "How to make perfect rice"
• "Step-by-step chicken stir-fry"
• "Help me cook for beginners"

**Features:**
• Real-time guidance
• Multiple timers
• Pause and resume
• Cooking tips

What would you like to cook? 🔥
            """
        
        else:
            response = """
🤖 **I'm here to help with nutrition!**

I didn't quite catch what you're looking for. Here are some things you can try:

**🔍 Recipe Discovery:** "Find me healthy chicken recipes"
**📊 Food Tracking:** "Log my breakfast"  
**📋 Meal Planning:** "Plan meals for this week"
**🛒 Grocery Lists:** "Create shopping list"
**👩‍🍳 Cooking Help:** "Guide me through cooking"

Or use these commands:
• /start - Main welcome
• /help - Detailed help  
• /features - All available features

Just tell me what you'd like to do! 😊
            """
        
        await update.message.reply_text(response, parse_mode='Markdown')
    
    # Create application
    application = Application.builder().token(token).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("features", features))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    return application

def main():
    """Main function"""
    print("🚀 Starting Simple Telegram Nutrition Bot...")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        return
    
    # Check token
    token = check_token()
    if not token:
        return
    
    try:
        # Create and run bot
        print("🤖 Creating bot...")
        application = create_simple_bot(token)
        
        print("✅ Bot created successfully!")
        print("🔄 Starting polling...")
        print("📱 Your bot is now live! Go to Telegram and test it!")
        print("🛑 Press Ctrl+C to stop the bot")
        print("-" * 50)
        
        # Run the bot
        application.run_polling(allowed_updates=['message', 'callback_query'])
        
    except Exception as e:
        print(f"❌ Error: {e}")
        logger.error(f"Bot error: {e}")

if __name__ == '__main__':
    main()