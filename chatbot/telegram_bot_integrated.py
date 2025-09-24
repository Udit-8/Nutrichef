#!/usr/bin/env python3
"""
Integrated Telegram Bot for Nutrition Chatbot
Properly integrates with the existing journey system
"""

import os
import sys
import logging
from typing import Dict, Any
from datetime import datetime

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, MessageHandler, 
    filters, ContextTypes, CallbackQueryHandler
)

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Simple session manager for Telegram (avoid import issues)
class SimpleTelegramSession:
    def __init__(self, user_id: int):
        self.user_id = user_id
        self.current_journey = None
        self.current_step = 1
        self.session_data = {}
        self.conversation_context = []
        self.journey_instance = None  # Store journey instance
        self.logged_foods = []  # Store logged foods for the day
        self.daily_totals = {"calories": 0, "protein": 0, "carbs": 0, "fat": 0}
        self.nutrition_goals = {  # Store user's custom nutrition goals
            "calories": 1800,
            "protein": 120,
            "carbs": 225,
            "fat": 60
        }
    
    def set(self, key: str, value: Any):
        self.session_data[key] = value
    
    def get(self, key: str, default=None):
        return self.session_data.get(key, default)
    
    def start_journey(self, journey_name: str):
        self.current_journey = journey_name
        self.current_step = 1
        self.journey_instance = None  # Reset journey instance
    
    def log_food(self, food_name: str, calories: int, protein: int, carbs: int = 0, fat: int = 0):
        """Log a food item to the daily tracker"""
        food_entry = {
            "name": food_name,
            "calories": calories,
            "protein": protein,
            "carbs": carbs,
            "fat": fat,
            "time": datetime.now().strftime('%H:%M'),
            "timestamp": datetime.now()
        }
        self.logged_foods.append(food_entry)
        
        # Update daily totals
        self.daily_totals["calories"] += calories
        self.daily_totals["protein"] += protein
        self.daily_totals["carbs"] += carbs
        self.daily_totals["fat"] += fat
        
        return food_entry
    
    def get_daily_summary(self):
        """Get today's food diary summary"""
        return {
            "logged_foods": self.logged_foods,
            "totals": self.daily_totals,
            "goals": self.nutrition_goals,
            "food_count": len(self.logged_foods)
        }
    
    def update_nutrition_goals(self, **kwargs):
        """Update nutrition goals with new values"""
        for key, value in kwargs.items():
            if key in self.nutrition_goals:
                self.nutrition_goals[key] = int(value)
        return self.nutrition_goals
    
    def get_goal_percentages(self):
        """Get current progress percentages based on goals"""
        return {
            "calories": int((self.daily_totals["calories"] / self.nutrition_goals["calories"]) * 100) if self.nutrition_goals["calories"] > 0 else 0,
            "protein": int((self.daily_totals["protein"] / self.nutrition_goals["protein"]) * 100) if self.nutrition_goals["protein"] > 0 else 0,
            "carbs": int((self.daily_totals["carbs"] / self.nutrition_goals["carbs"]) * 100) if self.nutrition_goals["carbs"] > 0 else 0,
            "fat": int((self.daily_totals["fat"] / self.nutrition_goals["fat"]) * 100) if self.nutrition_goals["fat"] > 0 else 0
        }

# Simple journey implementations that provide interactive flows
class SimpleRecipeDiscovery:
    def __init__(self, session):
        self.session = session
        self.step = 1
        
    def start_journey(self, user_input=""):
        self.step = 1
        return self.handle_step_1()
    
    def handle_input(self, user_input: str):
        if self.step == 1:
            return self.handle_step_1(user_input)
        elif self.step == 2:
            return self.handle_step_2(user_input)
        elif self.step == 3:
            return self.handle_step_3(user_input)
        elif self.step == 4:
            return self.handle_step_4(user_input)
        else:
            return self.start_journey()
    
    def handle_step_1(self, user_input=""):
        if user_input.strip():  # If user provided input, advance to step 2
            # Interpret the user's cuisine choice
            cuisine_choices = {
                "1": "Italian",
                "2": "Asian", 
                "3": "Mexican",
                "4": "American",
                "5": "Mediterranean",
                "6": "Indian"
            }
            
            # Get the actual choice text
            if user_input.strip() in cuisine_choices:
                cuisine_text = cuisine_choices[user_input.strip()]
            else:
                cuisine_text = user_input.strip()  # Use custom input as-is
            
            self.session.set('cuisine_choice', cuisine_text)
            self.step = 2
            return f"""✅ **Great choice: {cuisine_text}**

🔍 **Recipe Discovery - Step 2/4**

How much time do you have for cooking?

**Time Options:**
1️⃣ **Quick & Easy** (15-30 minutes)
2️⃣ **Moderate** (30-60 minutes)
3️⃣ **Elaborate** (1+ hours)
4️⃣ **No time limit**

**Skill Level:**
🥄 **Beginner** - Simple recipes
👨‍🍳 **Intermediate** - Moderate complexity  
👩‍🍳 **Advanced** - Complex techniques

Reply with time preference and skill level!"""
        
        # Otherwise show step 1
        self.step = 1
        response = """🔍 **Recipe Discovery - Step 1/4**

What type of cuisine or dish are you looking for?

**Popular Options:**
1️⃣ **Italian** (Pasta, Pizza, Risotto)
2️⃣ **Asian** (Stir-fry, Curry, Noodles)  
3️⃣ **Mexican** (Tacos, Burritos, Enchiladas)
4️⃣ **American** (Burgers, BBQ, Comfort food)
5️⃣ **Mediterranean** (Greek, Turkish, Middle Eastern)
6️⃣ **Indian** (Curry, Biryani, Tandoori)

**Or specify:**
• A specific dish name
• Main ingredient (chicken, beef, vegetarian)
• Dietary preference (low-carb, gluten-free, vegan)

What sounds good to you? 🍽️"""
        return response
    
    def handle_step_2(self, user_input: str):
        if user_input.strip():  # If user provided input, advance to step 3
            # Interpret the user's time preference choice
            time_choices = {
                "1": "Quick & Easy (15-30 minutes)",
                "2": "Moderate (30-60 minutes)", 
                "3": "Elaborate (1+ hours)",
                "4": "No time limit"
            }
            
            # Get the actual choice text
            if user_input.strip() in time_choices:
                time_text = time_choices[user_input.strip()]
            else:
                time_text = user_input.strip()  # Use custom input as-is
            
            self.session.set('time_preference', time_text)
            self.step = 3
            return f"""⏰ **Time noted: {time_text}**

🔍 **Recipe Discovery - Step 3/4**

Any dietary restrictions or preferences?

**Common Restrictions:**
1️⃣ **Vegetarian** 🥕
2️⃣ **Vegan** 🌱
3️⃣ **Gluten-free** 🚫🌾
4️⃣ **Low-carb/Keto** 🥩
5️⃣ **Dairy-free** 🚫🥛
6️⃣ **High-protein** 💪
7️⃣ **Low-sodium** 🧂
8️⃣ **No restrictions** ✅

**Allergies to avoid:**
• Nuts, shellfish, eggs, etc.

What dietary needs should I consider? 🥗"""
        
        # This shouldn't happen in normal flow
        return "Please provide your time preference!"
    
    def handle_step_3(self, user_input: str):
        if user_input.strip():  # If user provided input, advance to step 4
            # Interpret the user's dietary restriction choice
            dietary_choices = {
                "1": "Vegetarian",
                "2": "Vegan",
                "3": "Gluten-free",
                "4": "Low-carb/Keto",
                "5": "Dairy-free",
                "6": "High-protein",
                "7": "Low-sodium",
                "8": "No restrictions"
            }
            
            # Get the actual choice text
            if user_input.strip() in dietary_choices:
                dietary_text = dietary_choices[user_input.strip()]
            else:
                dietary_text = user_input.strip()  # Use custom input as-is
            
            self.session.set('dietary_restrictions', dietary_text)
            self.step = 4
            
            cuisine = self.session.get('cuisine_choice', 'your preferred cuisine')
            time_pref = self.session.get('time_preference', 'your time preference')
            
            # Generate personalized recipes based on user choices
            recipes = self._generate_personalized_recipes(cuisine, time_pref, dietary_text)
            
            response = f"""🎉 **Perfect! Here are your personalized recipes:**

🔍 **Recipe Discovery - Step 4/4 (Results)**

**Your preferences:** {cuisine}, {time_pref}, {dietary_text}

**🍝 RECIPE RECOMMENDATIONS:**

{recipes}

**Next Steps:**
📋 Get full recipe with instructions
🛒 Create shopping list for ingredients
👩‍🍳 Start cooking with step-by-step guidance
📊 Log this meal in your food diary

Which recipe interests you most? 🍽️

Ready to start cooking? Type /start to begin a new journey! 🚀"""
            
            # Reset for next use
            self.step = 1
            self.session.current_journey = None
            return response
            
        # This shouldn't happen in normal flow  
        return "Please specify your dietary preferences!"
    
    def _generate_personalized_recipes(self, cuisine, time_pref, dietary):
        """Generate personalized recipe recommendations based on user preferences"""
        
        # Recipe database organized by cuisine and dietary restrictions
        recipe_data = {
            "Italian": {
                "default": [
                    ("Spaghetti Carbonara", "25 min", "380 cal", "Classic pasta with eggs, cheese, pancetta"),
                    ("Margherita Pizza", "30 min", "320 cal", "Fresh mozzarella, basil, tomato sauce"),
                    ("Chicken Parmigiana", "40 min", "450 cal", "Breaded chicken with marinara and cheese")
                ],
                "Vegetarian": [
                    ("Caprese Pasta", "20 min", "340 cal", "Fresh mozzarella, cherry tomatoes, basil"),
                    ("Eggplant Parmigiana", "45 min", "380 cal", "Layers of eggplant, cheese, marinara"),
                    ("Mushroom Risotto", "35 min", "320 cal", "Creamy arborio rice with porcini mushrooms")
                ],
                "Vegan": [
                    ("Pasta Arrabbiata", "15 min", "280 cal", "Spicy tomato sauce with garlic and chili"),
                    ("Minestrone Soup", "30 min", "180 cal", "Hearty vegetable soup with beans"),
                    ("Pasta Primavera", "25 min", "320 cal", "Seasonal vegetables with olive oil")
                ]
            },
            "Asian": {
                "default": [
                    ("Chicken Teriyaki", "20 min", "350 cal", "Glazed chicken with steamed rice"),
                    ("Beef Stir-Fry", "15 min", "380 cal", "Quick beef and vegetables in soy sauce"),
                    ("Salmon Teriyaki", "25 min", "420 cal", "Glazed salmon with Asian vegetables")
                ],
                "Vegetarian": [
                    ("Vegetable Pad Thai", "20 min", "340 cal", "Rice noodles with tofu and vegetables"),
                    ("Mushroom Fried Rice", "15 min", "280 cal", "Wok-fried rice with mixed mushrooms"),
                    ("Vegetable Spring Rolls", "30 min", "220 cal", "Fresh rolls with peanut dipping sauce")
                ],
                "Vegan": [
                    ("Tofu Stir-Fry", "15 min", "260 cal", "Crispy tofu with mixed vegetables"),
                    ("Vegetable Ramen", "25 min", "320 cal", "Rich broth with fresh vegetables and noodles"),
                    ("Asian Lettuce Wraps", "20 min", "180 cal", "Crisp lettuce with seasoned vegetables")
                ]
            },
            "Mexican": {
                "default": [
                    ("Chicken Fajitas", "25 min", "380 cal", "Sizzling chicken with peppers and onions"),
                    ("Beef Tacos", "20 min", "320 cal", "Seasoned ground beef in soft tortillas"),
                    ("Chicken Quesadillas", "15 min", "420 cal", "Grilled tortillas with chicken and cheese")
                ],
                "Vegetarian": [
                    ("Black Bean Quesadillas", "15 min", "360 cal", "Cheese and black beans in crispy tortillas"),
                    ("Vegetable Enchiladas", "35 min", "340 cal", "Rolled tortillas with mixed vegetables"),
                    ("Refried Bean Tostadas", "20 min", "280 cal", "Crispy tostadas with beans and toppings")
                ]
            }
        }
        
        # Get recipes for the chosen cuisine
        if cuisine in recipe_data:
            cuisine_recipes = recipe_data[cuisine]
            
            # Try to get dietary-specific recipes first
            if dietary in cuisine_recipes:
                recipes = cuisine_recipes[dietary]
            elif dietary in ["Gluten-free", "Low-carb/Keto", "Dairy-free", "High-protein", "Low-sodium"]:
                # For other dietary restrictions, use default recipes with notes
                recipes = cuisine_recipes.get("default", cuisine_recipes.get("Vegetarian", []))
            else:
                recipes = cuisine_recipes.get("default", [])
        else:
            # Fallback for unknown cuisines
            recipes = [
                ("Grilled Chicken Bowl", "25 min", "380 cal", "Healthy protein with mixed vegetables"),
                ("Quinoa Salad", "15 min", "320 cal", "Nutritious grain bowl with fresh herbs"),
                ("Vegetable Stir-Fry", "20 min", "260 cal", "Quick and healthy mixed vegetables")
            ]
        
        # Format the recipes with personalization
        formatted_recipes = []
        for i, (name, time, calories, desc) in enumerate(recipes[:3], 1):
            # Add dietary compliance note
            dietary_note = ""
            if dietary == "Vegetarian" and "vegetarian" not in name.lower():
                dietary_note = f" • {dietary} friendly"
            elif dietary == "Vegan" and "vegan" not in name.lower():
                dietary_note = f" • {dietary} option available"
            elif dietary in ["Gluten-free", "Low-carb/Keto", "Dairy-free"]:
                dietary_note = f" • Can be made {dietary.lower()}"
            
            recipe_text = f"""**{i}. {name}** ⭐⭐⭐⭐{'⭐' if i == 1 else ''}
• **Time**: {time} | **Calories**: {calories}
• {desc}{dietary_note}
• **Perfect for**: {cuisine} lovers, {time_pref.lower()}"""
            formatted_recipes.append(recipe_text)
        
        return "\n\n".join(formatted_recipes)
    
    def handle_step_4(self, user_input: str):
        # This step is now integrated into step 3, but keeping for compatibility
        self.step = 1
        self.session.current_journey = None
        return "Recipe discovery completed! Type /start to begin a new journey! 🚀"

