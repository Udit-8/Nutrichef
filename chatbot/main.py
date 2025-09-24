#!/usr/bin/env python3
"""
Nutrition Chatbot - Main Entry Point
Handles user interactions and routes to appropriate journey modules.
"""

from core.chatbot_manager import ChatbotManager
from core.intent_classifier import IntentClassifier
from core.session_manager import SessionManager
from data.data_loader import DataLoader

def main():
    """Main chatbot entry point"""
    print("🍽️ Welcome to your Nutrition Assistant!")
    print("I can help you with recipes, meal planning, cooking guidance, and more!")
    print("Type 'exit' to quit anytime.\n")
    
    # Initialize core components
    data_loader = DataLoader()
    session_manager = SessionManager()
    intent_classifier = IntentClassifier()
    chatbot_manager = ChatbotManager(session_manager, intent_classifier, data_loader)
    
    # Start conversation loop
    chatbot_manager.start_conversation()

if __name__ == "__main__":
    main()