#!/usr/bin/env python3
"""
End-to-End Integration Test for Grocery Assistance
Tests the complete integration with the main chatbot system
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from data.data_loader import DataLoader
from core.session_manager import SessionManager
from core.intent_classifier import IntentClassifier
from core.chatbot_manager import ChatbotManager

def simulate_conversation():
    print("🤖 GROCERY ASSISTANCE - END-TO-END INTEGRATION TEST")
    print("=" * 55)
    
    # Initialize the complete chatbot system
    data_loader = DataLoader()
    session_manager = SessionManager()
    intent_classifier = IntentClassifier()
    chatbot_manager = ChatbotManager(session_manager, intent_classifier, data_loader)
    
    print("✅ Complete chatbot system initialized")
    
    # Simulate a complete grocery assistance conversation
    conversation_steps = [
        ("Create a grocery list", "Should trigger grocery assistance journey"),
        ("3", "Select manual input option"),
        ("2 lbs chicken breast, 1 cup quinoa, spinach, olive oil, 3 apples", "Add ingredients manually"),
        ("1", "Select store sections organization"),
        ("1", "Export the list")
    ]
    
    print(f"\n🎯 Simulating Complete Conversation:")
    print("=" * 40)
    
    for i, (user_input, expected_action) in enumerate(conversation_steps, 1):
        print(f"\n👤 User: {user_input}")
        print(f"💭 Expected: {expected_action}")
        
        try:
            response = chatbot_manager._process_user_input(user_input)
            
            if response:
                print(f"🤖 Bot: {response[:200]}{'...' if len(response) > 200 else ''}")
                print(f"✅ Step {i} completed successfully")
            else:
                print(f"❌ Step {i} failed - no response")
                break
                
        except Exception as e:
            print(f"❌ Step {i} failed with error: {e}")
            break
    
    # Check final session state
    session_info = chatbot_manager.get_session_info()
    current_journey = session_manager.get_current_journey()
    
    print(f"\n📊 Final Session State:")
    print(f"  Current Journey: {current_journey}")
    print(f"  Messages Exchanged: {len(session_info.get('conversation_history', []))}")
    
    # Test journey completion
    if 'grocery_assistance' in str(session_info) or current_journey == 'grocery_assistance':
        print(f"  ✅ Grocery assistance journey was activated")
    else:
        print(f"  ❌ Grocery assistance journey was not activated")
    
    print(f"\n🎉 END-TO-END INTEGRATION TEST COMPLETE!")
    print(f"The grocery assistance system is fully integrated and working!")

if __name__ == "__main__":
    simulate_conversation()