class SimpleFoodTracking:
    def __init__(self, session):
        self.session = session
        self.step = 1
        
    def start_journey(self, user_input=""):
        self.step = 1
        return self.handle_step_1()
    
    def handle_input(self, user_input: str):
        if self.step == 1:
            return self.handle_step_1(user_input)
        elif self.step == 2:
            return self.handle_step_2(user_input)
        elif self.step == 3:
            return self.handle_step_3(user_input)
        elif self.step == 4:
            return self.handle_step_4(user_input)
        else:
            return self.start_journey()
    
    def handle_step_1(self, user_input=""):
        if user_input.strip():  # If user provided input, move to step 2
            # Interpret the user's choice
            action_choices = {
                "1": "Log New Food",
                "2": "View Food Diary", 
                "3": "Set Goals",
                "4": "Check Progress"
            }
            
            # Get the actual choice text
            if user_input.strip() in action_choices:
                action_text = action_choices[user_input.strip()]
            else:
                action_text = user_input.strip()  # Use custom input as-is
            
            self.session.set('tracking_action', action_text)
            self.session.set('user_choice', user_input.strip())
            self.step = 2
            return self.handle_step_2("")  # Call with empty input to show step 2 content
        
        # Otherwise show step 1
        self.step = 1
        response = """📊 **Food Calorie Tracking - Step 1/4**

What would you like to do?

**Options:**
1️⃣ **Log New Food** - Add what you just ate
2️⃣ **View Food Diary** - See today's summary
3️⃣ **Set Goals** - Define nutrition targets
4️⃣ **Check Progress** - Review your stats

Choose an option (1-4) or tell me what you ate! 🍎"""
        return response
    
    def handle_step_2(self, user_input: str):
        if user_input.strip():  # If user provided input, process it and advance to step 3
            # Store the step 2 choice
            self.session.set('step2_choice', user_input.strip())
            
            # Get the action the user chose in step 1
            user_choice = self.session.get('user_choice', '1')
            action = self.session.get('tracking_action', 'Log New Food')
            
            # Process the step 2 choice and generate step 3 content
            step3_response = self._process_step2_choice(user_choice, user_input.strip())
            
            self.step = 3
            return step3_response
        
        # Get the action the user chose in step 1 (for initial step 2 display)
        user_choice = self.session.get('user_choice', '1')
        action = self.session.get('tracking_action', 'Log New Food')
        
        # Provide different step 2 based on their step 1 choice
        if user_choice in ['1']:  # Log New Food
            response = f"""✅ **Action: {action}**

📝 **Food Logging - Step 2/4**

How would you like to add your food?

**Methods:**
1️⃣ **Search Database** - Find food by name
   *"chicken breast", "apple", "greek yogurt"*

2️⃣ **Quick Entry** - Common foods
   *Breakfast, lunch, dinner basics*

3️⃣ **Manual Entry** - Custom foods
   *Restaurant meals, homemade dishes*

**Examples:**
• "I ate grilled chicken with rice"
• "Log breakfast: oatmeal and banana"  
• "Add snack: trail mix"

What did you eat? 🍽️"""
        
        elif user_choice in ['2']:  # View Food Diary
            # Get actual logged foods from session
            daily_summary = self.session.get_daily_summary()
            logged_foods = daily_summary["logged_foods"]
            totals = daily_summary["totals"]
            
            # Format logged foods
            if logged_foods:
                foods_text = ""
                for i, food in enumerate(logged_foods, 1):
                    foods_text += f"• **{food['time']}**: {food['name']} ({food['calories']} cal)\n"
            else:
                foods_text = "• No foods logged today yet\n"
            
            # Get user's custom goals and calculate percentages
            goals = daily_summary["goals"]
            percentages = self.session.get_goal_percentages()
            
            response = f"""✅ **Action: {action}**

📊 **Food Diary - Step 2/4**

**Today's Logged Foods:**
{foods_text}
**Daily Totals:**
• **Calories**: {totals["calories"]} / {goals["calories"]} goal ({percentages["calories"]}%)
• **Protein**: {totals["protein"]}g / {goals["protein"]}g goal ({percentages["protein"]}%)
• **Carbs**: {totals["carbs"]}g / {goals["carbs"]}g goal ({percentages["carbs"]}%)
• **Fat**: {totals["fat"]}g / {goals["fat"]}g goal ({percentages["fat"]}%)

**What would you like to do next?**
1️⃣ **Log more food**
2️⃣ **View detailed breakdown**
3️⃣ **Set new goals**
4️⃣ **Export diary**

Choose your next action! 📝"""
        
        elif user_choice in ['3']:  # Set Goals
            current_goals = self.session.nutrition_goals
            response = f"""✅ **Action: {action}**

🎯 **Goal Setting - Step 2/4**

**Current Goals:**
• **Daily Calories**: {current_goals['calories']} cal
• **Protein**: {current_goals['protein']}g
• **Carbs**: {current_goals['carbs']}g
• **Fat**: {current_goals['fat']}g

**What would you like to adjust?**
1️⃣ **Daily calorie target**
2️⃣ **Protein goals**
3️⃣ **Carb/fat balance**
4️⃣ **Weight loss/gain goals**

Which goal would you like to modify? ⚖️"""
        
        else:  # Check Progress (4) or custom input
            response = f"""✅ **Action: {action}**

📈 **Progress Check - Step 2/4**

**This Week's Summary:**
• **Average Calories**: 1,650 /day
• **Days on Track**: 5/7 days
• **Weight**: -1.2 lbs this week
• **Streak**: 12 days logging

**Achievements:**
🏆 **Protein Master** - Hit protein goals 6/7 days
⭐ **Consistent Logger** - 12 day streak
🥗 **Veggie Champion** - 5+ servings daily

**What would you like to review?**
1️⃣ **Weekly trends**
2️⃣ **Nutrient breakdown**
3️⃣ **Goal progress**
4️⃣ **Achievement history**

What interests you most? 📊"""
        
        return response
    
    def _process_step2_choice(self, user_choice, step2_input):
        """Process the user's step 2 choice and return appropriate step 3 content"""
        
        # Special handling for food diary sub-menu choices
        if user_choice == '2' and step2_input in ['1', '2', '3', '4']:
            return self._handle_food_diary_followup(step2_input)
        
        if user_choice == '1':  # Log New Food path
            method_choices = {
                "1": "Search Database",
                "2": "Quick Entry",
                "3": "Manual Entry"
            }
            
            method = method_choices.get(step2_input, step2_input)
            self.session.set('food_method', method)
            
            if step2_input == "1":  # Search Database
                return f"""🔍 **Method: {method}**

📝 **Food Logging - Step 3/4**

**Enter the food you want to search for:**

**Popular searches:**
• Chicken breast
• Greek yogurt  
• Apple
• Salmon
• Rice
• Eggs

**Or be specific:**
• "Grilled chicken breast"
• "Honeycrisp apple"
• "Brown rice cooked"

What food would you like to search for? 🔍"""
            
            elif step2_input == "2":  # Quick Entry
                return f"""⚡ **Method: {method}**

📝 **Food Logging - Step 3/4**

**Quick food options:**

**Breakfast:**
1️⃣ Oatmeal with banana (320 cal)
2️⃣ Greek yogurt with berries (180 cal)
3️⃣ Scrambled eggs (2 eggs, 140 cal)

**Lunch/Dinner:**
4️⃣ Grilled chicken salad (350 cal)
5️⃣ Turkey sandwich (420 cal)
6️⃣ Pasta with marinara (380 cal)

**Snacks:**
7️⃣ Apple with peanut butter (190 cal)
8️⃣ Mixed nuts (160 cal)
9️⃣ String cheese (80 cal)

Choose a number or describe your food! 🍽️"""
            
            elif step2_input == "3":  # Manual Entry
                return f"""✏️ **Method: {method}**

📝 **Food Logging - Step 3/4**

**Manual food entry:**

Please provide the following details:

**Format:** "[Food name] - [Amount] - [Calories]"

**Examples:**
• "Homemade pizza slice - 1 slice - 320 calories"
• "Restaurant pasta - 1 bowl - 450 calories" 
• "Protein smoothie - 16 oz - 280 calories"

**Or just describe it:**
• "Large coffee with milk and sugar"
• "Handful of trail mix"
• "Leftover dinner from yesterday"

What did you eat? ✏️"""
        
        elif user_choice == '2':  # View Food Diary path
            # Get actual data from session
            daily_summary = self.session.get_daily_summary()
            totals = daily_summary["totals"]
            logged_foods = daily_summary["logged_foods"]
            goals = daily_summary["goals"]
            percentages = self.session.get_goal_percentages()
            
            # Calculate breakdown percentages
            total_cals = totals["calories"] if totals["calories"] > 0 else 1  # Avoid division by zero
            carb_percent = int((totals["carbs"] * 4 / total_cals) * 100) if total_cals > 0 else 0
            fat_percent = int((totals["fat"] * 9 / total_cals) * 100) if total_cals > 0 else 0
            
            # Recent foods list
            recent_foods = ""
            if logged_foods:
                for food in logged_foods[-3:]:  # Show last 3 foods
                    recent_foods += f"• {food['time']}: {food['name']} - {food['calories']} cal, {food['protein']}g protein\n"
            else:
                recent_foods = "• No foods logged yet today\n"
            
            return f"""📊 **Diary Action Selected**

**Food Diary - Step 3/4**

**Recent Logged Foods:**
{recent_foods}
**Detailed Nutrient Breakdown:**
• **Carbohydrates**: {totals["carbs"]}g ({carb_percent}% of calories)
  - Target: 45-65% of calories
• **Protein**: {totals["protein"]}g ({percentages["protein"]}% of goal)
  - Daily goal: {goals["protein"]}g
• **Fats**: {totals["fat"]}g ({fat_percent}% of calories)
  - Target: 20-35% of calories

**Daily Progress:**
• **Total Calories**: {totals["calories"]} / {goals["calories"]} goal
• **Foods Logged**: {len(logged_foods)} items today
• **Avg Calories/Item**: {int(totals["calories"]/len(logged_foods)) if logged_foods else 0}

**Any specific questions about your nutrition data?**
Type your question or "done" to finish! 📈"""
        
        elif user_choice == '3':  # Set Goals path
            current_goals = self.session.nutrition_goals
            return f"""🎯 **Goal Setting - Step 3/4**

**Current Daily Calorie Goal: {current_goals['calories']}**

**Recommended ranges based on your profile:**
• **Weight Loss**: 1400-1600 cal/day
• **Maintenance**: 1800-2000 cal/day  
• **Muscle Gain**: 2200-2400 cal/day

**Activity Level Adjustment:**
• **Sedentary**: -200 calories
• **Lightly Active**: Current setting
• **Very Active**: +300 calories
• **Athlete**: +500 calories

What's your new daily calorie target? 🎯"""
        
        else:  # Check Progress path (4)
            return f"""📈 **Progress Review - Step 3/4**

**Weekly Nutrient Trends:**

**This Week vs Last Week:**
📈 **Calories**: 1,650 avg (+50 cal/day)
📊 **Protein**: 98g avg (+15g/day) ✅
📉 **Carbs**: 180g avg (-20g/day)
📈 **Fat**: 65g avg (+8g/day)

**Consistency Metrics:**
• **Days Logged**: 7/7 days ✅
• **Goals Met**: 5/7 days (71%)
• **Meal Timing**: Regular ✅
• **Hydration**: 6 cups/day ⚠️

**Achievement Progress:**
🏆 **Protein Master**: 6/7 days (86%)
⭐ **Consistency King**: 12 day streak
🥗 **Veggie Lover**: Need 2 more servings/day

What would you like to improve this week? 🎯"""
    
    def handle_step_3(self, user_input: str):
        user_choice = self.session.get('user_choice', '1')
        action = self.session.get('tracking_action', 'Log New Food')
        
        # Special handling for food diary follow-up actions
        if user_choice == '2' and user_input.strip() in ['1', '2', '3', '4']:
            return self._handle_food_diary_followup(user_input.strip())
        
        if user_input.strip():  # If user provided input, move to step 4
            self.step = 4
            return self.handle_step_4(user_input)
        
        # This should not happen since step 3 content is now generated in _process_step2_choice
        return "Please provide your input to continue..."
    
    def _handle_food_diary_followup(self, choice: str):
        """Handle food diary sub-menu choices: 1=Log more food, 2=View breakdown, 3=Set goals, 4=Export"""
        
        if choice == '1':  # Log more food
            # Reset to food logging mode
            self.session.set('user_choice', '1')  # Switch to Log New Food mode
            self.session.set('tracking_action', 'Log New Food')
            self.step = 2
            
            # Show food logging method selection
            return f"""🍽️ **Starting New Food Log**

📝 **Food Logging - Step 2/4**

**How would you like to log your food?**

1️⃣ **Search Database** - Find food in our database
2️⃣ **Quick Entry** - Choose from popular foods
3️⃣ **Manual Entry** - Enter custom food details

**Or just describe what you ate:**
• "Grilled chicken with rice"
• "Apple with peanut butter"
• "Homemade pasta salad"

What method works best for you? 📱"""
            
        elif choice == '2':  # View detailed breakdown
            daily_summary = self.session.get_daily_summary()
            totals = daily_summary["totals"]
            goals = daily_summary["goals"]
            percentages = self.session.get_goal_percentages()
            logged_foods = daily_summary["logged_foods"]
            
            # Calculate detailed breakdowns
            total_cals = totals["calories"] if totals["calories"] > 0 else 1
            carb_cals = totals["carbs"] * 4
            protein_cals = totals["protein"] * 4  
            fat_cals = totals["fat"] * 9
            
            carb_percent = int((carb_cals / total_cals) * 100) if total_cals > 0 else 0
            protein_percent = int((protein_cals / total_cals) * 100) if total_cals > 0 else 0
            fat_percent = int((fat_cals / total_cals) * 100) if total_cals > 0 else 0
            
            self.step = 1  # Reset for next action
            self.session.current_journey = None
            
            return f"""📊 **Detailed Nutrition Breakdown**

**Macronutrient Distribution:**
🍞 **Carbohydrates**: {totals['carbs']}g ({carb_percent}% of calories)
   Target: 45-65% | Status: {"✅ Good" if 45 <= carb_percent <= 65 else "⚠️ Adjust"}

💪 **Protein**: {totals['protein']}g ({protein_percent}% of calories)
   Goal: {goals['protein']}g | Progress: {percentages['protein']}%
   Status: {"✅ Excellent" if percentages['protein'] >= 80 else "📈 Increase" if percentages['protein'] < 70 else "👍 Good"}

🥑 **Fat**: {totals['fat']}g ({fat_percent}% of calories)
   Target: 20-35% | Status: {"✅ Good" if 20 <= fat_percent <= 35 else "⚠️ Adjust"}

**Calorie Analysis:**
🔥 **Total Calories**: {totals['calories']} / {goals['calories']} goal
📊 **Goal Progress**: {percentages['calories']}%
🍽️ **Foods Logged**: {len(logged_foods)} items

**Nutritional Quality Score:** {"A+" if percentages['calories'] >= 90 and percentages['protein'] >= 80 else "A" if percentages['calories'] >= 75 else "B+" if percentages['calories'] >= 60 else "B"}

**Recommendations:**
{"🎯 You're hitting your targets perfectly!" if percentages['calories'] >= 80 and percentages['protein'] >= 80 else "📈 Focus on reaching your calorie goal" if percentages['calories'] < 70 else "💪 Add more protein-rich foods" if percentages['protein'] < 70 else "🌟 Great progress, keep it up!"}

Ready for your next nutrition goal! 💪"""
            
        elif choice == '3':  # Set new goals
            # Switch to goal setting mode
            self.session.set('user_choice', '3')
            self.session.set('tracking_action', 'Set Goals')
            self.step = 2
            
            current_goals = self.session.nutrition_goals
            return f"""🎯 **Goal Setting Mode**

📊 **Current Nutrition Goals:**
• **Calories**: {current_goals['calories']} cal/day
• **Protein**: {current_goals['protein']}g/day  
• **Carbs**: {current_goals['carbs']}g/day
• **Fat**: {current_goals['fat']}g/day

**Quick Goal Updates:**
• "Set calories to 2000"
• "Change protein to 150g" 
• "I want 1800 calories and 120g protein"

**Popular Targets:**
🔥 **Weight Loss**: 1200-1500 calories
⚖️ **Maintenance**: 1800-2000 calories  
💪 **Muscle Gain**: 2200-2500 calories
🏃‍♀️ **Athletic**: 2500-3000 calories

What goals would you like to set? 🎯"""
            
        elif choice == '4':  # Export diary
            daily_summary = self.session.get_daily_summary()
            logged_foods = daily_summary["logged_foods"]
            totals = daily_summary["totals"]
            goals = daily_summary["goals"]
            
            # Generate export text
            foods_export = "\n".join([
                f"{food['time']}: {food['name']} - {food['calories']} cal, {food['protein']}g protein"
                for food in logged_foods
            ]) if logged_foods else "No foods logged today"
            
            self.step = 1  # Reset for next action
            self.session.current_journey = None
            
            return f"""📤 **Food Diary Export**

**Daily Summary - {datetime.now().strftime('%B %d, %Y')}**

**Foods Consumed:**
{foods_export}

**Daily Totals:**
• Calories: {totals['calories']}/{goals['calories']} ({int((totals['calories']/goals['calories'])*100) if goals['calories'] > 0 else 0}%)
• Protein: {totals['protein']}g/{goals['protein']}g ({int((totals['protein']/goals['protein'])*100) if goals['protein'] > 0 else 0}%)
• Carbs: {totals['carbs']}g/{goals['carbs']}g
• Fat: {totals['fat']}g/{goals['fat']}g

**Export Options:**
📋 Copy this summary to your notes
📊 Screenshot for your records
📱 Share with your nutritionist
💾 Save for meal planning

**Streak:** {len(logged_foods)} foods logged today!
Keep up the great tracking! 📈"""
        
        else:
            return "Please choose a valid option (1-4) or describe what you'd like to do! 🤔"
    
    def handle_step_4(self, user_input: str):
        user_choice = self.session.get('user_choice', '1')
        action = self.session.get('tracking_action', 'Log New Food')
        
        # Generate final response based on the original choice
        if user_choice == '1':  # Log New Food
            food_info = self._generate_food_info(user_input)
            goals = self.session.nutrition_goals
            response = f"""✅ **Food Logged Successfully!**

**Added to your diary:**
• **Food**: {food_info['name']}
• **Portion**: {food_info['portion']}
• **Calories**: {food_info['calories']}
• **Protein**: {food_info['protein']}
• **Time**: {datetime.now().strftime('%H:%M')}

**Updated Daily Totals:**
• **Calories**: {food_info['total_calories']} / {goals['calories']} ({food_info['calorie_percent']}%)
• **Protein**: {food_info['total_protein']}g / {goals['protein']}g ({food_info['protein_percent']}%)

**Insights:**
{food_info['insights']}

**What's Next?**
🍽️ Log more food
📊 View full diary  
📋 Plan next meal
🥗 Get meal suggestions

Anything else you'd like to track? 📝"""

        elif user_choice == '2':  # View Food Diary
            response = f"""📊 **Food Diary Action Complete!**

**Summary of diary review:**
• Reviewed detailed nutrient breakdown
• Identified improvement areas
• Current progress: 54% of daily calories

**Key Takeaways:**
✅ **Strengths**: Good protein intake, balanced meals
⚠️ **Areas to improve**: Need more calcium-rich foods
🎯 **Next goal**: Add 965 calories for dinner

**Recommended actions:**
📝 Log dinner when ready
🥛 Add dairy or calcium-rich foods
🥗 Include more leafy greens

Your food diary is looking great! Keep it up! 💪"""

        elif user_choice == '3':  # Set Goals
            if user_input.strip() and user_input.strip() not in ['1', '2', '3', '4']:
                # Parse the goal setting input
                input_text = user_input.strip().lower()
                
                # Extract calorie goal if mentioned
                new_calories = None
                new_protein = None
                
                # Look for calorie numbers
                import re
                calorie_match = re.search(r'(\d+)\s*cal', input_text)
                if calorie_match:
                    new_calories = int(calorie_match.group(1))
                elif re.search(r'\b(\d{4})\b', input_text):  # 4-digit number likely calories
                    new_calories = int(re.search(r'\b(\d{4})\b', input_text).group(1))
                elif re.search(r'\b(\d{3,4})\b', input_text):  # 3-4 digit number
                    possible_cal = int(re.search(r'\b(\d{3,4})\b', input_text).group(1))
                    if possible_cal >= 800:  # reasonable calorie range
                        new_calories = possible_cal
                
                # Look for protein numbers
                protein_match = re.search(r'(\d+)\s*(?:g|gram|protein)', input_text)
                if protein_match:
                    new_protein = int(protein_match.group(1))
                
                # Update goals if values found
                updates = {}
                if new_calories:
                    updates['calories'] = new_calories
                    # Calculate proportional macros
                    updates['protein'] = int((new_calories * 0.25) / 4)  # 25% of calories from protein
                    updates['carbs'] = int((new_calories * 0.45) / 4)    # 45% from carbs
                    updates['fat'] = int((new_calories * 0.30) / 9)      # 30% from fat
                
                if new_protein and not new_calories:
                    updates['protein'] = new_protein
                
                if updates:
                    self.session.update_nutrition_goals(**updates)
                    updated_goals = self.session.nutrition_goals
                    
                    response = f"""🎯 **Goals Updated Successfully!**

**Your new nutrition goals:**
• **Daily Calories**: {updated_goals['calories']} cal/day
• **Protein**: {updated_goals['protein']}g/day
• **Carbs**: {updated_goals['carbs']}g/day  
• **Fat**: {updated_goals['fat']}g/day

**Goal activated:** Starting now
**Progress tracking:** Enabled
**Notifications:** You'll get reminders

**What this means:**
📈 Adjusted targets for your goals
⚖️ Balanced macronutrient ratios
🎯 Personalized to your needs

Ready to crush your new goals! 💪🎯"""
                else:
                    response = f"""🎯 **Set Your Nutrition Goals**

**Example goal inputs:**
• "Set my calories to 2000"
• "I want 1500 calories and 100g protein"
• "Change my calorie goal to 1800"
• "Set protein goal to 120g"

**Current goals:**
• Calories: {self.session.nutrition_goals['calories']} cal/day
• Protein: {self.session.nutrition_goals['protein']}g/day
• Carbs: {self.session.nutrition_goals['carbs']}g/day
• Fat: {self.session.nutrition_goals['fat']}g/day

What would you like to change? 🎯"""
            else:
                # Show goal setting options
                current_goals = self.session.nutrition_goals
                response = f"""🎯 **Set Your Nutrition Goals**

**Current Goals:**
• **Calories**: {current_goals['calories']} cal/day
• **Protein**: {current_goals['protein']}g/day
• **Carbs**: {current_goals['carbs']}g/day
• **Fat**: {current_goals['fat']}g/day

**To update your goals, tell me:**
• "Set my calories to 2000"
• "I want 1500 calories and 100g protein"
• "Change my calorie goal to 1800"
• "Set protein goal to 120g"

**Popular targets:**
🔥 **Weight Loss**: 1200-1500 calories
⚖️ **Maintenance**: 1800-2000 calories
💪 **Muscle Gain**: 2200-2500 calories

What would you like to set? 🎯"""

        else:  # Check Progress (4)
            daily_summary = self.session.get_daily_summary()
            totals = daily_summary["totals"]
            goals = daily_summary["goals"]
            percentages = self.session.get_goal_percentages()
            food_count = daily_summary["food_count"]
            
            # Calculate weekly average (simplified - using today's data as example)
            avg_goal_achievement = (percentages['calories'] + percentages['protein']) // 2
            consistency_days = min(food_count, 7)  # Max 7 days for display
            
            # Generate grade based on goal achievement
            if avg_goal_achievement >= 90:
                grade = "A+ (95%)"
                grade_emoji = "🏆"
            elif avg_goal_achievement >= 80:
                grade = "A- (85%)"
                grade_emoji = "🌟"
            elif avg_goal_achievement >= 70:
                grade = "B+ (75%)"
                grade_emoji = "👍"
            else:
                grade = "B (65%)"
                grade_emoji = "📈"
                
            # Key achievements based on actual data
            achievements = []
            if food_count > 0:
                achievements.append(f"✅ {food_count}-entry logging streak maintained")
            if percentages['protein'] >= 80:
                achievements.append("💪 Excellent protein intake")
            if percentages['calories'] <= 100 and percentages['calories'] >= 80:
                achievements.append("🎯 Perfect calorie balance")
            if not achievements:
                achievements.append("🌱 Started your nutrition journey")
                
            # Areas for improvement
            improvements = []
            if percentages['calories'] < 70:
                improvements.append("🍽️ Increase food intake to meet goals")
            elif percentages['calories'] > 110:
                improvements.append("⚖️ Monitor portion sizes")
            if percentages['protein'] < 80:
                improvements.append("🥩 Add more protein-rich foods")
            if food_count < 3:
                improvements.append("📝 Log meals more consistently")
            if not improvements:
                improvements.append("💧 Stay hydrated throughout the day")
                improvements.append("🥬 Add variety with more vegetables")
            
            response = f"""📈 **Progress Review Complete!**

**Current Performance:**
{grade_emoji} **Overall Grade**: {grade}
📊 **Consistency**: {food_count} entries logged
🎯 **Goal Achievement**: {avg_goal_achievement}%

**Today's Progress:**
🔥 Calories: {totals['calories']}/{goals['calories']} ({percentages['calories']}%)
💪 Protein: {totals['protein']}g/{goals['protein']}g ({percentages['protein']}%)

**Key Achievements:**
{chr(10).join(achievements)}

**Areas for growth:**
{chr(10).join(improvements)}

**Keep it up:**
• Stay consistent with logging
• Maintain balanced nutrition
• Celebrate your progress!

You're doing great! Keep going! 🌟"""
        
        # Reset for next use
        self.step = 1
        self.session.current_journey = None
        return response
    
    def _generate_food_info(self, user_input):
        """Generate realistic food info based on user input and log it to session"""
        
        # Enhanced food database with complete nutritional info
        food_database = {
            "1": {"name": "Oatmeal with banana", "portion": "1 bowl", "calories": 320, "protein": 8, "carbs": 65, "fat": 4},
            "2": {"name": "Greek yogurt with berries", "portion": "1 cup", "calories": 180, "protein": 15, "carbs": 20, "fat": 5},
            "3": {"name": "Scrambled eggs", "portion": "2 eggs", "calories": 140, "protein": 12, "carbs": 2, "fat": 10},
            "4": {"name": "Grilled chicken salad", "portion": "1 large bowl", "calories": 350, "protein": 28, "carbs": 15, "fat": 18},
            "5": {"name": "Turkey sandwich", "portion": "1 sandwich", "calories": 420, "protein": 24, "carbs": 45, "fat": 12},
            "6": {"name": "Pasta with marinara", "portion": "1.5 cups", "calories": 380, "protein": 14, "carbs": 72, "fat": 6},
            "7": {"name": "Apple with peanut butter", "portion": "1 apple + 2 tbsp", "calories": 190, "protein": 8, "carbs": 20, "fat": 16},
            "8": {"name": "Mixed nuts", "portion": "1 oz", "calories": 160, "protein": 6, "carbs": 6, "fat": 14},
            "9": {"name": "String cheese", "portion": "1 stick", "calories": 80, "protein": 6, "carbs": 1, "fat": 6},
        }
        
        # Additional foods for search/custom input
        custom_foods = {
            "chicken": {"name": "Grilled Chicken Breast", "portion": "4 oz", "calories": 185, "protein": 35, "carbs": 0, "fat": 4},
            "salmon": {"name": "Grilled Salmon", "portion": "4 oz", "calories": 206, "protein": 22, "carbs": 0, "fat": 12},
            "rice": {"name": "Brown Rice", "portion": "1 cup", "calories": 216, "protein": 5, "carbs": 45, "fat": 2},
            "broccoli": {"name": "Steamed Broccoli", "portion": "1 cup", "calories": 55, "protein": 4, "carbs": 11, "fat": 1},
            "apple": {"name": "Medium Apple", "portion": "1 apple", "calories": 95, "protein": 0, "carbs": 25, "fat": 0},
        }
        
        # Select food based on input
        if user_input.strip() in food_database:
            food = food_database[user_input.strip()]
        else:
            # Try to match custom foods
            input_lower = user_input.lower().strip()
            matched_food = None
            for key, food_data in custom_foods.items():
                if key in input_lower:
                    matched_food = food_data
                    break
            
            if matched_food:
                food = matched_food
            else:
                # Generate reasonable defaults based on input
                food_name = user_input.strip().title() if len(user_input.strip()) > 2 else "Healthy Food Choice"
                food = {
                    "name": food_name,
                    "portion": "1 serving", 
                    "calories": 200,  # reasonable default
                    "protein": 12,
                    "carbs": 25,
                    "fat": 8
                }
        
        # Log the food to the session
        logged_food = self.session.log_food(
            food["name"], 
            food["calories"], 
            food["protein"],
            food["carbs"],
            food["fat"]
        )
        
        # Get current totals from session
        daily_summary = self.session.get_daily_summary()
        total_calories = daily_summary["totals"]["calories"]
        total_protein = daily_summary["totals"]["protein"]
        goals = daily_summary["goals"]
        
        calorie_percent = int((total_calories / goals["calories"]) * 100) if goals["calories"] > 0 else 0
        protein_percent = int((total_protein / goals["protein"]) * 100) if goals["protein"] > 0 else 0
        
        # Generate insights based on the food
        insights = []
        if food["protein"] > 15:
            insights.append("💪 Great protein choice!")
        if food["calories"] < 200:
            insights.append("🌿 Light and healthy option!")
        if calorie_percent > 50:
            insights.append(f"📈 {calorie_percent}% toward calorie goal")
        else:
            insights.append("🎯 Good portion for your goals")
            
        if protein_percent > 50:
            insights.append("🥩 Excellent protein progress!")
        
        return {
            "name": food["name"],
            "portion": food["portion"],
            "calories": food["calories"],
            "protein": f"{food['protein']}g",
            "total_calories": total_calories,
            "total_protein": total_protein,
            "calorie_percent": calorie_percent,
            "protein_percent": protein_percent,
            "insights": "\n".join(insights) if insights else "🎯 On track for balanced nutrition"
        }

