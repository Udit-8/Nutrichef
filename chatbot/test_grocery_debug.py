#!/usr/bin/env python3
"""Debug grocery list generation"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.data_loader import DataLoader
from core.session_manager import SessionManager
from journeys.meal_planning import MealPlanningJourney

def debug_grocery_generation():
    """Debug why grocery list is empty"""
    data_loader = DataLoader()
    session_manager = SessionManager()
    meal_planning = MealPlanningJourney(data_loader, session_manager)
    
    # Set up a simple plan
    meal_planning.planning_duration = 2
    meal_planning.meal_types = ['breakfast', 'lunch']
    meal_planning.daily_calorie_target = 1500
    meal_planning.dietary_restrictions = ['vegetarian']
    meal_planning.time_constraints = 30
    
    # Generate a plan
    plan = meal_planning._generate_meal_plan()
    meal_planning.meal_plan = plan
    
    print("🔍 Debug: Grocery List Generation")
    print("=" * 40)
    
    # Check if meals in plan have components
    for day, meals in plan.items():
        print(f"\n{day}:")
        for meal_type, meal in meals.items():
            print(f"  {meal_type}: {meal['name']}")
            if 'components' in meal:
                print(f"    Components: {len(meal['components'])} items")
                for comp in meal['components'][:2]:  # Show first 2
                    print(f"      - {comp.get('name', 'Unknown')}: {comp.get('amount', 0)}{comp.get('unit', '')}")
            else:
                print("    No components found!")
    
    # Test grocery list generation
    print("\n" + "-" * 30)
    print("Testing grocery list generation...")
    
    grocery_result = meal_planning._generate_grocery_list()
    print("Result length:", len(grocery_result))
    if "No Ingredients Found" in grocery_result:
        print("❌ No ingredients found in grocery generation")
    else:
        print("✅ Ingredients found!")
        print("First 200 chars:", grocery_result[:200])

if __name__ == "__main__":
    debug_grocery_generation()