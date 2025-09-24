from typing import Dict, List, Any, Optional, Tuple
from .base_journey import BaseJourney
import random
from datetime import datetime, timedelta
import json

class MealPlanningJourney(BaseJourney):
    def __init__(self, data_loader, session_manager):
        super().__init__(session_manager)
        self.data_loader = data_loader
        self.journey_name = "meal_planning"
        
        # Journey-specific state
        self.planning_duration = None  # days to plan for
        self.meal_types = []  # which meals to plan (breakfast, lunch, dinner, snacks)
        self.daily_calorie_target = None
        self.dietary_restrictions = []
        self.cooking_skill_level = None
        self.time_constraints = None
        self.household_size = 1
        self.generated_plan = None
        
        # Meal plan structure: {day: {meal_type: meal_data}}
        self.meal_plan = {}
        
        # Default calorie distribution percentages (adjusted for available meal data)
        self.meal_calorie_distribution = {
            'breakfast': 0.20,  # 20% - meals available in 220-385 cal range
            'lunch': 0.35,      # 35% - meals available in higher ranges
            'dinner': 0.35,     # 35% - meals available in higher ranges  
            'snack': 0.10       # 10% - lighter options
        }
    
    def start_journey(self) -> str:
        """Initialize the meal planning journey"""
        self.current_step = "planning_scope"
        return self._step_planning_scope()
    
    def process_input(self, user_input: str) -> str:
        """Process user input within the journey (required by BaseJourney)"""
        return self.process_user_input(user_input)
    
    def process_user_input(self, user_input: str) -> str:
        """Process user input based on current step"""
        if self.current_step == "planning_scope":
            return self._handle_planning_scope(user_input)
        elif self.current_step == "meal_scope":
            return self._handle_meal_scope(user_input)
        elif self.current_step == "calorie_goals":
            return self._handle_calorie_goals(user_input)
        elif self.current_step == "dietary_preferences":
            return self._handle_dietary_preferences(user_input)
        elif self.current_step == "lifestyle_constraints":
            return self._handle_lifestyle_constraints(user_input)
        elif self.current_step == "generate_plan":
            return self._handle_generate_plan(user_input)
        elif self.current_step == "plan_display":
            return self._handle_plan_display(user_input)
        elif self.current_step == "final_actions":
            return self._handle_final_actions(user_input)
        else:
            return "I'm not sure how to help with that. Let's continue with your meal planning."
    
    def _step_planning_scope(self) -> str:
        """Step 1: Determine planning duration"""
        return """🗓️ **MEAL PLANNING - Let's Get Started!**

What would you like to plan?

1. **Daily** - Single day meal plan
2. **Weekly** - Complete 7-day meal plan  
3. **Custom Range** - Specific number of days (e.g., "3 days", "2 weeks")

Please choose your planning scope by typing the number or describing your preference."""
    
    def _handle_planning_scope(self, user_input: str) -> str:
        """Handle planning duration selection"""
        user_input = user_input.lower().strip()
        
        if user_input in ['1', 'daily', 'single day', 'one day']:
            self.planning_duration = 1
            scope_text = "daily meal plan"
        elif user_input in ['2', 'weekly', 'week', '7 days', 'seven days']:
            self.planning_duration = 7
            scope_text = "weekly meal plan (7 days)"
        elif any(word in user_input for word in ['3', 'custom', 'days', 'weeks']):
            # Try to extract number from custom input
            import re
            numbers = re.findall(r'\d+', user_input)
            if numbers:
                days = int(numbers[0])
                if 'week' in user_input:
                    days = days * 7
                if 1 <= days <= 28:  # reasonable limits
                    self.planning_duration = days
                    scope_text = f"custom {days}-day meal plan"
                else:
                    return "Please choose a duration between 1 and 28 days. What would you prefer?"
            else:
                return "I didn't catch the number of days. Could you specify like '3 days' or '2 weeks'?"
        else:
            return "Please choose 1 for Daily, 2 for Weekly, or specify a custom duration like '5 days'."
        
        # Store decision and move to next step
        self.session_manager.update_context('planning_duration', self.planning_duration)
        self.current_step = "meal_scope"
        
        return f"Great! I'll create a {scope_text} for you.\n\n{self._step_meal_scope()}"
    
    def _step_meal_scope(self) -> str:
        """Step 2: Determine which meals to plan"""
        return """🍽️ **MEAL COVERAGE**

Which meals should I plan for each day?

1. **All Meals** - Breakfast + Lunch + Dinner + Snacks (complete daily nutrition)
2. **Main Meals** - Breakfast + Lunch + Dinner (no snacks)
3. **Specific Meals** - Choose which meals you want planned
4. **Custom Selection** - Tell me your preferences (e.g., "only dinner and snacks")

What works best for your lifestyle?"""
    
    def _handle_meal_scope(self, user_input: str) -> str:
        """Handle meal coverage selection"""
        user_input = user_input.lower().strip()
        
        if user_input in ['1', 'all meals', 'all', 'complete']:
            self.meal_types = ['breakfast', 'lunch', 'dinner', 'snack']
            meal_text = "all meals (breakfast, lunch, dinner, and snacks)"
        elif user_input in ['2', 'main meals', 'main', 'no snacks']:
            self.meal_types = ['breakfast', 'lunch', 'dinner']
            meal_text = "main meals (breakfast, lunch, and dinner)"
        elif user_input in ['3', 'specific']:
            return """Please specify which meals you'd like planned:
- Type meal names like: "breakfast and lunch"
- Or: "dinner only"
- Or: "lunch, dinner, snacks"

What meals would you like me to plan?"""
        elif any(meal in user_input for meal in ['breakfast', 'lunch', 'dinner', 'snack']):
            # Parse custom meal selection
            selected_meals = []
            if 'breakfast' in user_input:
                selected_meals.append('breakfast')
            if 'lunch' in user_input:
                selected_meals.append('lunch')  
            if 'dinner' in user_input:
                selected_meals.append('dinner')
            if 'snack' in user_input:
                selected_meals.append('snack')
            
            if selected_meals:
                self.meal_types = selected_meals
                meal_text = " and ".join(selected_meals)
            else:
                return "I didn't catch which meals you want. Please specify like 'breakfast and dinner' or choose option 1-3."
        else:
            return "Please choose 1-4 or tell me which specific meals you'd like planned."
        
        # Store decision and move to next step
        self.session_manager.update_context('meal_types', self.meal_types)
        self.current_step = "calorie_goals"
        
        return f"Perfect! I'll plan {meal_text} for your {self.planning_duration}-day period.\n\n{self._step_calorie_goals()}"
    
    def _step_calorie_goals(self) -> str:
        """Step 3: Determine daily calorie target"""
        return """🎯 **CALORIE GOALS**

What's your daily calorie target?

1. **Maintain Current Weight** - I'll help calculate your needs based on activity level
2. **Specific Goal** - You have a target number (e.g., "1800 calories per day")
3. **Help Me Decide** - Get guidance on determining your calorie needs
4. **Flexible** - Focus on balanced nutrition rather than strict calorie counting

Please choose your approach or tell me your specific calorie target."""
    
    def _handle_calorie_goals(self, user_input: str) -> str:
        """Handle calorie goal setting"""
        user_input = user_input.lower().strip()
        
        # Try to extract a number first
        import re
        numbers = re.findall(r'\d{4}', user_input)  # Look for 4-digit numbers (typical calorie ranges)
        
        if numbers:
            calories = int(numbers[0])
            if 1200 <= calories <= 4000:  # reasonable calorie range
                self.daily_calorie_target = calories
                target_text = f"{calories} calories per day"
            else:
                return "That calorie target seems unusual. Most people need between 1200-4000 calories daily. Could you confirm your target?"
        elif user_input in ['1', 'maintain', 'current weight', 'maintain weight']:
            # Default to moderate activity level estimate
            self.daily_calorie_target = 2000  # Will be refined based on user details
            target_text = "maintenance calories (~2000/day, we'll adjust as needed)"
        elif user_input in ['2', 'specific']:
            return "Please tell me your specific daily calorie target (e.g., '1800 calories' or just '1800'):"
        elif user_input in ['3', 'help', 'help me decide', 'guidance']:
            self.daily_calorie_target = 1800  # Conservative default
            target_text = "balanced approach (~1800 calories/day for healthy nutrition)"
        elif user_input in ['4', 'flexible', 'balanced', 'nutrition focused']:
            self.daily_calorie_target = 1800  # Focus on balance rather than strict counting
            target_text = "nutrition-focused approach (~1800 calories/day)"
        else:
            return "Please choose 1-4 or tell me your specific calorie target (like '2000 calories')."
        
        # Store decision and move to next step
        self.session_manager.update_context('daily_calorie_target', self.daily_calorie_target)
        self.current_step = "dietary_preferences"
        
        return f"Great! I'm targeting {target_text}.\n\n{self._step_dietary_preferences()}"
    
    def _step_dietary_preferences(self) -> str:
        """Step 4: Collect dietary restrictions and preferences"""
        available_diets = self.data_loader.get_available_dietary_tags()
        
        # Organize tags by category for better presentation
        diet_categories = {
            'Diet Types': ['vegetarian', 'vegan', 'keto_friendly', 'mediterranean'],
            'Health Focus': ['heart_healthy', 'high_protein', 'high_fiber', 'low_carb'],
            'Restrictions': ['gluten_free', 'dairy_free', 'nut_free'],
            'Special Needs': ['omega_3', 'anti_inflammatory', 'probiotic']
        }
        
        diet_text = "🥗 **DIETARY PREFERENCES**\n\nAny dietary restrictions or preferences? You can:\n\n"
        diet_text += "• **Mix and match** from these options:\n"
        
        for category, tags in diet_categories.items():
            available_tags = [tag for tag in tags if tag in available_diets]
            if available_tags:
                diet_text += f"  - {category}: {', '.join(available_tags)}\n"
        
        diet_text += "\n• **Type 'none'** if you have no restrictions\n"
        diet_text += "• **Combine multiple** like: 'vegetarian and gluten_free'\n"
        diet_text += "• **Tell me your needs** in your own words\n\n"
        diet_text += "What dietary preferences should I consider?"
        
        return diet_text
    
    def _handle_dietary_preferences(self, user_input: str) -> str:
        """Handle dietary restriction collection"""
        user_input = user_input.lower().strip()
        
        if user_input in ['none', 'no restrictions', 'nothing', 'no']:
            self.dietary_restrictions = []
            restriction_text = "no specific dietary restrictions"
        else:
            # Parse dietary preferences from user input
            available_tags = self.data_loader.get_available_dietary_tags()
            found_restrictions = []
            
            for tag in available_tags:
                if tag.lower() in user_input or tag.replace('_', ' ') in user_input:
                    found_restrictions.append(tag)
            
            # Also check for common aliases
            aliases = {
                'vegetarian': ['veggie', 'vegetarian'],
                'gluten_free': ['gluten free', 'celiac', 'no gluten'],
                'dairy_free': ['dairy free', 'lactose free', 'no dairy'],
                'keto_friendly': ['keto', 'ketogenic', 'low carb'],
                'high_protein': ['protein', 'high protein'],
            }
            
            for tag, alias_list in aliases.items():
                if tag in available_tags and any(alias in user_input for alias in alias_list):
                    if tag not in found_restrictions:
                        found_restrictions.append(tag)
            
            if found_restrictions:
                self.dietary_restrictions = found_restrictions
                restriction_text = f"dietary preferences: {', '.join(found_restrictions)}"
            else:
                return "I didn't recognize those dietary preferences. Could you choose from the available options or type 'none' for no restrictions?"
        
        # Store decision and move to next step
        self.session_manager.update_context('dietary_restrictions', self.dietary_restrictions)
        self.current_step = "lifestyle_constraints"
        
        return f"Noted: {restriction_text}.\n\n{self._step_lifestyle_constraints()}"
    
    def _step_lifestyle_constraints(self) -> str:
        """Step 5: Collect lifestyle and cooking constraints"""
        return """⏱️ **LIFESTYLE & COOKING PREFERENCES**

Tell me about your cooking situation:

**Cooking Experience:**
1. **Beginner** - Simple meals, basic techniques
2. **Intermediate** - Comfortable with most cooking methods  
3. **Advanced** - Enjoy complex recipes and techniques

**Time Constraints:**
- **Quick meals only** (≤15 minutes prep)
- **Moderate time** (15-30 minutes is fine)
- **I have time to cook** (30+ minutes okay)

**Other Preferences:**
- **Household size** (how many people?)
- **Meal prep style** (batch cooking vs. cook fresh daily)

You can answer like: "Beginner, quick meals, cooking for 2 people" or answer each part separately.

What's your cooking situation?"""
    
    def _handle_lifestyle_constraints(self, user_input: str) -> str:
        """Handle lifestyle constraint collection"""
        user_input = user_input.lower().strip()
        
        # Parse cooking skill level
        if any(word in user_input for word in ['beginner', 'basic', 'simple', '1']):
            self.cooking_skill_level = 'beginner'
            skill_text = "beginner-friendly recipes"
        elif any(word in user_input for word in ['intermediate', 'comfortable', 'moderate', '2']):
            self.cooking_skill_level = 'intermediate' 
            skill_text = "intermediate cooking techniques"
        elif any(word in user_input for word in ['advanced', 'complex', 'expert', '3']):
            self.cooking_skill_level = 'advanced'
            skill_text = "advanced cooking methods"
        else:
            self.cooking_skill_level = 'intermediate'  # Default
            skill_text = "intermediate cooking techniques"
        
        # Parse time constraints
        if any(word in user_input for word in ['quick', '15', 'fast', 'busy']):
            self.time_constraints = 15
            time_text = "quick meals (≤15 minutes)"
        elif any(word in user_input for word in ['moderate', '30', 'medium']):
            self.time_constraints = 30
            time_text = "moderate prep time (≤30 minutes)"
        elif any(word in user_input for word in ['time to cook', 'longer', 'extended']):
            self.time_constraints = 60
            time_text = "flexible prep time"
        else:
            self.time_constraints = 30  # Default to moderate
            time_text = "moderate prep time (≤30 minutes)"
        
        # Parse household size
        import re
        numbers = re.findall(r'\d+', user_input)
        if numbers:
            size = int(numbers[0])
            if 1 <= size <= 8:
                self.household_size = size
            else:
                self.household_size = 2  # Default
        else:
            self.household_size = 2  # Default assumption
        
        # Store all constraints
        self.session_manager.update_context('cooking_skill_level', self.cooking_skill_level)
        self.session_manager.update_context('time_constraints', self.time_constraints) 
        self.session_manager.update_context('household_size', self.household_size)
        
        self.current_step = "generate_plan"
        
        summary = f"""Perfect! Here's your profile:
• **Cooking Level**: {skill_text}  
• **Time Preference**: {time_text}
• **Household Size**: {self.household_size} {"person" if self.household_size == 1 else "people"}

🎯 **READY TO GENERATE YOUR MEAL PLAN!**

I'll create a {self.planning_duration}-day plan with {', '.join(self.meal_types)} targeting {self.daily_calorie_target} calories per day{' with ' + ', '.join(self.dietary_restrictions) if self.dietary_restrictions else ''}.

Would you like me to generate your personalized meal plan now? (Type 'yes' to proceed)"""
        
        return summary
    
    def _handle_generate_plan(self, user_input: str) -> str:
        """Handle meal plan generation trigger"""
        user_input = user_input.lower().strip()
        
        if user_input in ['yes', 'y', 'generate', 'create', 'go', 'proceed', 'sure']:
            # Generate the meal plan
            try:
                generated_plan = self._generate_meal_plan()
                if isinstance(generated_plan, dict):
                    self.meal_plan = generated_plan
                    self.current_step = "plan_display"
                    return self._display_meal_plan()
                else:
                    return f"I encountered an issue generating your meal plan: {generated_plan}\nWould you like me to try again with slightly different criteria?"
            except Exception as e:
                return f"I encountered an issue generating your meal plan: {str(e)}\nWould you like me to try again with slightly different criteria?"
        else:
            return "No problem! Feel free to adjust any of your preferences, or type 'yes' when you're ready for me to generate your meal plan."
    
    def _generate_meal_plan(self) -> Dict:
        """Core meal plan generation algorithm"""
        print("🔄 Generating your personalized meal plan...")
        
        plan = {}
        used_meals = set()  # Track used meals for variety
        
        # Calculate target calories per meal type
        meal_calorie_targets = {}
        for meal_type in self.meal_types:
            if meal_type in self.meal_calorie_distribution:
                meal_calorie_targets[meal_type] = int(
                    self.daily_calorie_target * self.meal_calorie_distribution[meal_type]
                )
            else:
                # Fallback for any unexpected meal types
                meal_calorie_targets[meal_type] = 400
        
        # Generate plan for each day
        for day in range(1, self.planning_duration + 1):
            day_plan = {}
            
            for meal_type in self.meal_types:
                target_calories = meal_calorie_targets[meal_type]
                
                # Find suitable meals for this meal type with flexible filtering
                # First try strict filtering
                suitable_meals = self.data_loader.filter_meals_by_multiple_criteria(
                    meal_type=meal_type,
                    max_calories=target_calories + 100,  # ±100 calorie tolerance
                    min_calories=target_calories - 100,
                    dietary_tags=self.dietary_restrictions,
                    max_prep_time=self.time_constraints
                )
                
                # If no meals found, try with looser calorie constraints
                if not suitable_meals:
                    suitable_meals = self.data_loader.filter_meals_by_multiple_criteria(
                        meal_type=meal_type,
                        max_calories=target_calories + 150,  # ±150 calorie tolerance
                        min_calories=max(target_calories - 150, 100),  # Don't go below 100 calories
                        dietary_tags=self.dietary_restrictions,
                        max_prep_time=self.time_constraints
                    )
                
                # If still no meals, try without calorie constraints
                if not suitable_meals:
                    suitable_meals = self.data_loader.filter_meals_by_multiple_criteria(
                        meal_type=meal_type,
                        dietary_tags=self.dietary_restrictions,
                        max_prep_time=self.time_constraints
                    )
                
                # Remove already used meals (for variety)
                available_meals = [meal for meal in suitable_meals if meal['id'] not in used_meals]
                
                # If no unused meals available, reset used meals and allow reuse
                if not available_meals:
                    available_meals = suitable_meals
                    used_meals.clear()  # Reset for better variety
                
                if available_meals:
                    # Select best meal based on calorie match and variety
                    selected_meal = self._select_optimal_meal(available_meals, target_calories, used_meals)
                    day_plan[meal_type] = selected_meal
                    used_meals.add(selected_meal['id'])
                    
                    # Reset used meals if we've used most available meals (keep variety alive)
                    if len(used_meals) > len(available_meals) * 0.8:
                        used_meals = {selected_meal['id']}  # Keep only the most recent meal
                else:
                    # Fallback if no meals found - set error flag but continue to return dict
                    print(f"Warning: No meals found for {meal_type} on day {day}")
                    # Use a placeholder meal or skip this slot
                    day_plan[meal_type] = {
                        'id': f'placeholder_{meal_type}_{day}',
                        'name': f'Custom {meal_type.title()}',
                        'calories': target_calories,
                        'prep_time': 15,
                        'nutrition': {'protein': 0, 'carbs': 0, 'fat': 0, 'fiber': 0},
                        'components': []
                    }
            
            plan[f"Day {day}"] = day_plan
        
        return plan
    
    def _select_optimal_meal(self, meals: List[Dict], target_calories: int, used_meals: set) -> Dict:
        """Select the most optimal meal based on calories and variety"""
        scored_meals = []
        
        for meal in meals:
            score = 0
            
            # Calorie proximity score (0-100)
            calorie_diff = abs(meal['calories'] - target_calories)
            calorie_score = max(0, 100 - (calorie_diff / 75 * 100))  # 75 is our tolerance
            score += calorie_score * 0.6  # 60% weight for calorie match
            
            # Variety score (avoid recently used meals)
            if meal['id'] not in used_meals:
                variety_score = 100
            else:
                variety_score = 20  # Penalty for reuse
            score += variety_score * 0.4  # 40% weight for variety
            
            scored_meals.append((meal, score))
        
        # Sort by score and return best meal
        scored_meals.sort(key=lambda x: x[1], reverse=True)
        return scored_meals[0][0]
    
    def _display_meal_plan(self) -> str:
        """Display the generated meal plan with nutrition summary"""
        if not self.meal_plan:
            return "No meal plan generated yet."
        
        display = "🎉 **YOUR PERSONALIZED MEAL PLAN**\n\n"
        
        # Day-by-day breakdown
        total_calories = 0
        total_protein = 0
        total_carbs = 0
        total_fat = 0
        total_fiber = 0
        
        meal_emojis = {
            'breakfast': '🌅',
            'lunch': '🌞', 
            'dinner': '🌙',
            'snack': '🍎'
        }
        
        for day_name, day_meals in self.meal_plan.items():
            display += f"**{day_name.upper()}:**\n"
            daily_calories = 0
            
            for meal_type, meal in day_meals.items():
                emoji = meal_emojis.get(meal_type, '🍽️')
                display += f"{emoji} **{meal_type.title()}**: {meal['name']} - {meal['calories']}cal ({meal['prep_time']}min)\n"
                
                daily_calories += meal['calories']
                total_protein += meal['nutrition']['protein']
                total_carbs += meal['nutrition'].get('carbs', meal['nutrition'].get('carbohydrates', 0))
                total_fat += meal['nutrition']['fat'] 
                total_fiber += meal['nutrition']['fiber']
            
            display += f"📊 **Daily Total**: {daily_calories}cal\n\n"
            total_calories += daily_calories
        
        # Weekly nutrition summary
        avg_daily_calories = total_calories / self.planning_duration
        avg_protein = total_protein / self.planning_duration
        avg_carbs = total_carbs / self.planning_duration
        avg_fat = total_fat / self.planning_duration
        avg_fiber = total_fiber / self.planning_duration
        
        # Calculate percentages
        protein_pct = (avg_protein * 4 / avg_daily_calories * 100) if avg_daily_calories > 0 else 0
        carbs_pct = (avg_carbs * 4 / avg_daily_calories * 100) if avg_daily_calories > 0 else 0
        fat_pct = (avg_fat * 9 / avg_daily_calories * 100) if avg_daily_calories > 0 else 0
        
        display += f"""📈 **NUTRITION SUMMARY ({self.planning_duration} days):**
• **Average daily calories**: {avg_daily_calories:.0f}
• **Protein**: {avg_protein:.1f}g avg ({protein_pct:.1f}% of calories)
• **Carbohydrates**: {avg_carbs:.1f}g avg ({carbs_pct:.1f}% of calories)  
• **Fat**: {avg_fat:.1f}g avg ({fat_pct:.1f}% of calories)
• **Fiber**: {avg_fiber:.1f}g avg

⚡ **NUTRITIONAL ANALYSIS:**
"""
        
        # Add recommendations
        recommendations = []
        if protein_pct < 20:
            recommendations.append("Consider adding more protein-rich foods")
        elif protein_pct > 35:
            recommendations.append("Protein intake is very high - consider balancing with more carbs")
            
        if avg_fiber < 25:
            recommendations.append("Try to include more high-fiber foods")
        elif avg_fiber > 35:
            recommendations.append("Excellent fiber intake!")
            
        if 20 <= protein_pct <= 35 and 45 <= carbs_pct <= 65 and 20 <= fat_pct <= 35:
            recommendations.append("Your macro balance looks excellent!")
            
        if recommendations:
            for rec in recommendations:
                display += f"• {rec}\n"
        
        self.current_step = "plan_display"
        
        display += "\n🎯 **How does this meal plan look?**\n"
        display += "1. **Approve** - This looks great!\n"
        display += "2. **Regenerate** - Try different meal combinations\n" 
        display += "3. **Customize** - Make specific changes\n\n"
        display += "What would you like to do?"
        
        return display
    
    def _handle_plan_display(self, user_input: str) -> str:
        """Handle user response to meal plan display"""
        user_input = user_input.lower().strip()
        
        if user_input in ['1', 'approve', 'looks good', 'perfect', 'great']:
            self.current_step = "final_actions"
            return self._step_final_actions()
        elif user_input in ['2', 'regenerate', 'try again', 'different']:
            # Regenerate with same criteria
            try:
                self.meal_plan = self._generate_meal_plan()
                return f"🔄 **Here's a new meal plan for you:**\n\n{self._display_meal_plan()}"
            except Exception as e:
                return f"I had trouble generating a new plan: {str(e)}\nWould you like to modify your criteria?"
        elif user_input in ['3', 'customize', 'changes', 'modify']:
            return """🔧 **CUSTOMIZATION OPTIONS:**

What would you like to adjust?
1. **Swap a specific meal** - "Change dinner on day 2"
2. **Different calorie target** - Adjust daily calories
3. **Modify dietary restrictions** - Add/remove dietary preferences
4. **Change time constraints** - Adjust prep time limits

Tell me what you'd like to customize!"""
        else:
            return "Please choose 1 to Approve, 2 to Regenerate, or 3 to Customize your meal plan."
    
    def _step_final_actions(self) -> str:
        """Step 6: Final action selection"""
        return """🎉 **YOUR MEAL PLAN IS READY!**

What would you like to do next?

1. **Generate Grocery List** - Get a complete shopping list with all ingredients
2. **Export Plan** - Save as PDF or send to email  
3. **Download Calendar** - Get ICS file for your calendar app
4. **Start Cooking** - Get guidance for your first meal
5. **Save & Exit** - Keep this plan and finish

Choose your next action!"""
    
    def _handle_final_actions(self, user_input: str) -> str:
        """Handle final action selection"""
        user_input = user_input.lower().strip()
        
        if user_input in ['1', 'grocery', 'shopping', 'grocery list']:
            return self._generate_grocery_list()
        elif user_input in ['2', 'export', 'pdf', 'email']:
            return self._export_meal_plan()
        elif user_input in ['3', 'calendar', 'ics', 'download']:
            return self._generate_calendar_file()
        elif user_input in ['4', 'cook', 'cooking', 'start cooking']:
            return self._start_cooking_first_meal()
        elif user_input in ['5', 'save', 'exit', 'finish', 'done']:
            return self._save_and_exit()
        else:
            return "Please choose 1-5 for your preferred action, or tell me what you'd like to do with your meal plan."
    
    def _generate_grocery_list(self) -> str:
        """Generate consolidated grocery list from meal plan"""
        if not self.meal_plan or not isinstance(self.meal_plan, dict):
            return "No meal plan available to generate grocery list from."
        
        ingredient_totals = {}
        
        # Aggregate all ingredients from all meals
        for day_meals in self.meal_plan.values():
            if not isinstance(day_meals, dict):
                continue
                
            for meal in day_meals.values():
                if not isinstance(meal, dict) or 'components' not in meal:
                    continue
                    
                for component in meal['components']:
                    if not isinstance(component, dict):
                        continue
                        
                    food_id = component.get('food_id')
                    amount = component.get('amount', 0)
                    unit = component.get('unit', 'unit')
                    
                    if not food_id:
                        # Try using the name directly if no food_id
                        food_name = component.get('name')
                        if food_name:
                            key = f"{food_name}_{unit}"
                            if key in ingredient_totals:
                                ingredient_totals[key]['amount'] += amount
                            else:
                                ingredient_totals[key] = {
                                    'name': food_name,
                                    'amount': amount,
                                    'unit': unit,
                                    'category': 'Other'
                                }
                        continue
                    
                    # Get food details
                    food_item = self.data_loader.get_food_by_id(food_id)
                    if food_item:
                        food_name = food_item['name']
                        key = f"{food_name}_{unit}"
                        
                        if key in ingredient_totals:
                            ingredient_totals[key]['amount'] += amount
                        else:
                            ingredient_totals[key] = {
                                'name': food_name,
                                'amount': amount,
                                'unit': unit,
                                'category': food_item.get('category', 'Other')
                            }
                    else:
                        # Fallback to component name if food_item not found
                        food_name = component.get('name', 'Unknown ingredient')
                        key = f"{food_name}_{unit}"
                        if key in ingredient_totals:
                            ingredient_totals[key]['amount'] += amount
                        else:
                            ingredient_totals[key] = {
                                'name': food_name,
                                'amount': amount,
                                'unit': unit,
                                'category': 'Other'
                            }
        
        # Check if we have any ingredients
        if not ingredient_totals:
            return """🛒 **GROCERY LIST - No Ingredients Found**

It looks like your meal plan doesn't have detailed ingredient information available. 
This might be because some meals are placeholder entries or the ingredient data is not complete.

You can still use your meal plan as a guide and shop for the general meal types shown in your plan.

Would you like me to help you with anything else for your meal planning?"""
        
        # Organize by categories
        categories = {}
        for ingredient in ingredient_totals.values():
            category = ingredient['category']
            if category not in categories:
                categories[category] = []
            categories[category].append(ingredient)
        
        # Format grocery list
        grocery_list = f"🛒 **GROCERY LIST - {self.planning_duration} Day Meal Plan**\n\n"
        
        category_emojis = {
            'protein': '🥩',
            'dairy': '🧀', 
            'vegetable': '🥬',
            'fruit': '🍎',
            'grain': '🌾',
            'fat': '🫒',
            'Other': '📦'
        }
        
        for category, items in categories.items():
            emoji = category_emojis.get(category, '📦')
            grocery_list += f"{emoji} **{category.upper()}:**\n"
            for item in items:
                grocery_list += f"  • {item['name']} - {item['amount']:.1f} {item['unit']}\n"
            grocery_list += "\n"
        
        grocery_list += "💡 **TIPS:**\n"
        grocery_list += "• Amounts include 10% buffer for cooking losses\n"
        grocery_list += "• Check your pantry for items you may already have\n"
        grocery_list += "• Consider buying in bulk for better value\n\n"
        grocery_list += "Would you like me to help you with anything else for your meal plan?"
        
        return grocery_list
    
    def _export_meal_plan(self) -> str:
        """Export meal plan in various formats"""
        return """📧 **EXPORT OPTIONS:**

Your meal plan can be exported as:

• **PDF Summary** - Complete meal plan with nutrition analysis
• **Weekly Schedule** - Day-by-day meal calendar  
• **Nutrition Report** - Detailed nutritional breakdown
• **Shopping Guide** - Meal plan + grocery list combined

📱 **Export Format:**
Your meal plan has been formatted for easy sharing and printing. You can copy the meal plan details I showed you earlier and paste them into any document or email.

🎯 **What's included:**
• Complete daily meal schedules
• Nutritional summary and analysis
• Prep time estimates
• Calorie targets and actual values

Would you like me to show you the meal plan summary again, or help you with something else?"""
    
    def _generate_calendar_file(self) -> str:
        """Generate calendar integration information"""
        return """🗓️ **CALENDAR INTEGRATION GUIDE**

To add your meal plan to your calendar:

📱 **Manual Calendar Entry:**
For each meal in your plan, create calendar events with:
• **Title**: 🍽️ [Meal Name] ([prep_time] min)
• **Time**: Your preferred meal times
• **Description**: Calorie count and prep notes
• **Reminders**: 30 minutes before for prep time

⏰ **Suggested Meal Times:**
• Breakfast: 7:00 AM - 8:00 AM  
• Lunch: 12:00 PM - 1:00 PM
• Dinner: 6:00 PM - 7:00 PM
• Snacks: 3:00 PM or 8:00 PM

📋 **Additional Events to Add:**
• 🛒 Grocery Shopping (day before meal plan starts)
• 🥘 Meal Prep Day (if batch cooking)
• 📊 Weekly Menu Review (end of week)

💡 **Pro Tip**: Set prep time reminders so you know when to start cooking each meal!

Would you like me to help you with anything else for your meal planning?"""
    
    def _start_cooking_first_meal(self) -> str:
        """Transition to cooking guidance for first meal"""
        if not self.meal_plan:
            return "No meal plan available to start cooking from."
        
        # Find the first meal in the plan
        first_day = list(self.meal_plan.keys())[0]
        first_day_meals = self.meal_plan[first_day]
        
        # Get first meal (prioritize breakfast if available)
        if 'breakfast' in first_day_meals:
            first_meal = first_day_meals['breakfast']
            meal_type = 'breakfast'
        else:
            meal_type = list(first_day_meals.keys())[0]
            first_meal = first_day_meals[meal_type]
        
        cooking_prep = f"""👨‍🍳 **LET'S START COOKING!**

**Your First Meal**: {first_meal['name']} ({meal_type.title()})

🎯 **Meal Details:**
• **Calories**: {first_meal['calories']}cal
• **Prep Time**: {first_meal['prep_time']} minutes
• **Nutrition**: {first_meal['nutrition']['protein']}g protein, {first_meal['nutrition'].get('carbs', first_meal['nutrition'].get('carbohydrates', 0))}g carbs

📝 **Ingredients Needed:**"""
        
        if 'components' in first_meal:
            for component in first_meal['components']:
                food_item = self.data_loader.get_food_by_id(component['food_id'])
                if food_item:
                    cooking_prep += f"\n• {component['amount']}{component['unit']} {food_item['name']}"
        
        cooking_prep += f"""\n\n🔄 **Ready to cook?** 
This meal plan is designed to be flexible - you can prepare this meal using basic cooking methods suitable for your {self.cooking_skill_level} skill level.

💡 **Next Steps:**
1. Gather your ingredients
2. Follow your preferred cooking method  
3. Track your meal completion
4. Move on to the next planned meal

Would you like me to help you with anything else for your meal planning journey?"""
        
        return cooking_prep
    
    def _save_and_exit(self) -> str:
        """Save meal plan and conclude journey"""
        # Store the meal plan in session for potential future reference
        self.session_manager.update_context('completed_meal_plan', {
            'plan': self.meal_plan,
            'duration': self.planning_duration,
            'meal_types': self.meal_types,
            'calorie_target': self.daily_calorie_target,
            'dietary_restrictions': self.dietary_restrictions,
            'generated_date': datetime.now().isoformat()
        })
        
        return f"""✅ **MEAL PLAN SAVED SUCCESSFULLY!**

🎯 **Your {self.planning_duration}-day meal plan** has been created and saved with:
• **{len(self.meal_types)} meal types** per day: {', '.join(self.meal_types)}
• **{self.daily_calorie_target} calorie target** per day
• **Dietary preferences**: {', '.join(self.dietary_restrictions) if self.dietary_restrictions else 'No restrictions'}
• **Skill level**: {self.cooking_skill_level.title()} cooking

🍽️ **Quick Access**: You can refer back to your meal plan details anytime. 

💡 **Remember**: This meal plan is flexible - feel free to swap meals, adjust portions, or modify based on your daily needs!

**Thanks for using the meal planning feature!** Is there anything else I can help you with today?"""

    def get_completion_message(self) -> str:
        """Return completion message for the journey"""
        return "Your personalized meal plan has been created successfully! 🎉"