class SimpleMealPlanning:
    def __init__(self, session):
        self.session = session
        self.step = 1
    
    def start_journey(self, user_input=""):
        self.step = 1
        return self.handle_step_1()
    
    def handle_input(self, user_input: str):
        if self.step == 1:
            return self.handle_step_1(user_input)
        elif self.step == 2:
            return self.handle_step_2(user_input)
        elif self.step == 3:
            return self.handle_step_3(user_input)
        elif self.step == 4:
            return self.handle_step_4(user_input)
        else:
            return self.start_journey()
    
    def handle_step_1(self, user_input=""):
        if user_input.strip():  # If user provided input, move to step 2
            # Store the duration choice
            duration_choices = {
                "1": "3 Days",
                "2": "1 Week", 
                "3": "2 Weeks",
                "4": "Custom Duration"
            }
            
            # Get the actual choice text
            if user_input.strip() in duration_choices:
                duration_text = duration_choices[user_input.strip()]
            else:
                duration_text = user_input.strip()  # Use custom input as-is
                
            self.session.set('meal_duration', duration_text)
            self.session.set('user_choice', user_input.strip())
            self.step = 2
            return self.handle_step_2("")  # Call with empty input to show step 2 content
        
        # Otherwise show step 1
        self.step = 1
        response = """📋 **Meal Planning - Step 1/4**

Let's create your personalized meal plan!

**Planning Duration:**
1️⃣ **3 Days** - Weekend or short-term
2️⃣ **1 Week** - Weekly planning  
3️⃣ **2 Weeks** - Extended planning
4️⃣ **Custom** - Specify your own timeframe

**Which duration works best for you?** 🎯

Choose a number (1-4) or tell me your preferred timeframe!"""
        return response
    
    def handle_step_2(self, user_input: str):
        if user_input.strip():  # If user provided input, move to step 3
            # Store the goal choice
            goal_choices = {
                "1": "Weight Loss",
                "2": "Muscle Gain",
                "3": "Maintenance", 
                "4": "Athletic Performance"
            }
            
            # Get the actual choice text
            if user_input.strip() in goal_choices:
                goal_text = goal_choices[user_input.strip()]
            else:
                goal_text = user_input.strip()  # Use custom input as-is
                
            self.session.set('meal_goal', goal_text)
            self.session.set('goal_choice', user_input.strip())
            self.step = 3
            return self.handle_step_3("")  # Call with empty input to show step 3 content
        
        # Otherwise show step 2
        self.step = 2
        duration = self.session.get('meal_duration', '1 Week')
        
        response = f"""✅ **Duration: {duration}**

🎯 **Meal Planning - Step 2/4**

What's your primary goal for this meal plan?

**Planning Goals:**
1️⃣ **Weight Loss** - Lower calorie, high protein (1200-1500 cal/day)
2️⃣ **Muscle Gain** - Higher protein, more calories (2000-2500 cal/day)  
3️⃣ **Maintenance** - Balanced nutrition (1600-2000 cal/day)
4️⃣ **Athletic Performance** - High energy meals (2200-2800 cal/day)

**Each goal includes:**
• Customized calorie targets
• Optimized macronutrient ratios
• Meal timing recommendations
• Performance-focused foods

Which goal matches your needs? 🎯"""
        return response
    
    def handle_step_3(self, user_input: str):
        if user_input.strip():  # If user provided input, move to step 4
            # Store the dietary preference choice
            diet_choices = {
                "1": "Omnivore",
                "2": "Vegetarian",
                "3": "Vegan",
                "4": "Pescatarian",
                "5": "Keto",
                "6": "Paleo"
            }
            
            # Get the actual choice text
            if user_input.strip() in diet_choices:
                diet_text = diet_choices[user_input.strip()]
            else:
                diet_text = user_input.strip()  # Use custom input as-is
                
            self.session.set('meal_diet', diet_text)
            self.session.set('diet_choice', user_input.strip())
            self.step = 4
            return self.handle_step_4("")  # Call with empty input to show step 4 content
        
        # Otherwise show step 3
        self.step = 3
        duration = self.session.get('meal_duration', '1 Week')
        goal = self.session.get('meal_goal', 'Maintenance')
        
        response = f"""✅ **Duration: {duration} | Goal: {goal}**

🍽️ **Meal Planning - Step 3/4**

What are your dietary preferences?

**Dietary Styles:**
1️⃣ **Omnivore** - All foods including meat and dairy
2️⃣ **Vegetarian** - No meat, includes dairy and eggs
3️⃣ **Vegan** - Plant-based only, no animal products
4️⃣ **Pescatarian** - Fish and seafood, no other meat
5️⃣ **Keto** - Low-carb, high-fat for ketosis
6️⃣ **Paleo** - Whole foods, no processed items

**Special Considerations:**
• Food allergies (gluten, nuts, dairy)
• Cultural preferences
• Budget constraints
• Cooking skill level

Which dietary style fits your lifestyle? 🥗"""
        return response

    
    def handle_step_4(self, user_input: str):
        # Generate the final meal plan based on all choices
        duration = self.session.get('meal_duration', '1 Week')
        goal = self.session.get('meal_goal', 'Maintenance')
        diet = self.session.get('meal_diet', 'Omnivore')
        
        # Set calories based on goal
        goal_calories = {
            "Weight Loss": "1200-1500",
            "Muscle Gain": "2000-2500", 
            "Maintenance": "1600-2000",
            "Athletic Performance": "2200-2800"
        }
        
        cal_range = goal_calories.get(goal, "1600-2000")
        
        # Generate personalized meals based on diet preference and duration
        meals = self._generate_meals_by_diet(diet, goal, duration)
        
        response = f"""🎆 **Your Personalized Meal Plan Complete!**

**Plan Details:**
• **Duration**: {duration}
• **Goal**: {goal} ({cal_range} cal/day)
• **Diet Style**: {diet}
• **Created**: {datetime.now().strftime('%B %d, %Y')}

{meals}

**What would you like to do next?**
1️⃣ **Generate Grocery List** - Get shopping list for this plan
2️⃣ **Get Cooking Instructions** - Step-by-step meal prep
3️⃣ **Adjust Portions** - Modify serving sizes
4️⃣ **Save & Track** - Start following this plan

**Meal Prep Tips:**
🕒 Prep on Sundays for the week
🧊 Batch cook grains and proteins
🥬 Wash and chop vegetables in advance

Ready to transform your nutrition? 💪"""
        
        # Reset for next use
        self.step = 1
        self.session.current_journey = None
        return response
    
    def _generate_meals_by_diet(self, diet, goal, duration):
        """Generate meal plans based on dietary preference, goal, and duration"""
        
        # Determine number of days based on duration (check longer durations first)
        if "2 Weeks" in duration or duration == "2 Weeks":
            num_days = 14
        elif "1 Week" in duration or duration == "1 Week" or "Week" in duration:
            num_days = 7
        elif "3 Days" in duration or duration == "3 Days":
            num_days = 3
        else:
            # Parse custom duration or default to 7 days
            try:
                # Try to extract number from custom input like "5 days" or "10 days"
                import re
                numbers = re.findall(r'\d+', duration)
                if numbers:
                    num_days = min(int(numbers[0]), 14)  # Cap at 14 days for reasonable output
                else:
                    num_days = 7  # Default to 1 week
            except:
                num_days = 7
        
        # Define meal databases for each diet type
        meal_databases = {
            "Vegan": {
                "breakfasts": [
                    "Oatmeal with almond butter & banana (380 cal)",
                    "Chia pudding with berries (320 cal)",
                    "Smoothie with spinach & protein powder (350 cal)",
                    "Avocado toast with tomato (340 cal)",
                    "Quinoa breakfast bowl with fruit (360 cal)",
                    "Coconut yogurt parfait (330 cal)",
                    "Tofu scramble with vegetables (320 cal)"
                ],
                "lunches": [
                    "Quinoa Buddha bowl with tahini (520 cal)",
                    "Black bean tacos with avocado (450 cal)",
                    "Mediterranean chickpea salad (480 cal)",
                    "Lentil and vegetable soup (420 cal)",
                    "Hummus and veggie wrap (440 cal)",
                    "Tempeh stir-fry with brown rice (460 cal)",
                    "Roasted vegetable and quinoa salad (480 cal)"
                ],
                "dinners": [
                    "Lentil curry with brown rice (480 cal)",
                    "Vegetable stir-fry with tofu (420 cal)",
                    "Stuffed bell peppers with quinoa (440 cal)",
                    "Mushroom and barley risotto (460 cal)",
                    "Thai coconut curry with vegetables (450 cal)",
                    "Eggplant and chickpea tagine (470 cal)",
                    "Black bean and sweet potato chili (440 cal)"
                ],
                "snacks": [
                    "Hummus with veggie sticks (150 cal)",
                    "Mixed nuts and fruit (180 cal)",
                    "Dark chocolate & almonds (160 cal)",
                    "Apple with almond butter (170 cal)",
                    "Trail mix with dried fruit (160 cal)",
                    "Coconut energy balls (140 cal)",
                    "Roasted chickpeas (130 cal)"
                ]
            },
            "Keto": {
                "breakfasts": [
                    "Avocado & eggs with bacon (420 cal)",
                    "Keto smoothie with MCT oil (350 cal)",
                    "Keto pancakes with sugar-free syrup (320 cal)",
                    "Cream cheese and spinach omelet (380 cal)",
                    "Bulletproof coffee with eggs (360 cal)",
                    "Keto breakfast casserole (400 cal)",
                    "Coconut flour muffins with butter (340 cal)"
                ],
                "lunches": [
                    "Chicken Caesar salad (no croutons) (380 cal)",
                    "Zucchini noodles with pesto (320 cal)",
                    "Tuna salad lettuce wraps (340 cal)",
                    "Cobb salad with full-fat dressing (420 cal)",
                    "Cauliflower mac and cheese (360 cal)",
                    "Bunless burger with side salad (440 cal)",
                    "Chicken and broccoli alfredo (400 cal)"
                ],
                "dinners": [
                    "Salmon with asparagus in butter (520 cal)",
                    "Steak with cauliflower mash (580 cal)",
                    "Pork chops with green beans (540 cal)",
                    "Baked chicken thighs with brussels sprouts (560 cal)",
                    "Lamb chops with roasted vegetables (580 cal)",
                    "Cod with creamy spinach (480 cal)",
                    "Beef short ribs with turnip mash (620 cal)"
                ],
                "snacks": [
                    "Cheese and macadamia nuts (200 cal)",
                    "Pork rinds with guacamole (180 cal)",
                    "Fat bombs (chocolate coconut) (160 cal)",
                    "Hard-boiled eggs with salt (140 cal)",
                    "Pepperoni and cheese roll-ups (180 cal)",
                    "Olives and aged cheese (160 cal)",
                    "Avocado with sea salt (150 cal)"
                ]
            },
            "Vegetarian": {
                "breakfasts": [
                    "Greek yogurt parfait with granola (350 cal)",
                    "Vegetable omelet with cheese (380 cal)",
                    "Smoothie bowl with protein powder (340 cal)",
                    "Pancakes with maple syrup (420 cal)",
                    "Breakfast quinoa with berries (360 cal)",
                    "Cottage cheese with fruit (320 cal)",
                    "French toast with strawberries (400 cal)"
                ],
                "lunches": [
                    "Caprese sandwich with basil (420 cal)",
                    "Quinoa and black bean bowl (450 cal)",
                    "Grilled cheese with tomato soup (440 cal)",
                    "Mediterranean wrap with feta (460 cal)",
                    "Spinach and ricotta quesadilla (480 cal)",
                    "Chickpea salad sandwich (420 cal)",
                    "Vegetarian Buddha bowl (470 cal)"
                ],
                "dinners": [
                    "Eggplant parmesan with side salad (520 cal)",
                    "Pasta primavera with parmesan (480 cal)",
                    "Stuffed portobello mushrooms (420 cal)",
                    "Vegetarian lasagna (540 cal)",
                    "Mushroom and spinach risotto (460 cal)",
                    "Bean and cheese enchiladas (500 cal)",
                    "Caprese stuffed zucchini boats (440 cal)"
                ],
                "snacks": [
                    "Apple with peanut butter (190 cal)",
                    "Trail mix with dried fruit (170 cal)",
                    "Greek yogurt with honey (160 cal)",
                    "String cheese with crackers (180 cal)",
                    "Mixed nuts and seeds (160 cal)",
                    "Hummus with pita chips (170 cal)",
                    "Cottage cheese with berries (140 cal)"
                ]
            }
        }
        
        # Default to balanced omnivore meals if diet not in database
        if diet not in meal_databases:
            meal_databases[diet] = {
                "breakfasts": [
                    "Overnight oats with berries (320 cal)",
                    "Avocado toast with egg (380 cal)",
                    "Protein smoothie with banana (350 cal)",
                    "Greek yogurt with granola (340 cal)",
                    "Scrambled eggs with whole grain toast (360 cal)",
                    "Oatmeal with nuts and honey (330 cal)",
                    "Breakfast burrito with beans (400 cal)"
                ],
                "lunches": [
                    "Grilled chicken quinoa bowl (480 cal)",
                    "Turkey and hummus wrap (420 cal)",
                    "Mediterranean chicken salad (460 cal)",
                    "Salmon and avocado salad (500 cal)",
                    "Chicken and vegetable stir-fry (440 cal)",
                    "Tuna and white bean salad (420 cal)",
                    "Lean beef and quinoa bowl (480 cal)"
                ],
                "dinners": [
                    "Salmon with roasted vegetables (520 cal)",
                    "Lean beef stir-fry with brown rice (540 cal)",
                    "Pork tenderloin with sweet potato (500 cal)",
                    "Grilled chicken with quinoa pilaf (480 cal)",
                    "Baked cod with roasted vegetables (460 cal)",
                    "Turkey meatballs with zucchini noodles (440 cal)",
                    "Lean pork chops with brussels sprouts (520 cal)"
                ],
                "snacks": [
                    "Greek yogurt with nuts (180 cal)",
                    "Apple with almond butter (190 cal)",
                    "Mixed berries with cottage cheese (150 cal)",
                    "Hard-boiled egg with crackers (160 cal)",
                    "Protein bar and banana (200 cal)",
                    "Hummus with veggie sticks (140 cal)",
                    "Trail mix (170 cal)"
                ]
            }
        
        # Generate the meal plan
        meals = meal_databases.get(diet, meal_databases["Vegetarian"])  # Fallback to vegetarian
        
        plan_text = f"📅 **{duration} {diet} Meal Plan:**\n\n"
        
        for day in range(1, num_days + 1):
            plan_text += f"**DAY {day}:**\n"
            plan_text += f"🌅 **Breakfast**: {meals['breakfasts'][(day-1) % len(meals['breakfasts'])]}\n"
            plan_text += f"🌞 **Lunch**: {meals['lunches'][(day-1) % len(meals['lunches'])]}\n"
            plan_text += f"🌙 **Dinner**: {meals['dinners'][(day-1) % len(meals['dinners'])]}\n"
            plan_text += f"🍎 **Snack**: {meals['snacks'][(day-1) % len(meals['snacks'])]}\n"
            
            # Add spacing between days, but not after the last day
            if day < num_days:
                plan_text += "\n"
        
        return plan_text

