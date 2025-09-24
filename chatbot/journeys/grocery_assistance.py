from typing import Dict, List, Any, Optional
from .base_journey import BaseJourney
from utils.grocery_utils import IngredientExtractor, ListConsolidator, StoreOrganizer, SubstitutionManager
import re

class GroceryAssistanceJourney(BaseJourney):
    def __init__(self, data_loader, session_manager):
        super().__init__(session_manager)
        self.data_loader = data_loader
        self.journey_name = "grocery_assistance"
        
        # Initialize utility classes
        self.ingredient_extractor = IngredientExtractor(data_loader)
        self.list_consolidator = ListConsolidator(data_loader)
        self.store_organizer = StoreOrganizer(data_loader)
        self.substitution_manager = SubstitutionManager(data_loader)
        
        # Journey-specific state
        self.list_source = None  # 'recipes', 'meal_plan', 'manual', 'multiple'
        self.selected_recipes = []
        self.selected_meal_plan = None
        self.manual_ingredients = []
        self.extracted_ingredients = []
        self.consolidated_ingredients = []
        self.organized_list = {}
        self.final_grocery_list = None
        
        # User preferences
        self.dietary_restrictions = []
        self.household_size = 2
        self.organization_preference = 'store_sections'  # 'store_sections', 'meal_type', 'recipe', 'alphabetical'
        
        # Current step tracking
        self.current_step = None
    
    def start_journey(self) -> str:
        """Initialize the grocery assistance journey"""
        self.current_step = "list_source"
        return self._step_list_source_determination()
    
    def process_input(self, user_input: str) -> str:
        """Process user input within the journey (required by BaseJourney)"""
        return self.process_user_input(user_input)
    
    def process_user_input(self, user_input: str) -> str:
        """Process user input based on current step"""
        if self.current_step == "list_source":
            return self._handle_list_source(user_input)
        elif self.current_step == "recipe_selection":
            return self._handle_recipe_selection(user_input)
        elif self.current_step == "meal_plan_selection":
            return self._handle_meal_plan_selection(user_input)
        elif self.current_step == "manual_input":
            return self._handle_manual_input(user_input)
        elif self.current_step == "consolidation_review":
            return self._handle_consolidation_review(user_input)
        elif self.current_step == "organization_preference":
            return self._handle_organization_preference(user_input)
        elif self.current_step == "final_actions":
            return self._handle_final_actions(user_input)
        else:
            return "I'm not sure how to help with that. Let's continue with your grocery list."
    
    def _step_list_source_determination(self) -> str:
        """Step 1: Determine how to create grocery list"""
        return """🛒 **GROCERY ASSISTANCE - Let's Create Your Shopping List!**

How would you like to create your grocery list?

1. **From Recipes** - Select recipes and I'll extract all ingredients
2. **From Meal Plan** - Use an existing meal plan to generate the list
3. **Manual Entry** - Add specific items you need
4. **Multiple Sources** - Combine recipes, meal plans, and manual items

What works best for you today?"""
    
    def _handle_list_source(self, user_input: str) -> str:
        """Handle list source selection"""
        user_input = user_input.lower().strip()
        
        if user_input in ['1', 'recipes', 'from recipes', 'recipe']:
            self.list_source = 'recipes'
            self.current_step = "recipe_selection"
            return self._step_recipe_selection()
        elif user_input in ['2', 'meal plan', 'from meal plan', 'meal plans']:
            self.list_source = 'meal_plan'
            self.current_step = "meal_plan_selection"
            return self._step_meal_plan_selection()
        elif user_input in ['3', 'manual', 'manual entry', 'add items', 'specific items']:
            self.list_source = 'manual'
            self.current_step = "manual_input"
            return self._step_manual_input()
        elif user_input in ['4', 'multiple', 'multiple sources', 'combine', 'mix']:
            self.list_source = 'multiple'
            return self._step_multiple_sources()
        else:
            return "Please choose 1-4 or tell me how you'd like to create your grocery list."
    
    def _step_recipe_selection(self) -> str:
        """Step for selecting recipes"""
        return """📖 **RECIPE-BASED GROCERY LIST**

How would you like to select recipes?

1. **Search by Name** - "Find chicken recipes" or "Mediterranean dishes"
2. **Browse by Cuisine** - Italian, Mexican, Asian, etc.
3. **Specific Recipe** - If you know exactly which recipe you want
4. **Recent Favorites** - Choose from recipes you've used before

You can also tell me exactly what you're looking for, like:
• "I want to make chicken stir fry"
• "Show me vegetarian dinner recipes"
• "Find recipes with salmon"

What type of recipes are you interested in?"""
    
    def _handle_recipe_selection(self, user_input: str) -> str:
        """Handle recipe selection process"""
        user_input_lower = user_input.lower().strip()
        
        if user_input_lower in ['1', 'search', 'search by name']:
            return "Great! What type of recipes are you looking for? (e.g., 'chicken recipes', 'pasta dishes', 'healthy breakfast')"
        elif user_input_lower in ['2', 'browse', 'browse by cuisine', 'cuisine']:
            return self._show_available_cuisines()
        elif user_input_lower in ['3', 'specific', 'specific recipe']:
            return "Perfect! What's the name of the recipe you want to use?"
        elif user_input_lower in ['4', 'favorites', 'recent']:
            return "I don't have access to your recent recipes yet. Would you like to search for recipes or tell me a specific recipe name?"
        else:
            # Try to search for recipes based on user input
            return self._search_and_display_recipes(user_input)
    
    def _show_available_cuisines(self) -> str:
        """Show available cuisine types"""
        cuisines = self.data_loader.get_cuisine_types()
        if not cuisines:
            return "I don't have cuisine information available. Please tell me what type of recipes you're looking for."
        
        cuisine_text = "🌍 **Available Cuisines:**\n\n"
        for i, cuisine in enumerate(cuisines, 1):
            cuisine_text += f"{i}. {cuisine.title()}\n"
        
        cuisine_text += "\nChoose a number or tell me which cuisine interests you!"
        return cuisine_text
    
    def _search_and_display_recipes(self, search_term: str) -> str:
        """Search and display matching recipes"""
        # Search recipes by name
        recipes = self.data_loader.search_recipes_by_name(search_term)
        
        if not recipes:
            # Try cuisine search
            recipes = self.data_loader.filter_recipes_by_cuisine(search_term)
        
        if not recipes:
            return f"I couldn't find recipes matching '{search_term}'. Try different keywords like 'chicken', 'vegetarian', or 'Italian'."
        
        # Display found recipes
        recipe_text = f"🔍 **Found {len(recipes)} recipes for '{search_term}':**\n\n"
        
        for i, recipe in enumerate(recipes[:10], 1):  # Show max 10 recipes
            recipe_text += f"{i}. **{recipe['name']}** ({recipe.get('total_time', 'Unknown')} min)\n"
            recipe_text += f"   Cuisine: {recipe.get('cuisine', 'Not specified')}\n"
            recipe_text += f"   Servings: {recipe.get('servings', 'Not specified')}\n\n"
        
        if len(recipes) > 10:
            recipe_text += f"... and {len(recipes) - 10} more recipes\n\n"
        
        recipe_text += "**Select recipes by number** (e.g., '1, 3, 5') or tell me **'show more'** for additional options."
        
        # Store recipes for selection
        self.session_manager.update_context('available_recipes', recipes[:10])
        
        return recipe_text
    
    def _step_meal_plan_selection(self) -> str:
        """Step for selecting meal plan"""
        return """📅 **MEAL PLAN-BASED GROCERY LIST**

Which meal plan should I create a grocery list for?

1. **Current Week Plan** - Use your active meal plan
2. **Specific Days** - Choose specific days (e.g., "Monday to Wednesday")
3. **Date Range** - Select a custom date range
4. **Recent Meal Plan** - Use a recently created meal plan

If you have a meal plan ready, I can extract all the ingredients you'll need for shopping!

Which option works for you?"""
    
    def _handle_meal_plan_selection(self, user_input: str) -> str:
        """Handle meal plan selection"""
        user_input_lower = user_input.lower().strip()
        
        # Check if user has a completed meal plan in session
        completed_plan = self.session_manager.get_context('completed_meal_plan')
        
        if user_input_lower in ['1', 'current', 'current week', 'active']:
            if completed_plan and 'plan' in completed_plan:
                self.selected_meal_plan = completed_plan['plan']
                return self._process_meal_plan_ingredients()
            else:
                return "I don't see an active meal plan. Would you like to create one first, or try a different option?"
        
        elif user_input_lower in ['2', 'specific days', 'specific']:
            if completed_plan and 'plan' in completed_plan:
                return "Which days would you like ingredients for? (e.g., 'Monday and Tuesday' or 'Day 1, Day 2')"
            else:
                return "I don't have a meal plan available. Would you like to create one first?"
        
        elif user_input_lower in ['3', 'date range', 'custom']:
            return "I'll use your most recent meal plan. What date range interests you?"
        
        elif user_input_lower in ['4', 'recent', 'recent plan']:
            if completed_plan and 'plan' in completed_plan:
                self.selected_meal_plan = completed_plan['plan']
                return self._process_meal_plan_ingredients()
            else:
                return "I don't have any recent meal plans stored. Would you like to create a meal plan first or try manual entry?"
        
        else:
            # Try to parse specific days mentioned
            if completed_plan and 'plan' in completed_plan:
                selected_days = self._parse_day_selection(user_input, completed_plan['plan'])
                if selected_days:
                    self.selected_meal_plan = selected_days
                    return self._process_meal_plan_ingredients()
            
            return "I didn't understand your selection. Please choose 1-4 or tell me which days you want ingredients for."
    
    def _parse_day_selection(self, user_input: str, meal_plan: Dict) -> Optional[Dict]:
        """Parse which days user wants from meal plan"""
        user_input_lower = user_input.lower()
        selected_plan = {}
        
        # Try to match day names or numbers
        for day_key in meal_plan.keys():
            if day_key.lower() in user_input_lower:
                selected_plan[day_key] = meal_plan[day_key]
            elif any(str(i) in user_input for i in range(1, 8) if f"day {i}" == day_key.lower()):
                selected_plan[day_key] = meal_plan[day_key]
        
        return selected_plan if selected_plan else None
    
    def _process_meal_plan_ingredients(self) -> str:
        """Process ingredients from selected meal plan"""
        if not self.selected_meal_plan:
            return "No meal plan selected. Let's try a different approach."
        
        # Extract ingredients from meal plan
        self.extracted_ingredients = self.ingredient_extractor.extract_from_meal_plan(
            self.selected_meal_plan, 
            servings_multiplier=self.household_size / 2.0  # Assuming meal plan is for 2 people
        )
        
        if not self.extracted_ingredients:
            return "I couldn't extract ingredients from the meal plan. Would you like to try manual entry instead?"
        
        # Move to consolidation
        self.current_step = "consolidation_review"
        return self._perform_consolidation()
    
    def _step_manual_input(self) -> str:
        """Step for manual ingredient entry"""
        return """✍️ **MANUAL INGREDIENT ENTRY**

You can add ingredients in several ways:

**Option 1: List Format**
Type ingredients separated by commas or new lines:
*Example: "2 lbs chicken breast, 1 cup rice, spinach, 3 apples"*

**Option 2: One at a Time**
I'll ask you for each ingredient individually

**Option 3: Categories**
I'll guide you through food categories (produce, meat, dairy, etc.)

How would you like to add your ingredients?"""
    
    def _handle_manual_input(self, user_input: str) -> str:
        """Handle manual ingredient input"""
        user_input_lower = user_input.lower().strip()
        
        if user_input_lower in ['option 1', '1', 'list', 'list format']:
            return """📝 **List Format Entry**

Please type your ingredients separated by commas or new lines.

Examples:
• "2 lbs chicken, 1 cup rice, bunch of spinach"
• "eggs, milk, bread, 3 tomatoes"
• "olive oil, garlic, 2 onions, pasta"

What ingredients do you need?"""
        
        elif user_input_lower in ['option 2', '2', 'one at a time', 'individual']:
            return self._start_individual_entry()
        
        elif user_input_lower in ['option 3', '3', 'categories', 'guided']:
            return self._start_category_guided_entry()
        
        else:
            # Try to parse as ingredient list
            self.manual_ingredients = self.ingredient_extractor.extract_from_manual_input(user_input)
            
            if not self.manual_ingredients:
                return "I couldn't parse those ingredients. Try a format like '2 lbs chicken, 1 cup rice, spinach'. What ingredients do you need?"
            
            # Move to consolidation
            self.extracted_ingredients = self.manual_ingredients
            self.current_step = "consolidation_review"
            return self._perform_consolidation()
    
    def _start_individual_entry(self) -> str:
        """Start individual ingredient entry process"""
        self.session_manager.update_context('individual_entry_mode', True)
        return """🔢 **Individual Entry Mode**

I'll help you add ingredients one by one.

Tell me the first ingredient you need (with quantity if known):
*Example: "2 pounds chicken breast" or just "chicken"*

Type 'done' when you're finished adding ingredients."""
    
    def _start_category_guided_entry(self) -> str:
        """Start category-guided entry process"""
        return """🛒 **Category-Guided Entry**

Let's go through each store section:

**🥬 PRODUCE & FRESH VEGETABLES**
What fruits and vegetables do you need?
*Example: "3 apples, spinach, 2 onions, carrots"*

(Type 'skip' to move to the next category, or 'none' if you don't need anything from this section)"""
    
    def _step_multiple_sources(self) -> str:
        """Handle multiple sources combination"""
        return """🔄 **MULTIPLE SOURCES**

Great choice! I can combine ingredients from different sources.

Let's start with what you have:

1. **Do you have recipes** you want ingredients for? (yes/no)
2. **Do you have a meal plan** to use? (yes/no)  
3. **Do you have additional items** to add manually? (yes/no)

Or simply tell me: "I want recipes for chicken dinner plus some snacks" and I'll help you with both!

What combination works for you?"""
    
    def _perform_consolidation(self) -> str:
        """Consolidate extracted ingredients"""
        if not self.extracted_ingredients:
            return "No ingredients found to consolidate."
        
        print(f"🔄 Consolidating {len(self.extracted_ingredients)} ingredients...")
        
        # Consolidate the ingredients
        self.consolidated_ingredients = self.list_consolidator.consolidate_ingredients(
            self.extracted_ingredients
        )
        
        # Display consolidation results
        result_text = f"✅ **INGREDIENT CONSOLIDATION COMPLETE**\n\n"
        result_text += f"Found **{len(self.extracted_ingredients)}** ingredients from your sources\n"
        result_text += f"Consolidated to **{len(self.consolidated_ingredients)}** unique items\n\n"
        
        # Show preview of consolidated list
        result_text += "📋 **Preview of your ingredients:**\n"
        for ingredient in self.consolidated_ingredients[:10]:  # Show first 10
            display_name = ingredient.get('display_name', ingredient.get('name', 'Unknown'))
            amount = ingredient.get('amount', 1)
            unit = ingredient.get('unit', '')
            result_text += f"• {display_name} - {amount} {unit}\n"
        
        if len(self.consolidated_ingredients) > 10:
            result_text += f"... and {len(self.consolidated_ingredients) - 10} more items\n"
        
        result_text += "\n**How would you like your grocery list organized?**"
        
        self.current_step = "organization_preference"
        return result_text + "\n\n" + self._step_organization_preference()
    
    def _step_organization_preference(self) -> str:
        """Step for choosing list organization"""
        return """📊 **LIST ORGANIZATION**

How would you like your grocery list organized?

1. **By Store Sections** - Produce, Meat, Dairy, etc. (optimal shopping route)
2. **By Meal Type** - Breakfast ingredients, lunch ingredients, etc.
3. **By Recipe** - Keep ingredients for each recipe together
4. **Alphabetical** - Simple A-Z sorting

**Recommended**: Store sections for the most efficient shopping experience!

What's your preference?"""
    
    def _handle_organization_preference(self, user_input: str) -> str:
        """Handle organization preference selection"""
        user_input_lower = user_input.lower().strip()
        
        if user_input_lower in ['1', 'store sections', 'store', 'sections']:
            self.organization_preference = 'store_sections'
        elif user_input_lower in ['2', 'meal type', 'meals', 'meal']:
            self.organization_preference = 'meal_type'
        elif user_input_lower in ['3', 'recipe', 'recipes', 'by recipe']:
            self.organization_preference = 'recipe'
        elif user_input_lower in ['4', 'alphabetical', 'alphabetic', 'a-z']:
            self.organization_preference = 'alphabetical'
        else:
            return "Please choose 1-4 or tell me your organization preference."
        
        # Organize the list
        self.organized_list = self._organize_grocery_list()
        
        # Generate final list
        self.current_step = "final_actions"
        return self._generate_final_grocery_list()
    
    def _organize_grocery_list(self) -> Dict[str, Any]:
        """Organize grocery list based on user preference"""
        if self.organization_preference == 'store_sections':
            return self.store_organizer.organize_by_store_sections(self.consolidated_ingredients)
        elif self.organization_preference == 'alphabetical':
            return self._organize_alphabetically()
        elif self.organization_preference == 'meal_type':
            return self._organize_by_meal_type()
        elif self.organization_preference == 'recipe':
            return self._organize_by_recipe()
        else:
            # Default to store sections
            return self.store_organizer.organize_by_store_sections(self.consolidated_ingredients)
    
    def _organize_alphabetically(self) -> Dict[str, List[Dict[str, Any]]]:
        """Organize ingredients alphabetically"""
        sorted_ingredients = sorted(
            self.consolidated_ingredients,
            key=lambda x: x.get('display_name', x.get('name', '')).lower()
        )
        
        return {'All Ingredients': sorted_ingredients}
    
    def _organize_by_meal_type(self) -> Dict[str, List[Dict[str, Any]]]:
        """Organize ingredients by meal type"""
        organized = {}
        
        for ingredient in self.consolidated_ingredients:
            sources = ingredient.get('sources', ['unknown'])
            
            # Try to determine meal type from sources
            meal_types = set()
            for source in sources:
                if ':' in source:
                    parts = source.split(':')
                    if len(parts) >= 3 and 'meal_plan' in parts[0]:
                        meal_type = parts[2]  # day:meal_type
                        meal_types.add(meal_type.title())
                    elif 'recipe' in parts[0]:
                        meal_types.add('Recipe Ingredients')
                else:
                    meal_types.add('Other Items')
            
            # Add to appropriate meal type(s)
            for meal_type in meal_types:
                if meal_type not in organized:
                    organized[meal_type] = []
                organized[meal_type].append(ingredient)
        
        return organized
    
    def _organize_by_recipe(self) -> Dict[str, List[Dict[str, Any]]]:
        """Organize ingredients by recipe"""
        organized = {}
        
        for ingredient in self.consolidated_ingredients:
            sources = ingredient.get('sources', ['unknown'])
            
            # Group by recipe/source
            for source in sources:
                if ':' in source:
                    source_type, source_name = source.split(':', 1)
                    if source_type == 'recipe':
                        recipe_name = source_name
                    elif source_type == 'meal_plan':
                        recipe_name = f"Meal Plan ({source_name})"
                    else:
                        recipe_name = source_name.title()
                else:
                    recipe_name = source.title()
                
                if recipe_name not in organized:
                    organized[recipe_name] = []
                organized[recipe_name].append(ingredient)
        
        return organized
    
    def _generate_final_grocery_list(self) -> str:
        """Generate the final formatted grocery list"""
        if not self.organized_list:
            return "No grocery list to display."
        
        grocery_list_text = "🎉 **YOUR GROCERY LIST IS READY!**\n\n"
        grocery_list_text += f"📊 **Summary:** {len(self.consolidated_ingredients)} items organized by {self.organization_preference.replace('_', ' ')}\n\n"
        
        # Format the organized list
        grocery_list_text += self._format_organized_list()
        
        # Add shopping tips
        grocery_list_text += "\n💡 **SHOPPING TIPS:**\n"
        if self.organization_preference == 'store_sections':
            grocery_list_text += "• Follow the list order for optimal shopping route\n"
            grocery_list_text += "• Start with produce, end with frozen/refrigerated items\n"
        grocery_list_text += "• Check expiration dates\n"
        grocery_list_text += "• Bring reusable bags\n\n"
        
        grocery_list_text += "**What would you like to do with your grocery list?**"
        
        # Store the final list
        self.final_grocery_list = {
            'organized_list': self.organized_list,
            'total_items': len(self.consolidated_ingredients),
            'organization_type': self.organization_preference,
            'generated_date': self._get_current_date()
        }
        
        return grocery_list_text + "\n\n" + self._step_final_actions()
    
    def _format_organized_list(self) -> str:
        """Format the organized grocery list for display"""
        formatted_text = ""
        
        for section_name, ingredients in self.organized_list.items():
            # Get section icon if available
            section_icon = "📦"  # default
            if self.organization_preference == 'store_sections' and ingredients:
                first_ingredient = ingredients[0]
                if 'store_section' in first_ingredient:
                    section_icon = first_ingredient['store_section'].get('icon', '📦')
            
            formatted_text += f"{section_icon} **{section_name.upper()}**\n"
            
            for ingredient in ingredients:
                display_name = ingredient.get('display_name', ingredient.get('name', 'Unknown'))
                amount = ingredient.get('amount', 1)
                unit = ingredient.get('unit', '')
                
                # Format amount nicely
                if amount == int(amount):
                    amount_str = str(int(amount))
                else:
                    amount_str = f"{amount:.1f}"
                
                formatted_text += f"  ☐ {display_name}"
                if amount_str != "1" or unit:
                    formatted_text += f" - {amount_str} {unit}".rstrip()
                formatted_text += "\n"
            
            formatted_text += "\n"
        
        return formatted_text
    
    def _step_final_actions(self) -> str:
        """Step for final actions with grocery list"""
        return """🎯 **GROCERY LIST ACTIONS**

What would you like to do next?

1. **Export List** - Save as text, PDF, or email format
2. **Share with Others** - Send to family/roommates
3. **Save as Template** - Reuse this list in the future
4. **Start Shopping Mode** - Interactive shopping assistant
5. **Edit List** - Add, remove, or modify items
6. **Show Substitutions** - See alternatives for ingredients

Choose your next action!"""
    
    def _handle_final_actions(self, user_input: str) -> str:
        """Handle final action selection"""
        user_input_lower = user_input.lower().strip()
        
        if user_input_lower in ['1', 'export', 'save', 'export list']:
            return self._handle_export_list()
        elif user_input_lower in ['2', 'share', 'send', 'share list']:
            return self._handle_share_list()
        elif user_input_lower in ['3', 'template', 'save template', 'save as template']:
            return self._handle_save_template()
        elif user_input_lower in ['4', 'shopping', 'shopping mode', 'start shopping']:
            return self._handle_start_shopping_mode()
        elif user_input_lower in ['5', 'edit', 'modify', 'edit list']:
            return self._handle_edit_list()
        elif user_input_lower in ['6', 'substitutions', 'alternatives', 'substitutes']:
            return self._handle_show_substitutions()
        else:
            return "Please choose 1-6 or tell me what you'd like to do with your grocery list."
    
    def _handle_export_list(self) -> str:
        """Handle grocery list export"""
        if not self.final_grocery_list:
            return "No grocery list available to export."
        
        export_text = "📧 **EXPORT OPTIONS**\n\n"
        export_text += "Your grocery list is ready for export in multiple formats:\n\n"
        
        export_text += "📱 **TEXT FORMAT** (Copy & Paste Ready):\n"
        export_text += "Perfect for messaging apps, notes, or quick reference\n\n"
        
        export_text += "🖨️ **PRINT-FRIENDLY FORMAT**:\n"
        export_text += "Black and white optimized with checkboxes for easy marking\n\n"
        
        export_text += "📧 **EMAIL FORMAT**:\n"
        export_text += "Professional format with shopping tips and organization\n\n"
        
        export_text += "**Your grocery list is already formatted above** - you can copy it directly!\n\n"
        
        export_text += "Would you like me to help with anything else for your shopping trip?"
        
        return export_text
    
    def _handle_share_list(self) -> str:
        """Handle sharing grocery list"""
        return """👨‍👩‍👧‍👦 **SHARE GROCERY LIST**

Your list is ready to share! Here are your options:

**📲 QUICK SHARING:**
• Copy the list above and paste it into any messaging app
• Send via text message, email, or social media
• Share with family members or roommates

**🏠 HOUSEHOLD COORDINATION:**
• Split shopping assignments by store sections
• Avoid duplicate purchases by sharing the complete list
• Let others add items they need

**💡 SHARING TIPS:**
• Include the shopping tips for best results
• Mention any dietary restrictions or preferences
• Share before shopping to get input from others

Your formatted list above is ready to copy and share anywhere!

Need help with anything else for your grocery shopping?"""
    
    def _handle_save_template(self) -> str:
        """Handle saving list as template"""
        if not self.final_grocery_list:
            return "No grocery list available to save as template."
        
        # Store template in session (in real app, this would go to user profile/database)
        template_data = {
            'ingredients': self.consolidated_ingredients,
            'organization_preference': self.organization_preference,
            'template_name': f"Grocery Template {self._get_current_date()}",
            'created_date': self._get_current_date()
        }
        
        self.session_manager.update_context('saved_grocery_template', template_data)
        
        return """💾 **TEMPLATE SAVED SUCCESSFULLY!**

Your grocery list has been saved as a reusable template.

**Template Features:**
• **Reuse anytime** - "Use my grocery template" 
• **Modify as needed** - Add or remove items for future trips
• **Same organization** - Maintains your preferred list structure
• **Smart updates** - Learns from your shopping patterns

**Future Usage:**
Next time you need groceries, just say:
• "Use my saved template"
• "Load my grocery template"  
• "Create list from template"

Your template includes all {len(self.consolidated_ingredients)} ingredients and is ready for future shopping trips!

Is there anything else I can help with for your grocery shopping?"""
    
    def _handle_start_shopping_mode(self) -> str:
        """Handle interactive shopping mode"""
        if not self.final_grocery_list:
            return "No grocery list available for shopping mode."
        
        return """🛒 **INTERACTIVE SHOPPING MODE**

Ready to shop! I'll guide you through your list:

**✅ SHOPPING CHECKLIST:**
• I'll track your progress as you shop
• Check off items as you find them
• Get help if items are unavailable

**🔄 SUBSTITUTION SUPPORT:**
• Can't find an item? I'll suggest alternatives
• Get dietary-compatible substitutions
• Update your list with changes

**📍 SHOPPING NAVIGATION:**
• Follow the optimized store route
• Get reminders for each section
• Track what's left to find

**Ready to start?** 

Here's your first section:
""" + self._get_first_shopping_section()
    
    def _get_first_shopping_section(self) -> str:
        """Get the first shopping section to start with"""
        if not self.organized_list:
            return "No organized list available."
        
        # Get first section
        first_section_name = next(iter(self.organized_list.keys()))
        first_section_items = self.organized_list[first_section_name]
        
        section_text = f"\n🥬 **{first_section_name.upper()}**\n"
        
        for i, ingredient in enumerate(first_section_items[:5], 1):  # Show first 5 items
            display_name = ingredient.get('display_name', ingredient.get('name', 'Unknown'))
            amount = ingredient.get('amount', 1)
            unit = ingredient.get('unit', '')
            section_text += f"☐ {display_name} - {amount} {unit}\n"
        
        if len(first_section_items) > 5:
            section_text += f"... and {len(first_section_items) - 5} more items in this section\n"
        
        section_text += "\n**Found everything in this section?** Type 'next' to continue, or tell me if any items were unavailable!"
        
        return section_text
    
    def _handle_edit_list(self) -> str:
        """Handle editing the grocery list"""
        return """✏️ **EDIT GROCERY LIST**

You can modify your list in several ways:

**➕ ADD ITEMS:**
• "Add 2 lbs ground beef"
• "Include pasta sauce"
• "I also need bread"

**➖ REMOVE ITEMS:**
• "Remove spinach"
• "Delete the chicken"
• "I don't need tomatoes"

**🔄 MODIFY QUANTITIES:**
• "Change milk to 2 gallons"
• "Make it 3 pounds of chicken"
• "Update eggs to 2 dozen"

**📝 BULK CHANGES:**
• "Add all breakfast items: eggs, milk, bread, fruit"
• "Remove all vegetables"

What changes would you like to make to your grocery list?"""
    
    def _handle_show_substitutions(self) -> str:
        """Handle showing ingredient substitutions"""
        if not self.consolidated_ingredients:
            return "No ingredients available to show substitutions for."
        
        subs_text = "🔄 **INGREDIENT SUBSTITUTIONS**\n\n"
        subs_text += "Here are alternatives for key ingredients in your list:\n\n"
        
        # Show substitutions for first few ingredients that have them
        shown_count = 0
        for ingredient in self.consolidated_ingredients:
            if shown_count >= 5:  # Limit to first 5
                break
            
            substitutions = self.substitution_manager.get_substitutions_for_ingredient(
                ingredient, self.dietary_restrictions
            )
            
            if substitutions:
                display_name = ingredient.get('display_name', ingredient.get('name', 'Unknown'))
                subs_text += f"**{display_name}** alternatives:\n"
                
                for i, sub in enumerate(substitutions[:3], 1):  # Show top 3 substitutions
                    sub_name = sub.get('substitute_name', 'Unknown')
                    ratio = sub.get('ratio', '1:1')
                    notes = sub.get('notes', '')
                    
                    subs_text += f"  {i}. {sub_name} ({ratio})"
                    if notes:
                        subs_text += f" - {notes}"
                    subs_text += "\n"
                
                subs_text += "\n"
                shown_count += 1
        
        if shown_count == 0:
            subs_text += "No specific substitutions available for your ingredients, but you can always ask for alternatives while shopping!\n"
        else:
            subs_text += f"💡 **Tip:** These substitutions maintain nutritional value and work well in most recipes!\n"
        
        subs_text += "\nReady to go shopping, or need help with anything else?"
        
        return subs_text
    
    def _get_current_date(self) -> str:
        """Get current date string"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d")
    
    def get_completion_message(self) -> str:
        """Return completion message for the journey"""
        return "Your grocery list has been created successfully! 🛒"