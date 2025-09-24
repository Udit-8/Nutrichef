"""
Food Calorie Tracking Journey
Comprehensive 10-step food logging and nutrition analysis system
"""

import re
from datetime import datetime, date
from typing import Dict, List, Any, Optional, Tuple
try:
    from ..core.base_journey import BaseJourney
    from ..utils.nutrition_utils import (
        FoodSearchEngine, NutritionCalculator, DiaryManager, 
        ProgressTracker, FoodEntry
    )
except ImportError:
    from core.base_journey import BaseJourney
    from utils.nutrition_utils import (
        FoodSearchEngine, NutritionCalculator, DiaryManager, 
        ProgressTracker, FoodEntry
    )

class FoodCalorieTrackingJourney(BaseJourney):
    """
    Complete food calorie tracking journey with 10 comprehensive steps:
    1. Tracking Mode Determination
    2. Food Entry Method Selection
    3. Food Search & Identification
    4. Portion Size Selection
    5. Meal Timing & Classification
    6. Nutritional Analysis
    7. Daily Progress Tracking
    8. Insights & Recommendations
    9. Goal Achievement Monitoring
    10. Cross-Journey Integration
    """
    
    def __init__(self, data_loader, session_manager):
        super().__init__(session_manager)
        self.data_loader = data_loader
        self.journey_name = "food_calorie_tracking"
        
        # Initialize utility classes
        self.food_search = FoodSearchEngine(data_loader)
        self.nutrition_calc = NutritionCalculator()
        self.diary_manager = DiaryManager(session_manager)
        self.progress_tracker = ProgressTracker(session_manager)
        
        # Journey state
        self.current_food = None
        self.selected_serving = None
        self.tracking_mode = None
        self.entry_method = None
        
        # Step definitions
        self.steps = {
            1: "Tracking Mode Determination",
            2: "Food Entry Method Selection", 
            3: "Food Search & Identification",
            4: "Portion Size Selection",
            5: "Meal Timing & Classification",
            6: "Nutritional Analysis",
            7: "Daily Progress Tracking",
            8: "Insights & Recommendations",
            9: "Goal Achievement Monitoring",
            10: "Cross-Journey Integration"
        }
    
    def start_journey(self, user_input: str = "") -> str:
        """Start the food calorie tracking journey"""
        self.current_step = 1
        self.save_state()
        
        return self.step_1_tracking_mode_determination(user_input)
    
    def step_1_tracking_mode_determination(self, user_input: str) -> str:
        """Step 1: Determine what type of tracking action user wants"""
        self.current_step = 1
        
        # Analyze user intent from input
        user_input_lower = user_input.lower()
        
        # Check for specific tracking modes in user input
        if any(phrase in user_input_lower for phrase in ['view', 'show', 'diary', 'progress', 'totals', 'summary']):
            self.tracking_mode = "view_diary"
            return self._handle_view_diary_mode()
        
        elif any(phrase in user_input_lower for phrase in ['edit', 'delete', 'remove', 'change', 'modify']):
            self.tracking_mode = "manage_logs"
            return self._handle_manage_logs_mode()
        
        else:
            # Default to logging new food
            self.tracking_mode = "log_new_food"
        
        # Present tracking options
        response = "🍎 **Food Calorie Tracking**\n\n"
        response += "What would you like to do today?\n\n"
        response += "📝 **1. Log New Food** - Add food you just ate\n"
        response += "📊 **2. View Food Diary** - See today's progress\n"
        response += "✏️ **3. Manage Previous Logs** - Edit/delete entries\n\n"
        
        if self.tracking_mode == "log_new_food":
            response += "I'll help you **log new food**! Let's continue...\n\n"
            self.current_step = 2
            self.save_state()
            return response + self.step_2_food_entry_method_selection("")
        
        response += "Reply with '1', '2', or '3' to choose an option."
        
        self.save_state()
        return response
    
    def _handle_view_diary_mode(self) -> str:
        """Handle viewing food diary and daily progress"""
        daily_summary = self.diary_manager.get_daily_summary()
        
        response = "📊 **Today's Food Diary**\n\n"
        
        if daily_summary['total_entries'] == 0:
            response += "No food entries logged today yet.\n\n"
            response += "Would you like to start logging food?\n"
            response += "Reply 'yes' to begin food logging."
            return response
        
        # Show daily totals
        totals = daily_summary['nutrition_totals']
        response += f"🔢 **Daily Totals ({daily_summary['date']})**\n"
        response += f"• Total Calories: {totals['calories']}\n"
        response += f"• Protein: {totals['macros']['protein']}g\n"
        response += f"• Carbs: {totals['macros']['carbs']}g\n"
        response += f"• Fat: {totals['macros']['fat']}g\n"
        response += f"• Fiber: {totals['macros']['fiber']}g\n\n"
        
        # Show meal breakdown
        response += "🍽️ **Meals Today:**\n"
        for meal_type, meal_data in totals['meal_breakdown'].items():
            if meal_data['count'] > 0:
                response += f"• {meal_type.capitalize()}: {meal_data['calories']} cal ({meal_data['count']} items)\n"
        
        response += "\n"
        
        # Show recent entries
        response += "📝 **Recent Entries:**\n"
        for entry in daily_summary['entries'][-5:]:  # Show last 5
            response += f"• {entry['time']} - {entry['food_name']} ({entry['serving']}) - {entry['calories']} cal\n"
        
        # Show progress towards goals
        current_totals = daily_summary['nutrition_totals']
        progress = self.progress_tracker.calculate_progress(current_totals)
        
        response += f"\n🎯 **Goal Progress:**\n"
        response += f"• Calories: {progress['calories']['percentage']:.0f}% ({progress['calories']['current']}/{progress['calories']['goal']})\n"
        response += f"• {progress['overall']['status']}\n\n"
        
        response += "Would you like to:\n"
        response += "1. **Log more food**\n"
        response += "2. **Set nutrition goals**\n"
        response += "3. **Get detailed analysis**\n\n"
        response += "Reply with your choice or ask me anything about your nutrition!"
        
        return response
    
    def _handle_manage_logs_mode(self) -> str:
        """Handle editing or deleting previous entries"""
        entries = self.diary_manager.get_today_entries()
        
        if not entries:
            return "No food entries to manage today. Would you like to log some food instead?"
        
        response = "✏️ **Manage Food Entries**\n\n"
        response += "Today's entries:\n\n"
        
        for i, entry in enumerate(entries[-10:], 1):  # Show last 10
            response += f"{i}. {entry.timestamp.strftime('%H:%M')} - "
            response += f"{entry.food_name} ({entry.serving_description}) - "
            response += f"{entry.calories} cal - {entry.meal_type}\n"
        
        response += "\nTo delete an entry, reply with 'delete [number]' (e.g., 'delete 3')\n"
        response += "To add new food instead, reply 'add food'\n"
        
        return response
    
    def step_2_food_entry_method_selection(self, user_input: str) -> str:
        """Step 2: Choose how to enter food information"""
        self.current_step = 2
        
        # Check for specific entry method in user input
        user_input_lower = user_input.lower()
        
        if any(phrase in user_input_lower for phrase in ['search', 'find', 'look for']):
            self.entry_method = "text_search"
        elif any(phrase in user_input_lower for phrase in ['recent', 'previous', 'again', 'same']):
            self.entry_method = "recent_foods"
        elif any(phrase in user_input_lower for phrase in ['manual', 'custom', 'enter myself']):
            self.entry_method = "manual_entry"
        
        response = "🔍 **How to Add Your Food**\n\n"
        response += "Choose your preferred method:\n\n"
        response += "🔎 **1. Search Food Database** - Find food by name\n"
        response += "📝 **2. Manual Entry** - Enter calories yourself\n"
        response += "🕐 **3. Recent Foods** - Quick select from history\n\n"
        
        if self.entry_method:
            if self.entry_method == "text_search":
                response += "Great! I'll help you **search** for food.\n\n"
                return response + self._start_text_search()
            elif self.entry_method == "recent_foods":
                response += "Perfect! Let me show your **recent foods**.\n\n"
                return response + self._start_recent_foods()
            elif self.entry_method == "manual_entry":
                response += "Got it! I'll help you **manually enter** food details.\n\n"
                return response + self._start_manual_entry()
        
        response += "Reply with '1', '2', or '3' to choose your method."
        self.save_state()
        return response
    
    def _start_text_search(self) -> str:
        """Start text search process"""
        self.entry_method = "text_search"
        self.current_step = 3
        self.save_state()
        
        response = "🔎 **Search Food Database**\n\n"
        response += "Type the name of the food you want to log.\n\n"
        response += "**Examples:**\n"
        response += "• \"chicken breast\"\n"
        response += "• \"greek yogurt\"\n"
        response += "• \"quinoa\"\n"
        response += "• \"broccoli\"\n\n"
        response += "What food did you eat?"
        
        return response
    
    def _start_recent_foods(self) -> str:
        """Start recent foods selection"""
        self.entry_method = "recent_foods"
        
        recent_foods = self.food_search.get_recent_foods(self.diary_manager, limit=10)
        
        if not recent_foods:
            response = "No recent foods found in your history.\n\n"
            response += "Let's search for food instead. What food would you like to log?"
            return self._start_text_search()
        
        response = "🕐 **Recent Foods**\n\n"
        response += "Select from your recently logged foods:\n\n"
        
        for i, food in enumerate(recent_foods[:8], 1):
            last_serving = food.get('most_common_serving', 'Standard serving')
            response += f"{i}. **{food['name']}** ({last_serving})\n"
            
            # Show basic nutrition for 100g reference
            nutrition_100g = self.data_loader.calculate_food_nutrition_per_100g(food)
            response += f"   ~{nutrition_100g['calories']} cal/100g\n\n"
        
        response += "Reply with the number of your choice (1-8).\n"
        response += "Or type a food name to search instead."
        
        self.current_step = 3
        self.save_state()
        return response
    
    def _start_manual_entry(self) -> str:
        """Start manual food entry"""
        self.entry_method = "manual_entry"
        self.current_step = 3
        self.save_state()
        
        response = "📝 **Manual Food Entry**\n\n"
        response += "Please provide the food details in this format:\n\n"
        response += "**Food name, calories, protein(g), carbs(g), fat(g)**\n\n"
        response += "**Examples:**\n"
        response += "• \"Homemade pasta, 350, 12, 45, 8\"\n"
        response += "• \"Restaurant burger, 650, 25, 35, 40\"\n"
        response += "• \"Protein shake, 120, 20, 5, 2\"\n\n"
        response += "What food would you like to add?"
        
        return response
    
    def step_3_food_search_identification(self, user_input: str) -> str:
        """Step 3: Search and identify the food"""
        self.current_step = 3
        
        if not user_input.strip():
            return "Please tell me what food you'd like to log."
        
        # Handle different entry methods
        if self.entry_method == "text_search":
            return self._handle_text_search(user_input)
        elif self.entry_method == "recent_foods":
            return self._handle_recent_food_selection(user_input)
        elif self.entry_method == "manual_entry":
            return self._handle_manual_entry(user_input)
        else:
            # Default to text search
            return self._handle_text_search(user_input)
    
    def _handle_text_search(self, user_input: str) -> str:
        """Handle text-based food search"""
        search_results = self.food_search.search_foods(user_input, limit=8)
        
        if not search_results:
            response = "🔍 No foods found matching your search.\n\n"
            response += "**Suggestions:**\n"
            response += "• Try simpler terms (e.g., 'chicken' instead of 'grilled chicken breast')\n"
            response += "• Check spelling\n"
            response += "• Try manual entry if it's a custom food\n\n"
            response += "Search again or type 'manual' for manual entry."
            return response
        
        response = f"🔍 **Search Results for '{user_input}'**\n\n"
        response += "Select your food:\n\n"
        
        for i, food in enumerate(search_results, 1):
            response += f"{i}. **{food['name']}**\n"
            response += f"   Category: {food.get('category', 'N/A').capitalize()}\n"
            
            # Show nutrition for reference (100g serving)
            nutrition_100g = self.data_loader.calculate_food_nutrition_per_100g(food)
            response += f"   ~{nutrition_100g['calories']} cal/100g, "
            response += f"{nutrition_100g['macros'].get('protein', 0)}g protein\n"
            
            # Show available serving options count
            serving_count = len(food.get('serving_options', []))
            response += f"   {serving_count} serving options available\n\n"
        
        response += f"Reply with the number of your choice (1-{len(search_results)}).\n"
        response += "Or search for a different food."
        
        # Store search results for selection
        self.session_manager.set('food_search_results', search_results)
        self.save_state()
        return response
    
    def _handle_recent_food_selection(self, user_input: str) -> str:
        """Handle selection from recent foods"""
        try:
            choice = int(user_input.strip())
            recent_foods = self.food_search.get_recent_foods(self.diary_manager, limit=10)
            
            if 1 <= choice <= len(recent_foods):
                selected_food = recent_foods[choice - 1]
                self.current_food = selected_food
                self.current_step = 4
                self.save_state()
                return self.step_4_portion_size_selection("")
            else:
                return f"Please choose a number between 1 and {len(recent_foods)}."
                
        except ValueError:
            # User typed food name instead of number - switch to text search
            return self._handle_text_search(user_input)
    
    def _handle_manual_entry(self, user_input: str) -> str:
        """Handle manual food entry parsing"""
        # Parse format: "Food name, calories, protein, carbs, fat"
        parts = [part.strip() for part in user_input.split(',')]
        
        if len(parts) < 2:
            response = "Please use the format: **Food name, calories, protein(g), carbs(g), fat(g)**\n\n"
            response += "Example: \"Homemade pasta, 350, 12, 45, 8\""
            return response
        
        try:
            food_name = parts[0]
            calories = int(parts[1])
            protein = float(parts[2]) if len(parts) > 2 else 0
            carbs = float(parts[3]) if len(parts) > 3 else 0
            fat = float(parts[4]) if len(parts) > 4 else 0
            
            # Create custom food entry
            custom_food = {
                'id': f'custom_{datetime.now().timestamp()}',
                'name': food_name,
                'category': 'custom',
                'serving_options': [{
                    'id': 'serving_custom',
                    'description': 'As entered',
                    'weight_g': 100,
                    'calories': calories,
                    'macros': {
                        'protein': protein,
                        'carbs': carbs,
                        'fat': fat,
                        'fiber': 0,
                        'sugar': 0
                    }
                }]
            }
            
            self.current_food = custom_food
            self.selected_serving = custom_food['serving_options'][0]
            
            # Skip portion selection for manual entry
            self.current_step = 5
            self.save_state()
            
            response = f"✅ **Custom Food Added**\n\n"
            response += f"**{food_name}**\n"
            response += f"• Calories: {calories}\n"
            response += f"• Protein: {protein}g\n"
            response += f"• Carbs: {carbs}g\n"
            response += f"• Fat: {fat}g\n\n"
            
            return response + self.step_5_meal_timing_classification("")
            
        except (ValueError, IndexError):
            response = "Invalid format. Please use: **Food name, calories, protein(g), carbs(g), fat(g)**\n\n"
            response += "Numbers only for calories and macros.\n"
            response += "Example: \"Protein bar, 200, 15, 20, 6\""
            return response
    
    def step_4_portion_size_selection(self, user_input: str) -> str:
        """Step 4: Select portion size and quantity"""
        self.current_step = 4
        
        # Handle food selection from search results
        if not self.current_food and user_input.strip():
            try:
                choice = int(user_input.strip())
                search_results = self.session_manager.get('food_search_results', [])
                
                if 1 <= choice <= len(search_results):
                    self.current_food = search_results[choice - 1]
                else:
                    return f"Please choose a number between 1 and {len(search_results)}."
            except ValueError:
                return "Please enter the number of your food choice."
        
        if not self.current_food:
            return "Please select a food first."
        
        # Show serving options
        serving_options = self.current_food.get('serving_options', [])
        
        if not serving_options:
            return "This food doesn't have serving information available. Please try a different food."
        
        response = f"🥄 **Portion Size for {self.current_food['name']}**\n\n"
        response += "Choose your serving size:\n\n"
        
        for i, serving in enumerate(serving_options, 1):
            response += f"{i}. **{serving['description']}**\n"
            response += f"   {serving['calories']} calories, {serving['macros'].get('protein', 0)}g protein\n\n"
        
        response += f"Reply with the number (1-{len(serving_options)}) or specify quantity:\n"
        response += "• '2' for option 2\n"
        response += "• '1.5 x 3' for 1.5 times option 3\n"
        response += "• '0.5 x 1' for half of option 1"
        
        self.save_state()
        return response
    
    def step_5_meal_timing_classification(self, user_input: str) -> str:
        """Step 5: Classify meal type and timing"""
        self.current_step = 5
        
        # Handle portion selection
        if not self.selected_serving and user_input.strip():
            portion_result = self._parse_portion_input(user_input)
            if isinstance(portion_result, str):
                return portion_result  # Error message
        
        if not self.selected_serving:
            return "Please select a portion size first."
        
        # Determine meal type based on current time
        current_hour = datetime.now().hour
        
        if 5 <= current_hour < 11:
            suggested_meal = "breakfast"
        elif 11 <= current_hour < 16:
            suggested_meal = "lunch"
        elif 16 <= current_hour < 21:
            suggested_meal = "dinner"
        else:
            suggested_meal = "snack"
        
        response = f"🍽️ **Meal Classification**\n\n"
        response += f"**Food:** {self.current_food['name']}\n"
        response += f"**Serving:** {self.selected_serving['description']}\n"
        response += f"**Calories:** {self.selected_serving['calories']}\n\n"
        
        response += "What type of meal is this?\n\n"
        response += f"1. **Breakfast** 🌅\n"
        response += f"2. **Lunch** ☀️\n"
        response += f"3. **Dinner** 🌙\n"
        response += f"4. **Snack** 🍎\n\n"
        
        response += f"Based on the time ({datetime.now().strftime('%H:%M')}), I suggest: **{suggested_meal.capitalize()}**\n\n"
        response += f"Reply with the number (1-4) or press Enter for '{suggested_meal}'."
        
        # Store suggested meal type
        self.session_manager.set('suggested_meal_type', suggested_meal)
        self.save_state()
        return response
    
    def _parse_portion_input(self, user_input: str) -> Optional[str]:
        """Parse portion selection input"""
        user_input = user_input.strip().lower()
        serving_options = self.current_food.get('serving_options', [])
        
        # Parse different input formats
        # Format 1: Simple number (e.g., "2")
        if user_input.isdigit():
            choice = int(user_input)
            if 1 <= choice <= len(serving_options):
                self.selected_serving = serving_options[choice - 1].copy()
                self.selected_serving['quantity'] = 1.0
                return None
            else:
                return f"Please choose a number between 1 and {len(serving_options)}."
        
        # Format 2: Quantity x Choice (e.g., "1.5 x 2" or "2 x 1")
        quantity_match = re.match(r'(\d+(?:\.\d+)?)\s*x?\s*(\d+)', user_input)
        if quantity_match:
            quantity = float(quantity_match.group(1))
            choice = int(quantity_match.group(2))
            
            if 1 <= choice <= len(serving_options):
                base_serving = serving_options[choice - 1]
                
                # Scale the serving
                self.selected_serving = {
                    'id': base_serving['id'],
                    'description': f"{quantity} x {base_serving['description']}",
                    'weight_g': base_serving.get('weight_g', 0) * quantity,
                    'calories': int(base_serving['calories'] * quantity),
                    'macros': {},
                    'quantity': quantity
                }
                
                # Scale macros
                for macro, value in base_serving.get('macros', {}).items():
                    self.selected_serving['macros'][macro] = round(value * quantity, 1)
                
                return None
            else:
                return f"Please choose a serving number between 1 and {len(serving_options)}."
        
        return f"Invalid format. Please use a number (1-{len(serving_options)}) or 'quantity x number' (e.g., '1.5 x 2')."
    
    def step_6_nutritional_analysis(self, user_input: str) -> str:
        """Step 6: Provide detailed nutritional analysis"""
        self.current_step = 6
        
        # Handle meal type selection
        meal_type = self._parse_meal_type_input(user_input)
        if not meal_type:
            return "Please select a meal type (1-4) or press Enter for the suggested option."
        
        # Create food entry
        food_entry = FoodEntry(
            food_id=self.current_food['id'],
            food_name=self.current_food['name'],
            serving_id=self.selected_serving['id'],
            serving_description=self.selected_serving['description'],
            quantity=self.selected_serving.get('quantity', 1.0),
            calories=self.selected_serving['calories'],
            macros=self.selected_serving['macros'],
            meal_type=meal_type,
            timestamp=datetime.now()
        )
        
        # Add to diary
        if self.diary_manager.add_entry(food_entry):
            response = "✅ **Food Logged Successfully!**\n\n"
        else:
            response = "⚠️ **Food Added** (with temporary storage)\n\n"
        
        # Show detailed nutritional analysis
        response += f"**{food_entry.food_name}**\n"
        response += f"• Serving: {food_entry.serving_description}\n"
        response += f"• Meal Type: {meal_type.capitalize()}\n"
        response += f"• Time: {food_entry.timestamp.strftime('%H:%M')}\n\n"
        
        response += "📊 **Nutritional Breakdown:**\n"
        response += f"• **Calories:** {food_entry.calories}\n"
        response += f"• **Protein:** {food_entry.macros.get('protein', 0)}g\n"
        response += f"• **Carbs:** {food_entry.macros.get('carbs', 0)}g\n"
        response += f"• **Fat:** {food_entry.macros.get('fat', 0)}g\n"
        response += f"• **Fiber:** {food_entry.macros.get('fiber', 0)}g\n"
        response += f"• **Sugar:** {food_entry.macros.get('sugar', 0)}g\n\n"
        
        # Calculate macro percentages
        calories = food_entry.calories
        if calories > 0:
            protein_cal = food_entry.macros.get('protein', 0) * 4
            carbs_cal = food_entry.macros.get('carbs', 0) * 4
            fat_cal = food_entry.macros.get('fat', 0) * 9
            
            protein_pct = (protein_cal / calories) * 100
            carbs_pct = (carbs_cal / calories) * 100
            fat_pct = (fat_cal / calories) * 100
            
            response += "⚖️ **Macro Balance:**\n"
            response += f"• Protein: {protein_pct:.0f}%\n"
            response += f"• Carbs: {carbs_pct:.0f}%\n"
            response += f"• Fat: {fat_pct:.0f}%\n\n"
        
        # Add health insights
        if 'health_benefits' in self.current_food:
            benefits = self.current_food['health_benefits'][:3]  # Show top 3
            if benefits:
                response += "💚 **Health Benefits:**\n"
                for benefit in benefits:
                    response += f"• {benefit.replace('_', ' ').title()}\n"
                response += "\n"
        
        self.current_step = 7
        self.save_state()
        return response + self.step_7_daily_progress_tracking("")
    
    def _parse_meal_type_input(self, user_input: str) -> Optional[str]:
        """Parse meal type selection"""
        if not user_input.strip():
            # Use suggested meal type
            return self.session_manager.get('suggested_meal_type', 'snack')
        
        user_input = user_input.strip()
        
        # Handle numeric choices
        meal_types = ['breakfast', 'lunch', 'dinner', 'snack']
        if user_input.isdigit():
            choice = int(user_input)
            if 1 <= choice <= 4:
                return meal_types[choice - 1]
        
        # Handle text choices
        user_input_lower = user_input.lower()
        for meal_type in meal_types:
            if meal_type in user_input_lower or user_input_lower in meal_type:
                return meal_type
        
        return None
    
    def step_7_daily_progress_tracking(self, user_input: str) -> str:
        """Step 7: Show updated daily progress"""
        self.current_step = 7
        
        # Get updated daily summary
        daily_summary = self.diary_manager.get_daily_summary()
        totals = daily_summary['nutrition_totals']
        
        response = "📈 **Updated Daily Progress**\n\n"
        
        # Current totals
        response += f"🔢 **Today's Totals:**\n"
        response += f"• **Calories:** {totals['calories']}\n"
        response += f"• **Protein:** {totals['macros']['protein']}g\n"
        response += f"• **Carbs:** {totals['macros']['carbs']}g\n"
        response += f"• **Fat:** {totals['macros']['fat']}g\n"
        response += f"• **Fiber:** {totals['macros']['fiber']}g\n\n"
        
        # Meal breakdown
        response += "🍽️ **By Meal Type:**\n"
        for meal_type, meal_data in totals['meal_breakdown'].items():
            if meal_data['count'] > 0:
                response += f"• {meal_type.capitalize()}: {meal_data['calories']} cal ({meal_data['count']} items)\n"
        response += "\n"
        
        # Progress towards goals
        progress = self.progress_tracker.calculate_progress(totals)
        
        response += "🎯 **Goal Progress:**\n"
        response += f"• **Calories:** {progress['calories']['percentage']:.0f}% "
        response += f"({progress['calories']['current']}/{progress['calories']['goal']})\n"
        
        response += f"• **Protein:** {progress['protein']['percentage']:.0f}% "
        response += f"({progress['protein']['current']:.0f}g/{progress['protein']['goal']:.0f}g)\n"
        
        response += f"• **Overall:** {progress['overall']['status']}\n\n"
        
        self.current_step = 8
        self.save_state()
        return response + self.step_8_insights_recommendations("")
    
    def step_8_insights_recommendations(self, user_input: str) -> str:
        """Step 8: Provide personalized insights and recommendations"""
        self.current_step = 8
        
        daily_summary = self.diary_manager.get_daily_summary()
        totals = daily_summary['nutrition_totals']
        analysis = daily_summary['nutrition_analysis']
        
        response = "💡 **Personalized Insights**\n\n"
        
        # Nutrition balance analysis
        response += f"⚖️ **Balance Score:** {analysis['balance_score']}/100\n"
        response += f"**Macro Distribution:** {analysis['macro_balance']}\n\n"
        
        # Key insights
        if analysis['insights']:
            response += "🔍 **Key Insights:**\n"
            for insight in analysis['insights'][:3]:
                response += f"• {insight}\n"
            response += "\n"
        
        # Actionable recommendations
        if analysis['recommendations']:
            response += "📝 **Recommendations:**\n"
            for rec in analysis['recommendations'][:3]:
                response += f"• {rec}\n"
            response += "\n"
        
        # Goal-based recommendations
        progress = self.progress_tracker.calculate_progress(totals)
        goal_recs = self.progress_tracker.get_goal_recommendations(progress)
        
        if goal_recs:
            response += "🎯 **Goal-Based Tips:**\n"
            for rec in goal_recs:
                response += f"• {rec}\n"
            response += "\n"
        
        self.current_step = 9
        self.save_state()
        return response + self.step_9_goal_achievement_monitoring("")
    
    def step_9_goal_achievement_monitoring(self, user_input: str) -> str:
        """Step 9: Monitor progress towards nutrition goals"""
        self.current_step = 9
        
        daily_summary = self.diary_manager.get_daily_summary()
        totals = daily_summary['nutrition_totals']
        progress = self.progress_tracker.calculate_progress(totals)
        
        response = "🏆 **Goal Achievement Status**\n\n"
        
        # Overall progress
        overall_pct = progress['overall']['percentage']
        response += f"**Overall Progress:** {overall_pct:.0f}%\n"
        response += f"**Status:** {progress['overall']['status']}\n\n"
        
        # Detailed goal breakdown
        response += "📊 **Detailed Progress:**\n\n"
        
        for goal_type in ['calories', 'protein', 'carbs', 'fat']:
            goal_progress = progress[goal_type]
            pct = goal_progress['percentage']
            
            # Progress bar visualization
            filled_bars = int(pct / 10)
            empty_bars = 10 - filled_bars
            progress_bar = "█" * filled_bars + "░" * empty_bars
            
            response += f"**{goal_type.capitalize()}:** {pct:.0f}%\n"
            response += f"[{progress_bar}] {goal_progress['current']:.0f}/{goal_progress['goal']:.0f}\n"
            
            if goal_progress['remaining'] > 0:
                response += f"Remaining: {goal_progress['remaining']:.0f}\n"
            response += "\n"
        
        # Achievement badges/milestones
        badges = []
        if progress['calories']['percentage'] >= 80:
            badges.append("🔥 Calorie Crusher")
        if progress['protein']['percentage'] >= 100:
            badges.append("💪 Protein Pro")
        if overall_pct >= 90:
            badges.append("🎯 Goal Getter")
        if daily_summary['total_entries'] >= 5:
            badges.append("📝 Logging Legend")
        
        if badges:
            response += "🏅 **Today's Achievements:**\n"
            for badge in badges:
                response += f"• {badge}\n"
            response += "\n"
        
        self.current_step = 10
        self.save_state()
        return response + self.step_10_cross_journey_integration("")
    
    def step_10_cross_journey_integration(self, user_input: str) -> str:
        """Step 10: Integrate with other journeys and suggest next actions"""
        self.current_step = 10
        
        daily_summary = self.diary_manager.get_daily_summary()
        totals = daily_summary['nutrition_totals']
        progress = self.progress_tracker.calculate_progress(totals)
        
        response = "🔄 **What's Next?**\n\n"
        
        # Suggest related journeys based on current status
        suggestions = []
        
        # Meal planning suggestions
        if progress['calories']['percentage'] < 70:
            suggestions.append({
                'journey': 'meal_planning',
                'reason': 'Plan balanced meals to reach your calorie goals',
                'action': 'Get meal suggestions that fit your remaining calorie budget'
            })
        
        # Recipe discovery suggestions
        protein_pct = progress['protein']['percentage']
        if protein_pct < 70:
            suggestions.append({
                'journey': 'recipe_discovery',
                'reason': 'Find high-protein recipes to boost your intake',
                'action': 'Search for protein-rich recipes'
            })
        
        # Grocery assistance suggestions
        if daily_summary['total_entries'] >= 3:
            suggestions.append({
                'journey': 'grocery_assistance', 
                'reason': 'Plan shopping for your preferred foods',
                'action': 'Create a grocery list based on your food history'
            })
        
        # Cooking guidance suggestions
        recent_entries = self.diary_manager.get_recent_entries(limit=5)
        manual_entries = [e for e in recent_entries if e.food_id.startswith('custom_')]
        if len(manual_entries) >= 2:
            suggestions.append({
                'journey': 'cooking_guidance',
                'reason': 'Learn to cook your favorite foods',
                'action': 'Get cooking instructions for homemade meals'
            })
        
        # Present suggestions
        if suggestions:
            response += "Based on your nutrition tracking, you might want to:\n\n"
            for i, suggestion in enumerate(suggestions[:3], 1):
                response += f"{i}. **{suggestion['journey'].replace('_', ' ').title()}**\n"
                response += f"   {suggestion['reason']}\n"
                response += f"   → {suggestion['action']}\n\n"
        
        # Quick actions for food tracking
        response += "📱 **Quick Food Actions:**\n"
        response += "• **'Log more food'** - Add another food item\n"
        response += "• **'View diary'** - See complete daily summary\n" 
        response += "• **'Set goals'** - Adjust your nutrition goals\n"
        response += "• **'Food trends'** - View your eating patterns\n\n"
        
        # Completion message
        response += "✅ **Food logging complete!** Your nutrition data is saved.\n\n"
        response += "What would you like to do next?"
        
        # Reset journey state
        self.current_step = 1
        self.current_food = None
        self.selected_serving = None
        self.tracking_mode = None
        self.entry_method = None
        self.save_state()
        
        return response
    
    def handle_user_input(self, user_input: str) -> str:
        """Handle user input based on current step"""
        if not user_input.strip():
            return self.get_step_prompt()
        
        # Handle special commands
        user_input_lower = user_input.lower().strip()
        
        if user_input_lower in ['quit', 'exit', 'stop']:
            return self.end_journey()
        
        if user_input_lower in ['help', '?']:
            return self.get_help_message()
        
        if user_input_lower == 'restart':
            return self.start_journey()
        
        # Handle step-specific input
        step_handlers = {
            1: self.step_1_tracking_mode_determination,
            2: self.step_2_food_entry_method_selection,
            3: self.step_3_food_search_identification,
            4: self.step_4_portion_size_selection,
            5: self.step_5_meal_timing_classification,
            6: self.step_6_nutritional_analysis,
            7: self.step_7_daily_progress_tracking,
            8: self.step_8_insights_recommendations,
            9: self.step_9_goal_achievement_monitoring,
            10: self.step_10_cross_journey_integration
        }
        
        handler = step_handlers.get(self.current_step)
        if handler:
            return handler(user_input)
        else:
            return "Something went wrong. Let's restart the food tracking."
    
    def get_step_prompt(self) -> str:
        """Get prompt for current step"""
        prompts = {
            1: "What type of food tracking would you like to do?",
            2: "How would you like to add your food?",
            3: "What food would you like to log?",
            4: "Which serving size matches what you ate?",
            5: "What type of meal is this?",
            6: "Review your food entry above.",
            7: "Check your updated daily progress above.",
            8: "Review your personalized insights above.",
            9: "See your goal achievement status above.",
            10: "What would you like to do next?"
        }
        
        return prompts.get(self.current_step, "What would you like to do?")
    
    def get_help_message(self) -> str:
        """Get help message for current step"""
        step_name = self.steps.get(self.current_step, "Unknown Step")
        
        help_msg = f"🆘 **Help - {step_name}**\n\n"
        
        if self.current_step == 1:
            help_msg += "Choose what you want to do:\n"
            help_msg += "• Type '1' to log new food\n"
            help_msg += "• Type '2' to view your food diary\n"
            help_msg += "• Type '3' to manage previous entries"
        
        elif self.current_step == 2:
            help_msg += "Choose how to add food:\n"
            help_msg += "• Type '1' to search the food database\n"
            help_msg += "• Type '2' for manual entry\n" 
            help_msg += "• Type '3' to select from recent foods"
        
        elif self.current_step == 3:
            help_msg += "Enter food information:\n"
            help_msg += "• For search: Type food name (e.g., 'chicken breast')\n"
            help_msg += "• For manual: Use format 'Name, calories, protein, carbs, fat'\n"
            help_msg += "• For recent: Choose a number from the list"
        
        elif self.current_step == 4:
            help_msg += "Select portion size:\n"
            help_msg += "• Type the number of your serving choice\n"
            help_msg += "• Or specify quantity: '1.5 x 2' for 1.5 times option 2"
        
        elif self.current_step == 5:
            help_msg += "Classify your meal:\n"
            help_msg += "• Type '1' for breakfast\n"
            help_msg += "• Type '2' for lunch\n"
            help_msg += "• Type '3' for dinner\n"
            help_msg += "• Type '4' for snack\n"
            help_msg += "• Press Enter to use the suggested meal type"
        
        else:
            help_msg += "Continue through the journey or type:\n"
            help_msg += "• 'restart' to start over\n"
            help_msg += "• 'quit' to exit"
        
        help_msg += "\n\nType 'restart' to start over or 'quit' to exit."
        return help_msg
    
    def get_journey_summary(self) -> Dict[str, Any]:
        """Get summary of the current journey state"""
        daily_summary = self.diary_manager.get_daily_summary()
        
        return {
            'journey_name': self.journey_name,
            'current_step': self.current_step,
            'step_name': self.steps.get(self.current_step, 'Unknown'),
            'tracking_mode': self.tracking_mode,
            'entry_method': self.entry_method,
            'current_food': self.current_food['name'] if self.current_food else None,
            'daily_calories': daily_summary['nutrition_totals']['calories'],
            'daily_entries': daily_summary['total_entries'],
            'progress_status': 'In Progress' if self.current_step < 10 else 'Complete'
        }
    
    def end_journey(self) -> str:
        """End the food calorie tracking journey"""
        daily_summary = self.diary_manager.get_daily_summary()
        
        response = "👋 **Food Tracking Complete!**\n\n"
        response += f"**Today's Summary:**\n"
        response += f"• Foods logged: {daily_summary['total_entries']}\n"
        response += f"• Total calories: {daily_summary['nutrition_totals']['calories']}\n"
        response += f"• Total protein: {daily_summary['nutrition_totals']['macros']['protein']}g\n\n"
        response += "Your nutrition data has been saved. Come back anytime to log more food!\n\n"
        response += "Type 'food tracking' to start again."
        
        # Reset journey state
        self.reset_journey()
        return response