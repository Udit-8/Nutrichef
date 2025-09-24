#!/usr/bin/env python3
"""
Simple startup script for Telegram Nutrition Bot
"""

import os
import sys
from pathlib import Path

def main():
    """Start the Telegram bot with proper setup"""
    
    print("🚀 Starting Telegram Nutrition Bot...")
    print("=" * 50)
    
    # Load environment variables from .env file
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Loaded .env file")
    except ImportError:
        print("⚠️  python-dotenv not found, trying environment variables...")
    
    # Check if token is configured
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        print("⚠️  TELEGRAM_BOT_TOKEN not found in environment variables.")
        print("\n📝 Setup Instructions:")
        print("1. Copy .env.example to .env")
        print("2. Edit .env and add your bot token from @BotFather")
        print("3. Run: python start_telegram_bot.py")
        
        # Try to create .env file if it doesn't exist
        env_file = Path('.env')
        env_example = Path('.env.example')
        
        if env_example.exists() and not env_file.exists():
            print(f"\n💡 Creating .env file from example...")
            with open(env_example, 'r') as src, open(env_file, 'w') as dst:
                dst.write(src.read())
            print(f"✅ Created .env file. Please edit it with your bot token.")
        
        return
    
    print(f"✅ Bot token found")
    print(f"🤖 Starting bot...")
    
    # Import and start the bot
    try:
        from telegram_bot import main as start_bot
        start_bot()
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all dependencies are installed:")
        print("pip install -r requirements_telegram.txt")
    except Exception as e:
        print(f"❌ Error starting bot: {e}")

if __name__ == '__main__':
    main()