class SimpleGroceryAssistance:
    def __init__(self, session):
        self.session = session
        self.step = 1
    
    def start_journey(self, user_input=""):
        self.step = 1
        return self.handle_step_1()
    
    def handle_input(self, user_input: str):
        if self.step == 1:
            return self.handle_step_1(user_input)
        elif self.step == 2:
            return self.handle_step_2(user_input)
        elif self.step == 3:
            return self.handle_step_3(user_input)
        elif self.step == 4:
            return self.handle_step_4(user_input)
        else:
            return self.start_journey()
    
    def handle_step_1(self, user_input=""):
        if user_input.strip():  # If user provided input, move to step 2
            # Store the grocery type choice
            grocery_type_choices = {
                "1": "Weekly Meal Plan",
                "2": "Specific Recipes", 
                "3": "Healthy Staples",
                "4": "Quick Meals",
                "5": "Dietary Goal"
            }
            
            # Get the actual choice text
            if user_input.strip() in grocery_type_choices:
                grocery_type = grocery_type_choices[user_input.strip()]
            else:
                grocery_type = user_input.strip()  # Use custom input as-is
                
            self.session.set('grocery_type', grocery_type)
            self.session.set('grocery_choice', user_input.strip())
            self.step = 2
            return self.handle_step_2("")  # Call with empty input to show step 2 content
        
        # Otherwise show step 1
        self.step = 1
        response = """🛒 **Grocery Shopping Assistant - Step 1/4**

I'll help you create a smart shopping list!

**What do you need groceries for?**

1️⃣ **Weekly Meal Plan** - Complete week of meals
2️⃣ **Specific Recipes** - Ingredients for chosen dishes
3️⃣ **Healthy Staples** - Basic nutritious foods
4️⃣ **Quick Meals** - Easy breakfast/lunch/dinner options
5️⃣ **Dietary Goal** - Weight loss, muscle gain, etc.

**Special Considerations:**
🏠 **Family Size** - How many people?
💰 **Budget** - Any spending limits?
🕐 **Meal Prep** - Batch cooking ingredients?

What type of grocery list do you need? 🛍️"""
        return response
    
    def handle_step_2(self, user_input: str):
        if user_input.strip():  # If user provided input, move to step 3
            # Store the dietary preference choice
            diet_choices = {
                "1": "Omnivore",
                "2": "Vegetarian",
                "3": "Vegan",
                "4": "Pescatarian",
                "5": "Keto",
                "6": "Paleo"
            }
            
            # Get the actual choice text
            if user_input.strip() in diet_choices:
                diet_pref = diet_choices[user_input.strip()]
            else:
                diet_pref = user_input.strip()  # Use custom input as-is
                
            self.session.set('grocery_diet', diet_pref)
            self.session.set('diet_choice', user_input.strip())
            self.step = 3
            return self.handle_step_3("")  # Call with empty input to show step 3 content
        
        # Otherwise show step 2
        self.step = 2
        grocery_type = self.session.get('grocery_type', 'Weekly Meal Plan')
        
        response = f"""✅ **Type: {grocery_type}**

🛒 **Step 2/4 - Dietary Preferences**

**What's your dietary style?**

1️⃣ **Omnivore** - All foods including meat and dairy
2️⃣ **Vegetarian** - No meat, includes dairy and eggs  
3️⃣ **Vegan** - Plant-based only, no animal products
4️⃣ **Pescatarian** - Fish and seafood, no other meat
5️⃣ **Keto** - Low-carb, high-fat for ketosis
6️⃣ **Paleo** - Whole foods, no processed items

**Special Considerations:**
🚫 **Food Allergies** - Gluten, nuts, dairy, shellfish
💰 **Budget Level** - Economical, moderate, premium
🏠 **Family Size** - Single, couple, family of 4+
🕐 **Cooking Time** - Quick meals vs elaborate cooking

Which dietary style fits your needs? 🥗"""
        return response
    
    def handle_step_3(self, user_input: str):
        if user_input.strip():  # If user provided input, move to step 4
            # Store the shopping preferences choice
            preference_choices = {
                "1": "Budget-Friendly",
                "2": "Organic/Premium",
                "3": "Quick & Convenient",
                "4": "Meal Prep Focus"
            }
            
            # Get the actual choice text
            if user_input.strip() in preference_choices:
                preferences = preference_choices[user_input.strip()]
            else:
                preferences = user_input.strip()  # Use custom input as-is
                
            self.session.set('grocery_preferences', preferences)
            self.session.set('preferences_choice', user_input.strip())
            self.step = 4
            return self.handle_step_4("")  # Call with empty input to show step 4 content
        
        # Otherwise show step 3
        self.step = 3
        grocery_type = self.session.get('grocery_type', 'Weekly Meal Plan')
        grocery_diet = self.session.get('grocery_diet', 'Omnivore')
        
        response = f"""✅ **Type: {grocery_type} | Diet: {grocery_diet}**

🛒 **Step 3/4 - Shopping Preferences**

**What's most important for your shopping?**

1️⃣ **Budget-Friendly** - Cost-effective options and deals
2️⃣ **Organic/Premium** - High-quality, organic ingredients
3️⃣ **Quick & Convenient** - Pre-cut, ready-to-cook items
4️⃣ **Meal Prep Focus** - Bulk ingredients for batch cooking

**Additional Considerations:**
🏠 **Family Size** - Single person, couple, or family
💰 **Budget Range** - $30-50, $50-80, $80+
⏰ **Time Available** - Quick trips vs detailed shopping
🛒 **Store Type** - Supermarket, health store, bulk warehouse

**Allergy Considerations:**
• Gluten-free products needed?
• Dairy alternatives required?
• Nut-free household?
• Other specific restrictions?

Which shopping style matches your needs? 🛍️"""
        return response
    
    def handle_step_4(self, user_input: str):
        # Generate the final grocery list based on all choices
        grocery_type = self.session.get('grocery_type', 'Weekly Meal Plan')
        grocery_diet = self.session.get('grocery_diet', 'Omnivore')
        preferences = self.session.get('grocery_preferences', 'Budget-Friendly')
        
        # Generate personalized grocery list based on all selections
        grocery_list = self._generate_grocery_list_by_preferences(grocery_type, grocery_diet, preferences)
        
        response = f"""🎆 **Your Personalized Grocery List Complete!**

**List Details:**
• **Purpose**: {grocery_type}
• **Diet Style**: {grocery_diet}
• **Shopping Style**: {preferences}
• **Created**: {datetime.now().strftime('%B %d, %Y')}

{grocery_list}

**What would you like to do next?**
1️⃣ **Save to Phone** - Export list to your device
2️⃣ **Get Store Map** - Optimize shopping route
3️⃣ **Set Reminders** - Don't forget items
4️⃣ **Start Shopping** - Head to the store now

**Smart Shopping Tips:**
🕐 Shop early morning for best selection
🥬 Check produce quality before buying
💰 Compare unit prices for best deals

Ready to make your shopping efficient! 🛒"""
        
        # Reset for next use
        self.step = 1
        self.session.current_journey = None
        return response
    
    def _generate_grocery_list_by_preferences(self, grocery_type, diet, preferences):
        """Generate grocery lists based on type, diet, and preferences"""
        
        # Base lists for different diet types
        diet_lists = {
            "Vegan": {
                "produce": ["Spinach (5 oz)", "Kale (1 bunch)", "Bell peppers (3)", "Broccoli (2 heads)", "Avocados (4)", "Bananas (1 bunch)", "Berries (2 pints)", "Lemons (3)"],
                "proteins": ["Tofu (2 blocks)", "Tempeh (2 packages)", "Lentils (2 cans)", "Chickpeas (2 cans)", "Black beans (2 cans)", "Nutritional yeast (1 container)", "Plant protein powder (1 tub)"],
                "grains": ["Quinoa (2 lbs)", "Brown rice (2 lbs)", "Oats (18 oz)", "Whole grain pasta (2 boxes)", "Ezekiel bread (1 loaf)"],
                "alternatives": ["Almond milk (32 oz)", "Coconut milk (2 cans)", "Cashew cheese (8 oz)", "Vegan butter (1 container)", "Tahini (1 jar)"]
            },
            "Vegetarian": {
                "produce": ["Mixed greens (5 oz)", "Tomatoes (6)", "Bell peppers (3)", "Mushrooms (16 oz)", "Avocados (3)", "Bananas (1 bunch)", "Apples (6)", "Onions (3 lbs)"],
                "proteins": ["Greek yogurt (32 oz)", "Cottage cheese (16 oz)", "Eggs (2 dozen)", "Tofu (1 block)", "Black beans (2 cans)", "Mozzarella cheese (16 oz)"],
                "grains": ["Brown rice (2 lbs)", "Quinoa (1 lb)", "Whole grain bread (1 loaf)", "Pasta (2 boxes)", "Oats (18 oz)"],
                "dairy": ["Milk (32 oz)", "Greek yogurt (32 oz)", "Butter (1 lb)", "Parmesan cheese (8 oz)"]
            },
            "Keto": {
                "produce": ["Spinach (5 oz)", "Broccoli (2 heads)", "Cauliflower (1 head)", "Avocados (6)", "Zucchini (3)", "Bell peppers (3)", "Mushrooms (16 oz)"],
                "proteins": ["Ground beef (2 lbs)", "Chicken thighs (3 lbs)", "Salmon fillets (2 lbs)", "Eggs (2 dozen)", "Bacon (2 lbs)", "Cheddar cheese (16 oz)"],
                "fats": ["Olive oil (16 oz)", "Coconut oil (16 oz)", "Butter (2 lbs)", "Avocado oil (16 oz)", "MCT oil (8 oz)", "Nuts (mixed, 2 lbs)"],
                "pantry": ["Almond flour (5 lbs)", "Coconut flour (2 lbs)", "Sugar-free sweetener (1 container)", "Bone broth (32 oz)"]
            }
        }
        
        # Default to balanced omnivore list
        if diet not in diet_lists:
            diet_lists[diet] = {
                "produce": ["Mixed vegetables (variety)", "Fresh fruits (seasonal)", "Leafy greens (multiple types)", "Root vegetables (potatoes, carrots)"],
                "proteins": ["Lean meats (chicken, fish)", "Dairy products (milk, yogurt)", "Eggs (1 dozen)", "Plant proteins (beans, nuts)"],
                "grains": ["Whole grains (rice, quinoa)", "Bread (whole grain)", "Pasta (whole wheat)", "Oats (steel cut)"],
                "pantry": ["Healthy oils (olive, avocado)", "Spices and herbs", "Condiments (basic)", "Snacks (nuts, seeds)"]
            }
        
        # Modify based on shopping preferences
        selected_list = diet_lists.get(diet, diet_lists["Vegetarian"])
        
        # Generate formatted list
        list_text = f"📅 **{grocery_type} - {diet} Shopping List:**\n\n"
        
        if preferences == "Budget-Friendly":
            list_text += "💰 **Budget-Optimized List** (Focus on value and versatility)\n\n"
            cost_range = "$45-65"
        elif preferences == "Organic/Premium":
            list_text += "🌿 **Premium/Organic List** (High-quality ingredients)\n\n"
            cost_range = "$85-120"
        elif preferences == "Quick & Convenient":
            list_text += "⚡ **Quick & Convenient List** (Pre-prepped when possible)\n\n"
            cost_range = "$60-85"
        else:  # Meal Prep Focus
            list_text += "🍽️ **Meal Prep Focused List** (Bulk ingredients for batch cooking)\n\n"
            cost_range = "$70-95"
        
        # Add sections
        for section, items in selected_list.items():
            section_emoji = {"produce": "🥬", "proteins": "🥩", "grains": "🌾", "dairy": "🥛", "alternatives": "🌱", "fats": "🥑", "pantry": "📦"}
            emoji = section_emoji.get(section, "📋")
            list_text += f"**{emoji} {section.upper()} SECTION**\n"
            for item in items[:6]:  # Limit to 6 items per section for readability
                list_text += f"• {item}\n"
            list_text += "\n"
        
        # Add shopping summary
        list_text += f"**📊 SHOPPING SUMMARY:**\n"
        list_text += f"💰 **Estimated Cost**: {cost_range}\n"
        list_text += f"🛒 **Items**: ~{sum(len(items[:6]) for items in selected_list.values())} total\n"
        list_text += f"⏰ **Shopping Time**: 30-45 minutes\n"
        list_text += f"🥗 **Nutrition Focus**: {diet} optimized\n\n"
        
        list_text += "**📱 SMART FEATURES:**\n"
        list_text += "✅ Organized by store sections\n"
        list_text += "✅ Diet-specific selections\n"
        list_text += "✅ Preference-based optimization\n"
        list_text += "✅ Cost estimation included"
        
        return list_text

