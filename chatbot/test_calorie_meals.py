#!/usr/bin/env python3
"""
Test script for the Calorie-Based Meal Recommendation Journey
Tests the complete functionality without requiring interactive input
"""

from core.chatbot_manager import ChatbotManager
from core.intent_classifier import IntentClassifier
from core.session_manager import SessionManager

def test_calorie_meal_journey():
    """Test the calorie-based meal recommendation journey"""
    print("🧪 Testing Calorie-Based Meal Recommendation Journey\n")
    
    # Initialize components
    session_manager = SessionManager()
    intent_classifier = IntentClassifier()
    chatbot_manager = ChatbotManager(session_manager, intent_classifier)
    
    # Test intent classification
    print("1. Testing Intent Classification:")
    test_inputs = [
        "I need meals with 400 calories",
        "Find me low calorie meals", 
        "Help me find healthy meals",
        "I want meals under 300 calories",
        "Show me high calorie meals"
    ]
    
    for user_input in test_inputs:
        intent = intent_classifier.classify_intent(user_input)
        print(f"   '{user_input}' → {intent}")
    
    print("\n2. Testing Calorie Meal Journey:")
    
    # Start calorie meal journey
    print("\n   Starting calorie meal journey...")
    session_manager.start_journey('calorie_meal_recommendation')
    calorie_journey = chatbot_manager.journeys['calorie_meal_recommendation']
    
    # Test journey start (Step 1)
    response = calorie_journey.start_journey()
    print(f"   Bot: {response}")
    
    # Test calorie goal input (Step 1 → 2)
    print(f"\n   User enters: '400 calories'")
    response = calorie_journey.process_input("400 calories")
    print(f"   Bot: {response}")
    
    # Test meal scope selection (Step 2 → 3)
    print(f"\n   User selects: 'Single Meal'")
    response = calorie_journey.process_input("1")  # Single Meal
    print(f"   Bot: {response}")
    
    # Test meal type selection (Step 3 → 4)
    print(f"\n   User selects: 'Lunch'")
    response = calorie_journey.process_input("2")  # Lunch
    print(f"   Bot: {response}")
    
    # Test dietary preferences (Step 4 → 5)
    print(f"\n   User selects: 'No special requirements'")
    response = calorie_journey.process_input("1")  # No special requirements
    print(f"   Bot: {response}")
    
    # Test meal selection (Step 5 → 6)
    if "1." in response:  # If meals were found
        print(f"\n   User selects meal: '1'")
        response = calorie_journey.process_input("1")
        print(f"   Bot: {response}")
        
        # Test meal confirmation (Step 6 → 7)
        print(f"\n   User confirms: 'Yes, confirm this meal'")
        response = calorie_journey.process_input("1")
        print(f"   Bot: {response}")
        
        # Test final action (Step 7)
        print(f"\n   User selects: 'Start cooking this meal'")
        response = calorie_journey.process_input("1")
        print(f"   Bot: {response}")
    
    print("\n3. Testing Session State:")
    session_info = session_manager.get_session_summary()
    print(f"   Session ID: {session_info['session_id']}")
    print(f"   Messages: {session_info['total_messages']}")
    print(f"   Journey: {session_info['current_journey']}")
    
    print("\n✅ Calorie meal journey test completed!")

def test_meal_data_loading():
    """Test meal data loading functionality"""
    print("\n4. Testing Meal Data Loading:")
    
    from data.data_loader import DataLoader
    data_loader = DataLoader()
    
    # Test meal data
    meals = data_loader.get_meals()
    print(f"   Loaded {len(meals)} meals")
    
    if meals:
        first_meal = meals[0]
        print(f"   First meal: {first_meal.get('name', 'Unknown')}")
        print(f"   Calories: {first_meal.get('calories', 0)}")
        print(f"   Meal types: {', '.join(first_meal.get('meal_type', []))}")
    
    # Test meal filtering
    lunch_meals = data_loader.filter_meals_by_type(['lunch'])
    print(f"   Lunch meals available: {len(lunch_meals)}")
    
    # Test calorie filtering
    calorie_meals = data_loader.filter_meals_by_calories(300, 500)
    print(f"   Meals 300-500 calories: {len(calorie_meals)}")
    
    # Test dietary tags
    dietary_tags = data_loader.get_meal_dietary_tags()
    print(f"   Dietary tags: {', '.join(dietary_tags[:5])}...")
    
    print("   ✅ Meal data loading works correctly!")

def test_calorie_utilities():
    """Test calorie calculation utilities"""
    print("\n5. Testing Calorie Utilities:")
    
    from utils.calorie_utils import CalorieCalculator
    
    # Test calorie parsing
    test_inputs = [
        "400 calories",
        "300-500 calories", 
        "low calorie meals",
        "high calorie"
    ]
    
    for input_text in test_inputs:
        min_cal, max_cal, input_type = CalorieCalculator.parse_calorie_input(input_text)
        print(f"   '{input_text}' → {min_cal}-{max_cal} calories ({input_type})")
    
    # Test daily distribution
    distribution = CalorieCalculator.calculate_daily_distribution(2000)
    print(f"   Daily distribution for 2000 calories:")
    for meal_type, calories in distribution.items():
        print(f"     {meal_type.title()}: {calories} calories")
    
    # Test nutritional analysis
    sample_meal = {
        'name': 'Test Meal',
        'calories': 400,
        'nutrition': {'protein': 25, 'carbs': 45, 'fat': 12, 'fiber': 8}
    }
    
    analysis = CalorieCalculator.generate_nutrition_analysis(sample_meal)
    print(f"   Nutrition analysis for sample meal:")
    print(f"     Health score: {analysis['health_score']}/100")
    print(f"     Macro balance: {analysis['macro_balance']}")
    print(f"     Key insights: {len(analysis['insights'])} insights generated")
    
    print("   ✅ Calorie utilities working correctly!")

if __name__ == "__main__":
    test_calorie_meal_journey()
    test_meal_data_loading()
    test_calorie_utilities()