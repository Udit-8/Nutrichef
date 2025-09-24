#!/usr/bin/env python3
"""Simple test for meal planning journey to check if meals are found"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.data_loader import DataLoader
from core.session_manager import SessionManager
from journeys.meal_planning import MealPlanningJourney

def test_simple_meal_planning():
    """Test meal planning with a simple 1-day plan"""
    print("🧪 Simple Meal Planning Test")
    print("=" * 40)
    
    # Initialize components
    data_loader = DataLoader()
    session_manager = SessionManager()
    meal_planning = MealPlanningJourney(data_loader, session_manager)
    
    # Set up a simple daily plan manually
    meal_planning.planning_duration = 1  # Just 1 day
    meal_planning.meal_types = ['breakfast', 'lunch']  # Just 2 meals
    meal_planning.daily_calorie_target = 1500  # Lower target
    meal_planning.dietary_restrictions = ['vegetarian']
    meal_planning.time_constraints = 30
    
    print(f"Planning: {meal_planning.planning_duration} day")
    print(f"Meals: {meal_planning.meal_types}")
    print(f"Calories: {meal_planning.daily_calorie_target}")
    print(f"Diet: {meal_planning.dietary_restrictions}")
    print(f"Time limit: {meal_planning.time_constraints} min")
    
    print("\n" + "-" * 30)
    
    # Test meal generation
    try:
        plan = meal_planning._generate_meal_plan()
        print("✅ Meal plan generated successfully!")
        
        if isinstance(plan, dict):
            for day, meals in plan.items():
                print(f"\n{day}:")
                for meal_type, meal in meals.items():
                    print(f"  {meal_type}: {meal['name']} ({meal['calories']}cal)")
        else:
            print(f"❌ Plan generation returned: {plan}")
    
    except Exception as e:
        print(f"❌ Error generating plan: {e}")
        import traceback
        traceback.print_exc()

def test_meal_filtering_debug():
    """Debug the meal filtering with the new calorie targets"""
    print("\n🔍 Meal Filtering Debug")
    print("=" * 40)
    
    data_loader = DataLoader()
    
    # Test with new calorie distribution for 1500 calories
    calorie_targets = {
        'breakfast': int(1500 * 0.20),  # 300 calories
        'lunch': int(1500 * 0.35),      # 525 calories
    }
    
    for meal_type, target in calorie_targets.items():
        print(f"\n{meal_type.title()} targeting {target} calories:")
        
        # Try the flexible filtering approach
        meals = data_loader.filter_meals_by_multiple_criteria(
            meal_type=meal_type,
            max_calories=target + 100,
            min_calories=target - 100,
            dietary_tags=['vegetarian'],
            max_prep_time=30
        )
        
        print(f"  Found {len(meals)} meals (±100 cal tolerance)")
        
        if meals:
            for i, meal in enumerate(meals[:3]):
                print(f"    {i+1}. {meal['name']} - {meal['calories']}cal")
        
        # Try without calorie constraints if needed
        if not meals:
            meals = data_loader.filter_meals_by_multiple_criteria(
                meal_type=meal_type,
                dietary_tags=['vegetarian'],
                max_prep_time=30
            )
            print(f"  Without calorie constraints: {len(meals)} meals")

if __name__ == "__main__":
    test_meal_filtering_debug()
    test_simple_meal_planning()