class SimpleCookingGuidance:
    def __init__(self, session):
        self.session = session
        self.step = 1
        self.recipe_data = None
        self.cooking_instructions = None
        self.current_cooking_step = 1
        self.active_timers = []
        self.session_status = "not_started"
        self._load_recipe_databases()
    
    def _load_recipe_databases(self):
        """Load recipe and cooking instruction databases"""
        import json
        import os
        
        try:
            # Load recipes database
            recipes_path = "/Users/uditrai88/Desktop/nutrition-chatbot/raw_data/recipes_raw.json"
            with open(recipes_path, 'r') as f:
                self.recipes_db = json.load(f)
            
            # Load cooking instructions database  
            instructions_path = "/Users/uditrai88/Desktop/nutrition-chatbot/raw_data/cooking_instructions_raw.json"
            with open(instructions_path, 'r') as f:
                self.cooking_db = json.load(f)
                
        except Exception as e:
            # Fallback to empty databases if files not found
            self.recipes_db = {"recipes": []}
            self.cooking_db = {"cooking_instructions": []}
    
    def start_journey(self, user_input="", recipe_name=None):
        """Start cooking guidance with a specific recipe"""
        self.step = 1
        
        # Store recipe name from parameter or user input
        if recipe_name:
            self.session.set('requested_recipe', recipe_name)
        elif user_input:
            self.session.set('requested_recipe', user_input)
            
        return self.handle_step_1()
    
    def handle_input(self, user_input: str):
        try:
            # Handle special restart command
            if 'restart cooking' in user_input.lower():
                return self._restart_current_recipe()
            
            if self.step == 1:
                return self.handle_step_1(user_input)
            elif self.step == 2:
                return self.handle_step_2(user_input)
            elif self.step == 3:
                return self.handle_step_3(user_input)
            elif self.step == 4:
                return self.handle_step_4(user_input)
            elif self.step == 5:
                return self.handle_step_5(user_input)
            elif self.step == 6:
                return self.handle_step_6(user_input)
            else:
                return self.start_journey()
        except Exception as e:
            # Log detailed error information
            import traceback
            error_details = traceback.format_exc()
            
            # Store error for debugging
            if hasattr(self.session, 'set'):
                self.session.set('last_cooking_error', str(e))
                self.session.set('last_error_traceback', error_details)
            
            # Return user-friendly error with recovery options
            return f"""❌ **Cooking Assistant Error**

Something went wrong while processing your request.

**What happened:** {str(e)}

**Debug info:**
• Current step: {getattr(self, 'step', 'unknown')}
• Recipe loaded: {self.recipe_data is not None if hasattr(self, 'recipe_data') else 'unknown'}
• Instructions loaded: {self.cooking_instructions is not None if hasattr(self, 'cooking_instructions') else 'unknown'}

**Recovery options:**
• Type **"restart cooking"** to start over with the same recipe
• Use **/reset** to start completely fresh
• Try rephrasing your command

I apologize for the inconvenience! 🙏"""
    
    def _restart_current_recipe(self):
        """Restart cooking with the current recipe"""
        try:
            if self.recipe_data:
                recipe_name = self.recipe_data['name']
                # Reset all state
                self.step = 1
                self.current_cooking_step = 1
                self.session_status = "not_started"
                self.active_timers = []
                # Restart with the same recipe
                return self.start_journey('', recipe_name)
            else:
                return """🔄 **Restart Cooking**
                
I don't have a current recipe to restart. Please tell me which recipe you'd like to cook!

🎯 **CALL TO ACTION**: Type a recipe name to start cooking!"""
        except Exception as e:
            return f"❌ **Restart Failed**: {str(e)}\n\nPlease use /reset to start completely fresh."
    
    def _show_available_recipes(self):
        """Show all available recipes that can be cooked"""
        try:
            if not hasattr(self, 'recipes_db') or not self.recipes_db:
                return """❌ **Recipe database not available**
                
Please try again or use /reset to start fresh.

🎯 **CALL TO ACTION**: Type a specific recipe name to start cooking!"""
            
            recipes = self.recipes_db.get('recipes', [])
            if not recipes:
                return """❌ **No recipes available**
                
The recipe database appears to be empty.

🎯 **CALL TO ACTION**: Try typing a specific recipe name!"""
            
            response = "📚 Available Recipes for Cooking\n\n"
            response += "Here are all the recipes I can guide you through step-by-step:\n\n"
            
            for i, recipe in enumerate(recipes, 1):
                # Use simple formatting without problematic Markdown
                recipe_name = recipe.get('name', f'Recipe {i}')
                cuisine = recipe.get('cuisine', 'Various').title()
                difficulty = recipe.get('difficulty', 'Unknown').title()
                total_time = recipe.get('total_time', 'Unknown')
                calories = recipe.get('calories_per_serving', 'N/A')
                
                response += f"{i}. {recipe_name}\n"
                response += f"🌍 {cuisine} • ⭐ {difficulty} • ⏱️ {total_time} min\n"
                response += f"💡 {calories} cal/serving\n\n"
            
            response += "Choose Your Recipe:\n"
            response += "• Type the recipe name (e.g., Mediterranean Chicken Bowl)\n"
            response += "• Type the number (e.g., 1, 3)\n"
            response += "• All recipes include full step-by-step cooking guidance!\n\n"
            response += "🎯 CALL TO ACTION: Type a recipe name or number to start cooking!"
            
            return response
            
        except Exception as e:
            return f"""❌ **Error showing recipes**: {str(e)}

🎯 **CALL TO ACTION**: Try typing a specific recipe name to start cooking!"""
    
    def handle_step_1(self, user_input=""):
        """STEP 1: RECIPE VALIDATION - Load recipe data and verify it exists"""
        
        # Get requested recipe name
        recipe_name = self.session.get('requested_recipe', user_input.strip())
        
        if not recipe_name:
            # No recipe specified - need to get recipe name
            return """👩‍🍳 **Interactive Cooking Guide**

I'll guide you through cooking a specific recipe step-by-step!

**To get started, I need to know which recipe you'd like to cook.**

You can:
• Tell me a specific recipe name (e.g., "Mediterranean Chicken Bowl")
• Say "show available recipes" to see options
• Come from Recipe Discovery with a selected recipe

**What recipe would you like to cook today?** 🍽️

🎯 **CALL TO ACTION**: Type a recipe name or say **"show available recipes"**!"""
        
        # Check for special commands before searching for recipes
        recipe_name_lower = recipe_name.lower()
        if 'show available recipes' in recipe_name_lower or 'show recipes' in recipe_name_lower or 'available recipes' in recipe_name_lower or 'browse recipes' in recipe_name_lower:
            return self._show_available_recipes()
        elif 'find recipes' in recipe_name_lower or 'discover recipes' in recipe_name_lower:
            return """🔍 **Recipe Discovery**

For more recipe discovery options, please say one of:
• "Find me healthy recipes"
• "Show me quick recipes" 
• "Recipe discovery"

Or continue with cooking guidance by typing a specific recipe name!

🎯 **CALL TO ACTION**: Type a recipe name to start cooking!"""
        
        # Search for recipe in database
        self.recipe_data = self._find_recipe(recipe_name)
        
        if not self.recipe_data:
            # Recipe not found - show available options or suggest recipe discovery
            available_recipes = [recipe['name'] for recipe in self.recipes_db['recipes'][:5]]
            
            response = f"""❌ **Recipe Not Found: "{recipe_name}"**

I couldn't find that recipe in my database. Here are some recipes I can help you cook:

"""
            for i, recipe in enumerate(available_recipes, 1):
                response += f"{i}️⃣ **{recipe}**\n"
            
            response += """\n**Options:**
• Choose one of the recipes above by number
• Try a different recipe name
• Say "find recipes" to discover more options

Which recipe would you like to cook? 🔍

🎯 **CALL TO ACTION**: Type the recipe name or number (1-5) to start cooking!"""
            
            return response
        
        # Recipe found - load cooking instructions
        self.cooking_instructions = self._find_cooking_instructions(self.recipe_data['id'])
        
        if not self.cooking_instructions:
            return f"""⚠️ **Recipe Found But Missing Cooking Instructions**

I found "{self.recipe_data['name']}" but don't have step-by-step cooking instructions for it yet.

**Let me help you find a recipe with full cooking guidance:**
• Say "find similar recipes"
• Choose a different recipe
• Go back to Recipe Discovery

What would you like to do? 🤔"""
        
        # Success - recipe and instructions loaded
        self.step = 2
        
        response = f"""✅ **Great! Let's cook {self.recipe_data['name']}**

**Recipe Overview:**
⏱️ **Total Time**: {self.recipe_data['total_time']} minutes
👥 **Default Servings**: {self.recipe_data['servings']}
🔥 **Difficulty**: {self.recipe_data['difficulty'].title()}
📊 **Calories per serving**: {self.recipe_data['calories_per_serving']}

**What You'll Need:**
🔧 **Equipment**: {', '.join(self.cooking_instructions['equipment_needed'])}
📝 **Total Steps**: {self.cooking_instructions['total_steps']}
⏰ **Active Cooking Time**: ~{self.cooking_instructions['estimated_active_time']} minutes

**Ready to start cooking?** Let's set up your servings first! 👨‍🍳

🎯 **CALL TO ACTION**: Please tell me how many servings you want to make (e.g., "4 servings", "6", "double the recipe")"""
        
        return response
    
    def _find_recipe(self, recipe_name):
        """Find recipe by name (case-insensitive partial match)"""
        recipe_name_lower = recipe_name.lower()
        
        for recipe in self.recipes_db['recipes']:
            if recipe_name_lower in recipe['name'].lower() or recipe['name'].lower() in recipe_name_lower:
                return recipe
                
        # Try exact number match if user selected from list
        try:
            recipe_num = int(recipe_name) - 1
            if 0 <= recipe_num < len(self.recipes_db['recipes']):
                return self.recipes_db['recipes'][recipe_num]
        except ValueError:
            pass
            
        return None
    
    def _find_cooking_instructions(self, recipe_id):
        """Find cooking instructions by recipe ID"""
        for instructions in self.cooking_db['cooking_instructions']:
            if instructions['recipe_id'] == recipe_id:
                return instructions
        return None
    
    def _scale_ingredients(self, target_servings):
        """Scale ingredient quantities based on target servings"""
        if not self.recipe_data:
            return []
            
        original_servings = self.recipe_data['servings']
        scale_factor = target_servings / original_servings
        
        scaled_ingredients = []
        for ingredient in self.recipe_data['ingredients']:
            scaled_amount = ingredient['amount'] * scale_factor
            # Round to reasonable precision
            if scaled_amount < 0.1:
                scaled_amount = round(scaled_amount, 2)
            elif scaled_amount < 1:
                scaled_amount = round(scaled_amount, 1)
            else:
                scaled_amount = round(scaled_amount)
                
            scaled_ingredients.append({
                'name': ingredient['name'],
                'amount': scaled_amount,
                'unit': ingredient['unit']
            })
            
        return scaled_ingredients
    
    def handle_step_2(self, user_input: str):
        """STEP 2: SERVING SIZE SETUP - Ask how many servings to make"""
        
        if user_input.strip():
            # Parse serving size input
            try:
                target_servings = int(user_input.strip())
                if target_servings < 1 or target_servings > 20:
                    return """⚠️ **Invalid Serving Size**
                    
Please enter a number between 1 and 20 servings.

How many servings would you like to make? 👥"""
                
                # Store target servings
                self.session.set('target_servings', target_servings)
                
                # Scale ingredients 
                scaled_ingredients = self._scale_ingredients(target_servings)
                self.session.set('scaled_ingredients', scaled_ingredients)
                
                # Move to step 3
                self.step = 3
                return self.handle_step_3()
                
            except ValueError:
                return """⚠️ **Please Enter a Number**
                
I need a number for how many servings you'd like to make.

Examples: "2", "4", "6"

How many servings would you like to make? 👥"""
        
        # Show serving size options
        if not self.recipe_data:
            return "❌ **Error**: Recipe data not loaded. Please start over."
            
        original_servings = self.recipe_data['servings']
        
        response = f"""👥 **Step 2: Serving Size Setup**

**Recipe**: {self.recipe_data['name']}
**Original servings**: {original_servings}

**How many servings would you like to make?**

**Common Options:**
1️⃣ **{original_servings} servings** - Original recipe size
2️⃣ **{original_servings * 2} servings** - Double the recipe  
3️⃣ **1 serving** - Single portion
4️⃣ **Custom amount** - Enter any number

**Or just tell me a number** (e.g., "6 servings" or "8")

**Note**: I'll automatically adjust all ingredient quantities for your desired serving size.

How many servings do you want to make? 🍽️

🎯 **CALL TO ACTION**: Type the number of servings you want (e.g., "6", "8 servings", "double it")"""
        
        return response
    
    def handle_step_3(self, user_input=""):
        """STEP 3: EQUIPMENT & INGREDIENT CHECK - Show scaled ingredients and equipment needed"""
        
        if user_input.strip():
            response = user_input.strip().lower()
            if 'yes' in response or 'ready' in response or 'proceed' in response:
                # User is ready to start cooking
                self.step = 4
                return self.handle_step_4()
            elif 'no' in response or 'not ready' in response:
                # User is not ready - return to beginning  
                self.step = 1
                return "🔄 **No problem! Let's start over when you're ready.**\n\nSay the recipe name again when you'd like to cook! 😊"
            else:
                # Treat any other input as ready to proceed
                self.step = 4  
                return self.handle_step_4()
        
        # Show ingredient list and equipment check
        if not self.recipe_data or not self.cooking_instructions:
            return "❌ **Error**: Recipe data not loaded. Please start over."
            
        scaled_ingredients = self.session.get('scaled_ingredients', [])
        target_servings = self.session.get('target_servings', self.recipe_data['servings'])
        
        response = f"""📋 **Step 3: Equipment & Ingredient Check**

**Recipe**: {self.recipe_data['name']} ({target_servings} servings)

**🥄 INGREDIENTS YOU'LL NEED:**
"""
        
        for ingredient in scaled_ingredients:
            if ingredient['amount'] == int(ingredient['amount']):
                amount_str = str(int(ingredient['amount']))
            else:
                amount_str = str(ingredient['amount'])
            response += f"• **{ingredient['name']}**: {amount_str} {ingredient['unit']}\n"
        
        response += f"""
**🔧 EQUIPMENT NEEDED:**
"""
        for equipment in self.cooking_instructions['equipment_needed']:
            response += f"• {equipment.replace('_', ' ').title()}\n"
        
        response += f"""
**⏱️ TIME ESTIMATES:**
• **Total Time**: {self.recipe_data['total_time']} minutes
• **Active Cooking**: ~{self.cooking_instructions['estimated_active_time']} minutes
• **Total Steps**: {self.cooking_instructions['total_steps']} steps

**✅ READINESS CHECK:**
□ Do you have all the ingredients?
□ Do you have the required equipment?  
□ Are you ready to start cooking?

**🎯 CALL TO ACTION**: 
• Type **"YES"** - I'm ready to start cooking! 
• Type **"NO"** - I need more time to prepare"""
        
        return response
    
    def handle_step_4(self, user_input=""):
        """STEP 4: PREP PHASE - Begin with prep steps from cooking instructions"""
        
        # Add safety check for recipe data
        if not self.recipe_data or not self.cooking_instructions:
            return "❌ **Error**: Recipe data not loaded. Please start over by selecting a recipe again."
        
        if user_input.strip():
            response = user_input.strip().lower()
            if 'ready' in response or 'done' in response or 'start' in response:
                # Validate state before transition
                if not self.recipe_data:
                    return "❌ **Recipe data lost**. Please type **'restart cooking'** to reload the recipe."
                if not self.cooking_instructions:
                    return "❌ **Cooking instructions lost**. Please type **'restart cooking'** to reload the recipe."
                
                # User finished prep, move to interactive cooking
                self.step = 5
                self.current_cooking_step = 1
                self.session_status = "active"
                
                # Ensure current_cooking_step is properly initialized
                if not hasattr(self, 'current_cooking_step') or self.current_cooking_step is None:
                    self.current_cooking_step = 1
                
                try:
                    return self.handle_step_5()
                except Exception as e:
                    import traceback
                    tb = traceback.format_exc()
                    return f"""❌ **Error starting cooking steps**

**Error**: {str(e)}

**Possible solutions:**
• Type **"restart cooking"** to start over
• Use **/reset** to start completely fresh
• Check that you completed all prep steps

**Debug trace**: {tb[:500]}..."""
            else:
                # Continue with prep phase
                pass
        
        if not self.cooking_instructions:
            return "❌ **Error**: Cooking instructions not loaded. Please start over."
            
        # Get prep steps (phase: "prep")
        prep_steps = [step for step in self.cooking_instructions['steps'] if step['phase'] == 'prep']
        
        if not prep_steps:
            # No prep steps, go directly to cooking
            self.step = 5
            self.current_cooking_step = 1
            self.session_status = "active"
            return self.handle_step_5()
            
        response = f"""🔪 **Step 4: Prep Phase**

**Recipe**: {self.recipe_data['name']}
**Let's start by preparing our ingredients!**

**PREP STEPS:**
"""
        
        for i, step in enumerate(prep_steps, 1):
            response += f"""
**PREP {i}** ⏱️ *{step['duration_minutes']} min*
• {step['instruction']}
💡 **Tip**: {step['tips']}
"""
        
        response += f"""
**✅ PREP CHECKLIST:**
□ All ingredients prepped and ready
□ Equipment set up and accessible
□ Work area clean and organized

**🎯 CALL TO ACTION**: Type **"READY"** when you've finished all prep steps and want to start cooking!"""
        
        return response
    
    def handle_step_5(self, user_input=""):
        """STEP 5: INTERACTIVE COOKING STEPS - Step-by-step cooking with navigation"""
        
        # Add comprehensive safety checks
        if not self.recipe_data or not self.cooking_instructions:
            return "❌ **Error**: Recipe data not loaded. Please start over by selecting a recipe again."
            
        if not hasattr(self, 'current_cooking_step') or self.current_cooking_step is None:
            self.current_cooking_step = 1
            
        if not self.cooking_instructions or 'steps' not in self.cooking_instructions:
            return "❌ **Error**: Cooking instructions not available. Please start over."
            
        # Get cooking steps (not prep phase)
        cooking_steps = [step for step in self.cooking_instructions['steps'] if step['phase'] != 'prep']
        
        if not cooking_steps:
            # No cooking steps, go to completion
            self.step = 6
            return self.handle_step_6()
            
        # Handle user navigation
        if user_input.strip():
            cmd = user_input.strip().lower()
            if 'next' in cmd:
                self.current_cooking_step += 1
            elif 'prev' in cmd or 'back' in cmd:
                self.current_cooking_step = max(1, self.current_cooking_step - 1)
            elif 'repeat' in cmd:
                pass  # Stay on current step
            elif 'done' in cmd or 'finish' in cmd:
                # Move to completion
                self.step = 6
                return self.handle_step_6()
            elif 'pause' in cmd:
                self.session_status = "paused"
                return """⏸️ **Cooking Paused**
                
Your progress has been saved. Say "resume" when you're ready to continue cooking!

**Current Progress**: Step {self.current_cooking_step} of {len(cooking_steps)}"""
            elif 'resume' in cmd:
                self.session_status = "active"
                # Continue with current step
                
        # Check bounds
        if self.current_cooking_step > len(cooking_steps):
            # Finished all cooking steps
            self.step = 6
            return self.handle_step_6()
            
        if self.current_cooking_step < 1:
            self.current_cooking_step = 1
            
        # Display current cooking step with bounds checking
        try:
            current_step = cooking_steps[self.current_cooking_step - 1]
        except (IndexError, TypeError) as e:
            self.current_cooking_step = 1
            current_step = cooking_steps[0]
        
        response = f"""🔥 **Interactive Cooking - Step {self.current_cooking_step} of {len(cooking_steps)}**

**{current_step['instruction']}**

"""
        
        if current_step['duration_minutes']:
            response += f"⏲️ **Timer**: {current_step['duration_minutes']} minutes\n"
            
        if current_step['temperature']:
            response += f"🌡️ **Temperature**: {current_step['temperature']}\n"
            
        if current_step['tips']:
            response += f"💡 **Tips**: {current_step['tips']}\n"
            
        if current_step['visual_cues']:
            response += f"👁️ **Visual Cues**: {current_step['visual_cues']}\n"
            
        response += f"""
**🎯 CALL TO ACTION - Choose one:**
🔴 **"NEXT"** - Go to next cooking step
🔵 **"BACK"** - Go to previous step  
🟡 **"REPEAT"** - Show this step again
⏸️ **"PAUSE"** - Pause cooking session
✅ **"DONE"** - I've finished cooking!

**Progress**: {self.current_cooking_step}/{len(cooking_steps)} steps complete 📊"""
        
        return response
    
    def handle_step_6(self, user_input=""):
        """STEP 6: COOKING COMPLETION - Rating, feedback, and next actions"""
        
        if user_input.strip():
            cmd = user_input.strip().lower()
            if 'rate' in cmd:
                return """⭐ **Rate This Recipe**
                
How would you rate this cooking experience?

1⭐ - Poor
2⭐ - Fair  
3⭐ - Good
4⭐ - Very Good
5⭐ - Excellent

Just say the number of stars! ⭐"""
            elif cmd in ['1', '2', '3', '4', '5']:
                rating = int(cmd)
                self.session.set('recipe_rating', rating)
                return f"""🎉 **Thanks for rating this recipe {rating}⭐!**

Your feedback helps improve our cooking guidance.

**What would you like to do next?**
• "cook something else" - Find another recipe
• "track this meal" - Log nutrition info
• "save recipe" - Add to favorites"""
            elif 'cook' in cmd and 'else' in cmd:
                # Transition to recipe discovery
                self.step = 1
                self.session.current_journey = None
                return """🔍 **Let's find your next recipe!**
                
What would you like to cook next? You can say:
• A specific dish name
• "show me recipes"  
• "surprise me"

I'm ready to guide you through another cooking adventure! 👨‍🍳"""
        
        # Show completion message
        response = f"""🎆 **Congratulations! You've finished cooking {self.recipe_data['name']}!**

**🍽️ SERVING SUGGESTIONS:**
• Let rest for 2-3 minutes before serving
• Garnish as desired
• Serve immediately while hot

**📊 COOKING SESSION COMPLETE:**
• Recipe: {self.recipe_data['name']}
• Servings: {self.session.get('target_servings', self.recipe_data['servings'])}
• Total time: ~{self.recipe_data['total_time']} minutes

**What would you like to do next?**
🌟 **Rate** this recipe experience  
🍳 **Cook something else** 
📊 **Track this meal** in your food log
💾 **Save recipe** to favorites

How did it turn out? 🎉"""
        
        return response

