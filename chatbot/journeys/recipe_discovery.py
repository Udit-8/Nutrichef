"""
Recipe Discovery Journey Implementation
Follows the Recipe Discovery Design Flow Chart
"""

from typing import Dict, Any, Optional, List
from journeys.base_journey import BaseJourney
from data.data_loader import DataLoader

class RecipeDiscoveryJourney(BaseJourney):
    """Recipe Discovery customer journey implementation"""
    
    def __init__(self, session_manager):
        super().__init__(session_manager)
        self.data_loader = DataLoader()
        self.discovery_methods = [
            "Cuisine Type",
            "Available Ingredients", 
            "Dietary Restrictions",
            "Cooking Time",
            "Special Occasion"
        ]
    
    def start_journey(self) -> str:
        """Step 1: Greeting & Context"""
        self.update_step(1)
        user_prefs = self.session_manager.get_user_preferences()
        
        greeting = "I'd love to help you find the perfect recipe! 🍳"
        
        # Add personalization if we have user preferences
        if user_prefs.get('dietary_restrictions'):
            restrictions = ', '.join(user_prefs['dietary_restrictions'])
            greeting += f" I'll keep in mind your dietary preferences: {restrictions}."
        
        self.update_step(2)
        return f"{greeting}\n\nHow would you like to discover recipes today?{self.format_options(self.discovery_methods, 'discovery method')}"
    
    def process_input(self, user_input: str) -> Optional[str]:
        """Process user input based on current step"""
        current_step = self.get_current_step()
        
        if current_step == 2:
            return self._handle_discovery_method_selection(user_input)
        elif current_step == 3:
            return self._handle_path_specific_input(user_input)
        elif current_step == 4:
            return self._handle_recipe_selection(user_input)
        elif current_step == 5:
            return self._handle_final_actions(user_input)
        else:
            return "I'm not sure what step we're on. Let's start over with recipe discovery."
    
    def _handle_discovery_method_selection(self, user_input: str) -> str:
        """Step 2: Handle discovery method selection"""
        choice = self.parse_user_choice(user_input, self.discovery_methods)
        
        if not choice:
            return f"I didn't understand that choice. {self.format_options(self.discovery_methods, 'discovery method')}"
        
        self.record_decision("discovery_method", choice)
        self.update_step(3)
        
        if choice == "Cuisine Type":
            return self._start_cuisine_path()
        elif choice == "Available Ingredients":
            return self._start_ingredient_path()
        elif choice == "Dietary Restrictions":
            return self._start_dietary_path()
        elif choice == "Cooking Time":
            return self._start_time_path()
        elif choice == "Special Occasion":
            return self._start_occasion_path()
    
    def _start_cuisine_path(self) -> str:
        """Path A: Cuisine Selection"""
        cuisines = self.data_loader.get_cuisine_types()
        if not cuisines:
            return "I'm sorry, I don't have cuisine data available right now. Let's try a different approach."
        
        return f"What cuisine are you in the mood for?{self.format_options(cuisines, 'cuisine')}"
    
    def _start_ingredient_path(self) -> str:
        """Path B: Ingredient-Based Discovery"""
        return ("What ingredients do you have available? Please list them separated by commas.\n"
                "For example: 'chicken, rice, onions, tomatoes'")
    
    def _start_dietary_path(self) -> str:
        """Path C: Dietary Restrictions"""
        dietary_tags = self.data_loader.get_dietary_tags()
        if not dietary_tags:
            return "I'm sorry, I don't have dietary restriction data available right now."
        
        return f"What dietary requirements do you have?{self.format_options(dietary_tags, 'dietary option')}"
    
    def _start_time_path(self) -> str:
        """Path D: Time-Based"""
        time_options = [
            "Quick (under 15 minutes)",
            "Medium (15-30 minutes)", 
            "Normal (30-60 minutes)",
            "Extended (1+ hours)"
        ]
        return f"How much time do you have for cooking?{self.format_options(time_options, 'time option')}"
    
    def _start_occasion_path(self) -> str:
        """Path E: Occasion-Based"""
        occasions = [
            "Weeknight Dinner",
            "Weekend Cooking",
            "Date Night",
            "Family Gathering",
            "Meal Prep",
            "Comfort Food",
            "Healthy Eating"
        ]
        return f"What's the occasion?{self.format_options(occasions, 'occasion')}"
    
    def _handle_path_specific_input(self, user_input: str) -> str:
        """Step 3: Handle input based on selected discovery path"""
        journey_state = self.get_journey_state()
        discovery_method = journey_state.get('decision_points', {}).get('discovery_method', {}).get('choice')
        
        if discovery_method == "Cuisine Type":
            return self._handle_cuisine_selection(user_input)
        elif discovery_method == "Available Ingredients":
            return self._handle_ingredient_input(user_input)
        elif discovery_method == "Dietary Restrictions":
            return self._handle_dietary_selection(user_input)
        elif discovery_method == "Cooking Time":
            return self._handle_time_selection(user_input)
        elif discovery_method == "Special Occasion":
            return self._handle_occasion_selection(user_input)
    
    def _handle_cuisine_selection(self, user_input: str) -> str:
        """Handle cuisine type selection"""
        cuisines = self.data_loader.get_cuisine_types()
        choice = self.parse_user_choice(user_input, cuisines)
        
        if not choice:
            return f"I didn't recognize that cuisine. {self.format_options(cuisines, 'cuisine')}"
        
        self.record_decision("cuisine_choice", choice)
        recipes = self.data_loader.filter_recipes_by_cuisine(choice)
        
        return self._show_recipe_results(recipes, f"{choice} recipes")
    
    def _handle_ingredient_input(self, user_input: str) -> str:
        """Handle ingredient list input"""
        ingredients = [ing.strip() for ing in user_input.split(',')]
        self.record_decision("available_ingredients", ingredients)
        
        recipes = self.data_loader.filter_recipes_by_ingredients(ingredients)
        return self._show_recipe_results(recipes, "recipes you can make with your ingredients")
    
    def _handle_dietary_selection(self, user_input: str) -> str:
        """Handle dietary restriction selection"""
        dietary_tags = self.data_loader.get_dietary_tags()
        choice = self.parse_user_choice(user_input, dietary_tags)
        
        if not choice:
            return f"I didn't recognize that dietary option. {self.format_options(dietary_tags, 'dietary option')}"
        
        self.record_decision("dietary_restriction", choice)
        recipes = self.data_loader.filter_recipes_by_dietary_restrictions([choice])
        
        return self._show_recipe_results(recipes, f"{choice} recipes")
    
    def _handle_time_selection(self, user_input: str) -> str:
        """Handle cooking time selection"""
        time_options = [
            "Quick (under 15 minutes)",
            "Medium (15-30 minutes)", 
            "Normal (30-60 minutes)",
            "Extended (1+ hours)"
        ]
        choice = self.parse_user_choice(user_input, time_options)
        
        if not choice:
            return f"I didn't understand that time option. {self.format_options(time_options, 'time option')}"
        
        # Map choice to max minutes
        time_mapping = {
            "Quick (under 15 minutes)": 15,
            "Medium (15-30 minutes)": 30,
            "Normal (30-60 minutes)": 60,
            "Extended (1+ hours)": 999
        }
        
        max_minutes = time_mapping.get(choice, 60)
        self.record_decision("cooking_time", choice)
        
        recipes = self.data_loader.filter_recipes_by_prep_time(max_minutes)
        return self._show_recipe_results(recipes, f"recipes under {choice.split('(')[1].split(')')[0]}")
    
    def _handle_occasion_selection(self, user_input: str) -> str:
        """Handle occasion selection"""
        occasions = [
            "Weeknight Dinner", "Weekend Cooking", "Date Night", 
            "Family Gathering", "Meal Prep", "Comfort Food", "Healthy Eating"
        ]
        choice = self.parse_user_choice(user_input, occasions)
        
        if not choice:
            return f"I didn't recognize that occasion. {self.format_options(occasions, 'occasion')}"
        
        self.record_decision("occasion", choice)
        
        # For now, return all recipes - in a real implementation you'd filter by occasion tags
        recipes = self.data_loader.get_recipes()
        return self._show_recipe_results(recipes[:10], f"recipes perfect for {choice}")
    
    def _show_recipe_results(self, recipes: List[Dict[str, Any]], context: str) -> str:
        """Show recipe search results"""
        if not recipes:
            return f"I couldn't find any {context}. Would you like to try a different approach?"
        
        self.update_step(4, {'filtered_recipes': recipes})
        
        response = f"Great! I found {len(recipes)} {context}:\n\n"
        
        # Show top 5 recipes
        display_recipes = recipes[:5]
        for i, recipe in enumerate(display_recipes, 1):
            name = recipe.get('name', 'Unknown Recipe')
            prep_time = recipe.get('prep_time', 'Unknown')
            difficulty = recipe.get('difficulty', 'Unknown')
            
            response += f"{i}. {name}\n"
            response += f"   ⏱️ {prep_time} minutes | 📊 {difficulty} difficulty\n"
            if recipe.get('description'):
                response += f"   📝 {recipe['description'][:80]}...\n"
            response += "\n"
        
        if len(recipes) > 5:
            response += f"...and {len(recipes) - 5} more recipes!\n\n"
        
        response += "Please enter the number of the recipe you'd like to see, or type 'more' to see additional recipes:"
        
        return response
    
    def _handle_recipe_selection(self, user_input: str) -> str:
        """Step 4: Handle recipe selection"""
        if user_input.lower() == 'more':
            return self._show_more_recipes()
        
        step_data = self.get_journey_state().get('step_data', {}).get(4, {})
        filtered_recipes = step_data.get('filtered_recipes', [])
        
        if not filtered_recipes:
            return "I don't have any recipes to show you. Let's start over."
        
        try:
            choice_num = int(user_input.strip())
            if 1 <= choice_num <= min(5, len(filtered_recipes)):
                selected_recipe = filtered_recipes[choice_num - 1]
                return self._show_recipe_details(selected_recipe)
            else:
                return f"Please enter a number between 1 and {min(5, len(filtered_recipes))}, or type 'more' for additional recipes."
        except ValueError:
            return "Please enter a number, or type 'more' to see additional recipes."
    
    def _show_more_recipes(self) -> str:
        """Show additional recipes"""
        step_data = self.get_journey_state().get('step_data', {}).get(4, {})
        filtered_recipes = step_data.get('filtered_recipes', [])
        
        if len(filtered_recipes) <= 5:
            return "I've already shown you all available recipes."
        
        response = "Here are more recipes:\n\n"
        additional_recipes = filtered_recipes[5:10]
        
        for i, recipe in enumerate(additional_recipes, 6):
            name = recipe.get('name', 'Unknown Recipe')
            prep_time = recipe.get('prep_time', 'Unknown')
            difficulty = recipe.get('difficulty', 'Unknown')
            
            response += f"{i}. {name}\n"
            response += f"   ⏱️ {prep_time} minutes | 📊 {difficulty} difficulty\n\n"
        
        response += "Please enter the number of the recipe you'd like to see:"
        return response
    
    def _show_recipe_details(self, recipe: Dict[str, Any]) -> str:
        """Show detailed recipe information"""
        self.record_decision("selected_recipe", recipe.get('id'))
        self.update_step(5, {'selected_recipe': recipe})
        
        name = recipe.get('name', 'Unknown Recipe')
        description = recipe.get('description', 'No description available.')
        prep_time = recipe.get('prep_time', 'Unknown')
        servings = recipe.get('servings', 'Unknown')
        difficulty = recipe.get('difficulty', 'Unknown')
        
        response = f"🍳 **{name}**\n\n"
        response += f"📝 {description}\n\n"
        response += f"⏱️ Prep Time: {prep_time} minutes\n"
        response += f"👥 Servings: {servings}\n"
        response += f"📊 Difficulty: {difficulty}\n\n"
        
        # Show ingredients
        ingredients = recipe.get('ingredients', [])
        if ingredients:
            response += "🛒 **Ingredients:**\n"
            for ingredient in ingredients:
                name_ing = ingredient.get('name', 'Unknown ingredient')
                amount = ingredient.get('amount', '')
                unit = ingredient.get('unit', '')
                response += f"• {amount} {unit} {name_ing}\n"
            response += "\n"
        
        # Show cooking instructions preview
        instructions = recipe.get('instructions', [])
        if instructions:
            response += "👩‍🍳 **Instructions Preview:**\n"
            for i, instruction in enumerate(instructions[:3], 1):
                step_text = instruction.get('step', instruction) if isinstance(instruction, dict) else instruction
                response += f"{i}. {step_text}\n"
            
            if len(instructions) > 3:
                response += f"...and {len(instructions) - 3} more steps\n\n"
        
        response += "What would you like to do next?\n"
        response += "1. Start cooking this recipe\n"
        response += "2. Save recipe for later\n"
        response += "3. Find similar recipes\n"
        response += "4. Search for different recipes\n"
        response += "5. Create grocery list for this recipe\n"
        
        return response
    
    def _handle_final_actions(self, user_input: str) -> str:
        """Step 5: Handle final action selection"""
        actions = [
            "Start cooking this recipe",
            "Save recipe for later", 
            "Find similar recipes",
            "Search for different recipes",
            "Create grocery list for this recipe"
        ]
        
        choice = self.parse_user_choice(user_input, actions)
        
        if not choice:
            return f"I didn't understand that choice. {self.format_options(actions, 'action')}"
        
        step_data = self.get_journey_state().get('step_data', {}).get(5, {})
        selected_recipe = step_data.get('selected_recipe', {})
        recipe_name = selected_recipe.get('name', 'this recipe')
        
        if choice == "Start cooking this recipe":
            self.complete_journey()
            return f"Perfect! Let's start cooking {recipe_name}! I'll guide you through each step. (Transitioning to Cooking Guidance journey...)"
        
        elif choice == "Save recipe for later":
            self.complete_journey()
            return f"Great! I've saved {recipe_name} to your favorites. You can find it anytime by asking me to show your saved recipes."
        
        elif choice == "Find similar recipes":
            # Reset to step 4 with similar recipes
            self.update_step(4)
            return self._find_similar_recipes(selected_recipe)
        
        elif choice == "Search for different recipes":
            # Restart journey
            return self.start_journey()
        
        elif choice == "Create grocery list for this recipe":
            self.complete_journey()
            return f"I'll create a grocery list for {recipe_name}! (Transitioning to Grocery Assistance journey...)"
    
    def _find_similar_recipes(self, current_recipe: Dict[str, Any]) -> str:
        """Find recipes similar to the selected one"""
        cuisine = current_recipe.get('cuisine', '')
        similar_recipes = []
        
        if cuisine:
            similar_recipes = self.data_loader.filter_recipes_by_cuisine(cuisine)
            # Remove the current recipe from results
            current_id = current_recipe.get('id')
            similar_recipes = [r for r in similar_recipes if r.get('id') != current_id]
        
        if not similar_recipes:
            similar_recipes = self.data_loader.get_recipes()[:10]
        
        return self._show_recipe_results(similar_recipes, f"recipes similar to {current_recipe.get('name', 'your selection')}")