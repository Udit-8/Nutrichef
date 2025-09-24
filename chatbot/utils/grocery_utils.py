"""
Grocery Utility Classes
Handles ingredient extraction, consolidation, and store organization for grocery assistance
"""

import re
from typing import Dict, List, Any, Optional, Tuple
from collections import defaultdict

class IngredientExtractor:
    """Extracts ingredients from recipes, meal plans, and manual input"""
    
    def __init__(self, data_loader):
        self.data_loader = data_loader
    
    def extract_from_recipes(self, recipe_ids: List[str], servings_multiplier: float = 1.0) -> List[Dict[str, Any]]:
        """Extract ingredients from selected recipes"""
        ingredients = []
        
        for recipe_id in recipe_ids:
            recipe = self.data_loader.get_recipe_by_id(recipe_id)
            if not recipe:
                continue
                
            recipe_ingredients = recipe.get('ingredients', [])
            for ingredient in recipe_ingredients:
                # Scale quantities if needed
                amount = ingredient.get('amount', 1) * servings_multiplier
                
                extracted_ingredient = {
                    'name': ingredient.get('name', ''),
                    'amount': amount,
                    'unit': ingredient.get('unit', ''),
                    'source': f"recipe:{recipe.get('name', recipe_id)}",
                    'food_id': ingredient.get('food_id'),
                    'raw_ingredient': ingredient
                }
                ingredients.append(extracted_ingredient)
        
        return ingredients
    
    def extract_from_meal_plan(self, meal_plan: Dict[str, Any], servings_multiplier: float = 1.0) -> List[Dict[str, Any]]:
        """Extract ingredients from meal plan components"""
        ingredients = []
        
        for day_name, day_meals in meal_plan.items():
            if not isinstance(day_meals, dict):
                continue
                
            for meal_type, meal in day_meals.items():
                if not isinstance(meal, dict) or 'components' not in meal:
                    continue
                
                meal_components = meal.get('components', [])
                for component in meal_components:
                    # Scale quantities if needed
                    amount = component.get('amount', 1) * servings_multiplier
                    
                    extracted_ingredient = {
                        'name': component.get('name', ''),
                        'amount': amount,
                        'unit': component.get('unit', ''),
                        'source': f"meal_plan:{day_name}:{meal_type}",
                        'food_id': component.get('food_id'),
                        'raw_component': component
                    }
                    ingredients.append(extracted_ingredient)
        
        return ingredients
    
    def extract_from_manual_input(self, user_input: str) -> List[Dict[str, Any]]:
        """Extract ingredients from manual text input"""
        ingredients = []
        
        # Split input by common separators
        items = re.split(r'[,\n;]', user_input)
        
        for item in items:
            item = item.strip()
            if not item:
                continue
            
            # Try to parse quantity and unit
            parsed = self._parse_ingredient_text(item)
            if parsed:
                # Try to find canonical ingredient name using aliases
                canonical_name = self.data_loader.find_ingredient_by_alias(parsed['name'])
                if canonical_name:
                    parsed['canonical_name'] = canonical_name
                
                parsed['source'] = 'manual_input'
                ingredients.append(parsed)
        
        return ingredients
    
    def _parse_ingredient_text(self, text: str) -> Optional[Dict[str, Any]]:
        """Parse ingredient text like '2 lbs chicken breast' or '1 cup rice'"""
        # Common patterns for ingredient parsing
        patterns = [
            r'^(\d+\.?\d*)\s*([a-zA-Z]+)\s+(.+)$',  # "2 lbs chicken breast"
            r'^(\d+\.?\d*)\s+(.+)$',                # "2 chicken breast"
            r'^(.+)$'                               # "chicken breast"
        ]
        
        for pattern in patterns:
            match = re.match(pattern, text.strip())
            if match:
                if len(match.groups()) == 3:
                    amount, unit, name = match.groups()
                    return {
                        'name': name.strip(),
                        'amount': float(amount),
                        'unit': unit.strip(),
                        'raw_text': text
                    }
                elif len(match.groups()) == 2:
                    amount, name = match.groups()
                    return {
                        'name': name.strip(),
                        'amount': float(amount),
                        'unit': 'piece',
                        'raw_text': text
                    }
                else:
                    name = match.groups()[0]
                    return {
                        'name': name.strip(),
                        'amount': 1,
                        'unit': 'item',
                        'raw_text': text
                    }
        
        return None

