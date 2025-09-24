#!/usr/bin/env python3
"""Debug meal filtering to understand why no meals are being found"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from data.data_loader import DataLoader

def debug_meal_filtering():
    """Debug meal filtering logic"""
    data_loader = DataLoader()
    
    print("🔍 Debug: Analyzing meal filtering")
    print("=" * 50)
    
    # Test basic vegetarian filtering
    vegetarian_meals = data_loader.filter_meals_by_dietary_tags(['vegetarian'])
    print(f"Vegetarian meals available: {len(vegetarian_meals)}")
    
    if vegetarian_meals:
        print("\nFirst few vegetarian meals:")
        for i, meal in enumerate(vegetarian_meals[:3]):
            print(f"{i+1}. {meal['name']} - {meal['calories']}cal, Type: {meal['meal_type']}, Prep: {meal['prep_time']}min")
    
    print("\n" + "-" * 30)
    
    # Test breakfast meals specifically
    breakfast_meals = data_loader.filter_meals_by_type(['breakfast'])
    print(f"Total breakfast meals: {len(breakfast_meals)}")
    
    vegetarian_breakfast = []
    for meal in breakfast_meals:
        if 'vegetarian' in [tag.lower() for tag in meal.get('dietary_tags', [])]:
            vegetarian_breakfast.append(meal)
    
    print(f"Vegetarian breakfast meals: {len(vegetarian_breakfast)}")
    
    print("\n" + "-" * 30)
    
    # Test specific filtering criteria from meal plan generation
    print("Testing meal plan filtering criteria:")
    
    # Breakfast with 500 calories target (±75 tolerance)
    breakfast_criteria = data_loader.filter_meals_by_multiple_criteria(
        meal_type="breakfast",
        min_calories=425,  # 500-75
        max_calories=575,  # 500+75
        dietary_tags=["vegetarian"],
        max_prep_time=30
    )
    
    print(f"Breakfast meals (425-575 cal, vegetarian, ≤30min): {len(breakfast_criteria)}")
    
    if breakfast_criteria:
        for meal in breakfast_criteria[:2]:
            print(f"  - {meal['name']}: {meal['calories']}cal, {meal['prep_time']}min")
    
    # Try with looser criteria - just vegetarian breakfast
    loose_breakfast = data_loader.filter_meals_by_multiple_criteria(
        meal_type="breakfast",
        dietary_tags=["vegetarian"]
    )
    print(f"Just vegetarian breakfast (no calorie/time limits): {len(loose_breakfast)}")
    
    # Try even looser - just breakfast
    any_breakfast = data_loader.filter_meals_by_multiple_criteria(
        meal_type="breakfast"
    )
    print(f"Any breakfast meals: {len(any_breakfast)}")
    
    print("\n" + "-" * 30)
    
    # Check what dietary tags exist in breakfast meals
    print("Dietary tags in breakfast meals:")
    all_breakfast_tags = set()
    for meal in breakfast_meals:
        all_breakfast_tags.update(meal.get('dietary_tags', []))
    
    print("Available dietary tags:", sorted(list(all_breakfast_tags)))
    
    print("\n" + "-" * 30)
    
    # Check calorie ranges for vegetarian meals
    print("Calorie analysis for vegetarian meals:")
    veg_calories = []
    for meal in vegetarian_meals:
        veg_calories.append(meal['calories'])
    
    if veg_calories:
        print(f"Vegetarian meal calories range: {min(veg_calories)} - {max(veg_calories)}")
        print(f"Average vegetarian meal calories: {sum(veg_calories)/len(veg_calories):.1f}")

if __name__ == "__main__":
    debug_meal_filtering()