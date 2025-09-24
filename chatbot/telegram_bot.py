#!/usr/bin/env python3
"""
Telegram Bot Interface for Nutrition Chatbot
Integrates the existing nutrition chatbot with Telegram Bot API
"""

import os
import logging
import asyncio
from typing import Dict, Any
from datetime import datetime

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, 
    filters, ContextTypes, CallbackQueryHandler
)

# Import your existing chatbot components
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.session_manager import SessionManager
from core.intent_classifier import IntentClassifier
from data.data_loader import DataLoader
from core.chatbot_manager import ChatbotManager

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramNutritionBot:
    """Telegram bot interface for nutrition chatbot"""
    
    def __init__(self, token: str):
        self.token = token
        self.user_sessions: Dict[int, ChatbotManager] = {}
        
        # Initialize core components (shared across users)
        self.data_loader = DataLoader()
        self.intent_classifier = IntentClassifier()
        
        # Build application
        self.application = Application.builder().token(token).build()
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup Telegram bot command and message handlers"""
        
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("menu", self.menu_command))
        self.application.add_handler(CommandHandler("reset", self.reset_command))
        self.application.add_handler(CommandHandler("status", self.status_command))
        
        # Message handler for regular conversation
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        
        # Callback handler for inline keyboard buttons
        self.application.add_handler(CallbackQueryHandler(self.handle_callback))
    
    def _get_or_create_session(self, user_id: int) -> ChatbotManager:
        """Get existing session or create new one for user"""
        if user_id not in self.user_sessions:
            session_manager = SessionManager()
            session_manager.user_id = user_id  # Store user ID for persistence
            self.user_sessions[user_id] = ChatbotManager(
                session_manager, 
                self.intent_classifier, 
                self.data_loader
            )
        return self.user_sessions[user_id]
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        
        welcome_message = f"👋 Welcome to your **Nutrition Assistant**, {user.first_name}!\n\n"
        welcome_message += "I'm here to help you with:\n\n"
        welcome_message += "🔍 **Recipe Discovery** - Find recipes you'll love\n"
        welcome_message += "📋 **Meal Planning** - Plan your weekly meals\n"
        welcome_message += "📊 **Food Tracking** - Log and track your nutrition\n"
        welcome_message += "🛒 **Grocery Assistance** - Create shopping lists\n"
        welcome_message += "👩‍🍳 **Cooking Guidance** - Step-by-step cooking help\n"
        welcome_message += "🥗 **Calorie Recommendations** - Find meals by calories\n\n"
        welcome_message += "💡 **Quick Start:**\n"
        welcome_message += "• Type your request naturally (e.g., 'Find me a healthy recipe')\n"
        welcome_message += "• Use /menu to see all options\n"
        welcome_message += "• Use /help for more information\n\n"
        welcome_message += "What would you like to do today? 🍽️"
        
        # Create quick action keyboard
        keyboard = [
            [
                InlineKeyboardButton("🔍 Find Recipes", callback_data="recipe_discovery"),
                InlineKeyboardButton("📋 Plan Meals", callback_data="meal_planning")
            ],
            [
                InlineKeyboardButton("📊 Track Food", callback_data="food_tracking"),
                InlineKeyboardButton("🛒 Grocery List", callback_data="grocery_assistance")
            ],
            [
                InlineKeyboardButton("👩‍🍳 Cooking Help", callback_data="cooking_guidance"),
                InlineKeyboardButton("🥗 Calorie Meals", callback_data="calorie_meals")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            welcome_message, 
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = "🆘 **Nutrition Assistant Help**\n\n"
        
        help_text += "**🎯 Available Commands:**\n"
        help_text += "/start - Start fresh conversation\n"
        help_text += "/menu - Show main menu options\n"
        help_text += "/status - Check current session status\n"
        help_text += "/reset - Reset your current session\n"
        help_text += "/help - Show this help message\n\n"
        
        help_text += "**💬 How to Use:**\n"
        help_text += "Just type what you want naturally:\n\n"
        
        help_text += "**Recipe Discovery:**\n"
        help_text += "• 'Find me a chicken recipe'\n"
        help_text += "• 'Show me Italian dishes'\n"
        help_text += "• 'I want something vegetarian'\n\n"
        
        help_text += "**Food Tracking:**\n"
        help_text += "• 'Log my breakfast'\n"
        help_text += "• 'Track what I ate'\n"
        help_text += "• 'Show my food diary'\n\n"
        
        help_text += "**Meal Planning:**\n"
        help_text += "• 'Plan my meals for the week'\n"
        help_text += "• 'Create a meal plan'\n"
        help_text += "• 'Help me plan healthy meals'\n\n"
        
        help_text += "**Grocery & Cooking:**\n"
        help_text += "• 'Create a grocery list'\n"
        help_text += "• 'Guide me through cooking'\n"
        help_text += "• 'Help me cook pasta'\n\n"
        
        help_text += "**💡 Tips:**\n"
        help_text += "• The bot remembers your conversation context\n"
        help_text += "• You can switch between different features anytime\n"
        help_text += "• Use natural language - I understand context!\n"
        
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def menu_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /menu command"""
        menu_text = "🍽️ **Main Menu - Choose Your Action:**\n\n"
        
        keyboard = [
            [
                InlineKeyboardButton("🔍 Recipe Discovery", callback_data="recipe_discovery"),
                InlineKeyboardButton("📋 Meal Planning", callback_data="meal_planning")
            ],
            [
                InlineKeyboardButton("📊 Food Calorie Tracking", callback_data="food_tracking"),
                InlineKeyboardButton("🛒 Grocery Assistance", callback_data="grocery_assistance")
            ],
            [
                InlineKeyboardButton("👩‍🍳 Cooking Guidance", callback_data="cooking_guidance"),
                InlineKeyboardButton("🥗 Calorie-Based Meals", callback_data="calorie_meals")
            ],
            [
                InlineKeyboardButton("📊 My Status", callback_data="status"),
                InlineKeyboardButton("🔄 Reset Session", callback_data="reset")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            menu_text, 
            parse_mode='Markdown',
            reply_markup=reply_markup
        )
    
    async def reset_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /reset command"""
        user_id = update.effective_user.id
        
        if user_id in self.user_sessions:
            del self.user_sessions[user_id]
        
        await update.message.reply_text(
            "🔄 **Session Reset Complete!**\n\n"
            "Your conversation has been cleared and you can start fresh.\n"
            "Type /start to begin or just tell me what you'd like to do! 😊"
        )
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /status command"""
        user_id = update.effective_user.id
        chatbot = self._get_or_create_session(user_id)
        
        session_info = chatbot.get_session_info()
        
        status_text = "📊 **Your Session Status:**\n\n"
        status_text += f"🆔 Session ID: `{session_info.get('session_id', 'N/A')}`\n"
        status_text += f"🎯 Current Journey: **{session_info.get('current_journey', 'None')}**\n"
        status_text += f"📍 Current Step: **{session_info.get('current_step', 'N/A')}**\n"
        status_text += f"💬 Messages: **{session_info.get('total_messages', 0)}**\n"
        status_text += f"⏰ Session Started: {session_info.get('created_at', 'Unknown')}\n\n"
        
        if session_info.get('current_journey'):
            status_text += "✅ You have an active conversation in progress.\n"
            status_text += "Continue where you left off or use /reset to start fresh."
        else:
            status_text += "💡 No active journey. Ready to start something new!\n"
            status_text += "Tell me what you'd like to do."
        
        await update.message.reply_text(status_text, parse_mode='Markdown')
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle inline keyboard button clicks"""
        query = update.callback_query
        user_id = query.from_user.id
        
        await query.answer()  # Acknowledge the callback
        
        callback_data = query.data
        
        if callback_data == "reset":
            if user_id in self.user_sessions:
                del self.user_sessions[user_id]
            await query.edit_message_text("🔄 Session reset! Type /start to begin fresh.")
            return
        
        elif callback_data == "status":
            chatbot = self._get_or_create_session(user_id)
            session_info = chatbot.get_session_info()
            
            status_text = f"📊 **Session Status:**\n"
            status_text += f"Journey: **{session_info.get('current_journey', 'None')}**\n"
            status_text += f"Step: **{session_info.get('current_step', 'N/A')}**"
            
            await query.edit_message_text(status_text, parse_mode='Markdown')
            return
        
        # Handle journey start callbacks
        journey_map = {
            "recipe_discovery": "Find me a recipe",
            "meal_planning": "Help me plan meals", 
            "food_tracking": "Log my food",
            "grocery_assistance": "Create a grocery list",
            "cooking_guidance": "Guide me through cooking",
            "calorie_meals": "Find me low calorie meals"
        }
        
        if callback_data in journey_map:
            # Simulate user input for the selected journey
            user_input = journey_map[callback_data]
            chatbot = self._get_or_create_session(user_id)
            
            response = chatbot._process_user_input(user_input)
            
            if response:
                # Format response for Telegram
                formatted_response = self._format_response_for_telegram(response)
                await query.edit_message_text(formatted_response, parse_mode='Markdown')
            else:
                await query.edit_message_text("🤔 Something went wrong. Please try again or use /reset.")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular text messages"""
        user_id = update.effective_user.id
        user_input = update.message.text
        
        # Get or create user session
        chatbot = self._get_or_create_session(user_id)
        
        try:
            # Process the user input
            response = chatbot._process_user_input(user_input)
            
            if response:
                # Format and send response
                formatted_response = self._format_response_for_telegram(response)
                
                # Split long messages if needed
                if len(formatted_response) > 4000:
                    # Split into chunks
                    chunks = self._split_message(formatted_response, 4000)
                    for chunk in chunks:
                        await update.message.reply_text(chunk, parse_mode='Markdown')
                else:
                    await update.message.reply_text(formatted_response, parse_mode='Markdown')
            else:
                await update.message.reply_text(
                    "🤔 I'm not sure how to help with that. Try:\n"
                    "• /menu for options\n"
                    "• /help for guidance\n"
                    "• Or describe what you'd like to do!"
                )
        
        except Exception as e:
            logger.error(f"Error processing message from user {user_id}: {e}")
            await update.message.reply_text(
                "⚠️ Sorry, I encountered an error. Please try again or use /reset to start fresh."
            )
    
    def _format_response_for_telegram(self, response: str) -> str:
        """Format chatbot response for Telegram"""
        # Convert basic formatting
        response = response.replace("🤖 Bot: ", "")  # Remove bot prefix
        
        # Ensure proper Markdown formatting
        response = response.replace("**", "*")  # Use single asterisk for bold
        
        # Handle special characters that might break Markdown
        response = response.replace("_", "\\_")  # Escape underscores
        response = response.replace("`", "\\`")  # Escape backticks
        
        return response
    
    def _split_message(self, text: str, max_length: int) -> list:
        """Split long messages into chunks"""
        if len(text) <= max_length:
            return [text]
        
        chunks = []
        current_chunk = ""
        
        lines = text.split('\n')
        for line in lines:
            if len(current_chunk) + len(line) + 1 <= max_length:
                current_chunk += line + '\n'
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                current_chunk = line + '\n'
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    def run(self):
        """Start the Telegram bot"""
        logger.info("Starting Telegram Nutrition Bot...")
        self.application.run_polling()

def main():
    """Main function to start the Telegram bot"""
    
    # Load token from environment variable or file
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        # Try to load from .env file
        try:
            from dotenv import load_dotenv
            load_dotenv()
            token = os.getenv('TELEGRAM_BOT_TOKEN')
        except ImportError:
            pass
    
    if not token:
        print("❌ Error: TELEGRAM_BOT_TOKEN not found!")
        print("Please set your Telegram bot token:")
        print("1. Create a .env file with: TELEGRAM_BOT_TOKEN=your_token_here")
        print("2. Or set environment variable: export TELEGRAM_BOT_TOKEN=your_token_here")
        return
    
    # Create and run bot
    bot = TelegramNutritionBot(token)
    bot.run()

if __name__ == '__main__':
    main()