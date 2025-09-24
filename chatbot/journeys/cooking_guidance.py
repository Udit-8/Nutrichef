"""
Cooking Guidance Journey
Interactive step-by-step cooking assistance with timer management and real-time guidance
"""

from typing import Dict, List, Any, Optional
from .base_journey import BaseJourney
from utils.cooking_utils import CookingSessionState, TimerManager, StepNavigator, ProgressTracker, ServingScaler
import re
from datetime import datetime

class CookingGuidanceJourney(BaseJourney):
    def __init__(self, data_loader, session_manager):
        super().__init__(session_manager)
        self.data_loader = data_loader
        self.journey_name = "cooking_guidance"
        
        # Journey-specific state
        self.recipe_id = None
        self.recipe_name = None
        self.cooking_session = None
        
        # Current step tracking
        self.current_step = None  # recipe_validation, serving_setup, equipment_check, prep_phase, cooking_steps, completion
        
        # Entry context (from other journeys)
        self.entry_recipe_id = None
        self.entry_recipe_name = None
    
    def start_journey(self) -> str:
        """Initialize the cooking guidance journey"""
        self.current_step = "recipe_validation"
        return self._step_recipe_validation()
    
    def process_input(self, user_input: str) -> str:
        """Process user input within the journey (required by BaseJourney)"""
        return self.process_user_input(user_input)
    
    def process_user_input(self, user_input: str) -> str:
        """Process user input based on current step"""
        if self.current_step == "recipe_validation":
            return self._handle_recipe_validation(user_input)
        elif self.current_step == "serving_setup":
            return self._handle_serving_setup(user_input)
        elif self.current_step == "equipment_check":
            return self._handle_equipment_check(user_input)
        elif self.current_step == "prep_phase":
            return self._handle_prep_phase(user_input)
        elif self.current_step == "cooking_steps":
            return self._handle_cooking_steps(user_input)
        elif self.current_step == "completion":
            return self._handle_completion(user_input)
        else:
            return "I'm not sure how to help with that. Let's continue with cooking!"
    
    def _step_recipe_validation(self) -> str:
        """Step 1: Recipe validation and loading"""
        # Check if recipe was provided from another journey
        context_recipe = self.session_manager.get_context('selected_recipe')
        if context_recipe:
            recipe_id = context_recipe.get('recipe_id')
            if recipe_id:
                return self._load_recipe_for_cooking(recipe_id)
        
        return """👨‍🍳 **COOKING GUIDANCE - Let's Start Cooking!**

What recipe would you like to cook today?

**Options:**
1. **Tell me the recipe name** (e.g., "Mediterranean Chicken Bowl")
2. **Search for recipes** (e.g., "chicken recipes", "quick dinners")
3. **Browse available recipes** - Show me all cookable recipes

What sounds good to you?"""
    
    def _handle_recipe_validation(self, user_input: str) -> str:
        """Handle recipe validation input"""
        user_input = user_input.lower().strip()
        
        if user_input in ['1', 'recipe name', 'tell me']:
            return "Perfect! What's the name of the recipe you want to cook?"
        elif user_input in ['2', 'search', 'search for recipes']:
            return "What type of recipe are you looking for? (e.g., 'chicken', 'vegetarian', 'quick meals')"
        elif user_input in ['3', 'browse', 'show all', 'available recipes']:
            return self._show_available_recipes()
        else:
            # Try to find recipe by name or search
            return self._search_and_load_recipe(user_input)
    
    def _show_available_recipes(self) -> str:
        """Show all recipes that have cooking instructions"""
        cooking_instructions = self.data_loader.get_cooking_instructions()
        
        if not cooking_instructions:
            return "I don't have any cooking instructions available. Please check your data files."
        
        recipe_text = "📚 **Available Recipes for Cooking:**\n\n"
        
        for i, instruction in enumerate(cooking_instructions, 1):
            recipe_name = instruction.get('recipe_name', 'Unknown Recipe')
            estimated_time = instruction.get('estimated_active_time', 'Unknown')
            total_steps = instruction.get('total_steps', 'Unknown')
            
            recipe_text += f"{i}. **{recipe_name}**\n"
            recipe_text += f"   ⏱️ Time: {estimated_time} minutes | 📋 Steps: {total_steps}\n\n"
        
        recipe_text += "**Select a recipe by number or tell me the recipe name!**"
        
        # Store recipes for selection
        self.session_manager.update_context('available_cooking_recipes', cooking_instructions)
        
        return recipe_text
    
    def _search_and_load_recipe(self, search_term: str) -> str:
        """Search for recipe and load it for cooking"""
        # Check if it's a number selection from available recipes
        if search_term.isdigit():
            available_recipes = self.session_manager.get_context('available_cooking_recipes')
            if available_recipes:
                recipe_index = int(search_term) - 1
                if 0 <= recipe_index < len(available_recipes):
                    recipe_instruction = available_recipes[recipe_index]
                    recipe_id = recipe_instruction.get('recipe_id')
                    if recipe_id:
                        return self._load_recipe_for_cooking(recipe_id)
        
        # Search by name
        matching_recipes = self.data_loader.search_recipes_for_cooking(search_term)
        
        if not matching_recipes:
            return f"I couldn't find any cookable recipes matching '{search_term}'. Try different keywords or say 'show all recipes'."
        
        if len(matching_recipes) == 1:
            # Exact match, load directly
            recipe_id = matching_recipes[0].get('recipe_id')
            return self._load_recipe_for_cooking(recipe_id)
        
        # Multiple matches, show options
        recipe_text = f"🔍 **Found {len(matching_recipes)} recipes matching '{search_term}':**\n\n"
        
        for i, recipe in enumerate(matching_recipes, 1):
            recipe_name = recipe.get('name', 'Unknown Recipe')
            estimated_time = self.data_loader.get_recipe_total_time(recipe.get('recipe_id', ''))
            
            recipe_text += f"{i}. **{recipe_name}** ({estimated_time} min)\n"
        
        recipe_text += "\n**Select by number or tell me which recipe you want to cook!**"
        
        # Store for selection
        self.session_manager.update_context('matching_cooking_recipes', matching_recipes)
        
        return recipe_text
    
    def _load_recipe_for_cooking(self, recipe_id: str) -> str:
        """Load recipe data and cooking instructions"""
        recipe_data = self.data_loader.get_recipe_cooking_data(recipe_id)
        
        if not recipe_data:
            return "I couldn't load the cooking instructions for that recipe. Please try another recipe."
        
        # Initialize cooking session
        self.recipe_id = recipe_id
        self.recipe_name = recipe_data['recipe']['name']
        self.cooking_session = CookingSessionState(recipe_data)
        
        # Move to serving setup
        self.current_step = "serving_setup"
        return self._step_serving_setup()
    
    def _step_serving_setup(self) -> str:
        """Step 2: Serving size setup and ingredient scaling"""
        if not self.cooking_session:
            return "Something went wrong. Let's start over."
        
        recipe = self.cooking_session.recipe
        original_servings = recipe.get('servings', 4)
        estimated_time = self.data_loader.get_recipe_total_time(self.recipe_id)
        
        return f"""🍽️ **SERVING SIZE SETUP - {self.recipe_name}**

This recipe serves **{original_servings} people** and takes about **{estimated_time} minutes** to cook.

How many servings would you like to make?

**Options:**
• Type a number (e.g., "2", "6", "8")
• Say "same" to keep the original servings ({original_servings})
• Say "double" or "half" for quick adjustments

How many people are you cooking for?"""
    
    def _handle_serving_setup(self, user_input: str) -> str:
        """Handle serving size input"""
        user_input = user_input.lower().strip()
        original_servings = self.cooking_session.recipe.get('servings', 4)
        
        try:
            if user_input in ['same', 'original', 'keep']:
                target_servings = original_servings
            elif user_input in ['double', '2x', 'twice']:
                target_servings = original_servings * 2
            elif user_input in ['half', '0.5x', 'halve']:
                target_servings = max(1, original_servings // 2)
            elif user_input in ['triple', '3x']:
                target_servings = original_servings * 3
            elif user_input.isdigit():
                target_servings = int(user_input)
                if target_servings <= 0 or target_servings > 20:
                    return "Please choose between 1 and 20 servings. How many people are you cooking for?"
            else:
                # Try to extract number from text
                numbers = re.findall(r'\d+', user_input)
                if numbers:
                    target_servings = int(numbers[0])
                    if target_servings <= 0 or target_servings > 20:
                        return "Please choose between 1 and 20 servings. How many people are you cooking for?"
                else:
                    return "I didn't understand that. Please tell me how many servings you want (e.g., '4', 'double', 'same')."
            
            # Set target servings
            self.cooking_session.serving_scaler.set_target_servings(target_servings)
            
            # Scale ingredients
            scaled_ingredients = self.data_loader.scale_recipe_ingredients(
                self.cooking_session.recipe, 
                self.cooking_session.serving_scaler.scale_factor
            )
            self.cooking_session.scaled_ingredients = scaled_ingredients
            
            # Move to equipment check
            self.current_step = "equipment_check"
            return self._step_equipment_check()
            
        except ValueError:
            return "Please enter a valid number of servings (e.g., '4', 'double', 'same')."
    
    def _step_equipment_check(self) -> str:
        """Step 3: Equipment and ingredient check"""
        scaling_info = self.cooking_session.serving_scaler.get_scaling_info()
        equipment_list = self.data_loader.get_recipe_equipment_list(self.recipe_id)
        scaled_ingredients = self.cooking_session.scaled_ingredients
        
        equipment_text = "🔧 **EQUIPMENT & INGREDIENTS CHECK**\n\n"
        
        if scaling_info['scaling_needed']:
            equipment_text += f"📊 **Scaled for {scaling_info['target_servings']} servings** "
            equipment_text += f"({'↗️ scaling up' if scaling_info['scaling_up'] else '↘️ scaling down'})\n\n"
        
        # Show equipment needed
        equipment_text += "**🛠️ Equipment Needed:**\n"
        if equipment_list:
            for equipment in equipment_list:
                equipment_text += f"  • {equipment.replace('_', ' ').title()}\n"
        else:
            equipment_text += "  • Basic cooking utensils\n"
        
        equipment_text += "\n**🥘 Ingredients Needed:**\n"
        
        # Show scaled ingredients
        for ingredient in scaled_ingredients:
            name = ingredient.get('name', 'Unknown ingredient')
            amount = ingredient.get('amount', 1)
            unit = ingredient.get('unit', '')
            
            if scaling_info['scaling_needed']:
                formatted_amount = self.cooking_session.serving_scaler.format_scaled_amount(
                    amount, unit
                )
            else:
                formatted_amount = f"{amount} {unit}".strip()
            
            equipment_text += f"  • {formatted_amount} {name}\n"
        
        equipment_text += f"\n**Ready to start cooking?**\n"
        equipment_text += f"Say 'yes' when you have everything ready, or 'missing' if you need to get something."
        
        return equipment_text
    
    def _handle_equipment_check(self, user_input: str) -> str:
        """Handle equipment check response"""
        user_input = user_input.lower().strip()
        
        if user_input in ['yes', 'ready', 'good', 'good to go', 'lets start', "let's start", 'start']:
            self.cooking_session.equipment_ready = True
            self.current_step = "prep_phase"
            return self._step_prep_phase()
        elif user_input in ['no', 'not ready', 'missing', 'need more time']:
            return """⏸️ **No Problem!**

Take your time to gather everything you need.

**What you can do:**
• **Get missing ingredients** - I can help create a grocery list
• **Find equipment substitutes** - Tell me what you're missing
• **Adjust the recipe** - We can modify ingredients if needed

Say **'ready'** when you have everything, or tell me what you need help with!"""
        elif 'missing' in user_input or 'dont have' in user_input or "don't have" in user_input:
            return """🤔 **Missing Something?**

No worries! Tell me what you're missing and I can help:

• **Missing ingredients** - I can suggest substitutes or help you get them
• **Missing equipment** - I can suggest alternatives or modifications
• **Need more time** - We can pause and resume later

What specifically do you need help with?"""
        else:
            return "I didn't catch that. Are you **ready to start cooking** (say 'yes') or do you need more time to prepare?"
    
    def _step_prep_phase(self) -> str:
        """Step 4: Prep phase management"""
        prep_steps = self.data_loader.get_prep_steps(self.recipe_id)
        
        if not prep_steps:
            # No prep steps, go straight to cooking
            self.cooking_session.prep_completed = True
            self.current_step = "cooking_steps"
            return self._step_cooking_steps()
        
        prep_text = f"🥄 **PREP PHASE - {self.recipe_name}**\n\n"
        prep_text += f"Let's prepare our ingredients first. You have **{len(prep_steps)} prep steps**:\n\n"
        
        for i, step in enumerate(prep_steps, 1):
            instruction = step.get('instruction', '')
            duration = step.get('duration_minutes', 0)
            tips = step.get('tips', '')
            
            prep_text += f"**Step {i}:** {instruction}\n"
            if duration > 0:
                prep_text += f"  ⏱️ Time: ~{duration} minutes\n"
            if tips:
                prep_text += f"  💡 Tip: {tips}\n"
            prep_text += "\n"
        
        prep_text += "**Work through these prep steps at your own pace.**\n"
        prep_text += "Say **'done with prep'** or **'ready to cook'** when you've finished all preparation!"
        
        # Track prep phase start
        self.cooking_session.progress_tracker.start_cooking_phase('prep')
        
        return prep_text
    
    def _handle_prep_phase(self, user_input: str) -> str:
        """Handle prep phase completion"""
        user_input = user_input.lower().strip()
        
        if user_input in ['done', 'done with prep', 'ready to cook', 'ready', 'finished prep', 'prep done']:
            self.cooking_session.prep_completed = True
            self.current_step = "cooking_steps"
            return self._step_cooking_steps()
        elif user_input in ['help', 'need help', 'stuck']:
            return """🆘 **Prep Help Available**

What do you need help with?

• **Specific technique** - Tell me what you're struggling with
• **Time management** - Need help organizing the prep steps
• **Substitutions** - Missing an ingredient or tool
• **Visual cues** - Not sure if something is done right

Describe what you need help with, and I'll guide you through it!"""
        elif 'how long' in user_input or 'time' in user_input:
            prep_steps = self.data_loader.get_prep_steps(self.recipe_id)
            total_prep_time = sum(step.get('duration_minutes', 0) for step in prep_steps)
            return f"The prep phase should take about **{total_prep_time} minutes** total. Take your time and say **'ready to cook'** when finished!"
        else:
            return "Take your time with the prep! Say **'done with prep'** when you're ready to start cooking, or ask for **'help'** if you need assistance."
    
    def _step_cooking_steps(self) -> str:
        """Step 5: Interactive cooking steps with timer management"""
        if not self.cooking_session:
            return "Something went wrong. Let's start over."
        
        # Start cooking phase
        self.cooking_session.progress_tracker.start_cooking_phase('cooking')
        
        # Get first cooking step
        current_step_data = self.cooking_session.get_current_step_data()
        progress = self.cooking_session.step_navigator.get_progress()
        
        if not current_step_data:
            return "I couldn't find the cooking steps. Let me start over."
        
        return self._display_cooking_step(current_step_data, progress)
    
    def _display_cooking_step(self, step_data: Dict[str, Any], progress: Dict[str, Any]) -> str:
        """Display a cooking step with all relevant information"""
        step_number = step_data.get('step_number', 1)
        instruction = step_data.get('instruction', '')
        duration = step_data.get('duration_minutes', 0)
        temperature = step_data.get('temperature')
        tips = step_data.get('tips', '')
        visual_cues = step_data.get('visual_cues', '')
        equipment = step_data.get('equipment', [])
        
        step_text = f"👨‍🍳 **STEP {step_number} of {progress['total_steps']}** ({progress['progress_percentage']:.0f}% complete)\n\n"
        
        # Main instruction
        step_text += f"**🔸 {instruction}**\n\n"
        
        # Duration and timer
        if duration > 0:
            step_text += f"⏱️ **Time:** {duration} minutes\n"
        
        # Temperature
        if temperature:
            step_text += f"🌡️ **Heat:** {temperature.replace('_', ' ').title()}\n"
        
        # Equipment for this step
        if equipment:
            step_text += f"🛠️ **Equipment:** {', '.join(eq.replace('_', ' ').title() for eq in equipment)}\n"
        
        step_text += "\n"
        
        # Tips
        if tips:
            step_text += f"💡 **Tip:** {tips}\n"
        
        # Visual cues
        if visual_cues:
            step_text += f"👀 **Look for:** {visual_cues}\n"
        
        step_text += "\n"
        
        # Timer management
        if duration > 0 and step_data.get('timer_needed', False):
            step_text += "**⏰ TIMER AVAILABLE** - Say 'start timer' to begin countdown\n"
        
        # Navigation options
        step_text += "**Navigation:**\n"
        step_text += "• **'next'** - Continue to next step\n"
        step_text += "• **'repeat'** - Show this step again\n"
        if not progress['is_first_step']:
            step_text += "• **'back'** - Go to previous step\n"
        step_text += "• **'pause'** - Pause cooking session\n"
        if duration > 0 and step_data.get('timer_needed', False):
            step_text += "• **'timer'** - Start/check timers\n"
        
        return step_text
    
    def _handle_cooking_steps(self, user_input: str) -> str:
        """Handle cooking step navigation and commands"""
        user_input = user_input.lower().strip()
        
        # Timer commands
        if user_input in ['timer', 'start timer', 'set timer']:
            return self._handle_timer_command()
        elif user_input in ['check timer', 'check timers', 'timer status']:
            return self._check_timer_status()
        
        # Navigation commands
        elif user_input in ['next', 'continue', 'done', 'finished']:
            return self._next_cooking_step()
        elif user_input in ['back', 'previous', 'prev']:
            return self._previous_cooking_step()
        elif user_input in ['repeat', 'again', 'show again']:
            return self._repeat_current_step()
        elif user_input in ['pause', 'stop', 'hold on']:
            return self._pause_cooking_session()
        
        # Help and problem-solving
        elif user_input in ['help', 'stuck', 'problem']:
            return self._provide_cooking_help()
        elif 'not working' in user_input or 'problem' in user_input or 'wrong' in user_input:
            return self._handle_cooking_problem(user_input)
        
        # Status checks
        elif user_input in ['status', 'progress', 'where am i']:
            return self._show_cooking_status()
        
        else:
            return "I didn't understand that command. Try:\n• **'next'** - Continue\n• **'timer'** - Set timer\n• **'repeat'** - Show step again\n• **'help'** - Get assistance"
    
    def _handle_timer_command(self) -> str:
        """Handle timer start command"""
        current_step_data = self.cooking_session.get_current_step_data()
        
        if not current_step_data:
            return "I couldn't find the current step information."
        
        duration = current_step_data.get('duration_minutes', 0)
        timer_needed = current_step_data.get('timer_needed', False)
        
        if not timer_needed or duration <= 0:
            return "This step doesn't need a timer. Say 'next' when you're ready to continue."
        
        # Start the timer
        step_number = current_step_data.get('step_number')
        description = f"Step {step_number}: {current_step_data.get('instruction', '')[:50]}..."
        
        timer_id = self.cooking_session.timer_manager.start_timer(
            duration, description, step_number
        )
        
        visual_cues = current_step_data.get('visual_cues', '')
        
        timer_text = f"⏰ **TIMER STARTED** - {duration} minutes\n\n"
        timer_text += f"Timer ID: {timer_id}\n"
        timer_text += f"For: Step {step_number}\n\n"
        
        if visual_cues:
            timer_text += f"**While you wait, look for:** {visual_cues}\n\n"
        
        timer_text += "I'll let you know when the timer is up! You can:\n"
        timer_text += "• Continue with other steps\n"
        timer_text += "• Say 'check timer' for status\n"
        timer_text += "• Say 'next' when ready to move on"
        
        return timer_text
    
    def _check_timer_status(self) -> str:
        """Check status of all timers"""
        active_timers, expired_timers = self.cooking_session.timer_manager.get_all_active_timers()
        
        status_text = "⏰ **TIMER STATUS**\n\n"
        
        if expired_timers:
            status_text += "🔔 **FINISHED TIMERS:**\n"
            for timer in expired_timers:
                status_text += f"• {timer['description']} - ✅ DONE!\n"
            status_text += "\n"
        
        if active_timers:
            status_text += "⏳ **ACTIVE TIMERS:**\n"
            for timer in active_timers:
                remaining = timer['remaining_minutes']
                status_text += f"• {timer['description']}\n"
                status_text += f"  Time left: {remaining:.1f} minutes\n"
            status_text += "\n"
        
        if not active_timers and not expired_timers:
            status_text += "No active timers.\n\n"
        
        status_text += "Say 'next' to continue cooking!"
        
        return status_text
    
    def _next_cooking_step(self) -> str:
        """Move to next cooking step"""
        next_step, is_last = self.cooking_session.step_navigator.next_step()
        
        if is_last:
            # Check if we completed all steps
            progress = self.cooking_session.step_navigator.get_progress()
            if progress['current_step'] > progress['total_steps']:
                # Cooking completed
                self.current_step = "completion"
                return self._step_completion()
        
        # Get next step data
        current_step_data = self.cooking_session.get_current_step_data()
        progress = self.cooking_session.step_navigator.get_progress()
        
        if current_step_data:
            return self._display_cooking_step(current_step_data, progress)
        else:
            # Something went wrong, move to completion
            self.current_step = "completion"
            return self._step_completion()
    
    def _previous_cooking_step(self) -> str:
        """Move to previous cooking step"""
        prev_step, is_first = self.cooking_session.step_navigator.previous_step()
        
        current_step_data = self.cooking_session.get_current_step_data()
        progress = self.cooking_session.step_navigator.get_progress()
        
        if current_step_data:
            return f"⬅️ **Going back to previous step**\n\n" + self._display_cooking_step(current_step_data, progress)
        else:
            return "I couldn't go back to the previous step. Let's continue forward."
    
    def _repeat_current_step(self) -> str:
        """Repeat current cooking step"""
        current_step_data = self.cooking_session.get_current_step_data()
        progress = self.cooking_session.step_navigator.get_progress()
        
        if current_step_data:
            return f"🔄 **Repeating current step**\n\n" + self._display_cooking_step(current_step_data, progress)
        else:
            return "I couldn't repeat the current step. Let's continue cooking."
    
    def _pause_cooking_session(self) -> str:
        """Pause the cooking session"""
        self.cooking_session.progress_tracker.pause_session()
        self.cooking_session.timer_manager.pause_all_timers()
        
        # Save session state
        session_state = self.cooking_session.save_session_state()
        self.session_manager.update_context('paused_cooking_session', session_state)
        
        return """⏸️ **COOKING SESSION PAUSED**

Your cooking progress has been saved!

**While paused:**
• All timers are paused
• Your progress is saved
• You can resume anytime

**To resume cooking:**
• Say **'resume cooking'** or **'continue cooking'**
• I'll restore your exact position and timers

**Other options:**
• **'stop cooking'** - End the session
• **'cooking status'** - Check your progress

Take your time! I'll be here when you're ready to continue."""
    
    def _provide_cooking_help(self) -> str:
        """Provide cooking help and troubleshooting"""
        current_step_data = self.cooking_session.get_current_step_data()
        
        help_text = "🆘 **COOKING HELP**\n\n"
        help_text += "What do you need help with?\n\n"
        help_text += "**Common Issues:**\n"
        help_text += "• **'not browning'** - Heat or timing adjustments\n"
        help_text += "• **'too salty'** - How to fix overseasoning\n"
        help_text += "• **'not thickening'** - Sauce consistency help\n"
        help_text += "• **'overcooked'** - Recovery strategies\n"
        help_text += "• **'timing issues'** - Adjust cooking schedule\n\n"
        
        if current_step_data:
            tips = current_step_data.get('tips', '')
            visual_cues = current_step_data.get('visual_cues', '')
            
            if tips:
                help_text += f"**💡 Current Step Tip:** {tips}\n\n"
            if visual_cues:
                help_text += f"**👀 What to Look For:** {visual_cues}\n\n"
        
        help_text += "Describe your specific problem and I'll help you solve it!"
        
        return help_text
    
    def _handle_cooking_problem(self, problem_description: str) -> str:
        """Handle specific cooking problems"""
        problem_lower = problem_description.lower()
        
        if 'not browning' in problem_lower or 'no color' in problem_lower:
            return """🔥 **BROWNING ISSUES**

**Solutions:**
• **Increase heat** - Try medium-high instead of medium
• **Don't overcrowd** - Give food space in the pan
• **Pat dry** - Remove excess moisture from proteins
• **Less oil** - Too much oil prevents browning
• **Wait longer** - Let it develop color before flipping

Try one of these adjustments and continue with the current step!"""
        
        elif 'too salty' in problem_lower or 'oversalted' in problem_lower:
            return """🧂 **TOO SALTY - RECOVERY OPTIONS**

**Quick fixes:**
• **Add acid** - Lemon juice or vinegar balances salt
• **Add dairy** - Yogurt, cream, or cheese helps
• **Add starch** - Rice, pasta, or bread absorbs salt
• **Add sweetness** - Small amount of sugar or honey
• **Dilute** - Add more base ingredients if possible

Apply one of these fixes and continue cooking!"""
        
        elif 'not thickening' in problem_lower or 'too thin' in problem_lower:
            return """🥄 **THICKENING SOLUTIONS**

**Options:**
• **Cook longer** - Let liquid reduce naturally
• **Cornstarch slurry** - Mix 1 tbsp cornstarch + 2 tbsp cold water
• **Flour roux** - Cook equal parts flour and butter, then add liquid
• **Reduce heat** - Simmer gently to avoid breaking sauce

Try one method and give it a few minutes to work!"""
        
        elif 'overcooked' in problem_lower or 'burnt' in problem_lower:
            return """🚨 **OVERCOOKED RECOVERY**

**Don't panic! Options:**
• **Lower heat** - Reduce to prevent further cooking
• **Add liquid** - Broth, wine, or water to deglaze
• **Scrape fond** - Brown bits often add flavor
• **Adjust seasoning** - May need extra salt/acid
• **Serve differently** - Turn into a different dish

Assess the damage and let's adapt the recipe if needed!"""
        
        else:
            return """🤔 **GENERAL COOKING HELP**

I understand you're having an issue. Here's what we can do:

**Tell me more specifically:**
• What step are you on?
• What's not working as expected?
• How does it look/smell/taste right now?

**Common solutions:**
• Adjust heat (higher/lower)
• Give it more time
• Add liquid or seasoning
• Change technique slightly

Describe what you're seeing and I'll give you specific guidance!"""
    
    def _show_cooking_status(self) -> str:
        """Show comprehensive cooking status"""
        if not self.cooking_session:
            return "No active cooking session."
        
        session_status = self.cooking_session.get_session_status()
        
        status_text = f"📊 **COOKING STATUS - {self.recipe_name}**\n\n"
        
        # Progress
        progress = session_status['progress']
        status_text += f"**Progress:** Step {progress['current_step']} of {progress['total_steps']} "
        status_text += f"({progress['progress_percentage']:.0f}% complete)\n\n"
        
        # Current step
        current_step = session_status['current_step']
        if current_step:
            status_text += f"**Current Step:** {current_step.get('instruction', '')[:100]}...\n\n"
        
        # Timers
        active_timers = session_status['active_timers']
        expired_timers = session_status['expired_timers']
        
        if active_timers:
            status_text += f"**Active Timers:** {len(active_timers)}\n"
            for timer in active_timers:
                status_text += f"  • {timer['remaining_minutes']:.1f} min remaining\n"
            status_text += "\n"
        
        if expired_timers:
            status_text += f"**⏰ {len(expired_timers)} timer(s) finished!**\n\n"
        
        # Time tracking
        session_summary = session_status['session_summary']
        elapsed = session_summary['elapsed_time_minutes']
        status_text += f"**Cooking Time:** {elapsed:.1f} minutes elapsed\n\n"
        
        status_text += "Say 'next' to continue or 'help' if you need assistance!"
        
        return status_text
    
    def _step_completion(self) -> str:
        """Step 6: Completion phase with rating and transitions"""
        if not self.cooking_session:
            return "Congratulations on completing your cooking!"
        
        self.cooking_session.progress_tracker.complete_session()
        session_summary = self.cooking_session.progress_tracker.get_session_summary()
        elapsed_time = session_summary['elapsed_time_minutes']
        
        completion_text = f"🎉 **CONGRATULATIONS! You've finished cooking {self.recipe_name}!**\n\n"
        
        completion_text += f"**📊 Cooking Summary:**\n"
        completion_text += f"• Total cooking time: {elapsed_time:.0f} minutes\n"
        completion_text += f"• Steps completed: {self.cooking_session.step_navigator.total_steps}\n"
        completion_text += f"• Servings made: {self.cooking_session.serving_scaler.target_servings}\n\n"
        
        # Modifications made
        if session_summary['modifications']:
            completion_text += f"**🔧 Modifications made:** {len(session_summary['modifications'])}\n\n"
        
        completion_text += "**🍽️ SERVING SUGGESTIONS:**\n"
        completion_text += "• Let it rest for a few minutes before serving\n"
        completion_text += "• Taste and adjust seasoning if needed\n"
        completion_text += "• Garnish as desired\n\n"
        
        completion_text += "**What would you like to do next?**\n"
        completion_text += "1. **Rate this recipe** - Share your experience\n"
        completion_text += "2. **Add cooking notes** - Record what you learned\n"
        completion_text += "3. **Share recipe** - Send to friends/family\n"
        completion_text += "4. **Cook something else** - Find another recipe\n"
        completion_text += "5. **Track this meal** - Log nutrition info\n"
        completion_text += "6. **Plan leftovers** - Organize remaining food\n\n"
        
        completion_text += "How did your cooking turn out?"
        
        return completion_text
    
    def _handle_completion(self, user_input: str) -> str:
        """Handle completion phase actions"""
        user_input = user_input.lower().strip()
        
        if user_input in ['1', 'rate', 'rate recipe', 'rating']:
            return self._handle_recipe_rating()
        elif user_input in ['2', 'notes', 'add notes', 'cooking notes']:
            return self._handle_cooking_notes()
        elif user_input in ['3', 'share', 'share recipe']:
            return self._handle_share_recipe()
        elif user_input in ['4', 'cook more', 'cook something else', 'another recipe']:
            return self._transition_to_recipe_discovery()
        elif user_input in ['5', 'track', 'track meal', 'log meal']:
            return self._transition_to_meal_tracking()
        elif user_input in ['6', 'leftovers', 'plan leftovers']:
            return self._transition_to_meal_planning()
        elif 'great' in user_input or 'good' in user_input or 'amazing' in user_input:
            return "🌟 Wonderful! I'm so glad it turned out well. Would you like to **rate the recipe** or **cook something else**?"
        elif 'okay' in user_input or 'fine' in user_input:
            return "👍 Not bad! Would you like to **add some notes** about what could be improved, or try **cooking something else**?"
        elif 'not good' in user_input or 'bad' in user_input or 'terrible' in user_input:
            return "😔 Sorry it didn't turn out as expected. Would you like to **add notes** about what went wrong so I can help you improve next time?"
        else:
            return "I'd love to hear more! Would you like to **rate the recipe**, **add notes**, or **cook something else**?"
    
    def _handle_recipe_rating(self) -> str:
        """Handle recipe rating"""
        return """⭐ **RATE THIS RECIPE**

How would you rate your cooking experience with {self.recipe_name}?

**Rating Scale:**
⭐ 1 - Didn't work out
⭐⭐ 2 - Needs improvement  
⭐⭐⭐ 3 - Good
⭐⭐⭐⭐ 4 - Great
⭐⭐⭐⭐⭐ 5 - Amazing!

Type a number (1-5) or tell me your rating!"""
    
    def _handle_cooking_notes(self) -> str:
        """Handle cooking notes collection"""
        return f"""📝 **ADD COOKING NOTES - {self.recipe_name}**

Share your thoughts about cooking this recipe:

**What to include:**
• What worked really well?
• What would you change next time?
• Any substitutions you made?
• Timing adjustments needed?
• Tips for future cooking?

Tell me your notes and I'll save them for future reference!"""
    
    def _handle_share_recipe(self) -> str:
        """Handle recipe sharing"""
        return f"""📤 **SHARE RECIPE - {self.recipe_name}**

Great idea to share your cooking success!

**Sharing options:**
• **Summary format** - Recipe + your cooking notes
• **Step-by-step** - Complete cooking guide  
• **Ingredients only** - Shopping list format
• **With modifications** - Include your personal changes

Your recipe sharing summary is ready to copy and send to friends and family!

Would you like to **cook something else** now?"""
    
    def _transition_to_recipe_discovery(self) -> str:
        """Transition to recipe discovery journey"""
        # Store cooking experience for personalization
        cooking_experience = {
            'completed_recipe': self.recipe_name,
            'cooking_success': True,
            'session_time': datetime.now()
        }
        self.session_manager.update_context('cooking_experience', cooking_experience)
        
        return """🔍 **FIND YOUR NEXT RECIPE**

You're on a cooking roll! Let's find something else delicious to make.

**Based on your success with {self.recipe_name}, you might like:**
• Similar cuisine styles
• Recipes with similar techniques
• Same difficulty level
• Complementary dishes

Transitioning you to recipe discovery... 

What type of recipe are you interested in cooking next?"""
    
    def _transition_to_meal_tracking(self) -> str:
        """Transition to meal tracking"""
        if not self.cooking_session:
            return "I'd need the recipe information to help with meal tracking."
        
        # Calculate nutrition for actual servings
        recipe = self.cooking_session.recipe
        servings_made = self.cooking_session.serving_scaler.target_servings
        
        nutrition_data = {
            'recipe_name': self.recipe_name,
            'servings_made': servings_made,
            'recipe_nutrition': recipe.get('nutrition', {}),
            'cooking_date': datetime.now().strftime('%Y-%m-%d')
        }
        
        self.session_manager.update_context('meal_to_track', nutrition_data)
        
        return f"""📊 **TRACK YOUR MEAL - {self.recipe_name}**

Perfect! Let's log this meal to your nutrition tracking.

**Meal Details:**
• Recipe: {self.recipe_name}
• Servings made: {servings_made}
• Cooked on: {datetime.now().strftime('%B %d, %Y')}

I can help you track:
• Calories consumed
• Portion sizes eaten
• Nutritional breakdown
• Add to daily food log

How much did you eat? (e.g., "1 serving", "half portion")"""
    
    def _transition_to_meal_planning(self) -> str:
        """Transition to meal planning for leftovers"""
        if not self.cooking_session:
            return "I'd need the cooking information to help plan leftovers."
        
        servings_made = self.cooking_session.serving_scaler.target_servings
        
        leftover_data = {
            'recipe_name': self.recipe_name,
            'total_servings_made': servings_made,
            'cooked_date': datetime.now().strftime('%Y-%m-%d'),
            'recipe_id': self.recipe_id
        }
        
        self.session_manager.update_context('leftovers_to_plan', leftover_data)
        
        return f"""📅 **PLAN YOUR LEFTOVERS - {self.recipe_name}**

Smart thinking! Let's organize your delicious leftovers.

**Leftover Details:**
• Recipe: {self.recipe_name}
• Total servings: {servings_made}
• Cooked today: {datetime.now().strftime('%B %d')}

**Storage & Planning:**
• How many servings will you eat today?
• When would you like to eat the leftovers?
• Proper storage recommendations
• Reheating instructions

Let's make sure nothing goes to waste! How many servings did you eat today?"""
    
    def get_completion_message(self) -> str:
        """Return completion message for the journey"""
        if self.recipe_name:
            return f"Congratulations on cooking {self.recipe_name}! 👨‍🍳"
        return "Cooking session completed successfully! 🍳"