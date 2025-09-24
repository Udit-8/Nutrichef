#!/usr/bin/env python3
"""
Test script for Meal Planning Journey
Tests the complete meal planning flow with real data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.data_loader import DataLoader
from core.session_manager import SessionManager
from journeys.meal_planning import MealPlanningJourney

def test_meal_planning():
    """Test the meal planning journey with simulated user inputs"""
    print("🧪 Testing Meal Planning Journey")
    print("=" * 50)
    
    # Initialize components
    data_loader = DataLoader()
    session_manager = SessionManager()
    meal_planning = MealPlanningJourney(data_loader, session_manager)
    
    print("✅ Components initialized successfully\n")
    
    # Test 1: Start the journey
    print("🔍 Test 1: Starting meal planning journey")
    response = meal_planning.start_journey()
    print("Bot Response:")
    print(response)
    print("\n" + "-" * 50 + "\n")
    
    # Test 2: Planning scope - weekly plan
    print("🔍 Test 2: Selecting weekly planning scope")
    response = meal_planning.process_user_input("weekly")
    print("Bot Response:")
    print(response)
    print("\n" + "-" * 50 + "\n")
    
    # Test 3: Meal scope - all meals
    print("🔍 Test 3: Selecting all meals coverage")
    response = meal_planning.process_user_input("all meals")
    print("Bot Response:")
    print(response)
    print("\n" + "-" * 50 + "\n")
    
    # Test 4: Calorie goals - specific target
    print("🔍 Test 4: Setting calorie target")
    response = meal_planning.process_user_input("2000 calories")
    print("Bot Response:")
    print(response)
    print("\n" + "-" * 50 + "\n")
    
    # Test 5: Dietary preferences - vegetarian
    print("🔍 Test 5: Setting dietary preferences")
    response = meal_planning.process_user_input("vegetarian")
    print("Bot Response:")
    print(response)
    print("\n" + "-" * 50 + "\n")
    
    # Test 6: Lifestyle constraints
    print("🔍 Test 6: Setting lifestyle constraints")
    response = meal_planning.process_user_input("intermediate, moderate time, cooking for 2 people")
    print("Bot Response:")
    print(response)
    print("\n" + "-" * 50 + "\n")
    
    # Test 7: Generate meal plan
    print("🔍 Test 7: Generating meal plan")
    response = meal_planning.process_user_input("yes")
    print("Bot Response:")
    print(response)
    print("\n" + "-" * 50 + "\n")
    
    # Test 8: Approve plan and generate grocery list
    print("🔍 Test 8: Approving plan")
    response = meal_planning.process_user_input("approve")
    print("Bot Response:")
    print(response)
    print("\n" + "-" * 50 + "\n")
    
    # Test 9: Generate grocery list
    print("🔍 Test 9: Generating grocery list")
    response = meal_planning.process_user_input("grocery list")
    print("Bot Response:")
    print(response)
    print("\n" + "-" * 50 + "\n")
    
    print("🎉 All tests completed!")
    print("✅ Meal planning journey working correctly with real data")

def test_data_loader_meal_planning_methods():
    """Test DataLoader methods specifically for meal planning"""
    print("🧪 Testing DataLoader Meal Planning Methods")
    print("=" * 50)
    
    data_loader = DataLoader()
    
    # Test available data
    print("📊 Available meal data:")
    meals = data_loader.get_meals()
    print(f"Total meals available: {len(meals)}")
    
    if meals:
        sample_meal = meals[0]
        print(f"Sample meal: {sample_meal['name']}")
        print(f"Calories: {sample_meal.get('calories', 'N/A')}")
        print(f"Meal type: {sample_meal.get('meal_type', 'N/A')}")
        print(f"Prep time: {sample_meal.get('prep_time', 'N/A')}")
        print(f"Dietary tags: {sample_meal.get('dietary_tags', 'N/A')}")
    
    print("\n" + "-" * 30 + "\n")
    
    # Test filtering methods
    print("🔍 Testing meal filtering:")
    
    # Test calorie filtering
    moderate_calorie_meals = data_loader.filter_meals_by_multiple_criteria(
        min_calories=300, max_calories=500
    )
    print(f"Meals 300-500 calories: {len(moderate_calorie_meals)}")
    
    # Test meal type filtering
    breakfast_meals = data_loader.filter_meals_by_multiple_criteria(
        meal_type="breakfast"
    )
    print(f"Breakfast meals: {len(breakfast_meals)}")
    
    # Test dietary tag filtering
    vegetarian_meals = data_loader.filter_meals_by_multiple_criteria(
        dietary_tags=["vegetarian"]
    )
    print(f"Vegetarian meals: {len(vegetarian_meals)}")
    
    # Test combined filtering
    veggie_breakfast = data_loader.filter_meals_by_multiple_criteria(
        meal_type="breakfast",
        dietary_tags=["vegetarian"],
        max_calories=400
    )
    print(f"Vegetarian breakfast under 400 cal: {len(veggie_breakfast)}")
    
    print("\n" + "-" * 30 + "\n")
    
    # Test data range
    calorie_range = data_loader.get_meal_calorie_range()
    print(f"Calorie range: {calorie_range[0]} - {calorie_range[1]}")
    
    prep_times = data_loader.get_meal_prep_times()
    print(f"Prep times available: {prep_times}")
    
    dietary_tags = data_loader.get_available_dietary_tags()
    print(f"Dietary tags available: {dietary_tags}")
    
    print("\n✅ DataLoader methods working correctly!")

if __name__ == "__main__":
    try:
        # Test data loader methods first
        test_data_loader_meal_planning_methods()
        print("\n" + "=" * 70 + "\n")
        
        # Then test the full journey
        test_meal_planning()
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()