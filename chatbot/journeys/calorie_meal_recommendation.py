"""
Calorie-Based Meal Recommendation Journey Implementation
Follows the Calorie-Based Meal Recommendation Design Flow Chart
"""

from typing import Dict, Any, Optional, List, Tuple
from journeys.base_journey import BaseJourney
from data.data_loader import DataLoader
from utils.calorie_utils import CalorieCalculator

class CalorieMealRecommendationJourney(BaseJourney):
    """Calorie-based meal recommendation customer journey implementation"""
    
    def __init__(self, session_manager):
        super().__init__(session_manager)
        self.data_loader = DataLoader()
        self.calorie_calc = CalorieCalculator()
        
        # Journey-specific constants
        self.calorie_input_methods = [
            "Specific Number (e.g., '400 calories')",
            "Calorie Range (e.g., '300-500 calories')", 
            "Goal-Based (Low/Moderate/High calorie)"
        ]
        
        self.meal_scopes = [
            "Single Meal - Find one optimal meal",
            "Daily Plan - All meals for today",
            "Multiple Days - Week or specific days"
        ]
        
        self.meal_types = [
            "Breakfast",
            "Lunch", 
            "Dinner",
            "Snack",
            "All Meals"
        ]
    
    def start_journey(self) -> str:
        """Step 1: Calorie Goal Determination"""
        self.update_step(1)
        user_prefs = self.session_manager.get_user_preferences()
        
        greeting = "I'll help you find meals that fit your calorie goals! 🍽️"
        
        # Add personalization if available
        if user_prefs.get('dietary_restrictions'):
            restrictions = ', '.join(user_prefs['dietary_restrictions'])
            greeting += f" I'll keep in mind your dietary preferences: {restrictions}."
        
        return (f"{greeting}\n\n"
                "What's your calorie target? You can say things like:\n"
                "• 'I need exactly 400 calories'\n"
                "• 'Between 300-500 calories'\n"
                "• 'Low calorie meals'\n"
                "• 'High protein, moderate calories'\n\n"
                "Please tell me your calorie goal:")
    
    def process_input(self, user_input: str) -> Optional[str]:
        """Process user input based on current step"""
        current_step = self.get_current_step()
        
        if current_step == 1:
            return self._handle_calorie_goal_input(user_input)
        elif current_step == 2:
            return self._handle_meal_scope_selection(user_input)
        elif current_step == 3:
            return self._handle_meal_type_selection(user_input)
        elif current_step == 4:
            return self._handle_dietary_preferences(user_input)
        elif current_step == 5:
            return self._handle_meal_selection(user_input)
        elif current_step == 6:
            return self._handle_meal_confirmation(user_input)
        elif current_step == 7:
            return self._handle_final_actions(user_input)
        else:
            return "I'm not sure what step we're on. Let's start over with calorie-based meal recommendations."
    
    def _handle_calorie_goal_input(self, user_input: str) -> str:
        """Step 1: Handle calorie goal input"""
        try:
            min_cal, max_cal, input_type = self.calorie_calc.parse_calorie_input(user_input)
            
            # Store calorie goals
            self.record_decision("calorie_goal", {
                'min': min_cal,
                'max': max_cal,
                'type': input_type,
                'original_input': user_input
            })
            
            self.update_step(2)
            
            # Format the confirmed calorie range
            range_text = self.calorie_calc.format_calorie_range(min_cal, max_cal)
            
            response = f"Great! I'll find meals with {range_text}.\n\n"
            response += "Are you planning for:"
            response += self.format_options(self.meal_scopes, "planning scope")
            
            return response
            
        except Exception as e:
            return ("I didn't understand that calorie goal. Please try again with:\n"
                   "• A specific number: '400 calories'\n"
                   "• A range: '300-500 calories'\n"
                   "• A goal: 'low calorie meals'")
    
    def _handle_meal_scope_selection(self, user_input: str) -> str:
        """Step 2: Handle meal scope selection"""
        choice = self.parse_user_choice(user_input, self.meal_scopes)
        
        if not choice:
            return f"I didn't understand that choice. {self.format_options(self.meal_scopes, 'planning scope')}"
        
        self.record_decision("meal_scope", choice)
        self.update_step(3)
        
        # Get calorie goals for context
        calorie_goal = self.get_journey_state().get('decision_points', {}).get('calorie_goal', {}).get('choice', {})
        min_cal = calorie_goal.get('min', 0)
        max_cal = calorie_goal.get('max', 500)
        
        response = ""
        
        if "Single Meal" in choice:
            response = "Perfect! I'll find you one optimal meal.\n\n"
        elif "Daily Plan" in choice:
            # Calculate daily distribution
            total_daily = (min_cal + max_cal) // 2 * 4  # Estimate daily calories
            distribution = self.calorie_calc.calculate_daily_distribution(total_daily)
            response = (f"Great! I'll plan all meals for today.\n"
                       f"Daily distribution (based on ~{total_daily} total calories):\n"
                       f"• Breakfast: ~{distribution['breakfast']} calories\n"
                       f"• Lunch: ~{distribution['lunch']} calories\n"
                       f"• Dinner: ~{distribution['dinner']} calories\n"
                       f"• Snacks: ~{distribution['snack']} calories\n\n")
        else:  # Multiple Days
            response = "Excellent! I'll help you plan for multiple days.\n\n"
        
        response += "Which meal(s) are you planning?"
        response += self.format_options(self.meal_types, "meal type")
        
        return response
    
    def _handle_meal_type_selection(self, user_input: str) -> str:
        """Step 3: Handle meal type selection"""
        choice = self.parse_user_choice(user_input, self.meal_types)
        
        if not choice:
            return f"I didn't understand that choice. {self.format_options(self.meal_types, 'meal type')}"
        
        self.record_decision("meal_type", choice)
        self.update_step(4)
        
        # Get available dietary tags
        dietary_tags = self.data_loader.get_meal_dietary_tags()
        
        if not dietary_tags:
            # Skip dietary preferences if no tags available
            return self._proceed_to_meal_search()
        
        response = f"You selected: {choice}\n\n"
        
        # Show calorie ranges for specific meal types
        if choice != "All Meals":
            min_range, max_range = self.calorie_calc.get_meal_type_range(choice)
            response += f"Typical {choice.lower()} range: {min_range}-{max_range} calories\n\n"
        
        response += "Any dietary preferences or restrictions?"
        response += self.format_options(["No special requirements"] + dietary_tags, "dietary option")
        
        return response
    
    def _handle_dietary_preferences(self, user_input: str) -> str:
        """Step 4: Handle dietary preferences selection"""
        dietary_tags = ["No special requirements"] + self.data_loader.get_meal_dietary_tags()
        choice = self.parse_user_choice(user_input, dietary_tags)
        
        if not choice:
            return f"I didn't understand that choice. {self.format_options(dietary_tags, 'dietary option')}"
        
        # Record dietary choice
        selected_tags = [] if choice == "No special requirements" else [choice]
        self.record_decision("dietary_preferences", selected_tags)
        
        return self._proceed_to_meal_search()
    
    def _proceed_to_meal_search(self) -> str:
        """Step 5: Execute meal database search and show results"""
        self.update_step(5)
        
        # Get all stored criteria
        journey_state = self.get_journey_state()
        decisions = journey_state.get('decision_points', {})
        
        calorie_goal = decisions.get('calorie_goal', {}).get('choice', {})
        min_cal = calorie_goal.get('min', 0)
        max_cal = calorie_goal.get('max', 500)
        
        meal_type = decisions.get('meal_type', {}).get('choice', '')
        dietary_prefs = decisions.get('dietary_preferences', {}).get('choice', [])
        
        # Convert meal type to list for filtering
        meal_types = []
        if meal_type and meal_type != "All Meals":
            meal_types = [meal_type.lower()]
        
        # Search for meals
        filtered_meals = self.data_loader.filter_meals_by_multiple_criteria(
            min_calories=min_cal,
            max_calories=max_cal,
            meal_types=meal_types,
            dietary_tags=dietary_prefs
        )
        
        if not filtered_meals:
            return self._handle_no_meals_found(min_cal, max_cal, meal_types, dietary_prefs)
        
        # Store results and show them
        self.update_step(5, {'filtered_meals': filtered_meals})
        return self._show_meal_results(filtered_meals, min_cal, max_cal)
    
    def _handle_no_meals_found(self, min_cal: int, max_cal: int, meal_types: List[str], dietary_tags: List[str]) -> str:
        """Handle case when no meals match criteria"""
        response = f"I couldn't find meals matching {min_cal}-{max_cal} calories"
        
        if meal_types:
            response += f" for {', '.join(meal_types)}"
        if dietary_tags:
            response += f" with {', '.join(dietary_tags)} requirements"
        
        response += ".\n\nLet me suggest some alternatives:\n\n"
        
        # Suggest alternatives
        alternatives = self.calorie_calc.suggest_calorie_alternatives(min_cal, max_cal)
        
        for i, alt in enumerate(alternatives, 1):
            range_text = self.calorie_calc.format_calorie_range(alt['min'], alt['max'])
            response += f"{i}. {alt['description']}: {range_text}\n"
        
        response += f"{len(alternatives) + 1}. Remove dietary restrictions\n"
        response += f"{len(alternatives) + 2}. Try different meal type\n"
        response += f"{len(alternatives) + 3}. Start over\n"
        
        response += "\nWhich alternative would you like to try?"
        
        return response
    
    def _show_meal_results(self, meals: List[Dict[str, Any]], min_cal: int, max_cal: int) -> str:
        """Step 6: Display meal results"""
        range_text = self.calorie_calc.format_calorie_range(min_cal, max_cal)
        
        response = f"Great! I found {len(meals)} meals with {range_text}:\n\n"
        
        # Show top 5 meals
        display_meals = meals[:5]
        for i, meal in enumerate(display_meals, 1):
            name = meal.get('name', 'Unknown Meal')
            calories = meal.get('calories', 0)
            prep_time = meal.get('prep_time', 'Unknown')
            nutrition = meal.get('nutrition', {})
            dietary_tags = meal.get('dietary_tags', [])
            
            response += f"{i}. {name}\n"
            response += f"   🔥 {calories} calories | ⏱️ {prep_time} min prep\n"
            response += f"   💪 {nutrition.get('protein', 0)}g protein | "
            response += f"🌾 {nutrition.get('carbs', 0)}g carbs | "
            response += f"🥑 {nutrition.get('fat', 0)}g fat\n"
            
            if dietary_tags:
                response += f"   🏷️ {', '.join(dietary_tags)}\n"
            
            # Show component preview
            components = meal.get('components', [])
            if components:
                component_names = [comp.get('name', '') for comp in components[:3]]
                response += f"   📋 Components: {', '.join(component_names)}"
                if len(components) > 3:
                    response += f" + {len(components) - 3} more"
                response += "\n"
            
            response += "\n"
        
        if len(meals) > 5:
            response += f"...and {len(meals) - 5} more meals!\n\n"
        
        response += "Please enter the number of the meal you'd like to see details for, or type 'more' for additional options:"
        
        return response
    
    def _handle_meal_selection(self, user_input: str) -> str:
        """Step 5: Handle meal selection from results"""
        if user_input.lower() == 'more':
            return self._show_more_options()
        
        step_data = self.get_journey_state().get('step_data', {}).get(5, {})
        filtered_meals = step_data.get('filtered_meals', [])
        
        if not filtered_meals:
            return "I don't have any meals to show you. Let's start over."
        
        try:
            choice_num = int(user_input.strip())
            if 1 <= choice_num <= min(5, len(filtered_meals)):
                selected_meal = filtered_meals[choice_num - 1]
                return self._show_meal_details(selected_meal)
            else:
                return f"Please enter a number between 1 and {min(5, len(filtered_meals))}, or type 'more' for additional options."
        except ValueError:
            return "Please enter a number, or type 'more' for additional options."
    
    def _show_more_options(self) -> str:
        """Show additional meal options"""
        step_data = self.get_journey_state().get('step_data', {}).get(5, {})
        filtered_meals = step_data.get('filtered_meals', [])
        
        if len(filtered_meals) <= 5:
            return "I've already shown you all available meals matching your criteria."
        
        response = "Here are more meal options:\n\n"
        additional_meals = filtered_meals[5:10]
        
        for i, meal in enumerate(additional_meals, 6):
            name = meal.get('name', 'Unknown Meal')
            calories = meal.get('calories', 0)
            prep_time = meal.get('prep_time', 'Unknown')
            
            response += f"{i}. {name}\n"
            response += f"   🔥 {calories} calories | ⏱️ {prep_time} min prep\n\n"
        
        response += "Please enter the number of the meal you'd like to see details for:"
        return response
    
    def _show_meal_details(self, meal: Dict[str, Any]) -> str:
        """Show detailed meal information"""
        self.record_decision("selected_meal", meal.get('id'))
        self.update_step(6, {'selected_meal': meal})
        
        # Generate nutritional analysis
        analysis = self.calorie_calc.generate_nutrition_analysis(meal)
        
        name = meal.get('name', 'Unknown Meal')
        calories = meal.get('calories', 0)
        prep_time = meal.get('prep_time', 'Unknown')
        meal_types = ', '.join(meal.get('meal_type', []))
        
        response = f"🍽️ **{name}**\n\n"
        response += f"🔥 Calories: {calories}\n"
        response += f"⏱️ Prep Time: {prep_time} minutes\n"
        response += f"🍴 Meal Type: {meal_types}\n\n"
        
        # Detailed nutrition
        nutrition = meal.get('nutrition', {})
        percentages = analysis['percentages']
        
        response += "📊 **Nutrition Breakdown:**\n"
        response += f"💪 Protein: {nutrition.get('protein', 0)}g ({percentages['protein_pct']}%)\n"
        response += f"🌾 Carbohydrates: {nutrition.get('carbs', 0)}g ({percentages['carbs_pct']}%)\n"
        response += f"🥑 Fat: {nutrition.get('fat', 0)}g ({percentages['fat_pct']}%)\n"
        response += f"🌿 Fiber: {nutrition.get('fiber', 0)}g\n\n"
        
        # Dietary tags
        dietary_tags = meal.get('dietary_tags', [])
        if dietary_tags:
            response += f"🏷️ **Dietary Tags:** {', '.join(dietary_tags)}\n\n"
        
        # Components/Ingredients
        components = meal.get('components', [])
        if components:
            response += "📋 **Components:**\n"
            for comp in components:
                comp_name = comp.get('name', 'Unknown')
                amount = comp.get('amount', '')
                unit = comp.get('unit', '')
                response += f"• {amount} {unit} {comp_name}\n"
            response += "\n"
        
        # Health insights
        response += "💡 **Health Insights:**\n"
        for insight in analysis['insights']:
            response += f"• {insight}\n"
        
        response += f"\n🏆 Health Score: {analysis['health_score']}/100\n"
        response += f"⚖️ Macro Balance: {analysis['macro_balance']}\n\n"
        
        response += "Is this meal selection final?\n"
        response += "1. Yes, confirm this meal\n"
        response += "2. Show me similar meals\n"
        response += "3. Go back to meal list\n"
        response += "4. Start over with different criteria\n"
        
        return response
    
    def _handle_meal_confirmation(self, user_input: str) -> str:
        """Step 6: Handle meal confirmation"""
        confirmation_options = [
            "Yes, confirm this meal",
            "Show me similar meals", 
            "Go back to meal list",
            "Start over with different criteria"
        ]
        
        choice = self.parse_user_choice(user_input, confirmation_options)
        
        if not choice:
            return f"I didn't understand that choice. {self.format_options(confirmation_options, 'option')}"
        
        step_data = self.get_journey_state().get('step_data', {}).get(6, {})
        selected_meal = step_data.get('selected_meal', {})
        
        if choice == "Yes, confirm this meal":
            self.update_step(7)
            return self._show_final_actions(selected_meal)
        
        elif choice == "Show me similar meals":
            similar_meals = self.data_loader.find_similar_meals(selected_meal)
            if not similar_meals:
                return "I couldn't find similar meals. Let me show you the original results instead."
            
            self.update_step(5, {'filtered_meals': similar_meals})
            meal_name = selected_meal.get('name', 'your selection')
            return self._show_meal_results(similar_meals, 0, 1000)
        
        elif choice == "Go back to meal list":
            # Return to meal selection
            step_data = self.get_journey_state().get('step_data', {}).get(5, {})
            filtered_meals = step_data.get('filtered_meals', [])
            return self._show_meal_results(filtered_meals, 0, 1000)
        
        else:  # Start over
            return self.start_journey()
    
    def _show_final_actions(self, selected_meal: Dict[str, Any]) -> str:
        """Step 7: Show final action selection"""
        meal_name = selected_meal.get('name', 'this meal')
        
        response = f"Perfect! You've selected: **{meal_name}** 🎉\n\n"
        response += "What would you like to do next?\n"
        response += "1. Start cooking this meal\n"
        response += "2. Add to meal plan\n" 
        response += "3. Generate grocery list\n"
        response += "4. Save to favorites (this session)\n"
        response += "5. Find more meals\n"
        
        return response
    
    def _handle_final_actions(self, user_input: str) -> str:
        """Step 7: Handle final action selection"""
        final_actions = [
            "Start cooking this meal",
            "Add to meal plan",
            "Generate grocery list", 
            "Save to favorites (this session)",
            "Find more meals"
        ]
        
        choice = self.parse_user_choice(user_input, final_actions)
        
        if not choice:
            return f"I didn't understand that choice. {self.format_options(final_actions, 'action')}"
        
        step_data = self.get_journey_state().get('step_data', {}).get(6, {})
        selected_meal = step_data.get('selected_meal', {})
        meal_name = selected_meal.get('name', 'this meal')
        
        if choice == "Start cooking this meal":
            self.complete_journey()
            return f"Great! Let's start cooking {meal_name}! I'll guide you through each step. (Transitioning to Cooking Guidance journey...)"
        
        elif choice == "Add to meal plan":
            self.complete_journey()
            return f"Perfect! I'll add {meal_name} to your meal plan with the right timing and portions. (Transitioning to Meal Planning journey...)"
        
        elif choice == "Generate grocery list":
            self.complete_journey()
            return f"Excellent! I'll create a grocery list with all ingredients for {meal_name}. (Transitioning to Grocery Assistance journey...)"
        
        elif choice == "Save to favorites (this session)":
            # Add to session favorites
            session_favorites = self.session_manager.get_journey_state().get('session_favorites', [])
            session_favorites.append(selected_meal)
            self.session_manager.get_journey_state()['session_favorites'] = session_favorites
            
            return f"✅ {meal_name} has been saved to your favorites for this session! You can quickly find it again while we're chatting.\n\nWould you like to find more meals or do something else with this one?"
        
        elif choice == "Find more meals":
            # Return to meal search with same criteria
            return self._proceed_to_meal_search()