class SimpleCalorieMeals:
    def __init__(self, session):
        self.session = session
        self.step = 1
        self.calorie_target = None
        self.calorie_range = None
        self.meal_scope = None
        self.meal_types = []
        self.dietary_preferences = []
        self.search_results = []
        self.selected_meal = None
        self._load_meal_databases()
    
    def _load_meal_databases(self):
        """Load meal and food nutrition databases"""
        import json
        import os
        
        try:
            # Load meal suggestions database
            meals_path = "/Users/uditrai88/Desktop/nutrition-chatbot/raw_data/meal_suggestions_raw.json"
            with open(meals_path, 'r') as f:
                self.meals_db = json.load(f)
            
            # Load foods nutrition database  
            foods_path = "/Users/uditrai88/Desktop/nutrition-chatbot/raw_data/foods_nutrition_raw.json"
            with open(foods_path, 'r') as f:
                self.foods_db = json.load(f)
                
        except Exception as e:
            # Fallback to empty databases if files not found
            self.meals_db = {"meal_suggestions": []}
            self.foods_db = {"foods": []}
    
    def start_journey(self, user_input=""):
        self.step = 1
        return self.handle_step_1()
    
    def handle_input(self, user_input: str):
        try:
            if self.step == 1:
                return self.handle_step_1(user_input)
            elif self.step == 2:
                return self.handle_step_2(user_input)
            elif self.step == 3:
                return self.handle_step_3(user_input)
            elif self.step == 4:
                return self.handle_step_4(user_input)
            elif self.step == 5:
                return self.handle_step_5(user_input)
            elif self.step == 6:
                return self.handle_step_6(user_input)
            elif self.step == 7:
                return self.handle_step_7(user_input)
            elif self.step == 8:
                return self.handle_step_8(user_input)
            elif self.step == 9:
                return self.handle_step_9(user_input)
            else:
                return self.start_journey()
        except Exception as e:
            return f"""❌ **Calorie Meals Error**

Something went wrong: {str(e)}

**Recovery options:**
• Use **/reset** to start fresh
• Try rephrasing your input

I apologize for the inconvenience! 🙏"""
    
    def handle_step_1(self, user_input=""):
        """STEP 1: CALORIE GOAL DETERMINATION"""
        
        if user_input.strip():
            # Parse calorie input
            calorie_info = self._parse_calorie_input(user_input.strip())
            if calorie_info:
                self.calorie_target = calorie_info['target']
                self.calorie_range = calorie_info['range']
                self.session.set('calorie_target', self.calorie_target)
                self.session.set('calorie_range', self.calorie_range)
                self.step = 2
                return self.handle_step_2()
            else:
                return """❌ **Invalid Calorie Input**

I couldn't understand your calorie goal. Please try again!

**Valid examples:**
• "400 calories" or "400"
• "300-500 calories" or "between 300 and 500"  
• "low calorie lunch" (under 400)
• "high protein breakfast under 350"

🎯 **CALL TO ACTION**: Type your calorie goal clearly!"""
        
        # Show step 1 initial screen
        return """🎯 **Step 1: Calorie Goal Determination**

What's your calorie target for your meal?

**📊 CALORIE GUIDE:**

**🥗 Light Meals (150-350 calories)**
• Perfect for: Snacks, light breakfast, weight loss
• Examples: Greek yogurt parfait, small salads

**⚖️ Moderate Meals (350-500 calories)**  
• Perfect for: Regular meals, maintenance
• Examples: Balanced lunch bowls, most dinners

**🍽️ Hearty Meals (500-700 calories)**
• Perfect for: Post-workout, active lifestyle
• Examples: Power bowls, protein-rich meals

**💪 High-Energy Meals (700+ calories)**
• Perfect for: Athletes, muscle building, high activity
• Examples: Large portions, calorie-dense meals

**🕐 MEAL TIMING:**
🌅 Breakfast: 200-400 calories typical
🌞 Lunch: 300-600 calories typical  
🌙 Dinner: 400-700 calories typical
🍎 Snacks: 100-300 calories typical

**INPUT OPTIONS:**
• Specific number: "400 calories" or just "400"
• Range: "300-500 calories" or "between 300 and 500"
• Goal-based: "low calorie lunch" or "high protein under 450"

🎯 **CALL TO ACTION**: Tell me your calorie target!"""
    
    def _parse_calorie_input(self, user_input):
        """Parse various calorie input formats"""
        import re
        
        user_input_lower = user_input.lower()
        
        # Pattern 1: Specific number (e.g., "400", "400 calories")
        specific_match = re.search(r'(\d{2,4})\s*(?:cal|calories?)?', user_input_lower)
        if specific_match:
            target = int(specific_match.group(1))
            if 50 <= target <= 2000:  # Reasonable range
                # Use more flexible range for better matching
                range_buffer = max(75, target * 0.2)  # At least 75 or 20% of target
                range_buffer = min(range_buffer, 150)  # Cap at 150 calories
                return {
                    'target': target,
                    'range': (int(target - range_buffer), int(target + range_buffer))
                }
        
        # Pattern 2: Range (e.g., "300-500", "between 300 and 500")
        range_match = re.search(r'(?:between\s+)?(\d{2,4})\s*(?:[-to\s]+|and\s+)(\d{2,4})', user_input_lower)
        if range_match:
            min_cal = int(range_match.group(1))
            max_cal = int(range_match.group(2))
            if min_cal < max_cal and 50 <= min_cal <= 2000 and 50 <= max_cal <= 2000:
                return {
                    'target': (min_cal + max_cal) // 2,
                    'range': (min_cal, max_cal)
                }
        
        # Pattern 3: Goal-based (e.g., "low calorie", "high protein under 400")
        if 'low' in user_input_lower and 'calorie' in user_input_lower:
            return {'target': 300, 'range': (150, 350)}
        elif 'high' in user_input_lower and 'calorie' in user_input_lower:
            return {'target': 600, 'range': (500, 800)}
        elif 'moderate' in user_input_lower:
            return {'target': 450, 'range': (350, 550)}
        
        # Pattern 4: Under/over specific number
        under_match = re.search(r'under\s+(\d{2,4})', user_input_lower)
        if under_match:
            limit = int(under_match.group(1))
            return {'target': limit - 50, 'range': (100, limit)}
        
        over_match = re.search(r'over\s+(\d{2,4})', user_input_lower)
        if over_match:
            limit = int(over_match.group(1))
            return {'target': limit + 100, 'range': (limit, limit + 300)}
        
        return None
    
    def handle_step_2(self, user_input=""):
        """STEP 2: MEAL SCOPE SELECTION"""
        
        if user_input.strip():
            choice = user_input.strip().lower()
            if '1' in choice or 'single' in choice:
                self.meal_scope = 'single_meal'
                self.step = 3
                return self.handle_step_3()
            elif '2' in choice or 'daily' in choice or 'day' in choice:
                self.meal_scope = 'daily_plan'
                self.step = 3
                return self.handle_step_3()
            elif '3' in choice or 'multiple' in choice or 'week' in choice:
                self.meal_scope = 'multiple_days'
                self.step = 3
                return self.handle_step_3()
            else:
                return """❌ **Please select a valid option**

Type **1**, **2**, or **3** to continue, or use keywords like "single meal", "daily plan", or "weekly plan".

🎯 **CALL TO ACTION**: Choose your planning scope!"""
        
        return f"""📋 **Step 2: Meal Scope Selection**

**Target**: {self.calorie_target} calories ({self.calorie_range[0]}-{self.calorie_range[1]} range)

Are you planning for:

**1️⃣ SINGLE MEAL**
• Find one optimal meal that fits your calorie goal
• Perfect for immediate meal planning
• Quick and focused selection

**2️⃣ DAILY PLAN**  
• Plan all meals for today to reach your daily goals
• Calorie distribution: Breakfast 25%, Lunch 35%, Dinner 35%, Snacks 5%
• Complete daily nutrition balance

**3️⃣ MULTIPLE DAYS**
• Plan meals for a week or specific days
• Consistent calorie goals across multiple days
• Meal variety and planning ahead

🎯 **CALL TO ACTION**: Type **1**, **2**, or **3** to select your planning scope!"""
    
    def handle_step_3(self, user_input=""):
        """STEP 3: MEAL TYPE & TIMING"""
        
        if user_input.strip():
            # Parse meal type selection
            meal_selection = self._parse_meal_type_input(user_input.strip())
            if meal_selection:
                self.meal_types = meal_selection
                self.session.set('meal_types', self.meal_types)
                self.step = 4
                return self.handle_step_4()
            else:
                return """❌ **Please select valid meal types**

Choose from: breakfast, lunch, dinner, snack, or "all meals"
You can also use numbers: 1, 2, 3, 4

🎯 **CALL TO ACTION**: Tell me which meal type(s) you want!"""
        
        # Calculate calorie ranges for different meal types based on target
        breakfast_range = (int(self.calorie_target * 0.15), int(self.calorie_target * 0.35))
        lunch_range = (int(self.calorie_target * 0.25), int(self.calorie_target * 0.45))
        dinner_range = (int(self.calorie_target * 0.30), int(self.calorie_target * 0.50))
        snack_range = (int(self.calorie_target * 0.10), int(self.calorie_target * 0.25))
        
        scope_text = "single meal" if self.meal_scope == 'single_meal' else ("daily plan" if self.meal_scope == 'daily_plan' else "multiple days")
        
        return f"""🕐 **Step 3: Meal Type & Timing**

**Planning for**: {scope_text}
**Target calories**: {self.calorie_target} ({self.calorie_range[0]}-{self.calorie_range[1]} range)

Which meal(s) are you planning?

**1️⃣ BREAKFAST** 🌅
• Recommended: {breakfast_range[0]}-{breakfast_range[1]} calories
• Best for: Energy start, light to moderate portions

**2️⃣ LUNCH** 🌞  
• Recommended: {lunch_range[0]}-{lunch_range[1]} calories
• Best for: Midday fuel, balanced nutrition

**3️⃣ DINNER** 🌙
• Recommended: {dinner_range[0]}-{dinner_range[1]} calories  
• Best for: Evening satisfaction, hearty meals

**4️⃣ SNACKS** 🍎
• Recommended: {snack_range[0]}-{snack_range[1]} calories
• Best for: Between meals, light options

**5️⃣ ALL MEALS** 🍽️
• Plan multiple meal types together
• Balanced daily nutrition approach

🎯 **CALL TO ACTION**: Type the number(s) or meal name(s) you want to plan!"""
    
    def _parse_meal_type_input(self, user_input):
        """Parse meal type selection"""
        user_input_lower = user_input.lower()
        meal_types = []
        
        # Check for numbers
        if '1' in user_input or 'breakfast' in user_input_lower:
            meal_types.append('breakfast')
        if '2' in user_input or 'lunch' in user_input_lower:
            meal_types.append('lunch')
        if '3' in user_input or 'dinner' in user_input_lower:
            meal_types.append('dinner')
        if '4' in user_input or 'snack' in user_input_lower:
            meal_types.append('snack')
        if '5' in user_input or 'all' in user_input_lower:
            meal_types = ['breakfast', 'lunch', 'dinner', 'snack']
        
        return meal_types if meal_types else None
    
    def handle_step_4(self, user_input=""):
        """STEP 4: DIETARY PREFERENCES COLLECTION"""
        
        if user_input.strip():
            # Parse dietary preferences
            dietary_prefs = self._parse_dietary_preferences(user_input.strip())
            self.dietary_preferences = dietary_prefs
            self.session.set('dietary_preferences', self.dietary_preferences)
            self.step = 5
            return self.handle_step_5()
        
        meal_types_text = ', '.join(self.meal_types)
        
        return f"""🥗 **Step 4: Dietary Preferences & Restrictions**

**Planning**: {meal_types_text} 
**Target**: {self.calorie_target} calories ({self.calorie_range[0]}-{self.calorie_range[1]} range)

Any dietary preferences or restrictions?

**🌱 DIETARY TAGS AVAILABLE:**

**Lifestyle Diets:**
• **vegetarian** - No meat, fish allowed
• **vegan** - No animal products
• **keto_friendly** - Low carb, high fat
• **low_carb** - Reduced carbohydrate content

**Health Focus:**  
• **high_protein** - Protein-rich meals (25g+ protein)
• **high_fiber** - Fiber-rich options (8g+ fiber)
• **heart_healthy** - Good for cardiovascular health
• **omega_3** - Rich in healthy omega-3 fats

**Allergies/Intolerances:**
• **gluten_free** - No gluten-containing ingredients  
• **dairy_free** - No dairy products
• **nut_free** - No nuts or nut products

**INPUT OPTIONS:**
• Specific tags: "vegetarian and high protein"
• Multiple: "gluten free, dairy free, high fiber"
• None: "no restrictions" or "none"

🎯 **CALL TO ACTION**: Tell me your dietary preferences, or type "none" for no restrictions!"""
    
    def _parse_dietary_preferences(self, user_input):
        """Parse dietary preferences from user input"""
        user_input_lower = user_input.lower()
        
        if 'none' in user_input_lower or 'no restriction' in user_input_lower:
            return []
        
        available_tags = [
            'vegetarian', 'vegan', 'gluten_free', 'keto_friendly', 'low_carb',
            'high_protein', 'high_fiber', 'heart_healthy', 'omega_3', 
            'dairy_free', 'nut_free'
        ]
        
        selected_tags = []
        for tag in available_tags:
            # Handle various formats
            tag_variations = [
                tag, 
                tag.replace('_', ' '),
                tag.replace('_', '-'),
                tag.replace('_friendly', ''),
                tag.replace('_free', ' free')
            ]
            
            if any(variation in user_input_lower for variation in tag_variations):
                selected_tags.append(tag)
        
        return selected_tags
    
    def handle_step_5(self, user_input=""):
        """STEP 5: MEAL DATABASE SEARCH"""
        
        # Automatically perform search based on collected criteria
        self.search_results = self._search_meal_database()
        
        # Store whether fallback search was used for display purposes
        self.used_fallback = self._check_if_fallback_used()
        
        if self.search_results:
            self.step = 6
            return self.handle_step_6()
        else:
            # No meals found - show error handling options
            return self._handle_no_meals_found()
    
    def _check_if_fallback_used(self):
        """Check if any results came from fallback searches"""
        if not self.search_results:
            return False
        
        # Check if any meal is outside original criteria
        for meal in self.search_results:
            # Check if outside original calorie range
            if not (self.calorie_range[0] <= meal['calories'] <= self.calorie_range[1]):
                return True
            
            # Check if meal type doesn't match requested types
            meal_types_match = any(mt in meal.get('meal_type', []) for mt in self.meal_types)
            if not meal_types_match:
                return True
        
        return False
    
    def _search_meal_database(self):
        """Search meal database with collected criteria"""
        meals = self.meals_db.get('meal_suggestions', [])
        
        # Try primary search first
        matching_meals = self._perform_search(meals, strict=True)
        
        # If no matches, try fallback searches
        if not matching_meals:
            matching_meals = self._perform_fallback_searches(meals)
        
        # Sort by score and return top matches
        matching_meals.sort(key=lambda x: x[1], reverse=True)
        return [meal for meal, score in matching_meals[:5]]  # Top 5 matches
    
    def _perform_search(self, meals, strict=True):
        """Perform meal search with given criteria"""
        matching_meals = []
        
        for meal in meals:
            # Check calorie range
            if not (self.calorie_range[0] <= meal['calories'] <= self.calorie_range[1]):
                continue
            
            # Check meal type (strict vs flexible)
            if strict:
                meal_types_match = any(mt in meal.get('meal_type', []) for mt in self.meal_types)
                if not meal_types_match:
                    continue
            
            # Check dietary restrictions
            meal_tags = meal.get('dietary_tags', [])
            dietary_match = all(pref in meal_tags for pref in self.dietary_preferences)
            if not dietary_match:
                continue
            
            # Calculate match score for ranking
            score = self._calculate_meal_score(meal)
            matching_meals.append((meal, score))
        
        return matching_meals
    
    def _perform_fallback_searches(self, meals):
        """Perform fallback searches when primary search fails"""
        matching_meals = []
        
        # Fallback 1: Expand calorie range by ±100 calories
        expanded_range = (self.calorie_range[0] - 100, self.calorie_range[1] + 100)
        original_range = self.calorie_range
        self.calorie_range = expanded_range
        
        matching_meals = self._perform_search(meals, strict=True)
        
        # Fallback 2: If still no matches, relax meal type restrictions
        if not matching_meals:
            matching_meals = self._perform_search(meals, strict=False)
        
        # Fallback 3: If still no matches, ignore dietary preferences (but keep calorie range)
        if not matching_meals:
            original_dietary = self.dietary_preferences
            self.dietary_preferences = []
            matching_meals = self._perform_search(meals, strict=False)
            self.dietary_preferences = original_dietary
        
        # Restore original range
        self.calorie_range = original_range
        
        return matching_meals
    
    def _calculate_meal_score(self, meal):
        """Calculate relevance score for meal ranking"""
        score = 0
        
        # Calorie accuracy (closer to target = higher score)
        calorie_diff = abs(meal['calories'] - self.calorie_target)
        calorie_score = max(0, 100 - calorie_diff)  # Higher score for closer match
        score += calorie_score
        
        # Prep time preference (shorter = slightly higher score)
        prep_time = meal.get('prep_time', 30)
        prep_score = max(0, 50 - prep_time)  # Max 50 points for prep time
        score += prep_score
        
        # Dietary tag bonus
        meal_tags = meal.get('dietary_tags', [])
        tag_bonus = len([tag for tag in self.dietary_preferences if tag in meal_tags]) * 10
        score += tag_bonus
        
        # Nutrition quality bonus  
        nutrition = meal.get('nutrition', {})
        if nutrition.get('protein', 0) >= 20:  # High protein bonus
            score += 15
        if nutrition.get('fiber', 0) >= 8:   # High fiber bonus
            score += 10
        
        return score
    
    def handle_step_6(self, user_input=""):
        """STEP 6: MEAL RESULTS DISPLAY"""
        
        if user_input.strip():
            # Handle meal selection or actions
            return self._handle_meal_selection(user_input.strip())
        
        # Display search results
        fallback_note = ""
        if getattr(self, 'used_fallback', False):
            fallback_note = """⚠️ **Expanded Search Results**
No exact matches found for your criteria, so I've expanded the search to show the best available options:

"""

        results_text = f"""🍽️ **Step 6: Meal Results ({len(self.search_results)} matches)**

**Your original criteria:**
• **Calories**: {self.calorie_range[0]}-{self.calorie_range[1]}
• **Meal types**: {', '.join(self.meal_types)}
• **Dietary prefs**: {', '.join(self.dietary_preferences) if self.dietary_preferences else 'None'}

{fallback_note}**🎯 BEST AVAILABLE MATCHES:**

"""
        
        for i, meal in enumerate(self.search_results, 1):
            nutrition = meal.get('nutrition', {})
            components = meal.get('components', [])
            tags = meal.get('dietary_tags', [])
            
            # Format components preview
            component_names = [comp['name'] for comp in components[:3]]
            components_text = ', '.join(component_names)
            if len(components) > 3:
                components_text += f', +{len(components)-3} more'
            
            # Format dietary tags
            tag_badges = ' '.join([f"🏷️{tag.replace('_', ' ')}" for tag in tags[:3]])
            
            results_text += f"""**{i}. {meal['name']}**
• **{meal['calories']} calories** | ⏱️ {meal.get('prep_time', 'Unknown')} min prep
• **Nutrition**: {nutrition.get('protein', 0)}g protein | {nutrition.get('carbs', 0)}g carbs | {nutrition.get('fat', 0)}g fat
• **Components**: {components_text}
• **Tags**: {tag_badges}

"""
        
        results_text += f"""**ACTIONS:**
• Type **1-{len(self.search_results)}** to select a meal
• Type **"details X"** for full meal information (e.g., "details 1")
• Type **"more options"** to see additional meals
• Type **"refine search"** to adjust your criteria

🎯 **CALL TO ACTION**: Select a meal number or choose an action!"""
        
        return results_text
    
    def _handle_meal_selection(self, user_input):
        """Handle meal selection from results"""
        user_input_lower = user_input.lower()
        
        # Check for meal number selection
        for i in range(1, len(self.search_results) + 1):
            if str(i) in user_input:
                self.selected_meal = self.search_results[i-1]
                self.step = 7
                return self.handle_step_7()
        
        # Check for details request
        if 'details' in user_input_lower:
            try:
                num = int(''.join(filter(str.isdigit, user_input)))
                if 1 <= num <= len(self.search_results):
                    return self._show_meal_details(self.search_results[num-1])
            except:
                pass
        
        # Check for more options
        if 'more' in user_input_lower or 'additional' in user_input_lower:
            return self._show_more_options()
        
        # Check for refine search
        if 'refine' in user_input_lower or 'adjust' in user_input_lower:
            self.step = 4  # Go back to dietary preferences
            return self.handle_step_4()
        
        return """❌ **Invalid selection**

Please choose:
• A meal number (1, 2, 3, etc.)
• "details X" for meal information
• "more options" for additional meals
• "refine search" to adjust criteria

🎯 **CALL TO ACTION**: Make a valid selection!"""
    
    def _show_meal_details(self, meal):
        """Show detailed meal information"""
        nutrition = meal.get('nutrition', {})
        components = meal.get('components', [])
        tags = meal.get('dietary_tags', [])
        
        # Calculate nutrition percentages
        total_cals = meal['calories']
        protein_cals = nutrition.get('protein', 0) * 4
        carb_cals = nutrition.get('carbs', 0) * 4  
        fat_cals = nutrition.get('fat', 0) * 9
        
        protein_pct = int((protein_cals / total_cals) * 100) if total_cals > 0 else 0
        carb_pct = int((carb_cals / total_cals) * 100) if total_cals > 0 else 0
        fat_pct = int((fat_cals / total_cals) * 100) if total_cals > 0 else 0
        
        details = f"""📋 **Detailed View: {meal['name']}**

**CALORIES & MACROS:**
• **Total**: {meal['calories']} calories
• **Protein**: {nutrition.get('protein', 0)}g ({protein_pct}% of calories)
• **Carbs**: {nutrition.get('carbs', 0)}g ({carb_pct}% of calories) 
• **Fat**: {nutrition.get('fat', 0)}g ({fat_pct}% of calories)
• **Fiber**: {nutrition.get('fiber', 0)}g

**COMPLETE INGREDIENTS:**
"""
        
        for component in components:
            details += f"• {component['name']}: {component['amount']}{component['unit']}\n"
        
        details += f"""
**MEAL BENEFITS:**
• **Prep time**: {meal.get('prep_time', 'Unknown')} minutes
• **Dietary tags**: {', '.join(tags) if tags else 'None specified'}
• **Meal types**: {', '.join(meal.get('meal_type', []))}

**NUTRITION ANALYSIS:**
• **Calorie target**: {abs(meal['calories'] - self.calorie_target)} calories from your {self.calorie_target} target
• **Protein quality**: {'Excellent (25g+)' if nutrition.get('protein', 0) >= 25 else 'Good (15-24g)' if nutrition.get('protein', 0) >= 15 else 'Moderate'}
• **Fiber content**: {'High (8g+)' if nutrition.get('fiber', 0) >= 8 else 'Good (5-7g)' if nutrition.get('fiber', 0) >= 5 else 'Low'}

Type the meal number to select it, or "back" to return to results!"""
        
        return details
    
    def _show_more_options(self):
        """Show additional search options or expanded criteria"""
        return f"""🔍 **More Options**

**EXPAND SEARCH:**
• **Calorie range**: Try ±100 calories ({self.calorie_target-100}-{self.calorie_target+100})
• **Meal types**: Include more meal times
• **Dietary prefs**: Relax some restrictions

**OTHER ACTIONS:**
• **"expand calories"** - Search wider calorie range
• **"any meal type"** - Include all meal types  
• **"fewer restrictions"** - Reduce dietary filters
• **"custom meal"** - Build a custom meal to hit your target

**CROSS-JOURNEY OPTIONS:**
• **"browse recipes"** - Switch to recipe discovery
• **"meal planning"** - Plan full daily meals

🎯 **CALL TO ACTION**: Choose an expansion option or action!"""
    
    def _handle_no_meals_found(self):
        """Handle case when no meals match criteria"""
        return f"""❌ **No Meals Found**

No meals match your criteria:
• **Calories**: {self.calorie_range[0]}-{self.calorie_range[1]}
• **Meal types**: {', '.join(self.meal_types)}
• **Dietary prefs**: {', '.join(self.dietary_preferences) if self.dietary_preferences else 'None'}

**SUGGESTIONS:**

**1️⃣ EXPAND CALORIE RANGE**
• Try ±100 calories: {self.calorie_target-100}-{self.calorie_target+100}

**2️⃣ RELAX DIETARY RESTRICTIONS**
• Remove some dietary preferences temporarily

**3️⃣ DIFFERENT MEAL TYPE**
• Try different meal timing (breakfast, lunch, dinner, snack)

**4️⃣ CUSTOM MEAL BUILDER**
• Build a custom meal to reach your {self.calorie_target} calorie target

🎯 **CALL TO ACTION**: Type "expand calories", "fewer restrictions", "different meal type", or "custom meal"!"""
    
    def handle_step_7(self, user_input=""):
        """STEP 7: MEAL CONFIRMATION"""
        
        if user_input.strip():
            user_input_lower = user_input.strip().lower()
            if 'yes' in user_input_lower or 'confirm' in user_input_lower or 'final' in user_input_lower:
                self.step = 8
                return self.handle_step_8()
            elif 'no' in user_input_lower or 'back' in user_input_lower or 'change' in user_input_lower:
                self.step = 6
                return self.handle_step_6()
            else:
                return """❌ **Please confirm your selection**

Type:
• **"Yes"** or **"Confirm"** to proceed with this meal
• **"No"** or **"Back"** to return to meal selection

🎯 **CALL TO ACTION**: Confirm your meal choice!"""
        
        # Display meal confirmation
        meal = self.selected_meal
        nutrition = meal.get('nutrition', {})
        components = meal.get('components', [])
        
        confirmation_text = f"""✅ **Step 7: Meal Confirmation**

**Selected Meal**: {meal['name']}

**📊 MEAL SUMMARY:**
• **Calories**: {meal['calories']} (target: {self.calorie_target})
• **Prep time**: {meal.get('prep_time', 'Unknown')} minutes
• **Meal types**: {', '.join(meal.get('meal_type', []))}

**🥗 NUTRITION BREAKDOWN:**
• **Protein**: {nutrition.get('protein', 0)}g
• **Carbs**: {nutrition.get('carbs', 0)}g  
• **Fat**: {nutrition.get('fat', 0)}g
• **Fiber**: {nutrition.get('fiber', 0)}g

**🛒 COMPONENT LIST:**
"""
        
        for component in components:
            confirmation_text += f"• {component['name']}: {component['amount']}{component['unit']}\n"
        
        confirmation_text += f"""
**🎯 CALORIE ANALYSIS:**
• Your target: {self.calorie_target} calories
• This meal: {meal['calories']} calories  
• Difference: {meal['calories'] - self.calorie_target:+d} calories

**Is this meal selection final?**

🎯 **CALL TO ACTION**: Type **"Yes"** to confirm or **"No"** to go back and choose differently!"""
        
        return confirmation_text
    
    def handle_step_8(self, user_input=""):
        """STEP 8: NUTRITIONAL ANALYSIS"""
        
        # Generate comprehensive nutritional analysis
        meal = self.selected_meal
        nutrition = meal.get('nutrition', {})
        
        # Calculate detailed macro percentages
        total_calories = meal['calories']
        protein_g = nutrition.get('protein', 0)
        carbs_g = nutrition.get('carbs', 0)
        fat_g = nutrition.get('fat', 0)
        fiber_g = nutrition.get('fiber', 0)
        
        protein_cals = protein_g * 4
        carbs_cals = carbs_g * 4
        fat_cals = fat_g * 9
        
        protein_pct = int((protein_cals / total_calories) * 100) if total_calories > 0 else 0
        carbs_pct = int((carbs_cals / total_calories) * 100) if total_calories > 0 else 0
        fat_pct = int((fat_cals / total_calories) * 100) if total_calories > 0 else 0
        
        # Calculate goal comparison
        calorie_diff = meal['calories'] - self.calorie_target
        calorie_diff_pct = int((calorie_diff / self.calorie_target) * 100)
        
        # Determine nutritional highlights
        highlights = []
        if protein_g >= 25: highlights.append("High protein (25g+)")
        if fiber_g >= 8: highlights.append("High fiber (8g+)")
        if fat_g >= 15 and 'healthy_fats' in meal.get('dietary_tags', []): highlights.append("Healthy fats")
        if protein_pct >= 25: highlights.append("Protein-rich (25%+ calories)")
        
        # Generate visual representation
        protein_bar = "█" * min(protein_pct // 5, 20)
        carbs_bar = "█" * min(carbs_pct // 5, 20) 
        fat_bar = "█" * min(fat_pct // 5, 20)
        
        calorie_progress = min(100, int((meal['calories'] / self.calorie_target) * 100))
        calorie_bar = "█" * (calorie_progress // 5)
        
        analysis_text = f"""📊 **Step 8: Comprehensive Nutritional Analysis**

**🎯 CALORIE ANALYSIS:**
• **Your meal**: {meal['calories']} calories
• **Target**: {self.calorie_target} calories
• **Difference**: {calorie_diff:+d} calories ({calorie_diff_pct:+d}% of target)
• **Goal progress**: {calorie_bar} {calorie_progress}%

**🥗 MACRONUTRIENT BREAKDOWN:**

**Protein**: {protein_g}g ({protein_pct}% of calories)
{protein_bar}

**Carbs**: {carbs_g}g ({carbs_pct}% of calories)  
{carbs_bar}

**Fat**: {fat_g}g ({fat_pct}% of calories)
{fat_bar}

**Fiber**: {fiber_g}g

**⭐ NUTRITIONAL HIGHLIGHTS:**
• {' • '.join(highlights) if highlights else 'Balanced nutrition profile'}

**🏆 DIETARY BENEFITS:**
• **Tags**: {', '.join(meal.get('dietary_tags', [])) if meal.get('dietary_tags') else 'General nutrition'}
• **Prep efficiency**: {meal.get('prep_time', 'Unknown')} minutes
• **Meal appropriateness**: {', '.join(meal.get('meal_type', []))}

**📈 NUTRITION SCORE:**
• **Protein quality**: {'Excellent' if protein_g >= 25 else 'Good' if protein_g >= 15 else 'Fair'}
• **Fiber content**: {'High' if fiber_g >= 8 else 'Good' if fiber_g >= 5 else 'Low'}
• **Calorie accuracy**: {'Perfect' if abs(calorie_diff) <= 25 else 'Good' if abs(calorie_diff) <= 50 else 'Fair'}

Ready to take action with this meal?"""
        
        self.step = 9
        return self.handle_step_9()
    
    def handle_step_9(self, user_input=""):
        """STEP 9: ACTION SELECTION"""
        
        if user_input.strip():
            return self._handle_final_actions(user_input.strip())
        
        meal = self.selected_meal
        
        action_text = f"""🎬 **Step 9: What's Next?**

**Selected**: {meal['name']} ({meal['calories']} calories)

What would you like to do with this meal?

**🔥 IMMEDIATE ACTIONS:**

**1️⃣ START COOKING** 🍳
• Get step-by-step cooking instructions
• Interactive cooking guidance 
• Timer and technique help

**2️⃣ ADD TO MEAL PLAN** 📋
• Schedule this meal for specific days
• Balance with other daily meals
• Track weekly nutrition goals

**3️⃣ GENERATE GROCERY LIST** 🛒
• Get shopping list for ingredients
• Organized by store sections
• Include quantities and alternatives

**4️⃣ TRACK THIS MEAL** 📊
• Log to your food diary now
• Track calories and nutrients
• Monitor daily goal progress

**5️⃣ SAVE TO FAVORITES** ⭐
• Save for quick reorder (this session)
• Easy access to meal details
• Remember for future planning

**6️⃣ FIND MORE MEALS** 🔍
• Browse similar calorie meals
• Try different dietary options
• Expand your meal options

**🎯 CALL TO ACTION**: Type **1-6** or the action name (e.g., "start cooking", "meal plan", "grocery list")!"""
        
        return action_text
    
    def _handle_final_actions(self, user_input):
        """Handle final action selection"""
        user_input_lower = user_input.lower()
        meal = self.selected_meal
        
        # Action 1: Start Cooking
        if '1' in user_input or 'cook' in user_input_lower:
            # Check if recipe exists for cooking guidance
            recipe_id = meal.get('recipe_id')  # Check if meal has associated recipe
            if recipe_id:
                return f"""🍳 **Starting Cooking Guidance**

Transitioning to interactive cooking for **{meal['name']}**...

📝 **Transferred Information:**
• Recipe: {meal['name']}
• Servings: Based on your {meal['calories']} calorie portion
• Ingredients: {len(meal.get('components', []))} components ready
• Nutrition target: {meal['calories']} calories

🎯 **CALL TO ACTION**: Say **"start cooking {meal['name']}"** or switch to cooking guidance!"""
            else:
                return f"""⚠️ **Cooking Instructions Not Available**

{meal['name']} doesn't have detailed cooking instructions yet.

**Alternative options:**
• **"meal plan"** - Add to your meal planning
• **"grocery list"** - Get ingredients for preparation
• **"find recipes"** - Browse recipes with cooking guidance

🎯 **CALL TO ACTION**: Choose an alternative action!"""
        
        # Action 2: Add to Meal Plan  
        elif '2' in user_input or 'meal plan' in user_input_lower or 'plan' in user_input_lower:
            meal_types = ', '.join(meal.get('meal_type', []))
            return f"""📋 **Adding to Meal Plan**

**{meal['name']}** ({meal['calories']} calories)

**Meal timing options**: {meal_types}

This will transition to **Meal Planning** where you can:
• Choose specific dates for this meal
• Balance with other daily meals  
• Plan complete daily nutrition

🎯 **CALL TO ACTION**: Say **"plan meals"** or **"meal planning"** to continue!"""
        
        # Action 3: Generate Grocery List
        elif '3' in user_input or 'grocery' in user_input_lower or 'shopping' in user_input_lower:
            components = meal.get('components', [])
            return f"""🛒 **Grocery List Generation**

**For**: {meal['name']}
**Ingredients needed**: {len(components)} items

**Shopping list includes:**
• All meal components with quantities
• Organized by food categories
• Alternative options when available

This will transition to **Grocery Assistance** for optimized shopping.

🎯 **CALL TO ACTION**: Say **"grocery list"** or **"shopping help"** to continue!"""
        
        # Action 4: Track This Meal
        elif '4' in user_input or 'track' in user_input_lower or 'log' in user_input_lower:
            nutrition = meal.get('nutrition', {})
            return f"""📊 **Meal Tracking**

Logging **{meal['name']}** to your food diary:

**Nutrition to track:**
• **Calories**: {meal['calories']}
• **Protein**: {nutrition.get('protein', 0)}g
• **Carbs**: {nutrition.get('carbs', 0)}g  
• **Fat**: {nutrition.get('fat', 0)}g
• **Fiber**: {nutrition.get('fiber', 0)}g

This will update your daily nutrition goals and tracking.

🎯 **CALL TO ACTION**: Say **"track food"** or **"log meal"** to continue!"""
        
        # Action 5: Save to Favorites
        elif '5' in user_input or 'favorite' in user_input_lower or 'save' in user_input_lower:
            # Save to session favorites
            from datetime import datetime
            favorites = self.session.get('favorite_meals', [])
            favorites.append({
                'meal': meal,
                'calories': meal['calories'],
                'saved_at': datetime.now().strftime('%Y-%m-%d %H:%M')
            })
            self.session.set('favorite_meals', favorites)
            
            return f"""⭐ **Meal Saved to Favorites**

**{meal['name']}** has been saved to your session favorites!

**Saved details:**
• **Calories**: {meal['calories']}
• **Components**: {len(meal.get('components', []))} ingredients  
• **Saved at**: {datetime.now().strftime('%Y-%m-%d %H:%M')}

**Access anytime this session:**
• Quick reorder for meal planning
• Easy reference for cooking
• Fast nutrition lookup

**Note**: Favorites reset when session ends (no persistent storage)

🎯 **CALL TO ACTION**: Type **"find more meals"** to continue exploring or choose another action!"""
        
        # Action 6: Find More Meals
        elif '6' in user_input or 'more' in user_input_lower or 'find' in user_input_lower:
            return f"""🔍 **Finding More Meals**

Searching for meals similar to **{meal['name']}** ({meal['calories']} calories)...

**Search criteria:**
• **Calorie range**: {self.calorie_range[0]}-{self.calorie_range[1]}
• **Meal types**: {', '.join(self.meal_types)}
• **Dietary prefs**: {', '.join(self.dietary_preferences) if self.dietary_preferences else 'None'}

**Options:**
• **"same criteria"** - Find meals with identical criteria
• **"similar calories"** - Expand calorie range ±100  
• **"different style"** - Try different dietary tags
• **"start fresh"** - Begin new calorie meal search

🎯 **CALL TO ACTION**: Choose how you'd like to find more meals!"""
        
        else:
            return """❌ **Invalid Action**

Please choose:
• **1** or **"cooking"** - Start cooking guidance  
• **2** or **"meal plan"** - Add to meal planning
• **3** or **"grocery list"** - Generate shopping list
• **4** or **"track"** - Log to food diary
• **5** or **"favorites"** - Save meal to session
• **6** or **"more meals"** - Find additional options

🎯 **CALL TO ACTION**: Choose a valid action number or name!"""

class TelegramNutritionBot:
    """Integrated Telegram bot with journey flows"""
    
    def __init__(self, token: str):
        self.token = token
        self.user_sessions: Dict[int, SimpleTelegramSession] = {}
        self.journeys = {}
        
        # Build application
        self.application = Application.builder().token(token).build()
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup Telegram bot handlers"""
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("reset", self.reset_command))
        self.application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))
        self.application.add_handler(CallbackQueryHandler(self.handle_callback))
    
    def _get_or_create_session(self, user_id: int) -> SimpleTelegramSession:
        """Get existing session or create new one"""
        if user_id not in self.user_sessions:
            self.user_sessions[user_id] = SimpleTelegramSession(user_id)
        return self.user_sessions[user_id]
    
    def _create_journey(self, journey_name: str, session: SimpleTelegramSession):
        """Create journey instance"""
        if journey_name == 'recipe_discovery':
            return SimpleRecipeDiscovery(session)
        elif journey_name == 'food_tracking':
            return SimpleFoodTracking(session)  
        elif journey_name == 'meal_planning':
            return SimpleMealPlanning(session)
        elif journey_name == 'grocery_assistance':
            return SimpleGroceryAssistance(session)
        elif journey_name == 'cooking_guidance':
            return SimpleCookingGuidance(session)
        elif journey_name == 'calorie_meals':
            return SimpleCalorieMeals(session)
        return None
    
    def _classify_intent(self, user_input: str) -> str:
        """Simple intent classification"""
        user_input = user_input.lower()
        
        # Recipe discovery patterns
        if any(word in user_input for word in ['recipe', 'dish', 'italian', 'asian', 'mexican', 'find recipe', 'show recipe']):
            return 'recipe_discovery'
        
        # Food tracking patterns  
        elif any(word in user_input for word in ['track', 'log', 'food', 'calorie', 'ate', 'breakfast', 'lunch', 'dinner', 'diary']):
            return 'food_tracking'
        
        # Meal planning patterns
        elif any(word in user_input for word in ['plan', 'meal plan', 'weekly', 'week']):
            return 'meal_planning'
        
        # Grocery patterns
        elif any(word in user_input for word in ['grocery', 'shopping', 'list', 'buy', 'store']):
            return 'grocery_assistance'
        
        # Cooking guidance patterns
        elif any(word in user_input for word in ['cooking', 'guide', 'help cook', 'cook this', 'how to cook']):
            return 'cooking_guidance'
        
        # Calorie-based meals patterns
        elif any(word in user_input for word in ['calorie meal', 'low calorie', 'high calorie', 'calories']):
            return 'calorie_meals'
        
        return None
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        session = self._get_or_create_session(user.id)
        
        welcome_message = f"👋 **Welcome {user.first_name}!**\n\n"
        welcome_message += "🤖 I'm your **AI Nutrition Assistant** with interactive journeys!\n\n"
        welcome_message += "**🎯 Available Features:**\n\n"
        welcome_message += "🔍 **Recipe Discovery** - Find personalized recipes\n"
        welcome_message += "📊 **Food Tracking** - Log and track nutrition\n" 
        welcome_message += "📋 **Meal Planning** - Create weekly meal plans\n"
        welcome_message += "🛒 **Grocery Lists** - Smart shopping assistance\n"
        welcome_message += "👩‍🍳 **Cooking Help** - Step-by-step guidance\n\n"
        welcome_message += "**💡 How to use:**\n"
        welcome_message += "Just type what you want naturally:\n"
        welcome_message += "• \"Find me Italian recipes\"\n" 
        welcome_message += "• \"Track my breakfast\"\n"
        welcome_message += "• \"Plan meals for this week\"\n\n"
        welcome_message += "**What would you like to do first?** 🍽️"
        
        keyboard = [
            [
                InlineKeyboardButton("🔍 Find Recipes", callback_data="recipe_discovery"),
                InlineKeyboardButton("📊 Track Food", callback_data="food_tracking")
            ],
            [
                InlineKeyboardButton("📋 Plan Meals", callback_data="meal_planning"),
                InlineKeyboardButton("🛒 Grocery List", callback_data="grocery_assistance")
            ],
            [
                InlineKeyboardButton("👩‍🍳 Cooking Help", callback_data="cooking_guidance"),
                InlineKeyboardButton("🥗 Calorie Meals", callback_data="calorie_meals")
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(welcome_message, parse_mode='Markdown', reply_markup=reply_markup)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """🆘 **Nutrition Assistant Help**

**🎯 Interactive Journeys:**
Each feature guides you step-by-step through a conversation.

**🔍 Recipe Discovery:**
• Type: "Find Italian recipes" 
• I'll ask about time, dietary needs, etc.
• Get personalized recipe recommendations

**📊 Food Tracking:**
• Type: "Log my breakfast"
• Choose food entry method
• Track calories and nutrition goals

**📋 Meal Planning:**
• Type: "Plan meals for the week"
• Set preferences and restrictions  
• Get complete weekly meal plans

**💬 Natural Language:**
Just talk to me naturally! I understand context and will guide you through each journey step by step.

**Commands:**
/start - Main menu
/help - This help message  
/reset - Reset current conversation

Ready to start? Tell me what you'd like to do! 🌟"""
        
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def reset_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /reset command"""
        user_id = update.effective_user.id
        if user_id in self.user_sessions:
            del self.user_sessions[user_id]
        
        await update.message.reply_text(
            "🔄 **Session Reset!**\n\n"
            "Your conversation has been cleared.\n"  
            "Tell me what you'd like to do! 😊"
        )
    
    async def handle_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle inline button clicks"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        session = self._get_or_create_session(user_id)
        
        journey_name = query.data
        session.start_journey(journey_name)
        session.journey_instance = self._create_journey(journey_name, session)
        
        if session.journey_instance:
            response = session.journey_instance.start_journey()
            await query.edit_message_text(response, parse_mode='Markdown')
        else:
            await query.edit_message_text("🤔 Feature coming soon! Use /start to try other features.")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle regular messages"""
        user_id = update.effective_user.id
        user_input = update.message.text
        session = self._get_or_create_session(user_id)
        
        try:
            # Check if user is in a journey
            if session.current_journey:
                # Reuse existing journey instance or create new one
                if session.journey_instance is None:
                    session.journey_instance = self._create_journey(session.current_journey, session)
                
                journey = session.journey_instance
                if journey:
                    response = journey.handle_input(user_input)
                else:
                    response = "🤔 Something went wrong. Use /reset to start fresh."
            else:
                # New conversation - classify intent
                intent = self._classify_intent(user_input)
                
                if intent:
                    session.start_journey(intent)
                    session.journey_instance = self._create_journey(intent, session)
                    if session.journey_instance:
                        response = session.journey_instance.start_journey(user_input)
                    else:
                        response = "🤔 That feature is coming soon! Try recipe discovery or food tracking."
                else:
                    response = """🤖 **I'm here to help with nutrition!**

I can assist you with:

🔍 **Recipe Discovery** - "Find me healthy recipes"
📊 **Food Tracking** - "Log my breakfast" 
📋 **Meal Planning** - "Plan meals for the week"
🛒 **Grocery Lists** - "Create shopping list"
👩‍🍳 **Cooking Help** - "Guide me through cooking"

What would you like to do? Just tell me naturally! 😊"""
            
            # Determine if we should use Markdown parsing
            # Skip Markdown for recipe lists and other potentially problematic content
            use_markdown = True
            if 'Available Recipes for Cooking' in response:
                use_markdown = False
            elif 'Error showing recipes' in response:
                use_markdown = False
            
            # Split long messages
            if len(response) > 4000:
                chunks = [response[i:i+4000] for i in range(0, len(response), 4000)]
                for chunk in chunks:
                    if use_markdown:
                        await update.message.reply_text(chunk, parse_mode='Markdown')
                    else:
                        await update.message.reply_text(chunk)
            else:
                if use_markdown:
                    await update.message.reply_text(response, parse_mode='Markdown')
                else:
                    await update.message.reply_text(response)
                
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            # Check if this is a Markdown parsing error
            if "can't parse entities" in str(e).lower() or "parse entities" in str(e).lower():
                # Try sending the response without Markdown
                try:
                    if len(response) > 4000:
                        chunks = [response[i:i+4000] for i in range(0, len(response), 4000)]
                        for chunk in chunks:
                            await update.message.reply_text(chunk)
                    else:
                        await update.message.reply_text(response)
                except:
                    # If that also fails, send generic error
                    await update.message.reply_text(
                        "⚠️ Sorry, I encountered a formatting error. Use /reset to start fresh or try rephrasing your request."
                    )
            else:
                await update.message.reply_text(
                    "⚠️ Sorry, I encountered an error. Use /reset to start fresh or try rephrasing your request."
                )
    
    def run(self):
        """Start the bot"""
        logger.info("Starting Integrated Telegram Nutrition Bot...")
        self.application.run_polling()

def main():
    """Main function"""
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    
    if not token:
        print("❌ TELEGRAM_BOT_TOKEN not found!")
        print("Please check your .env file")
        return
    
    print("🚀 Starting Integrated Telegram Nutrition Bot...")
    print("✅ This version includes full journey flows!")
    print("📱 Users can now have complete interactive conversations")
    print("-" * 50)
    
    bot = TelegramNutritionBot(token)
    bot.run()

if __name__ == '__main__':
    main()