class ListConsolidator:
    """Consolidates ingredients by merging duplicates and converting units"""
    
    def __init__(self, data_loader):
        self.data_loader = data_loader
    
    def consolidate_ingredients(self, ingredients: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Consolidate ingredient list by merging duplicates and standardizing units"""
        if not ingredients:
            return []
        
        # Group ingredients by canonical name
        ingredient_groups = defaultdict(list)
        
        for ingredient in ingredients:
            # Determine canonical name
            canonical_name = self._get_canonical_name(ingredient)
            ingredient_groups[canonical_name].append(ingredient)
        
        # Consolidate each group
        consolidated = []
        for canonical_name, group in ingredient_groups.items():
            consolidated_ingredient = self._consolidate_ingredient_group(canonical_name, group)
            if consolidated_ingredient:
                consolidated.append(consolidated_ingredient)
        
        return consolidated
    
    def _get_canonical_name(self, ingredient: Dict[str, Any]) -> str:
        """Get canonical name for ingredient using aliases"""
        name = ingredient.get('name', '').strip()
        
        # Check if already has canonical name
        if 'canonical_name' in ingredient:
            return ingredient['canonical_name']
        
        # Try to find using aliases
        canonical = self.data_loader.find_ingredient_by_alias(name)
        if canonical:
            return canonical
        
        # Fallback to normalized name
        return name.lower().replace(' ', '_')
    
    def _consolidate_ingredient_group(self, canonical_name: str, ingredients: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Consolidate a group of ingredients with the same canonical name"""
        if not ingredients:
            return None
        
        # Use the first ingredient as base
        base_ingredient = ingredients[0].copy()
        base_ingredient['canonical_name'] = canonical_name
        
        # Determine the best display name
        display_name = self._get_best_display_name(ingredients)
        base_ingredient['display_name'] = display_name
        
        # Consolidate quantities
        total_amount = 0
        unit_amounts = defaultdict(float)
        sources = set()
        
        for ingredient in ingredients:
            amount = ingredient.get('amount', 0)
            unit = ingredient.get('unit', '').lower()
            source = ingredient.get('source', '')
            
            unit_amounts[unit] += amount
            sources.add(source)
        
        # Try to consolidate units
        consolidated_amount, consolidated_unit = self._consolidate_units(canonical_name, unit_amounts)
        
        base_ingredient.update({
            'amount': consolidated_amount,
            'unit': consolidated_unit,
            'sources': list(sources),
            'original_count': len(ingredients)
        })
        
        return base_ingredient
    
    def _get_best_display_name(self, ingredients: List[Dict[str, Any]]) -> str:
        """Get the best display name from a group of ingredients"""
        names = [ing.get('name', '') for ing in ingredients]
        # Prefer the longest/most descriptive name
        return max(names, key=len) if names else 'Unknown ingredient'
    
    def _consolidate_units(self, ingredient_name: str, unit_amounts: Dict[str, float]) -> Tuple[float, str]:
        """Consolidate different units for the same ingredient"""
        if len(unit_amounts) == 1:
            unit, amount = next(iter(unit_amounts.items()))
            return amount, unit
        
        # Try to convert everything to a common unit
        primary_unit = self._get_primary_unit(unit_amounts)
        total_amount = 0
        
        for unit, amount in unit_amounts.items():
            if unit == primary_unit:
                total_amount += amount
            else:
                # Try to convert to primary unit
                converted_amount = self.data_loader.convert_unit(ingredient_name, amount, unit, primary_unit)
                total_amount += converted_amount
        
        return total_amount, primary_unit
    
    def _get_primary_unit(self, unit_amounts: Dict[str, float]) -> str:
        """Get the primary unit to use for consolidation"""
        # Priority order for common units
        unit_priority = {
            'kg': 1, 'lb': 2, 'g': 3, 'oz': 4,
            'l': 1, 'gallon': 2, 'quart': 3, 'cup': 4, 'ml': 5,
            'tbsp': 6, 'tsp': 7,
            'piece': 8, 'item': 9
        }
        
        # Choose the unit with highest priority (lowest number)
        sorted_units = sorted(unit_amounts.keys(), 
                            key=lambda u: unit_priority.get(u.lower(), 99))
        
        return sorted_units[0] if sorted_units else 'item'

class StoreOrganizer:
    """Organizes grocery list by store sections for optimal shopping"""
    
    def __init__(self, data_loader):
        self.data_loader = data_loader
    
    def organize_by_store_sections(self, ingredients: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        """Organize ingredients by store sections"""
        organized = defaultdict(list)
        
        for ingredient in ingredients:
            section_info = self._get_store_section(ingredient)
            section_name = section_info['display_name']
            
            # Add section info to ingredient
            ingredient['store_section'] = section_info
            organized[section_name].append(ingredient)
        
        # Sort sections by shopping order
        return self._sort_by_shopping_order(organized)
    
    def _get_store_section(self, ingredient: Dict[str, Any]) -> Dict[str, Any]:
        """Get store section for an ingredient"""
        # Try to get from food_id first
        food_id = ingredient.get('food_id')
        if food_id:
            category = self.data_loader.get_food_category_by_id(food_id)
            if category:
                section_info = self.data_loader.map_category_to_store_section(category)
                if section_info:
                    return section_info
        
        # Try to map by ingredient name
        canonical_name = ingredient.get('canonical_name', ingredient.get('name', ''))
        category = self._guess_category_from_name(canonical_name)
        
        section_info = self.data_loader.map_category_to_store_section(category)
        return section_info or {
            'section_id': 'pantry_grains',
            'display_name': 'Pantry & Grains',
            'icon': '📦',
            'order': 99,
            'shopping_tips': 'Store in cool, dry place'
        }
    
    def _guess_category_from_name(self, ingredient_name: str) -> str:
        """Guess food category from ingredient name"""
        name_lower = ingredient_name.lower()
        
        # Simple category mapping based on common keywords
        category_keywords = {
            'protein': ['chicken', 'beef', 'pork', 'fish', 'turkey', 'tofu', 'salmon', 'tuna'],
            'dairy': ['milk', 'cheese', 'yogurt', 'butter', 'cream'],
            'vegetable': ['spinach', 'broccoli', 'carrots', 'onion', 'tomato', 'pepper', 'lettuce'],
            'fruit': ['apple', 'banana', 'orange', 'berry', 'grape', 'lemon'],
            'grain': ['rice', 'quinoa', 'oats', 'bread', 'pasta'],
            'nut': ['almond', 'walnut', 'peanut', 'cashew'],
            'fat': ['oil', 'olive_oil', 'coconut_oil']
        }
        
        for category, keywords in category_keywords.items():
            if any(keyword in name_lower for keyword in keywords):
                return category
        
        return 'other'
    
    def _sort_by_shopping_order(self, organized: Dict[str, List[Dict[str, Any]]]) -> Dict[str, List[Dict[str, Any]]]:
        """Sort organized sections by optimal shopping order"""
        store_sections = self.data_loader.get_store_sections()
        
        # Create order mapping
        order_mapping = {}
        for section_id, section_data in store_sections.items():
            display_name = section_data.get('display_name', section_id)
            order = section_data.get('order', 99)
            order_mapping[display_name] = order
        
        # Sort by order
        sorted_sections = sorted(organized.items(), 
                               key=lambda x: order_mapping.get(x[0], 99))
        
        return dict(sorted_sections)

class SubstitutionManager:
    """Manages ingredient substitutions and alternatives"""
    
    def __init__(self, data_loader):
        self.data_loader = data_loader
    
    def get_substitutions_for_ingredient(self, ingredient: Dict[str, Any], dietary_restrictions: List[str] = None) -> List[Dict[str, Any]]:
        """Get substitution options for an ingredient"""
        canonical_name = ingredient.get('canonical_name', ingredient.get('name', ''))
        
        substitutions = self.data_loader.get_substitutions_for_ingredient(
            canonical_name, dietary_restrictions
        )
        
        # Add formatted substitution info
        formatted_subs = []
        for sub in substitutions:
            formatted_sub = {
                'substitute_name': sub.get('substitute', ''),
                'ratio': sub.get('ratio', '1:1'),
                'notes': sub.get('notes', ''),
                'dietary_tags': sub.get('dietary_tags', []),
                'food_id': sub.get('food_id'),
                'compatibility_score': self._calculate_compatibility_score(sub, dietary_restrictions)
            }
            formatted_subs.append(formatted_sub)
        
        # Sort by compatibility score
        formatted_subs.sort(key=lambda x: x['compatibility_score'], reverse=True)
        
        return formatted_subs
    
    def _calculate_compatibility_score(self, substitution: Dict[str, Any], dietary_restrictions: List[str] = None) -> float:
        """Calculate compatibility score for substitution"""
        score = 0.5  # Base score
        
        if not dietary_restrictions:
            return score
        
        dietary_restrictions_lower = [dr.lower() for dr in dietary_restrictions]
        sub_tags = [tag.lower() for tag in substitution.get('dietary_tags', [])]
        
        # Boost score if substitution matches dietary restrictions
        matching_tags = sum(1 for dr in dietary_restrictions_lower if dr in sub_tags)
        score += matching_tags * 0.3
        
        return min(score, 1.0)