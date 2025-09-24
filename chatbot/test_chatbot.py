#!/usr/bin/env python3
"""
Test script for the Recipe Discovery Chatbot
Tests the core functionality without requiring interactive input
"""

from core.chatbot_manager import ChatbotManager
from core.intent_classifier import IntentClassifier
from core.session_manager import SessionManager

def test_recipe_discovery():
    """Test the recipe discovery journey"""
    print("🧪 Testing Recipe Discovery Chatbot\n")
    
    # Initialize components
    session_manager = SessionManager()
    intent_classifier = IntentClassifier()
    chatbot_manager = ChatbotManager(session_manager, intent_classifier)
    
    # Test intent classification
    print("1. Testing Intent Classification:")
    test_inputs = [
        "I want to find a recipe",
        "Show me some recipes",
        "What should I cook?",
        "Help me plan meals",
        "Track my calories"
    ]
    
    for user_input in test_inputs:
        intent = intent_classifier.classify_intent(user_input)
        print(f"   '{user_input}' → {intent}")
    
    print("\n2. Testing Recipe Discovery Journey:")
    
    # Start recipe discovery journey
    print("\n   Starting recipe discovery...")
    session_manager.start_journey('recipe_discovery')
    recipe_journey = chatbot_manager.journeys['recipe_discovery']
    
    # Test journey start
    response = recipe_journey.start_journey()
    print(f"   Bot: {response}")
    
    # Test discovery method selection
    print(f"\n   User selects: 'Cuisine Type'")
    response = recipe_journey.process_input("1")  # Cuisine Type
    print(f"   Bot: {response}")
    
    # Test cuisine selection
    print(f"\n   User selects: 'Italian'")
    response = recipe_journey.process_input("Italian")
    print(f"   Bot: {response}")
    
    # Test recipe selection
    if "1." in response:  # If recipes were found
        print(f"\n   User selects recipe: '1'")
        response = recipe_journey.process_input("1")
        print(f"   Bot: {response}")
        
        # Test final action
        print(f"\n   User selects: 'Start cooking this recipe'")
        response = recipe_journey.process_input("1")
        print(f"   Bot: {response}")
    
    print("\n3. Testing Session State:")
    session_info = session_manager.get_session_summary()
    print(f"   Session ID: {session_info['session_id']}")
    print(f"   Messages: {session_info['total_messages']}")
    print(f"   Journey: {session_info['current_journey']}")
    
    print("\n✅ Test completed successfully!")

def test_data_loading():
    """Test data loading functionality"""
    print("\n4. Testing Data Loading:")
    
    from data.data_loader import DataLoader
    data_loader = DataLoader()
    
    # Test recipe data
    recipes = data_loader.get_recipes()
    print(f"   Loaded {len(recipes)} recipes")
    
    if recipes:
        first_recipe = recipes[0]
        print(f"   First recipe: {first_recipe.get('name', 'Unknown')}")
    
    # Test cuisine types
    cuisines = data_loader.get_cuisine_types()
    print(f"   Available cuisines: {', '.join(cuisines[:5])}...")
    
    # Test dietary tags
    dietary_tags = data_loader.get_dietary_tags()
    print(f"   Dietary tags: {', '.join(dietary_tags[:5])}...")
    
    print("   ✅ Data loading works correctly!")

if __name__ == "__main__":
    test_recipe_discovery()
    test_data_loading()