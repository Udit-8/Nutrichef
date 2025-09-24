"""
Data Loader for Nutrition Chatbot
Handles loading and accessing JSON data files
"""

import json
import os
from typing import Dict, List, Any, Optional
from pathlib import Path

class DataLoader:
    """Handles loading and accessing nutrition data"""
    
    def __init__(self):
        # Get the path to the raw_data folder
        self.base_path = Path(__file__).parent.parent.parent / "raw_data"
        self._data_cache = {}
        self._load_all_data()
    
    def _load_all_data(self) -> None:
        """Load all JSON data files into memory"""
        data_files = {
            'recipes': 'recipes_raw.json',
            'foods_nutrition': 'foods_nutrition_raw.json',
            'meal_suggestions': 'meal_suggestions_raw.json',
            'cooking_instructions': 'cooking_instructions_raw.json',
            'grocery_support': 'grocery_support_raw.json'
        }
        
        for data_key, filename in data_files.items():
            file_path = self.base_path / filename
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    self._data_cache[data_key] = json.load(f)
                print(f"✅ Loaded {data_key} data from {filename}")
            except FileNotFoundError:
                print(f"⚠️ Warning: {filename} not found")
                self._data_cache[data_key] = {}
            except json.JSONDecodeError as e:
                print(f"⚠️ Warning: Error parsing {filename}: {e}")
                self._data_cache[data_key] = {}
    
    def get_recipes(self) -> List[Dict[str, Any]]:
        """Get all recipes"""
        return self._data_cache.get('recipes', {}).get('recipes', [])
    
    def get_recipe_by_id(self, recipe_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific recipe by ID"""
        recipes = self.get_recipes()
        for recipe in recipes:
            if recipe.get('id') == recipe_id or recipe.get('recipe_id') == recipe_id:
                return recipe
        return None
    
    def search_recipes_by_name(self, search_term: str) -> List[Dict[str, Any]]:
        """Search recipes by name"""
        recipes = self.get_recipes()
        search_term_lower = search_term.lower()
        
        return [
            recipe for recipe in recipes
            if search_term_lower in recipe.get('name', '').lower()
        ]
    
    def filter_recipes_by_cuisine(self, cuisine: str) -> List[Dict[str, Any]]:
        """Filter recipes by cuisine type"""
        recipes = self.get_recipes()
        cuisine_lower = cuisine.lower()
        
        return [
            recipe for recipe in recipes
            if recipe.get('cuisine', '').lower() == cuisine_lower
        ]
    
    def filter_recipes_by_dietary_restrictions(self, restrictions: List[str]) -> List[Dict[str, Any]]:
        """Filter recipes by dietary restrictions"""
        recipes = self.get_recipes()
        filtered_recipes = []
        
        for recipe in recipes:
            recipe_tags = [tag.lower() for tag in recipe.get('dietary_tags', [])]
            # Check if recipe satisfies all restrictions
            if all(restriction.lower() in recipe_tags for restriction in restrictions):
                filtered_recipes.append(recipe)
        
        return filtered_recipes
    
    def filter_recipes_by_prep_time(self, max_minutes: int) -> List[Dict[str, Any]]:
        """Filter recipes by maximum preparation time"""
        recipes = self.get_recipes()
        
        return [
            recipe for recipe in recipes
            if recipe.get('prep_time', float('inf')) <= max_minutes
        ]
    
    def filter_recipes_by_ingredients(self, available_ingredients: List[str]) -> List[Dict[str, Any]]:
        """Filter recipes that can be made with available ingredients"""
        recipes = self.get_recipes()
        filtered_recipes = []
        available_lower = [ing.lower() for ing in available_ingredients]
        
        for recipe in recipes:
            recipe_ingredients = [
                ing.get('name', '').lower() 
                for ing in recipe.get('ingredients', [])
            ]
            
            # Check if at least 70% of recipe ingredients are available
            matching_ingredients = sum(
                1 for ing in recipe_ingredients 
                if any(avail in ing for avail in available_lower)
            )
            
            if len(recipe_ingredients) > 0:
                match_percentage = matching_ingredients / len(recipe_ingredients)
                if match_percentage >= 0.7:
                    filtered_recipes.append(recipe)
        
        return filtered_recipes
    
    def get_cuisine_types(self) -> List[str]:
        """Get all available cuisine types"""
        recipes = self.get_recipes()
        cuisine_types = set()
        
        for recipe in recipes:
            cuisine = recipe.get('cuisine', '')
            if cuisine:
                cuisine_types.add(cuisine)
        
        return sorted(list(cuisine_types))
    
    def get_dietary_tags(self) -> List[str]:
        """Get all available dietary tags"""
        recipes = self.get_recipes()
        dietary_tags = set()
        
        for recipe in recipes:
            tags = recipe.get('dietary_tags', [])
            dietary_tags.update(tags)
        
        return sorted(list(dietary_tags))
    
    def get_cooking_instructions(self, recipe_id: str) -> List[Dict[str, Any]]:
        """Get cooking instructions for a recipe"""
        cooking_data = self._data_cache.get('cooking_instructions', {})
        instructions = cooking_data.get('cooking_instructions', [])
        
        for instruction in instructions:
            if instruction.get('recipe_id') == recipe_id:
                return instruction.get('steps', [])
        
        return []
    
    def get_meals(self) -> List[Dict[str, Any]]:
        """Get all meal suggestions"""
        return self._data_cache.get('meal_suggestions', {}).get('meal_suggestions', [])
    
    def get_meal_by_id(self, meal_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific meal by ID"""
        meals = self.get_meals()
        for meal in meals:
            if meal.get('id') == meal_id:
                return meal
        return None
    
    def filter_meals_by_calories(self, min_calories: int, max_calories: int) -> List[Dict[str, Any]]:
        """Filter meals by calorie range"""
        meals = self.get_meals()
        return [
            meal for meal in meals
            if min_calories <= meal.get('calories', 0) <= max_calories
        ]
    
    def filter_meals_by_type(self, meal_types: List[str]) -> List[Dict[str, Any]]:
        """Filter meals by meal type (breakfast, lunch, dinner, snack)"""
        meals = self.get_meals()
        meal_types_lower = [mt.lower() for mt in meal_types]
        
        filtered_meals = []
        for meal in meals:
            meal_type_list = meal.get('meal_type', [])
            # Check if any of the meal's types match our target types
            if any(mt.lower() in meal_types_lower for mt in meal_type_list):
                filtered_meals.append(meal)
        
        return filtered_meals
    
    def filter_meals_by_dietary_tags(self, dietary_tags: List[str]) -> List[Dict[str, Any]]:
        """Filter meals by dietary tags"""
        if not dietary_tags:
            return self.get_meals()
        
        meals = self.get_meals()
        dietary_tags_lower = [tag.lower() for tag in dietary_tags]
        
        filtered_meals = []
        for meal in meals:
            meal_tags = [tag.lower() for tag in meal.get('dietary_tags', [])]
            # Check if meal contains all required dietary tags
            if all(tag in meal_tags for tag in dietary_tags_lower):
                filtered_meals.append(meal)
        
        return filtered_meals
    
    def filter_meals_by_multiple_criteria(self, 
                                        min_calories: int = 0, 
                                        max_calories: int = float('inf'),
                                        meal_type: str = None,
                                        meal_types: List[str] = None,
                                        dietary_tags: List[str] = None,
                                        max_prep_time: int = None) -> List[Dict[str, Any]]:
        """Filter meals by multiple criteria"""
        meals = self.get_meals()
        
        # Apply calorie filter
        meals = [meal for meal in meals 
                if min_calories <= meal.get('calories', 0) <= max_calories]
        
        # Apply single meal type filter (for meal planning)
        if meal_type:
            meal_type_lower = meal_type.lower()
            meals = [meal for meal in meals
                    if meal_type_lower in [mt.lower() for mt in meal.get('meal_type', [])]]
        
        # Apply meal type filter (multiple types)
        if meal_types:
            meal_types_lower = [mt.lower() for mt in meal_types]
            meals = [meal for meal in meals
                    if any(mt.lower() in meal_types_lower 
                          for mt in meal.get('meal_type', []))]
        
        # Apply dietary tags filter
        if dietary_tags:
            dietary_tags_lower = [tag.lower() for tag in dietary_tags]
            meals = [meal for meal in meals
                    if all(tag in [t.lower() for t in meal.get('dietary_tags', [])]
                          for tag in dietary_tags_lower)]
        
        # Apply prep time filter
        if max_prep_time:
            meals = [meal for meal in meals
                    if meal.get('prep_time', float('inf')) <= max_prep_time]
        
        return meals
    
    def get_meal_dietary_tags(self) -> List[str]:
        """Get all available dietary tags from meals"""
        meals = self.get_meals()
        dietary_tags = set()
        
        for meal in meals:
            tags = meal.get('dietary_tags', [])
            dietary_tags.update(tags)
        
        return sorted(list(dietary_tags))
    
    def get_meal_types(self) -> List[str]:
        """Get all available meal types"""
        meals = self.get_meals()
        meal_types = set()
        
        for meal in meals:
            types = meal.get('meal_type', [])
            meal_types.update(types)
        
        return sorted(list(meal_types))
    
    def find_similar_meals(self, reference_meal: Dict[str, Any], limit: int = 5) -> List[Dict[str, Any]]:
        """Find meals similar to the reference meal"""
        meals = self.get_meals()
        reference_id = reference_meal.get('id')
        reference_calories = reference_meal.get('calories', 0)
        reference_tags = set(reference_meal.get('dietary_tags', []))
        reference_types = set(reference_meal.get('meal_type', []))
        
        similar_meals = []
        for meal in meals:
            if meal.get('id') == reference_id:
                continue  # Skip the reference meal itself
            
            # Calculate similarity score
            score = 0
            
            # Calorie similarity (within 100 calories gets points)
            calorie_diff = abs(meal.get('calories', 0) - reference_calories)
            if calorie_diff <= 50:
                score += 3
            elif calorie_diff <= 100:
                score += 2
            elif calorie_diff <= 150:
                score += 1
            
            # Dietary tags similarity
            meal_tags = set(meal.get('dietary_tags', []))
            common_tags = reference_tags.intersection(meal_tags)
            score += len(common_tags)
            
            # Meal type similarity  
            meal_types = set(meal.get('meal_type', []))
            common_types = reference_types.intersection(meal_types)
            score += len(common_types) * 2
            
            if score > 0:
                similar_meals.append((meal, score))
        
        # Sort by similarity score and return top results
        similar_meals.sort(key=lambda x: x[1], reverse=True)
        return [meal for meal, score in similar_meals[:limit]]
    
    def get_foods_nutrition(self) -> List[Dict[str, Any]]:
        """Get all foods nutrition data"""
        return self._data_cache.get('foods_nutrition', {}).get('foods', [])
    
    def get_food_by_id(self, food_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific food item by ID"""
        foods = self.get_foods_nutrition()
        for food in foods:
            if food.get('food_id') == food_id:
                return food
        return None
    
    def get_available_dietary_tags(self) -> List[str]:
        """Get all available dietary tags from meals (for meal planning)"""
        return self.get_meal_dietary_tags()
    
    def get_meal_prep_times(self) -> List[int]:
        """Get all unique prep times from meals"""
        meals = self.get_meals()
        prep_times = set()
        
        for meal in meals:
            prep_time = meal.get('prep_time')
            if prep_time:
                prep_times.add(prep_time)
        
        return sorted(list(prep_times))
    
    def get_meal_calorie_range(self) -> tuple:
        """Get the min and max calorie values from meals"""
        meals = self.get_meals()
        if not meals:
            return (0, 0)
        
        calories = [meal.get('calories', 0) for meal in meals]
        return (min(calories), max(calories))
    
    def filter_meals_by_nutrition_criteria(self, 
                                         min_protein: float = None,
                                         max_protein: float = None,
                                         min_carbs: float = None,
                                         max_carbs: float = None,
                                         min_fat: float = None,
                                         max_fat: float = None,
                                         min_fiber: float = None) -> List[Dict[str, Any]]:
        """Filter meals by nutritional criteria"""
        meals = self.get_meals()
        filtered_meals = []
        
        for meal in meals:
            nutrition = meal.get('nutrition', {})
            protein = nutrition.get('protein', 0)
            carbs = nutrition.get('carbs', nutrition.get('carbohydrates', 0)) 
            fat = nutrition.get('fat', 0)
            fiber = nutrition.get('fiber', 0)
            
            # Check all criteria
            if min_protein and protein < min_protein:
                continue
            if max_protein and protein > max_protein:
                continue
            if min_carbs and carbs < min_carbs:
                continue
            if max_carbs and carbs > max_carbs:
                continue
            if min_fat and fat < min_fat:
                continue
            if max_fat and fat > max_fat:
                continue
            if min_fiber and fiber < min_fiber:
                continue
            
            filtered_meals.append(meal)
        
        return filtered_meals
    
    def get_meal_nutrition_summary(self, meals: List[Dict[str, Any]]) -> Dict[str, float]:
        """Calculate nutrition summary for a list of meals"""
        if not meals:
            return {'calories': 0, 'protein': 0, 'carbohydrates': 0, 'fat': 0, 'fiber': 0}
        
        totals = {'calories': 0, 'protein': 0, 'carbohydrates': 0, 'fat': 0, 'fiber': 0}
        
        for meal in meals:
            totals['calories'] += meal.get('calories', 0)
            nutrition = meal.get('nutrition', {})
            totals['protein'] += nutrition.get('protein', 0)
            totals['carbohydrates'] += nutrition.get('carbs', nutrition.get('carbohydrates', 0))
            totals['fat'] += nutrition.get('fat', 0)
            totals['fiber'] += nutrition.get('fiber', 0)
        
        return totals
    
    def get_grocery_support(self) -> Dict[str, Any]:
        """Get grocery support data"""
        return self._data_cache.get('grocery_support', {})
    
    def get_unit_conversions(self) -> Dict[str, Any]:
        """Get unit conversion data"""
        grocery_data = self.get_grocery_support()
        return grocery_data.get('unit_conversions', {})
    
    def get_store_sections(self) -> Dict[str, Any]:
        """Get store section organization data"""
        grocery_data = self.get_grocery_support()
        return grocery_data.get('store_sections', {})
    
    def get_ingredient_aliases(self) -> Dict[str, List[str]]:
        """Get ingredient aliases for smart matching"""
        grocery_data = self.get_grocery_support()
        return grocery_data.get('ingredient_aliases', {})
    
    def get_substitutions(self) -> Dict[str, List[Dict[str, Any]]]:
        """Get ingredient substitution data"""
        grocery_data = self.get_grocery_support()
        return grocery_data.get('substitutions', {})
    
    def find_ingredient_by_alias(self, ingredient_name: str) -> Optional[str]:
        """Find the canonical ingredient name using aliases"""
        ingredient_name_lower = ingredient_name.lower().strip()
        aliases = self.get_ingredient_aliases()
        
        # Check if it's already a canonical name
        if ingredient_name_lower in aliases:
            return ingredient_name_lower
        
        # Search through aliases
        for canonical_name, alias_list in aliases.items():
            for alias in alias_list:
                if ingredient_name_lower == alias.lower():
                    return canonical_name
        
        return None
    
    def get_food_category_by_id(self, food_id: str) -> Optional[str]:
        """Get food category for store section mapping"""
        food_item = self.get_food_by_id(food_id)
        if food_item:
            return food_item.get('category')
        return None
    
    def map_category_to_store_section(self, category: str) -> Optional[Dict[str, Any]]:
        """Map food category to store section"""
        if not category:
            return None
            
        store_sections = self.get_store_sections()
        category_lower = category.lower()
        
        for section_id, section_data in store_sections.items():
            categories = section_data.get('categories', [])
            if category_lower in [cat.lower() for cat in categories]:
                return {
                    'section_id': section_id,
                    'display_name': section_data.get('display_name', section_id),
                    'icon': section_data.get('icon', '📦'),
                    'order': section_data.get('order', 99),
                    'shopping_tips': section_data.get('shopping_tips', '')
                }
        
        # Default to pantry section if no match
        return {
            'section_id': 'pantry_grains',
            'display_name': 'Pantry & Grains',
            'icon': '📦',
            'order': 99,
            'shopping_tips': 'Store in cool, dry place'
        }
    
    def convert_unit(self, ingredient: str, amount: float, from_unit: str, to_unit: str) -> float:
        """Convert units using conversion tables"""
        conversions = self.get_unit_conversions()
        ingredient_lower = ingredient.lower().replace(' ', '_')
        
        # Check for ingredient-specific conversions first
        ingredient_conversions = conversions.get('ingredient_specific', {}).get(ingredient_lower, {})
        
        from_key = f"1_{from_unit.lower()}"
        if from_key in ingredient_conversions:
            # Extract numeric value from conversion (e.g., "120g" -> 120)
            conversion_str = ingredient_conversions[from_key]
            import re
            numbers = re.findall(r'\d+', conversion_str)
            if numbers:
                conversion_factor = float(numbers[0])
                if to_unit.lower() in conversion_str.lower():
                    return amount * conversion_factor
        
        # Fallback to general volume/weight conversions
        volume_conversions = conversions.get('volume', {})
        weight_conversions = conversions.get('weight', {})
        
        # Volume conversions
        from_ml_key = f"{from_unit.lower()}_to_ml"
        to_ml_key = f"{to_unit.lower()}_to_ml"
        
        if from_ml_key in volume_conversions:
            if to_unit.lower() == 'ml':
                return amount * volume_conversions[from_ml_key]
            elif to_ml_key in volume_conversions:
                ml_amount = amount * volume_conversions[from_ml_key]
                return ml_amount / volume_conversions[to_ml_key]
        
        # Weight conversions
        from_g_key = f"{from_unit.lower()}_to_g"
        to_g_key = f"{to_unit.lower()}_to_g"
        
        if from_g_key in weight_conversions:
            if to_unit.lower() == 'g':
                return amount * weight_conversions[from_g_key]
            elif to_g_key in weight_conversions:
                g_amount = amount * weight_conversions[from_g_key]
                return g_amount / weight_conversions[to_g_key]
        
        # If no conversion found, return original amount
        return amount
    
    def get_substitutions_for_ingredient(self, ingredient: str, dietary_restrictions: List[str] = None) -> List[Dict[str, Any]]:
        """Get substitution options for an ingredient"""
        substitutions = self.get_substitutions()
        ingredient_lower = ingredient.lower().replace(' ', '_')
        
        # Find substitutions for this ingredient
        ingredient_subs = substitutions.get(ingredient_lower, [])
        
        if not dietary_restrictions:
            return ingredient_subs
        
        # Filter by dietary restrictions
        compatible_subs = []
        dietary_restrictions_lower = [dr.lower() for dr in dietary_restrictions]
        
        for sub in ingredient_subs:
            sub_tags = [tag.lower() for tag in sub.get('dietary_tags', [])]
            # Check if substitution is compatible with dietary restrictions
            if any(dr in sub_tags for dr in dietary_restrictions_lower):
                compatible_subs.append(sub)
        
        return compatible_subs if compatible_subs else ingredient_subs
    
    def reload_data(self) -> None:
        """Reload all data from files"""
        self._data_cache.clear()
        self._load_all_data()
    
    # ========================================
    # COOKING GUIDANCE METHODS
    # ========================================
    
    def get_cooking_instructions(self) -> List[Dict[str, Any]]:
        """Get all cooking instructions"""
        return self._data_cache.get('cooking_instructions', {}).get('cooking_instructions', [])
    
    def get_cooking_instructions_by_recipe_id(self, recipe_id: str) -> Optional[Dict[str, Any]]:
        """Get cooking instructions for a specific recipe"""
        cooking_instructions = self.get_cooking_instructions()
        for instruction in cooking_instructions:
            if instruction.get('recipe_id') == recipe_id:
                return instruction
        return None
    
    def get_recipe_cooking_data(self, recipe_id: str) -> Optional[Dict[str, Any]]:
        """Get combined recipe and cooking instruction data"""
        recipe = self.get_recipe_by_id(recipe_id)
        cooking_instructions = self.get_cooking_instructions_by_recipe_id(recipe_id)
        
        if recipe and cooking_instructions:
            return {
                'recipe': recipe,
                'cooking_instructions': cooking_instructions
            }
        elif recipe:
            # Return recipe even without cooking instructions for basic functionality
            return {
                'recipe': recipe,
                'cooking_instructions': None
            }
        return None
    
    def scale_recipe_ingredients(self, recipe: Dict[str, Any], scale_factor: float) -> List[Dict[str, Any]]:
        """Scale recipe ingredients by a factor"""
        if not recipe or 'ingredients' not in recipe:
            return []
        
        scaled_ingredients = []
        for ingredient in recipe['ingredients']:
            scaled_ingredient = ingredient.copy()
            if 'amount' in scaled_ingredient:
                try:
                    scaled_ingredient['amount'] = scaled_ingredient['amount'] * scale_factor
                except (TypeError, ValueError):
                    # Keep original amount if scaling fails
                    pass
            scaled_ingredients.append(scaled_ingredient)
        
        return scaled_ingredients
    
    def get_recipe_equipment_list(self, recipe_id: str) -> List[str]:
        """Get equipment needed for a recipe"""
        cooking_instructions = self.get_cooking_instructions_by_recipe_id(recipe_id)
        if cooking_instructions and 'equipment_needed' in cooking_instructions:
            return cooking_instructions['equipment_needed']
        return []
    
    def get_recipe_total_time(self, recipe_id: str) -> int:
        """Get total estimated active time for a recipe"""
        cooking_instructions = self.get_cooking_instructions_by_recipe_id(recipe_id)
        if cooking_instructions and 'estimated_active_time' in cooking_instructions:
            return cooking_instructions['estimated_active_time']
        return 0
    
    def get_cooking_steps_by_phase(self, recipe_id: str, phase: str = None) -> List[Dict[str, Any]]:
        """Get cooking steps, optionally filtered by phase"""
        cooking_instructions = self.get_cooking_instructions_by_recipe_id(recipe_id)
        if not cooking_instructions or 'steps' not in cooking_instructions:
            return []
        
        steps = cooking_instructions['steps']
        if phase:
            steps = [step for step in steps if step.get('phase', '').lower() == phase.lower()]
        
        return steps
    
    def get_prep_steps(self, recipe_id: str) -> List[Dict[str, Any]]:
        """Get preparation steps for a recipe"""
        return self.get_cooking_steps_by_phase(recipe_id, 'prep')
    
    def get_cooking_phases(self, recipe_id: str) -> List[str]:
        """Get all unique phases for a recipe"""
        cooking_instructions = self.get_cooking_instructions_by_recipe_id(recipe_id)
        if not cooking_instructions or 'steps' not in cooking_instructions:
            return []
        
        phases = set()
        for step in cooking_instructions['steps']:
            phase = step.get('phase', '')
            if phase:
                phases.add(phase)
        
        return sorted(list(phases))
    
    def search_recipes_for_cooking(self, search_term: str) -> List[Dict[str, Any]]:
        """Search recipes that have cooking instructions available"""
        available_recipe_ids = set()
        cooking_instructions = self.get_cooking_instructions()
        
        for instruction in cooking_instructions:
            recipe_id = instruction.get('recipe_id')
            if recipe_id:
                available_recipe_ids.add(recipe_id)
        
        # Get recipes that match search term and have cooking instructions
        matching_recipes = []
        recipes = self.search_recipes_by_name(search_term)
        
        for recipe in recipes:
            recipe_id = recipe.get('id') or recipe.get('recipe_id')
            if recipe_id in available_recipe_ids:
                matching_recipes.append(recipe)
        
        return matching_recipes
    
    # ========================================
    # FOOD CALORIE TRACKING METHODS
    # ========================================
    
    def get_foods_nutrition(self) -> List[Dict[str, Any]]:
        """Get all foods nutrition data"""
        return self._data_cache.get('foods_nutrition', {}).get('foods', [])
    
    def get_food_by_id(self, food_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific food item by ID"""
        foods = self.get_foods_nutrition()
        for food in foods:
            if food.get('id') == food_id:
                return food
        return None
    
    def search_foods_by_name(self, search_term: str) -> List[Dict[str, Any]]:
        """Search foods by name and common names"""
        if not search_term or not search_term.strip():
            return []
            
        foods = self.get_foods_nutrition()
        search_term_lower = search_term.lower().strip()
        matching_foods = []
        
        for food in foods:
            # Check food name
            food_name = food.get('name', '').lower()
            if search_term_lower in food_name:
                matching_foods.append(food)
                continue
            
            # Check common names
            common_names = food.get('common_names', [])
            for common_name in common_names:
                if search_term_lower in common_name.lower():
                    matching_foods.append(food)
                    break
        
        return matching_foods
    
    def get_foods_by_category(self, category: str) -> List[Dict[str, Any]]:
        """Get foods by category"""
        foods = self.get_foods_nutrition()
        category_lower = category.lower()
        
        return [
            food for food in foods
            if food.get('category', '').lower() == category_lower
        ]
    
    def get_foods_by_dietary_tags(self, tags: List[str]) -> List[Dict[str, Any]]:
        """Get foods that match dietary tags"""
        if not tags:
            return self.get_foods_nutrition()
        
        foods = self.get_foods_nutrition()
        tags_lower = [tag.lower() for tag in tags]
        matching_foods = []
        
        for food in foods:
            # Check multiple tag fields (raw format uses dietary_tags)
            food_tags = [tag.lower() for tag in food.get('tags', [])]
            dietary_tags = [tag.lower() for tag in food.get('dietary_tags', [])]  # Raw format
            health_benefits = [benefit.lower() for benefit in food.get('health_benefits', [])]
            all_food_tags = food_tags + dietary_tags + health_benefits
            
            # Check if food has any of the requested tags
            if any(tag in all_food_tags for tag in tags_lower):
                matching_foods.append(food)
        
        return matching_foods
    
    def get_food_serving_options(self, food_id: str) -> List[Dict[str, Any]]:
        """Get serving options for a specific food"""
        food = self.get_food_by_id(food_id)
        if food:
            # Check if food has serving_options (new format)
            if 'serving_options' in food:
                return food['serving_options']
            
            # Convert from raw format (per_100g) to serving options format
            elif 'per_100g' in food:
                per_100g = food['per_100g']
                serving_options = [{
                    'id': 'serving_100g',
                    'description': '100g',
                    'weight_g': 100,
                    'calories': per_100g.get('calories', 0),
                    'macros': {
                        'protein': per_100g.get('protein', 0),
                        'carbs': per_100g.get('carbs', 0),
                        'fat': per_100g.get('fat', 0),
                        'fiber': per_100g.get('fiber', 0),
                        'sugar': per_100g.get('sugar', 0)
                    }
                }]
                
                # Add common serving sizes based on category
                category = food.get('category', '').lower()
                base_calories = per_100g.get('calories', 0)
                base_macros = {
                    'protein': per_100g.get('protein', 0),
                    'carbs': per_100g.get('carbs', 0),
                    'fat': per_100g.get('fat', 0),
                    'fiber': per_100g.get('fiber', 0),
                    'sugar': per_100g.get('sugar', 0)
                }
                
                # Add category-specific servings
                if category == 'protein':
                    # Add 85g serving (typical chicken breast piece)
                    serving_options.append({
                        'id': 'serving_85g',
                        'description': '1 piece (85g)',
                        'weight_g': 85,
                        'calories': int(base_calories * 0.85),
                        'macros': {k: round(v * 0.85, 1) for k, v in base_macros.items()}
                    })
                    
                    # Add 150g serving (large portion)
                    serving_options.append({
                        'id': 'serving_150g', 
                        'description': '1 large serving (150g)',
                        'weight_g': 150,
                        'calories': int(base_calories * 1.5),
                        'macros': {k: round(v * 1.5, 1) for k, v in base_macros.items()}
                    })
                
                elif category in ['dairy', 'vegetable', 'grain']:
                    # Add cup serving
                    cup_weight = 200 if category == 'dairy' else 150
                    factor = cup_weight / 100
                    serving_options.append({
                        'id': f'serving_{cup_weight}g',
                        'description': f'1 cup ({cup_weight}g)',
                        'weight_g': cup_weight,
                        'calories': int(base_calories * factor),
                        'macros': {k: round(v * factor, 1) for k, v in base_macros.items()}
                    })
                
                return serving_options
        
        return []
    
    def get_food_serving_by_id(self, food_id: str, serving_id: str) -> Optional[Dict[str, Any]]:
        """Get specific serving option for a food"""
        serving_options = self.get_food_serving_options(food_id)
        for serving in serving_options:
            if serving.get('id') == serving_id:
                return serving
        return None
    
    def get_food_categories(self) -> List[str]:
        """Get all available food categories"""
        foods = self.get_foods_nutrition()
        categories = set()
        
        for food in foods:
            category = food.get('category', '')
            if category:
                categories.add(category)
        
        return sorted(list(categories))
    
    def get_food_allergens(self, food_id: str) -> List[str]:
        """Get allergens for a specific food"""
        food = self.get_food_by_id(food_id)
        if food:
            return food.get('allergens', [])
        return []
    
    def get_popular_foods(self, limit: int = 20) -> List[Dict[str, Any]]:
        """Get popular foods (foods with more serving options are considered popular)"""
        foods = self.get_foods_nutrition()
        
        # Sort by number of serving options (popularity indicator)
        foods_with_popularity = []
        for food in foods:
            serving_count = len(food.get('serving_options', []))
            foods_with_popularity.append((food, serving_count))
        
        # Sort by serving count descending
        foods_with_popularity.sort(key=lambda x: x[1], reverse=True)
        
        return [food for food, count in foods_with_popularity[:limit]]
    
    def calculate_food_nutrition_per_100g(self, food: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate nutrition per 100g from serving options or raw data"""
        
        # Check if food has direct per_100g data (raw format)
        if 'per_100g' in food:
            per_100g = food['per_100g']
            return {
                'calories': per_100g.get('calories', 0),
                'macros': {
                    'protein': per_100g.get('protein', 0),
                    'carbs': per_100g.get('carbs', 0),
                    'fat': per_100g.get('fat', 0),
                    'fiber': per_100g.get('fiber', 0),
                    'sugar': per_100g.get('sugar', 0)
                }
            }
        
        # Otherwise use serving options (processed format)
        serving_options = food.get('serving_options', [])
        
        # Find 100g serving if available
        for serving in serving_options:
            if serving.get('weight_g') == 100:
                return {
                    'calories': serving.get('calories', 0),
                    'macros': serving.get('macros', {})
                }
        
        # If no 100g serving, calculate from first available serving
        if serving_options:
            first_serving = serving_options[0]
            weight_g = first_serving.get('weight_g', 100)
            calories = first_serving.get('calories', 0)
            macros = first_serving.get('macros', {})
            
            # Scale to 100g
            scale_factor = 100 / weight_g if weight_g > 0 else 1
            
            scaled_macros = {}
            for macro, value in macros.items():
                scaled_macros[macro] = round(value * scale_factor, 1)
            
            return {
                'calories': int(calories * scale_factor),
                'macros': scaled_macros
            }
        
        return {'calories': 0, 'macros': {}}
    
    def find_food_by_barcode(self, barcode: str) -> Optional[Dict[str, Any]]:
        """Find food by barcode"""
        foods = self.get_foods_nutrition()
        for food in foods:
            if food.get('barcode') == barcode:
                return food
        return None
    
    def get_foods_with_high_protein(self, min_protein_per_100g: float = 15.0) -> List[Dict[str, Any]]:
        """Get foods with high protein content"""
        foods = self.get_foods_nutrition()
        high_protein_foods = []
        
        for food in foods:
            nutrition_100g = self.calculate_food_nutrition_per_100g(food)
            protein = nutrition_100g.get('macros', {}).get('protein', 0)
            
            if protein >= min_protein_per_100g:
                high_protein_foods.append(food)
        
        return high_protein_foods
    
    def get_low_calorie_foods(self, max_calories_per_100g: int = 100) -> List[Dict[str, Any]]:
        """Get low calorie foods"""
        foods = self.get_foods_nutrition()
        low_cal_foods = []
        
        for food in foods:
            nutrition_100g = self.calculate_food_nutrition_per_100g(food)
            calories = nutrition_100g.get('calories', 0)
            
            if calories <= max_calories_per_100g:
                low_cal_foods.append(food)
        
        return low_cal_foods
    
    def get_nutrition_search_suggestions(self, partial_query: str) -> List[str]:
        """Get search suggestions based on partial input"""
        if not partial_query or len(partial_query) < 2:
            return []
        
        foods = self.get_foods_nutrition()
        suggestions = set()
        partial_lower = partial_query.lower()
        
        for food in foods:
            # Food name suggestions
            food_name = food.get('name', '')
            if partial_lower in food_name.lower():
                suggestions.add(food_name)
            
            # Common name suggestions
            for common_name in food.get('common_names', []):
                if partial_lower in common_name.lower():
                    suggestions.add(common_name)
        
        return sorted(list(suggestions))[:10]  # Return top 10 suggestions