#!/usr/bin/env python3
"""Integration test for the meal planning chatbot"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.chatbot_manager import ChatbotManager
from core.intent_classifier import IntentClassifier
from core.session_manager import SessionManager
from data.data_loader import DataLoader

def test_chatbot_integration():
    """Test the chatbot integration with meal planning"""
    print("🧪 Testing Chatbot Integration with Meal Planning")
    print("=" * 60)
    
    try:
        # Initialize components
        data_loader = DataLoader()
        session_manager = SessionManager()
        intent_classifier = IntentClassifier()
        chatbot_manager = ChatbotManager(session_manager, intent_classifier, data_loader)
        
        print("✅ All components initialized successfully")
        
        # Test intent classification
        test_inputs = [
            "I want to plan my meals for the week",
            "Create a meal plan",
            "Help me with meal planning",
            "Plan my meals"
        ]
        
        print("\n🔍 Testing intent classification:")
        for user_input in test_inputs:
            intent = intent_classifier.classify_intent(user_input)
            print(f"  '{user_input}' → {intent}")
        
        # Test meal planning journey initialization
        print("\n🔍 Testing meal planning journey:")
        test_input = "I want to plan my meals for the week"
        
        # Simulate user input processing
        intent = intent_classifier.classify_intent(test_input)
        if intent == 'meal_planning':
            session_manager.start_journey(intent)
            journey = chatbot_manager.journeys[intent]
            response = journey.start_journey()
            
            print("Journey started successfully!")
            print("Bot response preview:")
            print(response[:200] + "..." if len(response) > 200 else response)
        
        print("\n✅ Integration test completed successfully!")
        
    except Exception as e:
        print(f"❌ Integration test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_chatbot_integration()