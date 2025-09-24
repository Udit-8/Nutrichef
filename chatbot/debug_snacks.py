#!/usr/bin/env python3
"""Debug snack meal filtering"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.data_loader import DataLoader

def debug_snack_filtering():
    """Debug why snack meals aren't being found"""
    data_loader = DataLoader()
    
    print("🔍 Debug: Snack Meal Filtering")
    print("=" * 40)
    
    # First, check if any meals have "snacks" as meal type
    all_meals = data_loader.get_meals()
    snack_meals = []
    snacks_meals = []
    
    for meal in all_meals:
        meal_types = meal.get('meal_type', [])
        if 'snack' in [mt.lower() for mt in meal_types]:
            snack_meals.append(meal)
        if 'snacks' in [mt.lower() for mt in meal_types]:
            snacks_meals.append(meal)
    
    print(f"Meals with 'snack' in meal_type: {len(snack_meals)}")
    print(f"Meals with 'snacks' in meal_type: {len(snacks_meals)}")
    
    if snack_meals:
        print("\nFirst few snack meals:")
        for meal in snack_meals[:3]:
            print(f"  - {meal['name']}: {meal['meal_type']}, {meal['calories']}cal")
    
    # Test the actual filtering used in meal planning
    print("\n" + "-" * 30)
    print("Testing meal planning snack filtering:")
    
    # This is what the meal planning algorithm calls
    snack_results = data_loader.filter_meals_by_multiple_criteria(
        meal_type="snacks",  # This might be the issue - should be "snack"
        dietary_tags=["vegetarian"],
        max_prep_time=30
    )
    
    print(f"Results for meal_type='snacks': {len(snack_results)}")
    
    # Try with "snack" instead
    snack_results2 = data_loader.filter_meals_by_multiple_criteria(
        meal_type="snack",
        dietary_tags=["vegetarian"], 
        max_prep_time=30
    )
    
    print(f"Results for meal_type='snack': {len(snack_results2)}")
    
    if snack_results2:
        print("Vegetarian snack options found:")
        for meal in snack_results2[:3]:
            print(f"  - {meal['name']}: {meal['calories']}cal, dietary_tags: {meal.get('dietary_tags', [])}")

if __name__ == "__main__":
    debug_snack_filtering()