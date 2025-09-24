#!/usr/bin/env python3
"""
Startup script for Railway deployment of Telegram Nutrition Bot
"""

import os
import sys

# Add the chatbot directory to Python path
chatbot_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'chatbot')
sys.path.insert(0, chatbot_dir)

# Import and run the bot
if __name__ == '__main__':
    from telegram_bot_integrated import main
    main()