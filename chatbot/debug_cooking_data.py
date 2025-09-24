#!/usr/bin/env python3
"""
Debug script to check cooking data loading
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__)))

from data.data_loader import DataLoader

def debug_cooking_data():
    print("🔍 DEBUGGING COOKING DATA LOADING")
    print("=" * 40)
    
    data_loader = DataLoader()
    
    # Test basic recipe loading
    print("\n📚 Testing Recipe Loading:")
    recipes = data_loader.get_recipes()
    print(f"Total recipes loaded: {len(recipes)}")
    
    if recipes:
        first_recipe = recipes[0]
        print(f"First recipe ID: {first_recipe.get('recipe_id')}")
        print(f"First recipe name: {first_recipe.get('name')}")
    
    # Test cooking instructions loading
    print("\n👨‍🍳 Testing Cooking Instructions:")
    instructions = data_loader.get_cooking_instructions()
    print(f"Total cooking instructions: {len(instructions)}")
    
    if instructions:
        first_instruction = instructions[0]
        print(f"First instruction recipe ID: {first_instruction.get('recipe_id')}")
        print(f"First instruction recipe name: {first_instruction.get('recipe_name')}")
    
    # Test combined data loading
    print("\n🔗 Testing Combined Data Loading:")
    test_recipe_id = "recipe_001"
    
    recipe = data_loader.get_recipe_by_id(test_recipe_id)
    print(f"Recipe {test_recipe_id} found: {recipe is not None}")
    if recipe:
        print(f"Recipe name: {recipe.get('name')}")
    
    cooking_instruction = data_loader.get_cooking_instructions_by_recipe_id(test_recipe_id)
    print(f"Cooking instruction for {test_recipe_id} found: {cooking_instruction is not None}")
    if cooking_instruction:
        print(f"Instruction recipe name: {cooking_instruction.get('recipe_name')}")
    
    # Test the combined function
    combined = data_loader.get_recipe_cooking_data(test_recipe_id)
    print(f"Combined data for {test_recipe_id}: {combined is not None}")
    if combined:
        print(f"Contains recipe: {'recipe' in combined}")
        print(f"Contains instructions: {'cooking_instructions' in combined and combined['cooking_instructions'] is not None}")
    
    print(f"\n🎯 DEBUGGING COMPLETE")

if __name__ == "__main__":
    debug_cooking_data()